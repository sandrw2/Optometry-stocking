
# ====================================================================================
# IF RUNNING FROM OUTMOST DIRECTORY!!
import sys
import os

# Add project root (one level above OCR_test) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from OCR import find_brand_and_line
# ====================================================================================

import pytest
import json

# Load precomputed OCR results
with open("output/ocr_results.json", "r", encoding="utf-8") as f:
    all_results = json.load(f)

test_cases = [
    ("test_001.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_002.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_003.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_004.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_005.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_006.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_007.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_008.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_009.jpeg", ("COOPERVISION", "MYDAY MULTIFOCAL")),
    ("test_010.jpeg", ("ACUVUE", "ACUVUE OASYS MAX 1-DAY MULTIFOCAL")),
    ("test_011.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_012.jpeg", ("BAUSCH+LOMB", "ULTRA MULTIFOCAL FOR ASTIGMATISM")),
    ("test_013.jpeg", ("COOPERVISION", "BIOFINITY TORIC XR")),
    ("test_014.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_015.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_016.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_017.jpeg", ("ALCON", "TOTAL30 FOR ASTIGMATISM")),
    ("test_018.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY ASTIGMATISM")),
    ("test_019.jpeg", ("ALCON", "PRECISION1 FOR ASTIGMATISM")),
    ("test_020.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_021.jpeg", ["ACUVUE", "OASYS", "HYDRACLEAR", "ASTIGMATISM"]),
    ("test_022.jpeg", ["DAILIES", "TOTAL1", "ALCON"]),
    ("test_023.jpeg", ["1-DAY", "TORIC", "SILICONE"]),
    ("test_024.jpeg", ["PRECISION1", "ALCON"]),
    ("test_025.jpeg", ["ACUVUE", "OASYS", "HYDRACLEAR", "ASTIGMATISM"]),
    ("test_026.jpeg", ["DAILIES", "TOTAL1", "ALCON"]),
    ("test_027.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_028.jpeg", ["ACUVUE", "OASYS", "MAX", "1-DAY", "MULTIFOCAL"]),
    ("test_029.jpeg", ["COMFILCON", "XR", "TORIC"]),
    ("test_030.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_031.jpeg", ["1-DAY", "TORIC", "SILICONE"]),
    ("test_032.jpeg", ["ACUVUE", "OASYS", "HYDRACLEAR"]),
    ("test_033.jpeg", ["PRECISION1", "ALCON"]),
    ("test_034.jpeg", ["TOTAL30", "ASTIGMATISM", "ALCON"]),
    ("test_035.jpeg", ["ACUVUE", "OASYS", "HYDRACLEAR", "ASTIGMATISM"]),
    ("test_036.jpeg", ["1-DAY", "MULTIFOCAL", "SILICONE"]),
    ("test_037.jpeg", ["COMFILCON", "TORIC"]),
    ("test_038.jpeg", ["BAUSCH+LOMB", "ULTRA", "MULTIFOCAL", "ASTIGMATISM"]),
    ("test_039.jpeg", ["PRECISION1", "ALCON"])

]

@pytest.mark.parametrize("image_path,expected", test_cases)
def test_extract_title(image_path, expected):
    print(f"Testing {image_path}..")
    text = all_results.get(image_path, [])
    test_data = [x[0] for x in text]
    result = find_brand_and_line(test_data)
    assert set(result) == set(expected)

# def test_extracting_title_keywords():
#     assert 

# def test_extracting_brand_title():
#     assert add(-1, -1) == -2

# def test_matching_lines():
#     assert add(0, 5) == 5

