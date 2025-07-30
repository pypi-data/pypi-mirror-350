import os
import requests
import subprocess

# constant
OPENAPI_SPEC_URL = "https://api.etherealtest.net/openapi.json"

# request the spec
response = requests.get(OPENAPI_SPEC_URL)
response.raise_for_status()
openapi_spec = response.json()

# write the spec to a file
with open("openapi.json", "w") as f:
    f.write(response.text)


result = subprocess.run(
    [
        "uv",
        "run",
        "datamodel-codegen",
        "--input",
        "openapi.json",
        "--output",
        "ethereal/models/rest.py",
        "--input-file-type",
        "openapi",
        "--openapi-scopes",
        "paths",
        "schemas",
        "parameters",
        "--output-model-type",
        "pydantic_v2.BaseModel",
        "--snake-case-field",
    ],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print("Error:", result.stderr)
else:
    print("Generated types successfully")

# remove the openapi.json file
os.remove("openapi.json")
