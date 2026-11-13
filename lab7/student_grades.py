import re


def average_marks(marks_csv):
    if not isinstance(marks_csv, str) or not marks_csv.strip():
        raise ValueError("Marks cannot be empty")

    try:
        marks = [int(m.strip()) for m in marks_csv.split(",")]
    except ValueError:
        raise ValueError("Marks must contain valid integers")

    if any(mark < 0 or mark > 100 for mark in marks):
        raise ValueError("Marks must be between 0 and 100")

    return round(sum(marks) / len(marks), 2)


def parse_srn(srn):
    if not isinstance(srn, str):
        raise ValueError("SRN must be a string")

    match = re.fullmatch(r"([A-Z0-9]{4})UG(\d{2})([A-Z]{2})(\d{3})", srn)

    if not match:
        raise ValueError("Invalid SRN format")

    campus, year, dept, suffix = match.groups()

    return campus, int(year), dept


def short_name(full_name):
    if not isinstance(full_name, str):
        raise ValueError("Name must be a string")

    parts = full_name.split()

    if len(parts) != 2:
        raise ValueError("Enter exactly first name and last name")

    first, last = parts

    if not first.isalpha() or not last.isalpha():
        raise ValueError("Name must contain alphabetic characters")

    return first[0].upper() + ". " + last.capitalize()


def main():
    print("==== Running average_marks ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    result = average_marks(user_input)
    print("Average Marks:", result)

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    result = parse_srn(user_input)
    print("Campus, Year and Dept:", result)

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    result = short_name(user_input)
    print("Short Name:", result)


if __name__ == "__main__":
    main()
