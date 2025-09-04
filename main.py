from helper import get_ocr_results, create_ocr_bboxes








if __name__ == "__main__":

    input_image_folder_path = "test_images"
    output_file = "output/ocr_results.json"
    
    all_results = get_ocr_results(input_image_folder_path, output_file)
    
    boxed_image_folder_path = "output/bounded_images"
    create_ocr_bboxes(input_image_folder_path, all_results, boxed_image_folder_path)
