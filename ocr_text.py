from google.cloud import vision
from google.oauth2 import service_account
from ocr_parser import parse_contact_lens_data

# Path to your service account JSON key file
KEY_PATH = "/Users/sandrawang/Documents/Optometry_Apps/credentials/google_vision_key.json"

def detect_text_with_service_account(image_path):
    # Create credentials object from JSON key file
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    
    # Create the Vision API client with credentials
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)

    details = response.text_annotations[1:]

    text_details = {}
    if details:
        for det in details:
            word = det.description.upper()
            vertices = [(v.x, v.y) for v in det.bounding_poly.vertices]
            text_details[word] = vertices
        return text_details
    else:
        print("No text found")
        return {}

if __name__ == "__main__":
    img_path = "/Users/sandrawang/Documents/Optometry_Apps/OCR_test/test_024.jpeg"
    text = detect_text_with_service_account(img_path)
    data = parse_contact_lens_data(text)
