def letter_grade(marks):
    if marks < 0 or marks > 100:
        raise ValueError("invalid marks")
    if marks >= 90:
        return "S"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    elif marks >= 40:
        return "E"
    return "F"


def final_marks(internal, external, has_project):
    if internal > 40 or external > 60:
        raise ValueError("marks out of range")
    total = internal + external
    if has_project:
        total += 5
        if total > 100:
            total = 100
    return total


def exam_eligibility(attendance, fees_paid, has_medical):
    if not fees_paid:
        return "blocked"
    if attendance >= 75:
        return "eligible"
    elif attendance >= 65 and has_medical:
        return "eligible"
    return "detained"
