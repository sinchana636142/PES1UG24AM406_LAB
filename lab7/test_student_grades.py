import pytest
from hypothesis import given, strategies as st
from student_grades import average_marks, parse_srn, short_name

# Valid input tests


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=50))
def test_average_marks(marks):
    csv_marks = ",".join(map(str, marks))
    expected = round(sum(marks) / len(marks), 2)
    assert average_marks(csv_marks) == expected


@given(
    prefix=st.text(
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=4, max_size=4
    ),
    year=st.integers(min_value=0, max_value=99),
    dept=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    suffix=st.text(alphabet="0123456789", min_size=3, max_size=3),
)
def test_parse_srn(prefix, year, dept, suffix):
    srn = f"{prefix}UG{year:02d}{dept}{suffix}"
    assert parse_srn(srn) == (prefix, year, dept)


@given(
    first=st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        min_size=1,
        max_size=20,
    ),
    last=st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        min_size=1,
        max_size=20,
    ),
)
def test_short_name(first, last):
    expected = first[0].upper() + ". " + last.capitalize()
    assert short_name(f"{first} {last}") == expected


# Invalid input fuzz tests


@given(st.sampled_from(["", " ", "abc", "10,,20", "-1,50", "101,50", "1.5,2", ","]))
def test_average_marks_invalid(s):
    with pytest.raises(ValueError):
        average_marks(s)


@given(
    st.one_of(
        st.integers(min_value=-1000, max_value=-1),
        st.integers(min_value=101, max_value=1000),
    )
)
def test_average_marks_out_of_range(mark):
    with pytest.raises(ValueError):
        average_marks(str(mark))


@given(st.text(max_size=20))
def test_parse_srn_invalid(s):
    if len(s) != 13 or not (
        len(s) == 13
        and s[:4].isalnum()
        and s[4:6] == "UG"
        and s[6:8].isdigit()
        and s[8:10].isalpha()
        and s[8:10].isupper()
        and s[10:13].isdigit()
    ):
        with pytest.raises(ValueError):
            parse_srn(s)


@given(st.sampled_from(["", "ravi", "ravi kumar shetty", "123 kumar", "ravi 123"]))
def test_short_name_invalid(s):
    with pytest.raises(ValueError):
        short_name(s)


@given(st.one_of(st.none(), st.integers()))
def test_functions_reject_wrong_types(value):
    with pytest.raises(ValueError):
        average_marks(value)

    with pytest.raises(ValueError):
        parse_srn(value)

    with pytest.raises(ValueError):
        short_name(value)


import runpy
from pathlib import Path


def test_main_program(monkeypatch, capsys):
    inputs = iter(["78,85,92", "PES1UG23CS123", "ravi kumar"])

    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    script_path = Path(__file__).with_name("student_grades.py")

    runpy.run_path(str(script_path), run_name="__main__")

    output = capsys.readouterr().out

    assert "Average Marks:" in output
    assert "Campus, Year and Dept:" in output
    assert "Short Name:" in output
