from helper import get_ocr_results, create_ocr_bboxes, get_all_title_keywords, get_all_parameter_values, get_all_matched_parameter_values


if __name__ == "__main__":

    input_image_folder_path = "OCR_test/test_images"
    output_file = "output/ocr_results.json"
    keyword_file = "output/all_keywords.json"
    parameter_file = "output/all_param_values.json"
    boxed_image_folder_path = "output/bounded_images"
    matched_parameter_file = "output/matched_parameter_values.json"

    
    all_results = get_ocr_results(input_image_folder_path, output_file)
        
    #create_ocr_bboxes(input_image_folder_path, all_results, boxed_image_folder_path)

    #get_all_title_keywords(all_results, keyword_file)

    get_all_parameter_values(all_results, parameter_file)

    get_all_matched_parameter_values(all_results, matched_parameter_file)

