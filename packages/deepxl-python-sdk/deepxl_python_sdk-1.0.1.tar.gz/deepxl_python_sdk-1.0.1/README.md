# deepxl-python-sdk
Python Software Development Kit for DeepXL fraud detection services

## Installation

Install the SDK using pip

```bash
pip install deepxl-python-sdk
```

## Example

To use the DeepXL client, you must first create an API key in the [dashboard](https://app.deepxl.ai/settings?tab=apiKeys). You can create a new API key in Settings -> API Keys -> Create API Key.

Treat this API key like you would any environment secret. Do not commit to a public repository or store in plain text.

```python
from deepxl-python-sdk import DeepXLClient

client = new DeepXLClient(MY_API_KEY)

analysis_result = client.analyze_file("documents-model", ".\\file.pdf")
```

## Client methods

### check_usage
Returns the monthly usage quota and current usage for the payment period for each media type.

#### Returns:

Returns a ```UsageResponse``` object with the following properties:

|Property|Type|
|----|----|
|image_usage_limit|int|
|image_usage|int|
|video_usage_limit|int|
|video_usage|int|
|audio_usage_limit|int|
|audio_usage|int|
|document_usage_limit|int|
|document_usage|int|

### analyze

Analyze file data with DeepXL fraud detection. 

#### Inputs

- **model_name:** the name of the model to use. You can find a complete list in our docs.
- **file_name:** the name of the file to analyze
- **file_data**: byte array of file data to analyze

> Note: while you can use a constant string as file name, it is recommended you use unique identifiers to make files easier to find in analysis history.

### analyze_file

Analyze file with DeepXL fraud detection. This does the same thing as ```analyze``` but takes a file path as input instead of binary file data.

#### Inputs

- **model_name:** the name of the model to use. You can find a complete list in our docs.
- **file:** path of the file to analyze

#### Returns

Both ```analyze``` and ```analyze_file``` return an ```AnalysisResult``` object with the following properties:

| Property | Type | Description |
|----------|------|-|
|likelihood|float|The percent likelihood that the file has been manipulated|
|reasoning|str[]|model reasoning|
|model_results|dict|model-specific outputs|


