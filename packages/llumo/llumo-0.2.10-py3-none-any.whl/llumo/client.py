import requests


import time
import re
import json
import uuid

import os
import itertools
import pandas as pd
from typing import List, Dict
from .models import AVAILABLEMODELS, getProviderFromModel
from .execution import ModelExecutor
from .exceptions import LlumoAIError
from .helpingFuntions import *
from .sockets import LlumoSocketClient
from .functionCalling import LlumoAgentExecutor


postUrl = "https://app.llumo.ai/api/eval/run-multiple-column"
fetchUrl = "https://app.llumo.ai/api/eval/fetch-rows-data-by-column"
validateUrl = "https://app.llumo.ai/api/workspace-details"
socketUrl = "https://red-skull-service-392377961931.us-central1.run.app/"


class LlumoClient:

    def __init__(self, api_key):
        self.apiKey = api_key
        self.socket = LlumoSocketClient(socketUrl)
        self.processMapping = {}

    def validateApiKey(self, evalName=" "):
        headers = {
            "Authorization": f"Bearer {self.apiKey}",
            "Content-Type": "application/json",
        }
        reqBody = {"analytics": [evalName]}

        try:
            response = requests.post(url=validateUrl, json=reqBody, headers=headers)
            
            print("Response:   ",response.json())
            try:
                response_preview = response.text[:500]  # First 500 chars
                # print(f"Response preview: {response_preview}")
            except Exception as e:
                print(f"Could not get response preview: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Request exception: {str(e)}")
            raise LlumoAIError.RequestFailed(detail=str(e))

        if response.status_code == 401:
            raise LlumoAIError.InvalidApiKey()

        # Handle other common status codes
        if response.status_code == 404:
            raise LlumoAIError.RequestFailed(
                detail=f"Endpoint not found (404): {validateUrl}"
            )

        if response.status_code != 200:
            raise LlumoAIError.RequestFailed(
                detail=f"Unexpected status code: {response.status_code}"
            )

        # Try to parse JSON
        try:
            data = response.json()
        except ValueError as e:
            print(f"JSON parsing error: {str(e)}")
            # print(f"Response content that could not be parsed: {response.text[:1000]}...")
            raise LlumoAIError.InvalidJsonResponse()

        if "data" not in data or not data["data"]:
            # print(f"Invalid API response structure: {data}")
            raise LlumoAIError.InvalidApiResponse()

        try:
            self.hitsAvailable = data["data"]["data"].get("remainingHits", 0)
            self.workspaceID = data["data"]["data"].get("workspaceID")
            self.evalDefinition = data["data"]["data"].get("analyticsMapping")
            self.socketToken = data["data"]["data"].get("token")
            self.hasSubscribed = data["data"]["data"].get("hasSubscribed", False)
            self.trialEndDate = data["data"]["data"].get("trialEndDate", None)
            self.subscriptionEndDate = data["data"]["data"].get("subscriptionEndDate", None)
            self.email = data["data"]["data"].get("email", None)

        except Exception as e:
            # print(f"Error extracting data from response: {str(e)}")
            raise LlumoAIError.UnexpectedError(detail=str(e))

    def postBatch(self, batch, workspaceID):
        payload = {
            "batch": json.dumps(batch),
            "runType": "EVAL",
            "workspaceID": workspaceID,
        }
        # socketToken here if the "JWD" token
        headers = {
            "Authorization": f"Bearer {self.socketToken}",
            "Content-Type": "application/json",
        }
        try:
            # print(postUrl)
            response = requests.post(postUrl, json=payload, headers=headers)
            # print(f"Post API Status Code: {response.status_code}")
            # print(response.text)

        except Exception as e:
            print(f"Error in posting batch: {e}")

    def postDataStream(self, batch, workspaceID):
        payload = {
            "batch": json.dumps(batch),
            "runType": "DATA_STREAM",
            "workspaceID": workspaceID,
        }
        # socketToken here if the "JWD" token
        headers = {
            "Authorization": f"Bearer {self.socketToken}",
            "Content-Type": "application/json",
        }
        try:
            # print(postUrl)
            response = requests.post(postUrl, json=payload, headers=headers)
            # print(f"Post API Status Code: {response.status_code}")
            # print(response.text)

        except Exception as e:
            print(f"Error in posting batch: {e}")

    def AllProcessMapping(self):
        for batch in self.allBatches:
            for record in batch:
                rowId = record["rowID"]
                colId = record["columnID"]
                pid = f"{rowId}-{colId}-{colId}"
                self.processMapping[pid] = record

    def finalResp(self, results):
        seen = set()
        uniqueResults = []

        for item in results:
            for rowID in item:  # Each item has only one key
                # for rowID in item["data"]:
                if rowID not in seen:
                    seen.add(rowID)
                    uniqueResults.append(item)

        return uniqueResults

    def evaluate(
        self,
        dataframe,
        eval="Response Completeness",
        prompt_template="",
        outputColName="output",
        createExperiment: bool = False,
    ):

        results = {}
        try:
            socketID = self.socket.connect(timeout=150)

            # Ensure full connection before proceeding
            max_wait_secs = 20
            waited_secs = 0
            while not self.socket._connection_established.is_set():
                time.sleep(0.1)
                waited_secs += 0.1
                if waited_secs >= max_wait_secs:
                    raise RuntimeError(
                        "Timeout waiting for server 'connection-established' event."
                    )

            rowIdMapping = {}

            print(f"\n======= Running evaluation for: {eval} =======")

            try:
                self.validateApiKey(evalName=eval)
            except Exception as e:
                if hasattr(e, "response") and getattr(e, "response", None) is not None:
                    pass
                raise
            userHits = checkUserHits(
                self.workspaceID,
                self.hasSubscribed,
                self.trialEndDate,
                self.subscriptionEndDate,
                self.hitsAvailable,
                len(dataframe),
            )

            if not userHits["success"]:
                raise LlumoAIError.InsufficientCredits(userHits["message"])

            # if self.hitsAvailable == 0 or len(dataframe) > self.hitsAvailable:
            #     raise LlumoAIError.InsufficientCredits()

            evalDefinition = self.evalDefinition[eval]
            model = "GPT_4"
            provider = "OPENAI"
            evalType = "LLM"
            workspaceID = self.workspaceID
            email = self.email

            self.allBatches = []
            currentBatch = []

            for index, row in dataframe.iterrows():
                tools = [row["tools"]] if "tools" in dataframe.columns else []
                groundTruth = (
                    row["groundTruth"] if "groundTruth" in dataframe.columns else ""
                )
                messageHistory = (
                    [row["messageHistory"]]
                    if "messageHistory" in dataframe.columns
                    else []
                )
                promptTemplate = prompt_template

                keys = re.findall(r"{{(.*?)}}", promptTemplate)

                if not all([ky in dataframe.columns for ky in keys]):
                    raise LlumoAIError.InvalidPromptTemplate()

                inputDict = {key: row[key] for key in keys if key in row}
                output = (
                    row[outputColName] if outputColName in dataframe.columns else ""
                )

                activePlayground = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace(
                    "-", ""
                )
                rowID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                columnID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")

                # storing the generated rowID and the row index (dataframe) for later lookkup
                rowIdMapping[rowID] = index

                templateData = {
                    "processID": getProcessID(),
                    "socketID": socketID,
                    "source": "SDK",
                    "processData": {
                        "executionDependency": {
                            "query": "",
                            "context": "",
                            "output": output,
                            "tools": tools,
                            "groundTruth": groundTruth,
                            "messageHistory": messageHistory,
                        },
                        "definition": evalDefinition,
                        "model": model,
                        "provider": provider,
                        "analytics": eval,
                    },
                    "workspaceID": workspaceID,
                    "type": "EVAL",
                    "evalType": evalType,
                    "kpi": eval,
                    "columnID": columnID,
                    "rowID": rowID,
                    "playgroundID": activePlayground,
                    "processType": "EVAL",
                    "email": email,
                }

                query = ""
                context = ""
                for key, value in inputDict.items():
                    if isinstance(value, str):
                        length = len(value.split()) * 1.5
                        if length > 50:
                            context += f" {key}: {value}, "
                        else:
                            if promptTemplate:
                                tempObj = {key: value}
                                promptTemplate = getInputPopulatedPrompt(
                                    promptTemplate, tempObj
                                )
                            else:
                                query += f" {key}: {value}, "

                if not context.strip():
                    for key, value in inputDict.items():
                        context += f" {key}: {value}, "

                templateData["processData"]["executionDependency"][
                    "context"
                ] = context.strip()
                templateData["processData"]["executionDependency"][
                    "query"
                ] = query.strip()

                if promptTemplate and not query.strip():
                    templateData["processData"]["executionDependency"][
                        "query"
                    ] = promptTemplate

                currentBatch.append(templateData)

                if len(currentBatch) == 10 or index == len(dataframe) - 1:
                    self.allBatches.append(currentBatch)
                    currentBatch = []

            totalItems = sum(len(batch) for batch in self.allBatches)

            for cnt, batch in enumerate(self.allBatches):
                try:
                    self.postBatch(batch=batch, workspaceID=workspaceID)
                    # print("Betch Posted with item len: ", len(batch))
                except Exception as e:
                    continue

                time.sleep(1)

            timeout = max(50, min(600, totalItems * 10))

            self.socket.listenForResults(
                min_wait=40,
                max_wait=timeout,
                inactivity_timeout=150,
                expected_results=totalItems,
            )

            eval_results = self.socket.getReceivedData()
            results[eval] = self.finalResp(eval_results)

        except Exception as e:
            raise
        finally:
            try:
                self.socket.disconnect()
            except Exception as e:
                pass

        for evalName, records in results.items():
            dataframe[evalName] = None
            for item in records:
                for compound_key, value in item.items():
                    # for compound_key, value in item['data'].items():

                    rowID = compound_key.split("-")[0]
                    # looking for the index of each rowID , in the original dataframe
                    if rowID in rowIdMapping:
                        index = rowIdMapping[rowID]
                        # dataframe.at[index, evalName] = value
                        dataframe.at[index, evalName] = value["value"]
                        dataframe.at[index, f"{evalName} Reason"] = value["reasoning"]

                    else:
                        pass
                        # print(f"⚠️ Warning: Could not find rowID {rowID} in mapping")
        if createExperiment:
            pd.set_option("future.no_silent_downcasting", True)
            df = dataframe.fillna("Some error occured").astype(object)

            if createPlayground(email, workspaceID, df):
                print(
                    "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                )
        else:
            return dataframe

    def evaluateCompressor(self, dataframe, prompt_template):
        results = []

        try:
            # Connect to socket first
            # print("Connecting to socket server...")
            socketID = self.socket.connect(timeout=150)

            # Ensure full connection before proceeding
            max_wait_secs = 20
            waited_secs = 0
            while not self.socket._connection_established.is_set():
                time.sleep(0.1)
                waited_secs += 0.1
                if waited_secs >= max_wait_secs:
                    raise RuntimeError(
                        "Timeout waiting for server 'connection-established' event."
                    )

            # print(f"Connected with socket ID: {socketID}")

            try:
                # print(f"Validating API key...")
                self.validateApiKey()
                # print(f"API key validation successful. Hits available: {self.hitsAvailable}")
            except Exception as e:
                print(f"Error during API key validation: {str(e)}")
                if hasattr(e, "response") and getattr(e, "response", None) is not None:
                    print(f"Status code: {e.response.status_code}")
                    print(f"Response content: {e.response.text[:500]}...")
                raise

            # check for available hits and trial limit
            userHits = checkUserHits(
                self.workspaceID,
                self.hasSubscribed,
                self.trialEndDate,
                self.subscriptionEndDate,
                self.hitsAvailable,
                len(dataframe),
            )

            # do not proceed if subscription or trial limit has exhausted
            if not userHits["success"]:
                raise LlumoAIError.InsufficientCredits(userHits["message"])

            # if self.hitsAvailable == 0 or len(dataframe) > self.hitsAvailable:
            #     raise LlumoAIError.InsufficientCredits()

            model = "GPT_4"
            provider = "OPENAI"
            evalType = "LLUMO"
            workspaceID = self.workspaceID
            email = self.email
            # Prepare all batches before sending
            # print("Preparing batches...")
            self.allBatches = []
            currentBatch = []

            for index, row in dataframe.iterrows():
                promptTemplate = prompt_template

                # extracting the placeholders from the prompt template
                keys = re.findall(r"{{(.*?)}}", promptTemplate)
                inputDict = {key: row[key] for key in keys if key in row}

                if not all([ky in dataframe.columns for ky in keys]):
                    raise LlumoAIError.InvalidPromptTemplate()

                activePlayground = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace(
                    "-", ""
                )
                rowID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                columnID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")

                compressed_prompt_id = (
                    f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                )
                compressed_prompt_output_id = (
                    f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                )
                cost_id = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                cost_saving_id = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace(
                    "-", ""
                )

                # Use the server-provided socket ID here
                templateData = {
                    "processID": getProcessID(),
                    "socketID": socketID,
                    "source": "SDK",
                    "rowID": rowID,
                    "columnID": columnID,
                    "processType": "COST_SAVING",
                    "evalType": evalType,
                    "dependency": list(inputDict.keys()),
                    "costColumnMapping": {
                        "compressed_prompt": compressed_prompt_id,
                        "compressed_prompt_output": compressed_prompt_output_id,
                        "cost": cost_id,
                        "cost_saving": cost_saving_id,
                    },
                    "processData": {
                        "rowData": {
                            "query": {"type": "VARIABLE", "value": ""},
                            "context": {"type": "VARIABLE", "value": ""},
                        },
                        "dependency": list(inputDict.keys()),
                        "dependencyMapping": {ky: ky for ky in list(inputDict.keys())},
                        "provider": provider,
                        "model": model,
                        "promptText": promptTemplate,
                        "costColumnMapping": {
                            "compressed_prompt": compressed_prompt_id,
                            "compressed_prompt_output": compressed_prompt_output_id,
                            "cost": cost_id,
                            "cost_saving": cost_saving_id,
                        },
                    },
                    "workspaceID": workspaceID,
                    "email": email,
                    "playgroundID": activePlayground,
                }

                # Build query/context from input
                query = ""
                context = ""

                for key, value in inputDict.items():
                    if isinstance(value, str):
                        length = len(value.split()) * 1.5
                        if length > 50:
                            context += f" {key}: {value}, "
                        else:
                            if promptTemplate:
                                populatedPrompt = getInputPopulatedPrompt(
                                    promptTemplate, {key: value}
                                )
                                query += f"{populatedPrompt} "
                            else:
                                query += f" {key}: {value}, "

                if not context.strip():
                    for key, value in inputDict.items():
                        context += f" {key}: {value}, "

                templateData["processData"]["rowData"]["context"][
                    "value"
                ] = context.strip()
                templateData["processData"]["rowData"]["query"]["value"] = query.strip()

                if promptTemplate and not query.strip():
                    templateData["processData"]["rowData"]["query"][
                        "value"
                    ] = promptTemplate

                # print(templateData)
                currentBatch.append(templateData)

            if len(currentBatch) == 10 or index == len(dataframe) - 1:
                self.allBatches.append(currentBatch)
                currentBatch = []

            # Post all batches
            total_items = sum(len(batch) for batch in self.allBatches)
            # print(f"Posting {len(self.allBatches)} batches ({total_items} items total)")

            for cnt, batch in enumerate(self.allBatches):
                # print(f"Posting batch {cnt + 1}/{len(self.allBatches)} for eval '{eval}'")
                try:
                    self.postBatch(batch=batch, workspaceID=workspaceID)
                    # print(f"Batch {cnt + 1} posted successfully")
                except Exception as e:
                    print(f"Error posting batch {cnt + 1}: {str(e)}")
                    continue

                # Small delay between batches to prevent overwhelming the server
                time.sleep(1)

            # updating the dict for row column mapping
            self.AllProcessMapping()
            # Calculate a reasonable timeout based on the data size
            timeout = max(60, min(600, total_items * 10))
            # print(f"All batches posted. Waiting up to {timeout} seconds for results...")

            # Listen for results
            self.socket.listenForResults(
                min_wait=20,
                max_wait=timeout,
                inactivity_timeout=30,
                expected_results=None,
            )

            # Get results for this evaluation
            eval_results = self.socket.getReceivedData()
            # print(f"Received {len(eval_results)} results for evaluation '{eval}'")

            # Add these results to our overall results
            results = self.finalResp(eval_results)
            print(f"======= Completed evaluation: {eval} =======\n")

            # print("All evaluations completed successfully")

        except Exception as e:
            print(f"Error during evaluation: {e}")
            raise
        finally:
            # Always disconnect the socket when done
            try:
                self.socket.disconnect()
                # print("Socket disconnected")
            except Exception as e:
                print(f"Error disconnecting socket: {e}")

        compressed_prompt, compressed_prompt_output, cost, cost_saving = (
            costColumnMapping(results, self.processMapping)
        )
        dataframe["compressed_prompt"] = compressed_prompt
        dataframe["compressed_prompt_output"] = compressed_prompt_output
        dataframe["cost"] = cost
        dataframe["cost_saving"] = cost_saving

        return dataframe

    def run_sweep(
        self,
        templates: List[str],
        dataset: Dict[str, List[str]],
        model_aliases: List[AVAILABLEMODELS],
        apiKey: str,
        eval=["Response Correctness"],
        toEvaluate: bool = False,
        createExperiment: bool = False,
    ) -> pd.DataFrame:
        try:
            self.validateApiKey()
        except Exception as e:
            raise "Some error ocuured please check your API key"
        workspaceID = self.workspaceID
        email = self.email
        executor = ModelExecutor(apiKey)
        keys = list(dataset.keys())
        value_combinations = list(itertools.product(*dataset.values()))
        combinations = [dict(zip(keys, values)) for values in value_combinations]

        results = []

        # Iterate through combinations
        for combo in combinations:
            for template in templates:
                prompt = template
                for k, v in combo.items():
                    prompt = prompt.replace(f"{{{{{k}}}}}", v)
                # Add a row for each model
                for model in model_aliases:
                    row = {
                        "template": template,
                        "prompt": prompt,
                        **combo,
                        "model": model.value,
                    }

                    try:
                        provider = getProviderFromModel(model)
                        response = executor.execute(
                            provider, model.value, prompt, apiKey
                        )
                        row["output"] = response
                    except Exception as e:
                        row["output"] = f"Error: {str(e)}"

                    results.append(row)
        df = pd.DataFrame(results)
        if toEvaluate:

            res = self.evaluate(df, eval=eval, prompt_template=str(templates[0]))

            if createExperiment:
                pd.set_option("future.no_silent_downcasting", True)
                res = res.fillna("Some error occured")
                if createPlayground(email, workspaceID, res):
                    print(
                        "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                    )
            else:
                return res

        else:
            if createExperiment:
                pd.set_option("future.no_silent_downcasting", True)
                df = df.fillna("Some error occured")
                if createPlayground(email, workspaceID, df):
                    print(
                        "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                    )
            else:
                return df

    def evaluateAgents(
        self,
        dataframe,
        model,
        agents,
        model_api_key=None,
        prompt_template="Give answer for the given query: {{query}}",
        createExperiment: bool = False,
    ):
        if model.lower() not in ["openai", "google"]:
            raise ValueError("Model must be 'openai' or 'google'")

        # Run unified agent execution
        toolResponseDf = LlumoAgentExecutor.run(
            dataframe, agents, model=model, model_api_key=model_api_key
        )
        evals = [
            "Tool Reliability",
            "Stepwise Progression",
            "Tool Selection Accuracy",
            "Final Task Alignment",
        ]

        for eval in evals:
            # Perform evaluation
            toolResponseDf = self.evaluate(
                toolResponseDf,
                eval=eval,
                prompt_template=prompt_template,
                createExperiment=False,
            )
        if createExperiment:
            pd.set_option("future.no_silent_downcasting", True)
            df = toolResponseDf.fillna("Some error occured")
            if createPlayground(self.email, self.workspaceID, df):
                print(
                    "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                )
        else:
            return toolResponseDf

    def evaluateAgentResponses(
        self,
        dataframe,
        prompt_template="Give answer for the given query: {{query}}",
        createExperiment: bool = False,
    ):
        try:
            if "query" and "messageHistory" and "tools" not in dataframe.columns:
                raise ValueError(
                    "DataFrame must contain 'query', 'messageHistory', and 'tools' columns"
                )
            evals = [
                "Tool Reliability",
                "Stepwise Progression",
                "Tool Selection Accuracy",
                "Final Task Alignment",
            ]
            toolResponseDf = dataframe.copy()
            for eval in evals:
                # Perform evaluation
                toolResponseDf = self.evaluate(
                    toolResponseDf, eval=eval, prompt_template=prompt_template
                )
            return toolResponseDf

        except Exception as e:
            raise e

    def runDataStream(
        self,
        dataframe,
        streamName: str,
        queryColName: str = "query",
        createExperiment: bool = False,
    ):
        results = {}

        try:
            socketID = self.socket.connect(timeout=150)
            # Ensure full connection before proceeding
            max_wait_secs = 20
            waited_secs = 0
            while not self.socket._connection_established.is_set():
                time.sleep(0.1)
                waited_secs += 0.1
                if waited_secs >= max_wait_secs:
                    raise RuntimeError(
                        "Timeout waiting for server 'connection-established' event."
                    )
            # print(f"Connected with socket ID: {socketID}")
            rowIdMapping = {}
            try:
                # print(f"Validating API key...")
                self.validateApiKey()
                # print(f"API key validation successful. Hits available: {self.hitsAvailable}")
            except Exception as e:
                print(f"Error during API key validation: {str(e)}")
                if hasattr(e, "response") and getattr(e, "response", None) is not None:
                    print(f"Status code: {e.response.status_code}")
                    print(f"Response content: {e.response.text[:500]}...")
                raise
            # check for available hits and trial limit
            userHits = checkUserHits(
                self.workspaceID,
                self.hasSubscribed,
                self.trialEndDate,
                self.subscriptionEndDate,
                self.hitsAvailable,
                len(dataframe),
            )

            # do not proceed if subscription or trial limit has exhausted
            if not userHits["success"]:
                raise LlumoAIError.InsufficientCredits(userHits["message"])

            print("====🚀Sit back while we fetch data from the stream 🚀====")
            workspaceID = self.workspaceID
            email = self.email
            streamId = getStreamId(workspaceID, self.apiKey, streamName)
            # Prepare all batches before sending
            # print("Preparing batches...")
            self.allBatches = []
            currentBatch = []

            for index, row in dataframe.iterrows():
                activePlayground = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace(
                    "-", ""
                )
                rowID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")
                columnID = f"{int(time.time() * 1000)}{uuid.uuid4()}".replace("-", "")

                rowIdMapping[rowID] = index
                # Use the server-provided socket ID here
                templateData = {
                    "processID": getProcessID(),
                    "socketID": socketID,
                    "processData": {
                        "executionDependency": {"query": row[queryColName]},
                        "dataStreamID": streamId,
                    },
                    "workspaceID": workspaceID,
                    "email": email,
                    "type": "DATA_STREAM",
                    "playgroundID": activePlayground,
                    "processType": "DATA_STREAM",
                    "rowID": rowID,
                    "columnID": columnID,
                    "source": "SDK",
                }

                currentBatch.append(templateData)

            if len(currentBatch) == 10 or index == len(dataframe) - 1:
                self.allBatches.append(currentBatch)
                currentBatch = []

            # Post all batches
            total_items = sum(len(batch) for batch in self.allBatches)
            # print(f"Posting {len(self.allBatches)} batches ({total_items} items total)")

            for cnt, batch in enumerate(self.allBatches):
                # print(f"Posting batch {cnt + 1}/{len(self.allBatches)} for eval '{eval}'")
                try:
                    self.postDataStream(batch=batch, workspaceID=workspaceID)
                    # print(f"Batch {cnt + 1} posted successfully")
                except Exception as e:
                    print(f"Error posting batch {cnt + 1}: {str(e)}")
                    continue

                # Small delay between batches to prevent overwhelming the server
                time.sleep(1)

            # updating the dict for row column mapping
            self.AllProcessMapping()
            # Calculate a reasonable timeout based on the data size
            timeout = max(60, min(600, total_items * 10))
            # print(f"All batches posted. Waiting up to {timeout} seconds for results...")

            # Listen for results
            self.socket.listenForResults(
                min_wait=20,
                max_wait=timeout,
                inactivity_timeout=30,
                expected_results=None,
            )

            # Get results for this evaluation
            eval_results = self.socket.getReceivedData()
            # print(f"Received {len(eval_results)} results for evaluation '{eval}'")

            # Add these results to our overall results
            results["Data Stream"] = self.finalResp(eval_results)
            print(f"=======You are all set! continue your expectations 🚀======\n")

            # print("All evaluations completed successfully")

        except Exception as e:
            print(f"Error during evaluation: {e}")
            raise
        finally:
            # Always disconnect the socket when done
            try:
                self.socket.disconnect()
                # print("Socket disconnected")
            except Exception as e:
                print(f"Error disconnecting socket: {e}")

        for streamName, records in results.items():
            dataframe[streamName] = None
            for item in records:
                for compound_key, value in item.items():
                    # for compound_key, value in item['data'].items():

                    rowID = compound_key.split("-")[0]
                    # looking for the index of each rowID , in the original dataframe
                    if rowID in rowIdMapping:
                        index = rowIdMapping[rowID]
                        # dataframe.at[index, evalName] = value
                        dataframe.at[index, streamName] = value["value"]

                    else:
                        pass
                        # print(f"⚠️ Warning: Could not find rowID {rowID} in mapping")

        if createExperiment:
            pd.set_option("future.no_silent_downcasting", True)
            df = dataframe.fillna("Some error occured").astype(object)

            if createPlayground(email, workspaceID, df):
                print(
                    "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                )
        else:
            self.latestDataframe = dataframe
            return dataframe

    def createExperiment(self, dataframe):
        try:
            self.validateApiKey()

            flag = createPlayground(self.email, self.workspaceID, dataframe)
            if flag:
                print(
                    "Your data has been saved in the Llumo Experiment. Visit https://app.llumo.ai/evallm to see the results."
                )
        except Exception as e:
            raise "Some error ocuured please check your API key"


class SafeDict(dict):
    def __missing__(self, key):
        return ""
