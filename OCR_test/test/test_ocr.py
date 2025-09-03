from OCR.ocr_parser import find_title_keywords, find_brand_and_line, match_best_line 
from OCR.ocr_text import detect_text 
import pytest


test_cases = [
    ("test_001.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_002.jpeg", ["1-DAY", "ACUVUE", "MOIST"]),
    ("test_003.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_004.jpeg", ["COMFILCON", "TORIC"]),
    ("test_005.jpeg", ["COMFILCON", "TORIC"]),
    ("test_006.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_007.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_008.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE"]),
    ("test_009.jpeg", ["1-DAY", "MULTIFOCAL", "SILICONE"]),
    ("test_010.jpeg", ["ACUVUE", "OSASYS", "MAX", "1-DAY", "MULTIFOCAL"]),
    ("test_011.jpeg", ["COMFILCON", "TORIC"]),
    ("test_012.jpeg", ["BAUSCH+LOMB", "ULTRA", "MULTIFOCAL", "ASTIGMATISM"]),
    ("test_013.jpeg", ["COMFILCON", "XR", "TORIC"]),
    ("test_014.jpeg", ["COMFICON", "TORIC"]),
    ("test_015.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_016.jpeg", ["ACUVUE", "MOIST", "1-DAY"]),
    ("test_017.jpeg", ["TOTAL30", "ASTIGMATISM", "ALCON"]),
    ("test_018.jpeg", ["ACUVUE", "OASYS", "1-DAY", "HYDRALUXE", "ASTIGMATISM"]),
    ("test_019.jpeg", ["PRECISION1", "ALCON", "ASTIGMATISM"]),
    ("test_020.jpeg", ["COMFILCON", "TORIC"]),
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
def test_extract_value(image_path, expected):
    text = detect_text(f"OCR_test/test_images/{image_path}")
    half_length = len(text) // 2
    result = find_title_keywords(text[:half_length])
    assert result == expected

# def test_extracting_title_keywords():
#     assert 

# def test_extracting_brand_title():
#     assert add(-1, -1) == -2

# def test_matching_lines():
#     assert add(0, 5) == 5

