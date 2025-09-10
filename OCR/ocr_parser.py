from rapidfuzz import process, fuzz
import math
# from contacts import Contacts


def parse_contact_lens_data(text_data):

    line_keywords = find_title_keywords(text_data)
    brand, line = find_brand_and_line(line_keywords)
    print("Matched line:", line, "Brand:", brand)
    
    #Param_keys and param_values are dicts of words with their centers
    param_keys, param_values = clean_param(text_data)
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

def find_title_keywords(text_data):
    # Normalize OCR words
    words = text_data.keys()
    
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
    keyword_values = ["7", "30", "1"]
    
    line_keywords = {}

    line_values = {}
    

    for word in words:
        if word not in line_keywords:
                keyword_matched = find_best_match(word, keywords)
                value_matched = find_best_match(word, keyword_values)
                if keyword_matched:
                    line_keywords[keyword_matched] = get_center_of_vertices(text_data[word])
                if value_matched:
                    line_values[value_matched] = get_center_of_vertices(text_data[word])
    
    #If there are line_values, check if the values are close to title keywords total or precision
    if "TOTAL" in line_keywords or "PRECISION" in line_keywords:
        #find closest value to the keyword TOTAL or PRECISION
        closest_value = None
        if "TOTAL" in line_keywords:
            closest_value = find_closest_right_value(line_keywords["TOTAL"], line_values)
        else:
            closest_value = find_closest_right_value(line_keywords["PRECISION"], line_values)
        #Add closest_value to line_keywords
        if closest_value:
            line_keywords[closest_value] = None

    #Only return keywords, no more need to word location data
    line_keywords = list(line_keywords.keys())

    # seperate any TOTAL30s, PRECISION7s, etc
    if "TOTAL30" in line_keywords:
        line_keywords.remove("TOTAL30")
        line_keywords.append("TOTAL")
        line_keywords.append("30")
    elif "TOTAL1" in line_keywords:
        line_keywords.remove("TOTAL1")
        line_keywords.append("TOTAL")
        line_keywords.append("1")
    elif "PRECISION1" in line_keywords:
        line_keywords.remove("PRECISION1")
        line_keywords.append("PRECISION")
        line_keywords.append("1")
    elif "PRECISION7" in line_keywords:
        line_keywords.remove("PRECISION7")
        line_keywords.append("PRECISION")
        line_keywords.append("7")
    
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
                      "COMFILCON XR",
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
                  "PRECISION 1",
                  "PRECISION 1 FOR ASTIGMATISM",
                  "PRECISION 7",
                  "PRECISION 7 FOR ASTIGMATISM", 
                  "TOTAL 30",
                  "TOTAL 30 FOR ASTIGMATISM"]
        
    }
    
    #normalize keywords
    keywords = [k.upper() for k in keywords]
    brand = None
    line = None

    coopervision_brand_conversion = {"COMFILCON": "BIOFINITY",
                                     "COMFILCON XR": "BIOFINITY XR",
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
def clean_param(text_data):
    words = list(text_data.keys())
    values = {}
    params = {}
    
    word_bank ={
        "Power": ["SPH", "PWR", "D"],
        "Cylinder": ["CYL"],
        "Axis": ["AXIS", "AX"],
        "Add": ["ADD"]
    }

    Add_values =  ["HIGH", "MID", "MED", "LOW"]

    skip_next = False
    for i in range(len(words)):
        word = words[i]
        if not skip_next:
            # if the word is a sign, try to combine with next word and skip next
            if  (word == "-" or word == "+") and i + 1 < len(words):
                    try:
                        next = words[i+1]

                        #Check if next word is a float, if not then fail to combine
                        float(next)
                        
                        #create new bounding box
                        new_box = find_new_bounding_box(text_data[word], text_data[next])
                        values[word + next] = get_center_of_vertices(new_box)
                        skip_next = True
                    
                    except ValueError:
                        # print(f"{word} and {words[i+1]} could not be combined into a valid number.")
                        pass
            
            #If word has sign and value, keep as is
            elif "+" == word[0] or "-" == word[0]:
                values[word] = get_center_of_vertices(text_data[word])
            
            #else try to convert word to float directly, append if valid
            else:
                try:
                    float(word)
                    values[word] = get_center_of_vertices(text_data[word])
                except ValueError:
                    word = word.upper()
                    if word in word_bank["Power"]:
                        params["Power"] = get_center_of_vertices(text_data[word])
                    elif word in word_bank["Cylinder"]:
                        params["Cylinder"] = get_center_of_vertices(text_data[word])
                    elif word in word_bank["Axis"]:
                        params["Axis"] =  get_center_of_vertices(text_data[word])
                    elif word in word_bank["Add"]:
                        params["Add"] = get_center_of_vertices(text_data[word])
                    elif word in Add_values:
                        values[word] = get_center_of_vertices(text_data[word])
                    elif word == "N" or word == "D":
                        values[word] = get_center_of_vertices(text_data[word])
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
        temp_val = val.replace('+', '').strip()
    if not val.isdigit():
        try:
            temp_val = float(temp_val)
            valid = -12.00 <= temp_val <= 8.00 and (val * 100) % 25 == 0  # checks for 0.25 increments
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None

def is_valid_cyl(val):
    if not val.isdigit():
        try:
            temp_val = float(val)
            valid = (-6.0 <= temp_val <= 0.00 or 0.25 <= temp_val <= 6.0) and (temp_val * 100) % 25 == 0
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None
    
def is_valid_axis(val):
    if val.isdigit():
        try:
            temp_val = int(val)
            valid = 0 <= temp_val <= 180
            return valid, val
        except ValueError:
            return False, None
    else:
        return False, None
    
def is_valid_add(val):
    #ADD values can be floats or strings (HIGH, MID, LOW)
    if '+' in val:
        temp_val = val.replace('+', '').strip()
    if not val.is_digit():
        try:
            temp_val = float(temp_val)
            valid = 0.75 <= temp_val <= 3.00 and (temp_val * 100) % 25 == 0  # checks for 0.25 increments
            return valid, val
        except ValueError:
            if val.upper() in ["HIGH", "MID", "MED", "LOW"]:
                return True, val.upper()
            else:                           
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

def find_closest_right_value(keyword_center, values):
    closest_distance = float('inf')
    closest_value = None
    keyword_center_x, keyword_center_y  = keyword_center
    for value, value_center in values.items():
        value_center_x, value_center_y = value_center
        if value_center_x > keyword_center_x:
            distance  = math.sqrt((value_center_x - keyword_center_x)**2 + (value_center_y - keyword_center_y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_value = value
    return closest_value


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
