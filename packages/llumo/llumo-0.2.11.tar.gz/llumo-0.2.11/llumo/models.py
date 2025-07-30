from enum import Enum

class Provider(str, Enum):
    OPENAI = "OPENAI"
    GOOGLE = "GOOGLE"

# Maps model aliases → (provider, actual model name for API)
_MODEL_METADATA = {
    "GPT_4": (Provider.OPENAI, "gpt-4"),
    "GPT_4_32K": (Provider.OPENAI, "gpt-4-32k"),
    "GPT_35T": (Provider.OPENAI, "gpt-3.5-turbo"),
    "GPT_35T_INS": (Provider.OPENAI, "gpt-3.5-turbo-instruct"),
    "GPT_35T_16K": (Provider.OPENAI, "gpt-3.5-turbo-16k"),
    "GPT_35_TURBO": (Provider.OPENAI, "gpt-3.5-turbo"),

    "GOOGLE_15_FLASH": (Provider.GOOGLE, "gemini-1.5-flash-latest"),
    "GEMINI_PRO": (Provider.GOOGLE, "gemini-pro"),
    "TEXT_BISON": (Provider.GOOGLE, "text-bison-001"),
    "CHAT_BISON": (Provider.GOOGLE, "chat-bison-001"),
    "TEXT_BISON_32K": (Provider.GOOGLE, "text-bison-32k"),
    "TEXT_UNICORN": (Provider.GOOGLE, "text-unicorn-experimental"),
}

class AVAILABLEMODELS(str, Enum):
    GPT_4 = "gpt-4"
    GPT_4_32K = "gpt-4-32k"
    GPT_35T = "gpt-3.5-turbo"
    GPT_35T_INS = "gpt-3.5-turbo-instruct"
    GPT_35T_16K = "gpt-3.5-turbo-16k"
    GPT_35_TURBO = "gpt-3.5-turbo"

    GOOGLE_15_FLASH = "gemini-1.5-flash-latest"
    GEMINI_PRO = ""
    TEXT_BISON = "text-bison-001"
    CHAT_BISON = "chat-bison-001"
    TEXT_BISON_32K = "text-bison-32k"
    TEXT_UNICORN = "text-unicorn-experimental"

def getProviderFromModel(model: AVAILABLEMODELS) -> Provider:
    for alias, (provider, apiName) in _MODEL_METADATA.items():
        if model.value == apiName:
            return provider
    raise ValueError(f"Provider not found for model: {model}")