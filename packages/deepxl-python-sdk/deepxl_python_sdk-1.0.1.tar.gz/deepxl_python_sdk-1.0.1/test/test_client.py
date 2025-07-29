from deepxl_python_sdk import DeepXLClient, UsageResponse, AnalysisResponse, DeepXLError
import unittest
import os


API_KEY = os.environ['TESTING_API_KEY']


class TestClient(unittest.TestCase):

  def test_check_usage(self):
    client = DeepXLClient(API_KEY)
    response = client.check_usage()
    self.assertIsInstance(response, UsageResponse)
    self.assertTrue(response.image_usage_limit is not None)
    self.assertTrue(response.image_usage is not None)
    self.assertTrue(response.video_usage_limit is not None)
    self.assertTrue(response.video_usage is not None)
    self.assertTrue(response.audio_usage_limit is not None)
    self.assertTrue(response.audio_usage is not None)
    self.assertTrue(response.document_usage_limit is not None)
    self.assertTrue(response.document_usage is not None)


  def test_analyze(self):
    client = DeepXLClient(API_KEY)
    f = open(".\\test\\rickroll.jpg", 'rb')
    data = f.read()
    f.close()
    response = client.analyze("always-false", "rickroll.jpg", data)
    self.assertIsInstance(response, AnalysisResponse)
    self.assertTrue(response.likelihood is not None)
    self.assertTrue(response.reasoning is not None)
    self.assertTrue(response.model_results is not None)

  
  def test_analyze_file(self):
    client = DeepXLClient(API_KEY)
    response = client.analyze_file("always-true", ".\\test\\rickroll.jpg")
    print(response)
    self.assertIsInstance(response, AnalysisResponse)
    self.assertTrue(response.likelihood is not None)
    self.assertTrue(response.reasoning is not None)
    self.assertTrue(response.model_results is not None)


  def test_unauthorized(self):
    client = DeepXLClient("bad123")
    try:
      response = client.check_usage()
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, "Invalid API key.")

    try:
      response = client.analyze_file("always-true", "C:\\Users\\David\\Pictures\\rickroll.jpg")
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, "Invalid API key.")


  def test_invalid_model_name(self):
    client = DeepXLClient(API_KEY)
    model_name = "not-a-model"
    try:
      f = open(".\\test\\rickroll.jpg", 'rb')
      data = f.read()
      f.close()
      response = client.analyze(model_name, "rickroll.jpg", data)
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, f"Invalid model: {model_name}")

    try:
      response = client.analyze_file(model_name, ".\\test\\rickroll.jpg")
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, f"Invalid model: {model_name}")


  def test_no_file_data(self):
    client = DeepXLClient(API_KEY)
    try:
      response = client.analyze("always-true", "rickroll.jpg", b"")
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, "File data is missing or invalid.")


  def test_file_not_found(self):
    client = DeepXLClient(API_KEY)
    file = ".\\file\\not\\here.png"
    try:
      response = client.analyze_file("always-true", file)
    except Exception as e:
      self.assertIsInstance(e, DeepXLError)
      self.assertEqual(e.message, f'File "{file}" does not exist.')


if __name__ == '__main__':
  unittest.main()

