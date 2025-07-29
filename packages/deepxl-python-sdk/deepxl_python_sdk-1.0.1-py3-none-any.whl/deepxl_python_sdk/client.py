import requests
from .mimetypes import get_mimetype
from .error import DeepXLError
import re

URL = "https://api.deepxl.ai/"


class UsageResponse:
  def __init__(self, image_usage_limit, image_usage, video_usage_limit, video_usage, audio_usage_limit, audio_usage, document_usage_limit, document_usage):
    self.image_usage_limit = image_usage_limit
    self.image_usage = image_usage
    self.video_usage_limit = video_usage_limit
    self.video_usage = video_usage
    self.audio_usage_limit = audio_usage_limit
    self.audio_usage = audio_usage
    self.document_usage_limit = document_usage_limit
    self.document_usage = document_usage
  

  def __str__(self):
    return f"Image Usage: {self.image_usage} / {self.image_usage_limit}\nVideo Usage: {self.video_usage} / {self.video_usage_limit}\nAudio Usage: {self.audio_usage} / {self.audio_usage_limit}\nDocument Usage: {self.document_usage} / {self.document_usage_limit}"


class AnalysisResponse:
  def __init__(self, likelihood, reasoning, model_results: dict):
    self.likelihood = likelihood
    self.reasoning = reasoning
    self.model_results = model_results


  def __str__(self):
    return f"Likelihood: {self.likelihood}\nReasoning: {self.reasoning}\nModel Results: {self.model_results}"
  

def handle_http_error(res):
  json = res.json()
  # print(res.status_code, json)
  if res.status_code == 200:
    return
  if res.status_code == 400:
    raise DeepXLError(json["message"] if json["message"] else "Bad request.")
  if res.status_code == 401:
    raise DeepXLError("Invalid API key.")
  if res.status_code == 402:
    raise DeepXLError(json["message"] if json["message"] else "Usage limit reached.")
  if res.status_code == 403:
    pass
  if res.status_code == 404:
    raise DeepXLError(json["message"] if json["message"] else "Invalid model.")
  if res.status_code == 415: 
    raise DeepXLError(json["message"] if json["message"] else "Invalid file type or file type is not compatible with the model.")
  if res.statusCode == 500:
    raise DeepXLError("Server error occured. Contact support or try again later.")
  raise DeepXLError(f"An unknown error occured. Status code: {res.status_code}, Response: {json}")


class DeepXLClient:
  def __init__(self, api_key):
    """Initialize the DeepXL client with the given API key.
    args:
      api_key (str): The API key to use for authentication.
    """
    self.api_key = api_key


  def check_usage(self):
    """Return the usage and limits of the account."""
    res = requests.get(
      URL + "v1/account/",
      headers={ "x-api-key": self.api_key },
      timeout=5.0
    )
    try:
      if res.status_code == 200:
        json = res.json()
        return UsageResponse(
          json["imageUsageLimit"],
          json["imageUsage"],
          json["videoUsageLimit"],
          json["videoUsage"],
          json["audioUsageLimit"],
          json["audioUsage"],
          json["documentUsageLimit"],
          json["documentUsage"]
        )
      else:
        handle_http_error(res)
    except ConnectionError as e:
      raise e


  def analyze(self, model_name: str, file_name: str, file_data: bytes):
    """Analyze file data with the given model and return the result.
    
    args:
      model_name (str): The name of the model to use for analysis.
      file_name (str): The name of the file to analyze.
      file_data (bytes): The file data to analyze.
    returns:
      AnalysisResponse: The analysis result.
    """
    if (len(file_data) == 0):
      raise DeepXLError("File data is missing or invalid.")
    try:
      file_type = get_mimetype(file_name)
      res = requests.post(
        URL + "v1/analysis",
        headers={
          "x-api-key": self.api_key,
        },
        data={
          "model": model_name
        },
        files={
          "file": (file_name, file_data, file_type)
        },
        timeout=5.0
      )
      if res.status_code == 200:
        result = res.json()["result"]
        return AnalysisResponse(
          likelihood=result["likelihood"],
          reasoning=result["reasoning"],
          model_results=result["modelResults"]
        )
      else:
        handle_http_error(res)          
    except ConnectionError as e:
      raise e
    except DeepXLError as e:
      raise e

  
  def analyze_file(self, model_name: str, file: str):
    """Analyze a file witht the given model and return the result.
    args:
      model_name (str): The name of the model to use for analysis.
      file (str): The path to the file to analyze.
    returns:
      AnalysisResponse: The analysis result.
    """
    f = None
    try:
      f = open(file, "rb")
      base_name = file.split(r"[\\/]+")[-1]
      file_type = get_mimetype(file)
      res = requests.post(
        URL + "v1/analysis",
        headers={
          "x-api-key": self.api_key,
        },
        data={
          "model": model_name
        },
        files={
          "file": (base_name, f, file_type)
        },
        timeout=5.0
      )
      f.close()
      if res.status_code == 200:
        result = res.json()["result"]
        return AnalysisResponse(
          likelihood=result["likelihood"],
          reasoning=result["reasoning"],
          model_results=result["modelResults"]
        )
      else:
        handle_http_error(res)
    except ConnectionError as e:
      if not f.closed:
        f.close()
      raise e
    except FileNotFoundError as e:
      raise DeepXLError(f'File "{file}" does not exist.')
    except DeepXLError as e:
      raise e
  