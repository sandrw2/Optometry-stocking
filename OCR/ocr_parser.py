from rapidfuzz import process, fuzz
from contacts import Contacts


def parse_contact_lens_data(text_details):

    ocr_words = list(text_details.keys())
    half_length = len(ocr_words) // 2
    title_half = ocr_words[:half_length]
    title_data = read_title(title_half)
    
    #Param_keys and param_values are dicts of words with their centers
    param_keys, param_values = clean_param(ocr_words[half_length:], text_details)
    print(param_keys, param_values)
    param_data = match_parameters(param_keys, param_values)

    # contact_lens = Contacts(
    #     brand=title_data.get("Brand"),
    #     line=title_data.get("Line"),
    #     typ=title_data.get("Type"),
    #     duration=title_data.get("Duration"),
    #     power=param_data.get("Power"),
    #     cylinder=param_data.get("Cylinder"),
    #     axis=param_data.get("Axis"),
    #     add=param_data.get("Add"),
    # )

    # print(contact_lens.to_dict())
    # return contact_lens


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
        print("checking word:", word, details[word])
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
                        print(f"{word} and {words[i+1]} could not be combined into a valid number.")
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
                        print("Skipping unrecognized word:", word)
        if skip_next:
            print("Skipped next word due to sign combination.")
            skip_next = False
    print("Params:", params)
    print("Values:", values)
    return params, values

def find_new_bounding_box(box1, box2):
        new_box_values = box1 + box2
        left = min(x for x, _ in new_box_values)
        top = min(y for _, y in new_box_values)
        right = max(x for x, _ in new_box_values)
        bottom = max(y for _, y in new_box_values) 
        return (left, top), (right, top), (right, bottom), (left, bottom)

def find_best_match(word, bank, threshold=80):
        match, score, _ = process.extractOne(word, bank, scorer=fuzz.ratio)
        return match if score >= threshold else None

def read_title(title):
    # Normalize OCR words
    title = [w.upper() for w in title]
    
    word_bank = {
    "Brand": ["COMFILCON", "ACUVUE", "BIOFINITY", "AIR OPTIX", "BAUSCH", "TOTAL1","TOTAL30", "PRECISION1", "PRECISION7", "1 DAY"],
    "Line": ["HYDRALUXE", "MAX", "MOIST", "HYDRACLEAR"],
    "Type": ["TORIC", "ASTIGMATISM", "MULTIFOCAL", "PRESBYOPIA"],
    "Duration": ["1-DAY"]
    }


    data = {
        "Brand": None,
        "Line": None,
        "Type": "Spherical",
        "Duration": None
    }
    

    for word in title:
        for category in data.keys():
            if data[category] == None or data[category] == "Spherical":
                matched = find_best_match(word, word_bank[category])
                if matched:
                    data[category] = matched
                    break
    
    return data

def get_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def match_parameters(params, values):
    data  = {}
    for param in params.keys():
        param_center_x, param_center_y = params[param]
        closest_value = None
        closest_distance = float('inf')

        for value, value_center in values.items():
            print("checking value:", value, "for param:", param)
            value_center_x, value_center_y = value_center
            if value_center_x >= param_center_x:
                distance = get_distance((param_center_x, param_center_y), (value_center_x, value_center_y))
                if distance < closest_distance:
                        print("found closer value:", value, "for param:", param, "distance:", distance)
                        valid, valid_val = is_valid_parameter_value(param, value)
                        if valid:
                            print("valid value:", valid_val, "for param:", param)
                            closest_distance = distance
                            closest_value = value
        if closest_value is None:
            for value, value_center in values.items():
                value_center_y, value_center_y = value_center
                if value_center_y >= param_center_y:
                    distance = get_distance((param_center_x, param_center_y), (value_center_x, value_center_y))
                    if distance < closest_distance:
                        valid, valid_val = is_valid_parameter_value(param, value)
                        if valid:
                            closest_distance = distance
                            closest_value = value

        if closest_value is not None:
            try:
                data[param] = closest_value
            except ValueError:
                print("Could not convert value to float:", closest_value)
    print(data)
    return data
        


def get_center_of_vertices(vertices):
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    center_x = sum(x_coords) / len(vertices)
    center_y = sum(y_coords) / len(vertices)
    return center_x, center_y


def is_valid_parameter_value(param, val):
    if param == "Power":
        valid, valid_val = is_valid_sph(val)
    elif param == "Cylinder":
        valid, valid_val = is_valid_cyl(val)
    elif param == "Axis":
        print(val)
        valid, valid_val = is_valid_axis(val)
        print(valid_val)    
    elif param == "Add":
        valid, valid_val = is_valid_add(val)
    else:
        print("not a valid param:", param)
        return False, None
    return valid, valid_val
    

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