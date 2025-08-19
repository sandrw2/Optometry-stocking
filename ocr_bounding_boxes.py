from google.cloud import vision
from PIL import Image, ImageDraw

def draw_boxes(image_path):
    # Create a Vision API client
    client = vision.ImageAnnotatorClient()
    # Read the image file in binary mode
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    # Create a Vision API Image object
    image = vision.Image(content=content)
    # Sends the image to Google Vision, asking it to detect text and return results
    response = client.text_detection(image=image)
    # get text, skip full-text (first box is full box)
    texts = response.text_annotations[1:]  
    # Open the image using Pillow and prepare to draw
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)


    for text in texts:
        box = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        left = min([v[0] for v in box])
        top = min([v[1] for v in box])
        right = max([v[0] for v in box])
        bottom = max([v[1] for v in box])
        draw.rectangle([left, top, right, bottom], outline="red", width=3)
        draw.text((left, top - 15), text.description, fill="blue")
        print(text.description)
    
    img = img.rotate(-90, expand=True)
    img.save("output/output_4.jpg")

        

if __name__ == "__main__":
    # Change this to your actual image path
    image_path = "OCR_test/test_024.jpeg"
    draw_boxes(image_path)
