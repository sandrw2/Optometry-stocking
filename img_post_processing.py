import cv2
import os


def post_process_image(image_path):
    output_dir = "output"  # You can name this whatever you want
    output_img_path = "/Users/sandrawang/Documents/Optometry_Apps/OCR_crop_results/"

    # Check if the folder exists, and if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created folder: {output_dir}")

    # Read image
    img = cv2.imread(image_path) 

    #Convert to grayscale
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find edges
    edges = cv2.Canny(gray_scale, 50, 150)

    #Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crop and save areas that look like labels
    index = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 60 and h > 100:  # adjust this based on your label size
            cropped = img[y:y+h, x:x+w]
            output_path = os.path.join(output_dir, f"{os.path.basename(output_img_path)}_crop_{index}.jpg")
            cv2.imwrite(output_path, cropped)
            index += 1

    print(f"Processed {index} cropped images and saved to {output_dir}")

post_process_image("ocr_test/OCR-test3.jpeg")

