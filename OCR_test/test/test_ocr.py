
# ====================================================================================
# IF RUNNING FROM OUTMOST DIRECTORY!!
import sys
import os

# Add project root (one level above OCR_test) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from OCR import find_brand_and_line, find_title_keywords
# ====================================================================================

import pytest
import json

# Load precomputed OCR results
with open("output/ocr_results.json", "r", encoding="utf-8") as f:
    all_results = json.load(f)

test_cases = [
    ("test_001.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_002.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_003.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_004.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_005.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_006.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_007.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_008.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_009.jpeg", ("COOPERVISION", "MYDAY MULTIFOCAL")),
    ("test_010.jpeg", ("ACUVUE", "ACUVUE OASYS MAX 1-DAY MULTIFOCAL")),
    ("test_011.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_012.jpeg", ("BAUSCH+LOMB", "ULTRA MULTIFOCAL FOR ASTIGMATISM")),
    ("test_013.jpeg", ("COOPERVISION", "BIOFINITY TORIC XR")),
    ("test_014.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_015.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_016.jpeg", ("ACUVUE", "1-DAY ACUVUE MOIST")),
    ("test_017.jpeg", ("ALCON", "TOTAL30 FOR ASTIGMATISM")),
    ("test_018.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_019.jpeg", ("ALCON", "PRECISION1 FOR ASTIGMATISM")),
    ("test_020.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_021.jpeg", ("ACUVUE", "ACUVUE OASYS 2-Week")),
    ("test_022.jpeg", ("ALCON", "DAILIES TOTAL1")),
    ("test_023.jpeg", ("COOPERVISION", "MYDAY TORIC")),
    ("test_024.jpeg", ("ALCON", "PRECISION1")),
    ("test_025.jpeg", ("ACUVUE", "ACUVUE OASYS 2-Week FOR ASTIGMATISM")),
    ("test_026.jpeg", ("ALCON", "DAILIES TOTAL1")),
    ("test_027.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_028.jpeg", ("ACUVUE", "ACUVUE OASYS MAX 1-DAY MULTIFOCAL")),
    ("test_029.jpeg", ("COOPERVISION", "BIOFINITY TORIC XR")),
    ("test_030.jpeg", ("ACUVUE", "ACUVUE OASYS 1-DAY FOR ASTIGMATISM")),
    ("test_031.jpeg", ("COOPERVISION", "MYDAY TORIC")),
    ("test_032.jpeg", ("ACUVUE", "ACUVUE OASYS 2-Week")),
    ("test_033.jpeg", ("ALCON", "PRECISION1")),
    ("test_034.jpeg", ("ALCON", "TOTAL30 FOR ASTIGMATISM")),
    ("test_035.jpeg", ("ACUVUE","ACUVUE OASYS 2-Week FOR ASTIGMATISM")),
    ("test_036.jpeg", ("COOPERVISION", "MYDAY MULTIFOCAL")),
    ("test_037.jpeg", ("COOPERVISION", "BIOFINITY TORIC")),
    ("test_038.jpeg", ("BAUSCH+LOMB", "ULTRA MULTIFOCAL FOR ASTIGMATISM")),
    ("test_039.jpeg", ("ALCON", "PRECISION1"))

]

@pytest.mark.parametrize("image_path,expected", test_cases)
def test_extract_title(image_path, expected):
    text = all_results.get(image_path, [])
    test_data = [x[0] for x in text]
    keywords = find_title_keywords(test_data)
    result = find_brand_and_line(keywords)
    assert set(result) == set(expected)

# def test_extracting_title_keywords():
#     assert 

# def test_extracting_brand_title():
#     assert add(-1, -1) == -2

# def test_matching_lines():
#     assert add(0, 5) == 5

