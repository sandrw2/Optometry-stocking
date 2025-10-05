import os
import json

from OCR import detect_text, draw_boxes, find_title_keywords, parse_param_and_values, match_parameters, find_brand_and_line, get_contact_type

def get_ocr_results(input_img_folder, output_file):
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            all_results = json.load(f)
        print(f"Loaded OCR results from {output_file}")
    else:
        # WARNING!! pass for now to avoid calling vision on the entire folder again!!
        return
        all_results = {}
        for filename in os.listdir(input_img_folder):
            # Only process image files (basic check)
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(input_img_folder, filename)
                
                text_details = detect_text(image_path)
                all_results[filename] = text_details
                print(f"Added result for {filename}..")

        with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"All OCR results saved to {output_file}")

    return all_results


def create_ocr_bboxes(input_image_folder_path, all_results, boxed_image_folder_path):
    if not os.path.exists(boxed_image_folder_path):
        os.makedirs(boxed_image_folder_path)

    for img_name, image_result in all_results.items():
        image_path = os.path.join(input_image_folder_path, img_name)
        output_path = os.path.join(boxed_image_folder_path, f"boxed_{img_name}")

        if not os.path.exists(image_path):
            print(f"Image {img_name} not found in {input_image_folder_path}, skipping.")
            continue

        draw_boxes(image_path, image_result, output_path)

def get_all_title_keywords(all_results, output_file):
    keywords_results = {}
    for img_name, img_data in all_results.items():
        keywords_results[img_name] = find_title_keywords(img_data)

    with open(output_file, "w", encoding="utf-8") as f:
            json.dump(keywords_results, f, indent=2, ensure_ascii=False)

def get_all_parameter_values(all_results, output_file):
    param_values = {}
    for img_name, img_data in all_results.items():
        param_values[img_name] = parse_param_and_values(img_data)
        print(f"called param function for {img_name}")
    
    with open(output_file, "w", encoding="utf-8") as f:
            json.dump(param_values, f, indent=2, ensure_ascii=False)
    
    print(f"All param results saved to {output_file}")

def get_all_matched_parameter_values(all_results, output_file):
    param_values = {}
    for img_name, img_data in all_results.items():
        params, values = parse_param_and_values(img_data)
        keywords = find_title_keywords(img_data)
        _, line = find_brand_and_line(keywords)
        typ = get_contact_type(line)
        param_values[img_name] = match_parameters(params, values, typ)
        print(f"called param match function for {img_name}")
    
    with open(output_file, "w", encoding="utf-8") as f:
            json.dump(param_values, f, indent=2, ensure_ascii=False)
    
    print(f"All param results saved to {output_file}")
     
     



