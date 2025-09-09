from google.cloud import vision
from google.oauth2 import service_account

# image pre-processing libraries
from PIL import Image, ImageOps
from io import BytesIO

# Path to your service account JSON key file
KEY_PATH = "credentials/GOOGLE_API_KEY.json"

def detect_text(image_path):
    # Create credentials object from JSON key file
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    
    # Create the Vision API client with credentials
    client = vision.ImageAnnotatorClient(credentials=credentials)


    # Open image and fix orientation based on EXIF
    # NOTE: previewed images may look right side up
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)

    # Convert to bytes for Vision API 
    # Alternatively save the images again and then use the with open
    img_bytes = BytesIO()
    img.save(img_bytes, format="JPEG")
    content = img_bytes.getvalue()

    # with open(image_path, "rb") as image_file:
    #     content = image_file.read()


    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)

    details = response.text_annotations[1:]

    text_details = {}
    if details:
        for det in details:
            word = det.description.upper()
            vertices = [(v.x, v.y) for v in det.bounding_poly.vertices]
            # text_details[word] = vertices
            text_details[word] = vertices
        return text_details
    else:
        print("No text found")
        return {}