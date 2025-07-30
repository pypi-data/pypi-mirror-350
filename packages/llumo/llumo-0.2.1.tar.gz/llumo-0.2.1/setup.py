# from setuptools import setup, find_packages


# install_requires = [
#     "requests>=2.0.0",
#     "websocket-client>=1.0.0",
#     "pandas>=1.0.0",
#     "numpy>=1.0.0",
#     "python-socketio[client]==5.13.0",
#     "python-dotenv==1.1.0",
#     "openai==1.75.0",
#     "google-generativeai==0.8.5",
# ]
# setup(
#     name="llumo",
#     version="0.1.9",
#     description="Python SDK for interacting with the Llumo ai API.",
#     author="Llumo",
#     author_email="product@llumo.ai",
#     packages=find_packages(),
#     install_requires=install_requires,
#     python_requires=">=3.7",
#     include_package_data=True,
#     url="https://www.llumo.ai/",
#     license="Proprietary",
# )


# setup.py
import os
from setuptools import setup, find_packages

# Cloud Build will set TAG_NAME from the git tag.
VERSION = os.environ.get("TAG_NAME", "0.0.1.dev0")

# PyPI expects PEP 440 compliant versions.
# If your git tags are like 'v1.0.0', strip the leading 'v'.
if VERSION.startswith("v"):
    VERSION = VERSION[1:]

# --- Requirements ---
# Read requirements from requirements.txt
try:
    with open("requirements.txt", encoding="utf-8") as f:
        required = f.read().splitlines()
except FileNotFoundError:
    print("WARNING: requirements.txt not found. Setting install_requires to empty.")
    required = []

# --- Long Description ---
# Read the contents of your README file
long_description = ""
# setup(
#     name="llumo",
#     version="0.1.9",
#     description="Python SDK for interacting with the Llumo ai API.",
#     author="Llumo",
#     author_email="product@llumo.ai",
#     packages=find_packages(),
#     install_requires=install_requires,
#     python_requires=">=3.7",
#     include_package_data=True,
#     url="https://www.llumo.ai/",
#     license="Proprietary",
# )
setup(
    name="llumo",  # TODO: Replace with your SDK's actual name
    version=VERSION,
    description="Python SDK for interacting with the Llumo ai API.",
    author="Llumo",
    author_email="product@llumo.ai",
    url="https://www.llumo.ai/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    python_requires=">=3.7",  # TODO: Specify your minimum Python version
)

print(f"Building version: {VERSION}")
