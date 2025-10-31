
# ====================================================================================
# IF RUNNING FROM OUTMOST DIRECTORY!!
import sys
import os

# Add project root (one level above OCR_test) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from services import find_brand_and_line, find_title_keywords, match_parameters, parse_param_and_values, get_contact_type
# ====================================================================================

import pytest
import json

# Load precomputed OCR results
with open("../output/ocr_results.json", "r", encoding="utf-8") as f:
    all_results = json.load(f)

title_test_cases = [
    ("test_001.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_002.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_003.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_004.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_005.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_006.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_007.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_008.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY HYDRALUXE")),
    ("test_009.jpeg", ("COOPERVISION", "MYDAY MULTIFOCAL")),
    ("test_010.jpeg", ("ACUVUE", "ACUVUE OASYS MAX 1-DAY MULTIFOCAL")),
    ("test_011.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_012.jpeg", ("BAUSCH+LOMB", "ULTRA MULTIFOCAL FOR ASTIGMATISM")),
    ("test_013.jpeg", ("COOPERVISION", "BIOFINITY TORIC XR")),
    ("test_014.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_015.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_016.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_017.jpeg", ("ALCON", "TOTAL 30 FOR ASTIGMATISM")),
    ("test_018.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_019.jpeg", ("ALCON", "PRECISION 1 FOR ASTIGMATISM")),
    ("test_020.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_021.jpeg", ("ACUVUE", "ACUVUE OASYS 2-WEEK FOR ASTIGMATISM HYDRACLEAR")),
    ("test_022.jpeg", ("ALCON", "DAILIES TOTAL 1")),
    ("test_023.jpeg", ("COOPERVISION", "MYDAY TORIC")),
    ("test_024.jpeg", ("ALCON", "PRECISION 1")),
    ("test_025.jpeg", ("ACUVUE", "ACUVUE OASYS 2-WEEK FOR ASTIGMATISM HYDRACLEAR")),
    ("test_026.jpeg", ("ALCON", "DAILIES TOTAL 1")),
    ("test_027.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_028.jpeg", ("ACUVUE", "ACUVUE OASYS MAX 1-DAY MULTIFOCAL")),
    ("test_029.jpeg", ("COOPERVISION", "BIOFINITY TORIC XR")),
    ("test_030.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM HYDRALUXE")),
    ("test_031.jpeg", ("COOPERVISION", "MYDAY TORIC")),
    ("test_032.jpeg", ("ACUVUE", "ACUVUE OASYS 2-WEEK HYDRACLEAR")),
    ("test_033.jpeg", ("ALCON", "PRECISION 1")),
    ("test_034.jpeg", ("ALCON", "TOTAL 30 FOR ASTIGMATISM")),
    ("test_035.jpeg", ("ACUVUE","ACUVUE OASYS 2-WEEK FOR ASTIGMATISM HYDRACLEAR")),
    ("test_036.jpeg", ("COOPERVISION", "MYDAY MULTIFOCAL")),
    ("test_037.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_038.jpeg", ("BAUSCH+LOMB", "ULTRA MULTIFOCAL FOR ASTIGMATISM")),
    ("test_039.jpeg", ("ALCON", "PRECISION 1")),
    ("test_040.jpeg", ("ALCON", "PRECISION 7")), 
    ("test_041.jpeg", ("ACUVUE", "ACUVUE OASYS 2-WEEK FOR ASTIGMATISM HYDRACLEAR")),
    ("test_042.jpeg", ("ALCON", "TOTAL 30 FOR ASTIGMATISM")), 
    ("test_043.jpeg", ("ALCON", "PRECISION 7")), 
    ("test_044.jpeg", ("ALCON", "PRECISION 7")),
    ("test_045.jpeg", ("COOPERVISION", "BIOFINITY MULTIFOCAL")), 
    ("test_046.jpeg", ("COOPERVISION", "BIOFINITY MULTIFOCAL")),
    ("test_047.jpeg", ("COOPERVISION", "BIOFINITY MULTIFOCAL")),
    ("test_048.jpeg", ("COOPERVISION", "BIOFINITY MULTIFOCAL")),
    ("test_049.jpeg", ("COOPERVISION", "BIOFINITY XR")),
    ("test_050.jpeg", ("COOPERVISION", "BIOFINITY XR")), 
    ("test_051.jpeg", ("COOPERVISION", "BIOFINITY XR")),
    ("test_052.jpeg", ("COOPERVISION", "BIOFINITY")),
    ("test_053.jpeg", ("COOPERVISION", "BIOFINITY")),
    ("test_054.jpeg", ("COOPERVISION", "BIOFINITY XR")),
    ("test_055.jpeg", ("COOPERVISION", "BIOFINITY XR")), 
    ("test_056.jpeg", ("COOPERVISION", "BIOFINITY")),
    ("test_057.jpeg", ("COOPERVISION", "BIOFINITY XR")),
    ("test_058.jpeg", ("COOPERVISION", "BIOFINITY"))

]

@pytest.mark.parametrize("image_path,expected", title_test_cases)
def test_extract_title(image_path, expected):
    print(f"Testing Title {image_path}..")
    text_data = all_results.get(image_path, [])
    keywords = find_title_keywords(text_data)
    result = find_brand_and_line(keywords)
    assert set(result) == set(expected)


'''
Current Issue: 
- test_003 fails due to 'D' being matched with -0.75 being closest Horizontal Value
    issue: When value is matched horizontally, vertical values are not considered
- After modification: test_004 fails due to AX being matched to 17 rather than 10
    issue: Now that we consider both closest horizontal and vertical values, Biofinity
    might match incorrect values

Tests OK to FAIL:
- test_001: 'D' not detected as keyword due to glare
 
'''
parameter_test_cases = [
    ("test_001.jpeg", {"Power": "-6.00", "Cylinder": "-1.25", "Axis": "170"}),
    ("test_002.jpeg", {"Power": "-2.75"}),
    ("test_003.jpeg", {"Power": "-6.50", "Cylinder": "-0.75", "Axis": "10"}),
    ("test_004.jpeg", {"Power": "-0.50", "Cylinder": "-1.25", "Axis": "10"}),
    ("test_005.jpeg", {"Power": "-1.50", "Cylinder": "-1.25", "Axis": "170"}),
    ("test_006.jpeg", {"Power": "-3.00", "Cylinder": "-0.75", "Axis": "90"}),
    ("test_007.jpeg", {"Power": "-1.00", "Cylinder": "-1.25", "Axis": "180"}),
    ("test_008.jpeg", {"Power": "-4.75"}),
    ("test_009.jpeg", {"Power": "+2.00", "Add": "HIGH"}),
    ("test_010.jpeg", {"Power": "-5.75", "Add": "+1.75"}),
    ("test_011.jpeg", {"Power": "+0.50", "Cylinder": "-0.75", "Axis": "180"}),
    ("test_012.jpeg", {"Power": "-3.50", "Cylinder": "-1.75", "Axis": "180", "Add": "HIGH"}),
    ("test_013.jpeg", {"Power": "-4.50", "Cylinder": "-3.25", "Axis": "180"}),
    ("test_014.jpeg", {"Power": "-2.00", "Cylinder": "-0.75", "Axis": "30"}),
    ("test_015.jpeg", {"Power": "-4.50", "Cylinder": "-0.75", "Axis": "10"}),
    ("test_016.jpeg", {"Power": "-3.00"}),
    ("test_017.jpeg", {"Power": "-4.50", "Cylinder": "-0.75", "Axis": "10"}),
    ("test_018.jpeg", {"Power": "-3.00", "Cylinder": "-1.75", "Axis": "170"}),
    ("test_019.jpeg", {"Power": "-5.00", "Cylinder": "-1.25", "Axis": "10"}),
    ("test_020.jpeg", {"Power": "-6.00", "Cylinder": "-0.75", "Axis": "180"}),
    ("test_021.jpeg", {"Power": "+0.50", "Cylinder": "-1.75", "Axis": "180"}),
    ("test_022.jpeg", {"Power": "-9.00"}),
    ("test_023.jpeg", {"Power": "-6.50", "Cylinder": "-0.75", "Axis": "10"}),
    ("test_024.jpeg", {"Power": "-8.00"}),
    ("test_025.jpeg", {"Power": "-8.00", "Cylinder": "-2.25", "Axis": "10"}),
    ("test_026.jpeg", {"Power": "-9.00"}),
    ("test_027.jpeg", {"Power": "-3.00", "Cylinder": "-0.75", "Axis": "180"}),
    ("test_028.jpeg", {"Power": "-5.75", "Add": "+1.75"}),
    ("test_029.jpeg", {"Power": "-4.50", "Cylinder": "-2.75", "Axis": "180"}),
    ("test_030.jpeg", {"Power": "-0.50", "Cylinder": "-1.75", "Axis": "180"}),
    ("test_031.jpeg", {"Power": "-0.50", "Cylinder": "-0.75", "Axis": "180"}),
    ("test_032.jpeg", {"Power": "-1.25"}),
    ("test_033.jpeg", {"Power": "-7.50"}),
    ("test_034.jpeg", {"Power": "-5.00", "Cylinder": "-0.75", "Axis": "170"}),
    ("test_035.jpeg", {"Power": "-8.00", "Cylinder": "-2.25", "Axis": "170"}),
    ("test_036.jpeg", {"Power": "+1.50", "Add": "MED"}),
    ("test_037.jpeg", {"Power": "-0.50", "Cylinder": "-1.25", "Axis": "170"}),
    ("test_038.jpeg", {"Power": "-4.50", "Cylinder": "-1.25", "Axis": "180", "Add": "LOW"}),
    ("test_039.jpeg", {"Power": "-0.50"}),
    ("test_040.jpeg", {"Power": "-2.25"}),
    ("test_041.jpeg", {"Power": "-3.00", "Cylinder": "-0.75", "Axis": "180"}),
    ("test_042.jpeg", {"Power": "-0.50", "Cylinder": "-0.75", "Axis": "80"}),
    ("test_043.jpeg", {"Power": "+0.50"}),
    ("test_044.jpeg", {"Power": "+5.50"}),
    ("test_045.jpeg", {"Power": "+1.25", "Add": "+2.00N"}),
    ("test_046.jpeg", {"Power": "+0.25", "Add": "+2.00D"}),
    ("test_047.jpeg", {"Power": "+0.50", "Add": "+1.00D"}),
    ("test_048.jpeg", {"Power": "+0.25", "Add": "+2.50N"}),
    ("test_049.jpeg", {"Power": "+14.00"}),
    ("test_050.jpeg", {"Power": "+12.50"}), 
    ("test_051.jpeg", {"Power": "+13.50"}),
    ("test_052.jpeg", {"Power": "+7.50"}), 
    ("test_053.jpeg", {"Power": "+1.50"}), 
    ("test_054.jpeg", {"Power": "-13.00"}),
    ("test_055.jpeg", {"Power": "-14.00"}),
    ("test_056.jpeg", {"Power": "-2.00"}),
    ("test_057.jpeg", {"Power": "-18.00"}),
    ("test_058.jpeg", {"Power": "-4.50"})
  
]

@pytest.mark.parametrize("image_path,expected", parameter_test_cases)
def test_extract_parameters(image_path, expected):
    print(f"Testing Parameters {image_path}..")
    text_data = all_results.get(image_path, [])
    #Find brand line and type
    keywords = find_title_keywords(text_data)
    _, line = find_brand_and_line(keywords)
    typ = get_contact_type(line)
    params, values = parse_param_and_values(text_data)
    result = match_parameters(params, values, typ)
    assert result == expected

# def test_matching_lines():
#     assert add(0, 5) == 5

