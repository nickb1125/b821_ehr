"""Tests for funcitionality.py."""
import functionality
import pytest
import sqlite3
import make_fake_files


class FunctionError(Exception):
    """Error for function not acting properly (non-base python issue)."""

    pass


def test_seperate_lines_check_outer_length() -> None:
    """Test length of output is number of rows."""
    input_list = ["1\t2\t3\t4", "1\t2\t3\t4", "1\t2\t3\t4", "1\t2\t3\t4"]
    output = functionality.seperate_lines(input_list)
    assert len(output) == 4


def test_seperate_lines_uneven_within_inner_lengths() -> None:
    """Test length of each inner list is number of columns."""
    input_list = ["1\t3\t4", "1\t2\t3\t4", "1\t2\t3\t4", "1\t2\t3\t4"]
    output = functionality.seperate_lines(input_list)
    assert list(map(len, output)) == [3, 4, 4, 4]


def test_seperate_lines_empty_entry_inner_length() -> None:
    """Test missing entry is parsed and seperated."""
    input_list = ["1\t\t4", "1\t2\t3\t4", "1\t2\t3\t4", "1\t2\t3\t4"]
    output = functionality.seperate_lines(input_list)
    assert list(map(len, output)) == [3, 4, 4, 4]


def test_reorder_columns() -> None:
    """Test general off column order fix."""
    column_order_requested = ["b", "a", "d", "c"]
    list_of_list_input = [
        ["a", "b", "c", "d"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]
    output = functionality.reorder_columns(
        column_order_requested, list_of_list_input
    )
    assert output == [
        ["2", "1", "4", "3"],
        ["2", "1", "4", "3"],
    ]


def test_reorder_columns_unreasonable_column_order() -> None:
    """Test error return for unreasonable column order request."""
    column_order_requested = ["b", "f", "d", "c"]
    list_of_list_input = [
        ["a", "b", "c", "d"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]
    with pytest.raises(ValueError):
        functionality.reorder_columns(
            column_order_requested, list_of_list_input
        )


def test_reorder_columns_column_order_to_short() -> None:
    """Test error return for inappropriate column order length request."""
    column_order_requested = ["b", "d", "c"]
    list_of_list_input = [
        ["a", "b", "c", "d"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]
    with pytest.raises(ValueError):
        functionality.reorder_columns(
            column_order_requested, list_of_list_input
        )


def test_patient_cohort_general() -> None:
    """Test parse data general example."""
    test_sub_table = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        [
            "1A",
            "Male",
            "2000-06-15 02:45:40.547",
            "White",
            "Single",
            "English",
            "12.2",
        ],
    ]
    test_test_table = [
        [
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        ["1A", "1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"],
    ]
    with make_fake_files.fake_files(test_sub_table, test_test_table) as (
        sub_filenames,
        test_filenames,
    ):
        functionality.parse_data(sub_filenames, test_filenames)
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_1a_subjects_row_ex = cursor.execute("""SELECT * FROM Patients""")
        pat_1a_subjects_row = pat_1a_subjects_row_ex.fetchall()
        assert pat_1a_subjects_row == [
            (
                "1A",
                "Male",
                "2000-06-15 02:45:40.547",
                "White",
            )
        ]
        connection.close()


def test_parse_data_input_wrong_column_order() -> None:
    """Test parse data with switched up column order input."""
    test_sub_table = [
        [
            "PatientID",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
            "PatientGender",
            "PatientDateOfBirth",
        ],
        [
            "1A",
            "White",
            "Single",
            "English",
            "12.2",
            "Male",
            "2000-06-15 02:45:40.547",
        ],
    ]
    test_test_table = [
        [
            "LabValue",
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabUnits",
            "LabDateTime",
        ],
        ["37", "1A", "1", "POTASSIUM", "mg/dL", "2001-07-01 03:20:24.070"],
    ]
    with make_fake_files.fake_files(test_sub_table, test_test_table) as (
        sub_filenames,
        test_filenames,
    ):
        functionality.parse_data(sub_filenames, test_filenames)
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_1a_labs_row_ex = cursor.execute("""SELECT * FROM Labs""")
        pat_1a_labs_row = pat_1a_labs_row_ex.fetchall()
        assert pat_1a_labs_row == [
            (
                "0",
                "1A",
                "POTASSIUM",
                37.0,
                "mg/dL",
                "2001-07-01 03:20:24.070",
            )
        ]
        connection.close()


def test_patient_age_general() -> None:
    """Test general example of get age."""
    connection = sqlite3.connect("ehr.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Patients")
    cursor.execute(
        """CREATE TABLE Patients(
                PatientID VARCHAR PRIMARY KEY,
                PatientGender VARCHAR,
                PatientDateOfBirth TIMESTAMP,
                PatientRace VARCHAR)"""
    )
    cursor.execute(
        "INSERT INTO Patients Values (?, ?, ?, ?)",
        ("1A", "Male", "2001-07-01 03:20:24.070", "White"),
    )
    connection.commit()
    pat_1a = functionality.Patient(pat_id="1A")
    assert pat_1a.age == 21


def test_patient_age_wrong_format_dob() -> None:
    """Test wrong format error for date of birth in data input."""
    connection = sqlite3.connect("ehr.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Patients")
    cursor.execute(
        """CREATE TABLE Patients(
                PatientID VARCHAR PRIMARY KEY,
                PatientGender VARCHAR,
                PatientDateOfBirth TIMESTAMP,
                PatientRace VARCHAR)"""
    )
    cursor.execute(
        "INSERT INTO Patients Values (?, ?, ?, ?)",
        ("1A", "Male", "2000-06-15 02:40.547", "White"),
    )
    connection.commit()
    pat_1a = functionality.Patient(pat_id="1A")
    with pytest.raises(ValueError):
        pat_1a.dob


test_patient_age_wrong_format_dob()


def test_patient_sick() -> None:
    """Test (1) general get if sick patient example & not a patient error."""
    connection = sqlite3.connect("ehr.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Patients")
    cursor.execute("DROP TABLE IF EXISTS Labs")
    cursor.execute(
        """CREATE TABLE Patients(
                PatientID VARCHAR PRIMARY KEY,
                PatientGender VARCHAR,
                PatientDateOfBirth TIMESTAMP,
                PatientRace VARCHAR)"""
    )
    cursor.execute(
        """CREATE TABLE Labs(
                LabID VARCHAR PRIMARY KEY,
                PatientID VARCHAR,
                LabName VARCHAR,
                LabValue FLOAT,
                LabUnits VARCHAR,
                LabDateTime TIMESTAMP)"""
    )
    cursor.execute(
        "INSERT INTO Patients Values (?, ?, ?, ?)",
        ("1A", "Male", "2000-06-15 02:45:40.547", "White"),
    )
    connection.commit()
    connection.close()
    pat_1a = functionality.Patient(pat_id="1A")
    pat_1a.add_labs(
        lab_name="POTASSIUM",
        value=100,
        units="mg",
        time="2001-06-15 02:45:40.547",
    )
    # test general
    assert pat_1a.is_sick(lab_name="POTASSIUM", operator=">", value=36) is True


def test_get_patient_age_first_lab_general() -> None:
    """Tests function to get age at first patient lab"""
    connection = sqlite3.connect("ehr.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Patients")
    cursor.execute("DROP TABLE IF EXISTS Labs")
    cursor.execute(
        """CREATE TABLE Patients(
                PatientID VARCHAR PRIMARY KEY,
                PatientGender VARCHAR,
                PatientDateOfBirth TIMESTAMP,
                PatientRace VARCHAR)"""
    )
    cursor.execute(
        """CREATE TABLE Labs(
                LabID VARCHAR PRIMARY KEY,
                PatientID VARCHAR,
                LabName VARCHAR,
                LabValue FLOAT,
                LabUnits VARCHAR,
                LabDateTime TIMESTAMP)"""
    )
    cursor.execute(
        "INSERT INTO Patients Values (?, ?, ?, ?)",
        ("1A", "Male", "2001-07-01 03:20:24.070", "White"),
    )
    connection.commit()
    pat_1a = functionality.Patient(pat_id="1A")
    pat_1a.add_labs(
        lab_name="POTASSIUM",
        value=10,
        units="mg",
        time="2021-07-01 03:20:24.070",
    )

    pat_age_first_lab = pat_1a.get_age_at_first_lab()
    assert pat_age_first_lab == 20
