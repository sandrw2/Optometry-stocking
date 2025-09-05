from rapidfuzz import process, fuzz
# from contacts import Contacts


def parse_contact_lens_data(text_details):

    ocr_words = list(text_details.keys())
    half_length = len(ocr_words) // 2
    brand_line_half = ocr_words[:half_length]
    line_keywords = find_title_keywords(brand_line_half)
    brand, line = find_brand_and_line(line_keywords)
    print("Matched line:", line, "Brand:", brand)
    
    #Param_keys and param_values are dicts of words with their centers
    param_keys, param_values = clean_param(ocr_words, text_details)
    param_data = match_parameters(param_keys, param_values)
    print("Matched parameters:", param_data)

    # contact_lens = Contacts(
    #     brand=title_data.get("Brand"),
    #     subbrand=title_data.get("Subbrand"),
    #     tech = title_data.get("Tech")
    #     typ=title_data.get("Type"),
    #     duration=title_data.get("Duration"),
    #     power=param_data.get("Power"),
    #     cylinder=param_data.get("Cylinder"),
    #     axis=param_data.get("Axis"),
    #     add=param_data.get("Add"),
    # )

    # print(contact_lens.to_dict())
    # return contact_lens


#################################################
#Title matching functions 
#################################################

def find_title_keywords(title):
    # Normalize OCR words
    line_name = [w.upper() for w in title]
    
    keywords = ["ACUVUE OASYS",
                     "ACUVUE",
                     "OASYS", 
                     "AIR OPTIX", 
                     "HYDRALUXE", 
                     "MAX", 
                     "MOIST", 
                     "HYDRACLEAR", 
                     "COMFILCON", 
                     "SILICONE", 
                     "DAILIES",
                     "TOTAL30",
                     "TOTAL1",
                     "TOTAL",
                     "PRECISION",
                     "PRECISION1", 
                     "PRECISION7", 
                     "TORIC", 
                     "ASTIGMATISM", 
                     "MULTIFOCAL", 
                     "PRESBYOPIA",
                     "1-DAY",
                     "ULTRA", 
                     "BIOTRUE",
                     "XR",
                     "ALCON",
                     "BAUSCH"
                ]
    
    line_keywords = []
    

    for word in line_name:
        if word not in line_keywords:
                matched = find_best_match(word, keywords)
                if matched:
                    line_keywords.append(matched)
    
    return line_keywords

def find_brand_and_line(keywords):

    brand_line = {
        "ACUVUE": ["ACUVUE OASYS 2-WEEK HYDRACLEAR", 
                   "ACUVUE OASYS 2-WEEK FOR ASTIGMATISM HYDRACLEAR",
                   "1-DAY ACUVUE MOIST", 
                   "1-DAY ACUVUE MOIST FOR ASTIGMATISM", 
                   "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE",
                   "ACUVUE OASYS 1-DAY HYDRALUXE",
                   "ACUVUE OASYS MAX 1-DAY",
                   "ACUVUE OASYS MAX 1-DAY MULTIFOCAL"],
        "COOPERVISION": ["COMFILCON", 
                      "COMFILCON TORIC", 
                      "COMFILCON TORIC XR",
                      "COMFILCON MULTIFOCAL",
                      "1 DAY SILICONE", 
                      "1 DAY TORIC SILICONE",
                      "1 DAY MULTIFOCAL SILICONE",],
        "BAUSCH+LOMB": ["ULTRA", 
                        "ULTRA FOR ASTIGMATISM", 
                        "ULTRA FOR PRESBYOPIA",
                        "ULTRA MULTIFOCAL FOR ASTIGMATISM",
                        "INFUSE",
                        "BIOTRUE ONEDAY"],
        "ALCON": ["DAILIES TOTAL 1",
                  "PRECISION 7",
                  "PRECISION 7 FOR ASTIGMATISM", 
                  "PRECISION 1",
                  "PRECISION 1 FOR ASTIGMATISM",
                  "TOTAL 30",
                  "TOTAL 30 FOR ASTIGMATISM"]
        
    }

    {"ACUVUE": ("ACUVUE", "OASYS", "MOIST", "MAX"), }
    
    #normalize keywords
    keywords = [k.upper() for k in keywords]
    brand = None
    line = None

    coopervision_brand_conversion = {"COMFILCON": "BIOFINITY",
                                    "COMFILCON TORIC": "BIOFINITY TORIC",
                                    "COMFILCON TORIC XR": "BIOFINITY TORIC XR",
                                    "COMFILCON MULTIFOCAL": "BIOFINITY MULTIFOCAL",
                                    "1 DAY SILICONE": "MYDAY",
                                    "1 DAY TORIC SILICONE" : "MYDAY TORIC", 
                                    "1 DAY MULTIFOCAL SILICONE": "MYDAY MULTIFOCAL"
                                     }
    
                                    
    
    # First filter: Check which brand family 
    if "ACUVUE" in keywords or "OASYS" in keywords:
        brand = "ACUVUE"
        line = match_best_line(keywords, brand_line[brand])
    elif "ALCON" in keywords or "DAILIES" in keywords or "PRECISION" in keywords or "PRECISION1" in keywords or "PRECISION7" in keywords or "TOTAL" in keywords or "TOTAL1" in keywords or "TOTAL30" in keywords:
        brand = "ALCON"
        line = match_best_line(keywords, brand_line[brand])
    elif "BAUSCH" in keywords or "BIOTRUE" in keywords or "ULTRA" in keywords:
        # not the contact has samflicon which matches with COMFILCON
        brand = "BAUSCH+LOMB"
        line = match_best_line(keywords, brand_line[brand])
    elif "SILICONE" in keywords or "COMFILCON" in keywords:
        brand = "COOPERVISION"
        line = match_best_line(keywords, brand_line[brand])
        line = coopervision_brand_conversion[line]
    
    
    return brand,line
            
#returns best matching line from list given keyword list
def match_best_line(keywords, brand_lines):
    top_match = None
    top_score = float('-inf')
    #Check each line check if line contains keyword, keep highest scoring line
    #Scoring based on matched/length ratio
    for line in brand_lines:
        matched = 0 
        line_array = line.split()
        for word in keywords:
            if word in line_array: 
                matched += 1
            else:
                matched -= 1
        score = matched/len(line_array)
        if score > top_score:
            top_score = score
            top_match = line
    return top_match

#################################################
#Parameter matching functions
#################################################
def clean_param(words, details):
    values = {}
    params = {}
    
    word_bank ={
        "Power": ["SPH", "PWR", "D"],
        "Cylinder": ["CYL"],
        "Axis": ["AXIS", "AX"],
        "Add": ["ADD"]
    }

    skip_next = False
    for i in range(len(words)):
        word = words[i]
        if not skip_next:
            # if the word is a sign, try to combine with next word and skip next
            if  (word == "-" or word == "+") and i + 1 < len(words):
                    try:
                        next = words[i+1]
                        val = float(next)
                        
                        #create new bounding box
                        new_box = find_new_bounding_box(details[word], details[next])
                        values[word + next] = get_center_of_vertices(new_box)
                        skip_next = True
                    
                    except ValueError:
                        # print(f"{word} and {words[i+1]} could not be combined into a valid number.")
                        pass
            
            #If word has sign and value, keep as is
            elif "+" == word[0] or "-" == word[0]:
                values[word] = get_center_of_vertices(details[word])
            
            #else try to convert word to float directly, append if valid
            else:
                try:
                    val = float(word)
                    values[word] = get_center_of_vertices(details[word])
                except ValueError:
                    word = word.upper()
                    if word in word_bank["Power"]:
                        params["Power"] = get_center_of_vertices(details[word])
                    elif word in word_bank["Cylinder"]:
                        params["Cylinder"] = get_center_of_vertices(details[word])
                    elif word in word_bank["Axis"]:
                        params["Axis"] =  get_center_of_vertices(details[word])
                    elif word in word_bank["Add"]:
                        params["Add"] = get_center_of_vertices(details[word])
                    else:
                        pass
        else:
            skip_next = False
    return params, values

def find_new_bounding_box(box1, box2):
        new_box_values = box1 + box2
        left = min(x for x, _ in new_box_values)
        top = min(y for _, y in new_box_values)
        right = max(x for x, _ in new_box_values)
        bottom = max(y for _, y in new_box_values) 
        return (left, top), (right, top), (right, bottom), (left, bottom)

def match_parameters(params, values):
    data  = {}
    for param in params.keys():
        param_center = params[param]
        best_value = None
        best_score = float('inf')

        #Check values to the right of param first
        for value, value_center in values.items():
            new_score = get_score("Horizontal", param_center, value_center)
            if new_score < best_score:
                    valid, valid_val = is_valid_parameter_value(param, value)
                    if valid:
                        best_score = new_score
                        best_value = valid_val
        #Check values below if none found to the right
        if best_value is None:
            for value, value_center in values.items():
                new_score = get_score("Vertical", param_center, value_center)
                if new_score < best_score:
                    valid, valid_val = is_valid_parameter_value(param, value)
                    if valid:
                        best_score = new_score
                        best_value = valid_val
        data[param] = best_value
    return data
        
def is_valid_parameter_value(param, val):
    if param == "Power":
        valid, valid_val = is_valid_sph(val)
    elif param == "Cylinder":
        valid, valid_val = is_valid_cyl(val)
    elif param == "Axis":
        valid, valid_val = is_valid_axis(val)
    elif param == "Add":
        valid, valid_val = is_valid_add(val)
    else:
        return False, None
    return valid, valid_val

###############################################
#Validation functions for each parameter type
################################################

def is_valid_sph(val):
    if "+" in val:
        val = val.replace('+', '').strip()
    if not val.isdigit():
        try:
            val = float(val)
            valid = -12.00 <= val <= 8.00 and (val * 100) % 25 == 0  # checks for 0.25 increments
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None

def is_valid_cyl(val):
    if not val.isdigit():
        try:
            val = float(val)
            valid = (-6.0 <= val <= 0.00 or 0.25 <= val <= 6.0) and (val * 100) % 25 == 0
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None
    
def is_valid_axis(val):
    if val.isdigit():
        try:
            val = int(val)
            valid = 0 <= val <= 180
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None
    
def is_valid_add(val):
    if '+' in val:
        val = val.replace('+', '').strip()
    if not val.is_digit():
        try:
            val = float(val)
            valid = 0.75 <= val <= 3.00 and (val * 100) % 25 == 0  # checks for 0.25 increments
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None

################################################
#Utility functions
################################################
def get_center_of_vertices(vertices):
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    center_x = sum(x_coords) / len(vertices)
    center_y = sum(y_coords) / len(vertices)
    return center_x, center_y

def find_best_match(word, bank, threshold=75):
        match, score, _ = process.extractOne(word, bank, scorer=fuzz.ratio)
        return match if score >= threshold else None

def get_score(bias, point1, point2):
    if bias == "Horizontal":
        horizontal_penalty = 1.0
        vertical_penalty = 2.0
    else:
        horizontal_penalty = 2.0
        vertical_penalty = 1.0
    horizontal_distance = abs(point2[0] - point1[0])
    vertical_distance = abs(point2[1] - point1[1])
    score = (horizontal_penalty * horizontal_distance) + (vertical_penalty * vertical_distance)
    return score 

if __name__ == "__main__":
    print(find_best_match("DAY", ["1-DAY", "WORD"]))
