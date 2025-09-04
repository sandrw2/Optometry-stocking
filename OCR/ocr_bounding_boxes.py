from PIL import Image, ImageDraw, ImageOps

def draw_boxes(img_path, img_result, output_path):
    # Open the image and fix orientation
    img = Image.open(img_path)
    img = ImageOps.exif_transpose(img)
    draw = ImageDraw.Draw(img)

    # Draw each word's bounding box
    for word, vertices in img_result.items():
        xs, ys = zip(*vertices)
        left, top, right, bottom = min(xs), min(ys), max(xs), max(ys)

        draw.rectangle([left, top, right, bottom], outline="red", width=3)
        draw.text((left, top - 15), word, fill="blue")

    # Save the boxed image
    img.save(output_path)
    print(f"Saved boxed image to {output_path}")