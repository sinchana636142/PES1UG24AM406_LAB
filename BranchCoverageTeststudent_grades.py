import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

#Example test cases:
def test_s_grade():
    assert letter_grade(95) == "S"

def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"

#Write the rest of the test cases so that the code is 90- 100% covered.


import pytest
from student_grades import letter_grade, final_marks, exam_eligibility


def test_letter_grade_all_bands():
    assert letter_grade(95) == "S"
    assert letter_grade(85) == "A"
    assert letter_grade(75) == "B"
    assert letter_grade(65) == "C"
    assert letter_grade(55) == "D"
    assert letter_grade(45) == "E"
    assert letter_grade(20) == "F"


def test_letter_grade_invalid():
    with pytest.raises(ValueError):
        letter_grade(-1)
    with pytest.raises(ValueError):
        letter_grade(101)


def test_final_marks_valid():
    assert final_marks(30, 50, False) == 80
    assert final_marks(30, 50, True) == 85
    assert final_marks(40, 56, True) == 100


def test_final_marks_invalid():
    with pytest.raises(ValueError):
        final_marks(41, 50, False)
    with pytest.raises(ValueError):
        final_marks(30, 61, False)


def test_exam_eligibility():
    assert exam_eligibility(80, False, False) == "blocked"
    assert exam_eligibility(80, True, False) == "eligible"
    assert exam_eligibility(65, True, True) == "eligible"
    assert exam_eligibility(65, True, False) == "detained"
    assert exam_eligibility(64, True, True) == "detained"