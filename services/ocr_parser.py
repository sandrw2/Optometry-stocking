from rapidfuzz import process, fuzz
import math
import re
import os
import json
# from contacts import Contacts


def parse_contact_lens_data(text_data):

    line_keywords = find_title_keywords(text_data)
    brand, line = find_brand_and_line(line_keywords)
    print("Matched line:", line, "Brand:", brand)
    
    #Param_keys and param_values are dicts of words with their centers
    param_keys, param_values = parse_param_and_values(text_data)
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
                    line_keywords[keyword_matched] = text_data[word]
                if value_matched:
                    line_values[value_matched] = text_data[word]
    
    # If there are line_values, check if the values are close to title keywords total or precision
    # Case: Total and Precision always have a number following after. Therefore, find the closest value 
    #to the right of the keyword. 
    # (Note: If the number is not read, and there is any other value that matches
    # "7", "30", "1", this will be considered the closest value resulting in unexpected behavior)

    if "TOTAL" in line_keywords or "PRECISION" in line_keywords:
        #find closest value to the keyword TOTAL or PRECISION
        pattern = re.compile(r"^(30|7|1)$")
        closest_value = None
        if "TOTAL" in line_keywords:
            closest_value = find_closest_right_value(line_keywords["TOTAL"], line_values, pattern)
        else:
            closest_value = find_closest_right_value(line_keywords["PRECISION"], line_values, pattern)
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

def get_contact_type(line):
    if line == None:
        return "SPHERE"
    elif "MULTIFOCAL" in line and "ASTIGMATISM" in line:
        return "MULTIFOCAL ASTIGMATISM"
    elif "ASTIGMATISM" in line or  "TORIC" in line:
        return "ASTIGMATISM"
    elif "MULTIFOCAL" in line:
        return "MULTIFOCAL"
    else:
        return "SPHERE"
    

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
def parse_param_and_values(text_data):
    values = {}
    params = {}
    
    word_bank ={
        "Power": ["SPH", "PWR", "D"],
        "Cylinder": ["CYL"],
        "Axis": ["AXIS", "AX"],
        "Add": ["ADD"],
        "Add_values": ["HIGH", "HGH", "HI", "MID", "MED", "LOW", "LO"],
        "Signs": ["+", "-"],
        "Dominant": ["N", "D"]
    }

    power_regex_no_sign = re.compile(r"(?:\d{1,2}\.\d{2}|PLANO)")
    power_regex = re.compile(r"(?:[+-]?\d{1,2}\.\d{2}|PLANO)")
    cylinder_regex = re.compile(r"[+-]?\d{1,2}\.\d{2}")
    axis_regex = re.compile(r"\d{1,3}")   # filter later for <=180
    add_regex = re.compile(r"([+-]?\d{1,2}(?:\.\d{2})?)([DN])?")
    cyl_axis_regex = re.compile(r"([+-]?\d{1,2}\.\d{2})\s*[xX]\s*(\d{1,3})°?"
)


    # Detect all parameters and values 
    # 1) If word matches the word banks of POWER, CYLINDER, AXIS, ADD then add the parameter and center
    #   coordinate to the params dict 
    # 2) If word matches the word banks of Add_values, Signs, Dominant, then add the value and the center
    #   coordinate to the values dict
    # 3) If word matches the regex values for power, cyl, axis, and add, then add the value and the center
    #   coordinate to the values dict

    for word, bbox in text_data.items():
        if word in word_bank["Power"]:
            if "Power" in params:
                params["Power"][word] = bbox
            else:
                params["Power"] = {word : bbox}
        elif word in word_bank["Cylinder"]:
            params["Cylinder"] = bbox
        elif word in word_bank["Axis"]:
            params["Axis"] = bbox
        elif word in word_bank["Add"]:
            params["Add"] = bbox
        elif word in word_bank["Add_values"] or word in word_bank["Signs"] or word in word_bank["Dominant"]:
            values[word] = bbox
        else:
            # check regex 
            if power_regex.fullmatch(word):
                values[word] = bbox
            elif cylinder_regex.fullmatch(word):
                values[word] = bbox
            elif axis_regex.fullmatch(word):
                values[word] = bbox
            elif add_regex.fullmatch(word):
                values[word] = bbox
            elif cyl_axis_regex.fullmatch(word):
                match = re.match(r"\s*([+-]?\d+(?:\.\d+)?)\s*[xX]\s*(\d{1,3})", word)
                if match:
                    values[word] = bbox
            else:
                pass
    
    #Patch: If Power has two values such as PWR and D, create separate
    #dict entry for D 
    #else set power to the first thing on the list
    #result should be Params["Power"] = singular_power_bbox
    if "Power" in params:
        if len(params["Power"]) > 1:
            values["D"] = params["Power"].get("D")
            params["Power"] = params["Power"].get("PWR")
        else:
            params["Power"] = list(params["Power"].values())[0]

    #Clean values dict by combining "+" "-" and "N" "D" values to the numerical value
    #Check for closest right value that matches add regex value 
    sign_set = ["+", "-", "D", "N"]
    while any(item in values for item in sign_set):
        concatenate_direction = None
        if "+" in values or "-" in values:
            concatenate_direction = "prefix"
            sign = "+" if "+" in values else "-"
            sign_bbox = values[sign]
            closest_val = find_closest_right_value(sign_bbox, values, power_regex_no_sign)
            print(f"found closest_val {closest_val} for {sign}")
            
        elif "N" in values or "D" in values:
            concatenate_direction = "suffix"
            sign = "N" if "N" in values else "D"
            sign_bbox = values[sign]
            closest_val = find_closest_left_value(sign_bbox, values, power_regex)

        if closest_val:
                #Concatenate sign and closest val
                new_val = ""
                bbox_sign = text_data[sign]
                bbox_val = text_data[closest_val]
                combined_bbox = find_new_combined_box(bbox_sign, bbox_val)
                if concatenate_direction == "prefix":
                    new_val = sign + closest_val
                else:
                    new_val = closest_val + sign
                #update values dict
                values[new_val] = combined_bbox
                values.pop(closest_val)

        #remove values dict
        values.pop(sign)

    return params, values

def find_new_combined_box(box1, box2):
        new_box_values = box1 + box2
        left = min(x for x, _ in new_box_values)
        top = min(y for _, y in new_box_values)
        right = max(x for x, _ in new_box_values)
        bottom = max(y for _, y in new_box_values) 
        return (left, top), (right, top), (right, bottom), (left, bottom)

def match_parameters(params, values, typ):
    # ISSUE: Find better way for when to match vertical vs horizontal
    matches  = {}
    typs = {
        "SPHERE" : ["Power"],
        "ASTIGMATISM" : ["Power", "Cylinder", "Axis"],
        "MULTIFOCAL" : ["Power", "Add"],
        "MULTIFOCAL ASTIGMATISM": ["Power", "Cylinder", "Axis", "Add"]

    }
    needed_params = typs[typ]


    # If type is astigmatism and has a value that match "cyl x axis" format then 
    # match cyl and axis to corresponding values and add into matches dictionary
    cyl_axis_regex = re.compile(r"([+-]?\d{1,2}\.\d{2})\s*[xX]\s*(\d{1,3})°?")
    for val in values: 
        match = cyl_axis_regex.fullmatch(val)
        if match and typ == "ASTIGMATISM":
            cyl, axis = match.groups()
            matches["Cylinder"] = cyl
            matches["Axis"] = axis
            needed_params.remove("Cylinder")
            needed_params.remove("Axis")


    # For each needed parameter given type, look at all values and match by the 
    # closest proximity. Check Horizontal first, then vertical
    for param in needed_params:
        if param in params.keys():
            param_bbox = params[param]
            best_value = None
            best_score = float('inf')            

            #Check values to the right of param first
            for value, value_bbox in values.items():
                value_center_x,_ = get_center(value_bbox)
                param_center_x,_ = get_center(param_bbox)
                if value_center_x > param_center_x:
                    new_score = get_score("Horizontal", param_bbox, value_bbox)
                    if new_score < best_score:
                            valid, valid_val = is_valid_parameter_value(param, value)
                            if valid:
                                best_score = new_score
                                best_value = valid_val
            #Check values below if none found to the right
            for value, value_bbox in values.items():
                _, value_center_y = get_center(value_bbox)
                _, param_center_y = get_center(param_bbox)
                if value_center_y > param_center_y:
                    new_score = get_score("Vertical", param_bbox, value_bbox)
                    if new_score < best_score:
                        valid, valid_val = is_valid_parameter_value(param, value)
                        if valid:
                            best_score = new_score
                            best_value = valid_val
            matches[param] = best_value
        else:
            #Error handling for missed values
            print(f"Could not detect values for {param}")
    return matches
        
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
    temp_val = val
    if "+" in val:
        temp_val = val.replace('+', '').strip()
    if not val.isdigit():
        try:
            temp_val = float(temp_val)
            valid = -14.00 <= temp_val <= 14.00 and (temp_val * 100) % 25 == 0  # checks for 0.25 increments
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
            return valid, str(temp_val)
        except ValueError:
            return False, None
    else:
        return False, None
    
def is_valid_add(val):
    temp_val = val
    #ADD values can be floats or strings (HIGH, MID, LOW)
    if '+' in val:
        temp_val = val.replace('+', '').strip()
    if 'N' in val or 'D' in val:
        temp_val = val[:-1]
    
    if val.upper() in ["HIGH", "MID", "MED", "LOW"]:
            return True, val.upper()
    else:                           
        if not val.isdigit():
            try:
                temp_val = float(temp_val)
                valid = 0.75 <= temp_val <= 3.00 and (temp_val * 100) % 25 == 0  # checks for 0.25 increments
                return valid, val
            except ValueError:
                pass

    return False, None

################################################
#Utility functions
################################################
def get_center(vertices):
    #print(vertices)
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    center_x = sum(x_coords) / len(vertices)
    center_y = sum(y_coords) / len(vertices)
    return center_x, center_y

def find_best_match(word, bank, threshold=75):
        match, score, _ = process.extractOne(word, bank, scorer=fuzz.ratio)
        return match if score >= threshold else None

def find_closest_right_value(keyword_bbox, values, regx):
    #Implement Range Logic 
    closest_distance = float('inf')
    closest_value = None
    keyword_center_x, keyword_center_y  = get_center(keyword_bbox)
    for value, value_bbox in values.items():
        value_center_x, value_center_y = get_center(value_bbox)
        if value_center_x > keyword_center_x:
            distance  = math.sqrt((value_center_x - keyword_center_x)**2 + (value_center_y - keyword_center_y)**2)
            if distance < closest_distance and regx.fullmatch(value) and find_range(keyword_bbox):
                closest_distance = distance
                closest_value = value
    return closest_value

def find_closest_left_value(keyword_bbox, values, regx):
    #Implement range logic 
    closest_distance = float('inf')
    closest_value = None
    keyword_center_x, keyword_center_y  = get_center(keyword_bbox)
    for value, value_bbox in values.items():
        value_center_x, value_center_y = get_center(value_bbox)
        if value_center_x < keyword_center_x:
            distance  = math.sqrt((value_center_x - keyword_center_x)**2 + (value_center_y - keyword_center_y)**2)
            if distance < closest_distance and regx.fullmatch(value) and distance < find_range(value_bbox):
                closest_distance = distance
                closest_value = value
    return closest_value

def find_range(bbox):
    print(bbox)
    p1, p2, _, _ = bbox
    px1, _ = p1
    px2, _ = p2
    return abs(px2 - px1)
    
def get_score(bias, bbox1, bbox2):
    if bias == "Horizontal":
        horizontal_penalty = 1.0
        vertical_penalty = 3.0
    else:
        horizontal_penalty = 3.0
        vertical_penalty = 1.0
    point1 = get_center(bbox1)
    point2 = get_center(bbox2)
    horizontal_distance = abs(point2[0] - point1[0])
    vertical_distance = abs(point2[1] - point1[1])
    score = (horizontal_penalty * horizontal_distance) + (vertical_penalty * vertical_distance)
    return score 

if __name__ == "__main__":
    output_file = "/Users/sandrawang/Documents/Optometry_Apps/Optometry-stocking/output/ocr_results.json"
    all_results = None
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            all_results = json.load(f)
        print(f"Loaded OCR results from {output_file}")

    keywords = find_title_keywords(all_results["test_001.jpeg"])
    _, line = find_brand_and_line(keywords)
    typ = get_contact_type(line)
    print(typ)
    params, values = parse_param_and_values(all_results["test_001.jpeg"])
    contact_data = match_parameters(params, values, typ)
    print(contact_data)