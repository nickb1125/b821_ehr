"""Tests for funcitionality.py."""
import os
import sys

import functionality
import pytest
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
    """Test parge data general example."""
    pat_1a = functionality.Patient(
        pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )
    pat_1a.add_labs(
        functionality.Lab(
            pat_id="1A",
            name="POTASSIUM",
            value="37",
            units="mg/dL",
            time="2001-07-01 03:20:24.070",
        )
    )

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
        output = functionality.parse_data(sub_filenames, test_filenames)
        assert output["1A"].get_lab_test_values(
            "POTASSIUM"
        ) == pat_1a.get_lab_test_values("POTASSIUM")


def test_parse_data_input_wrong_column_order() -> None:
    """Test parse data with switched up column order input."""
    pat_1a = functionality.Patient(
        pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )
    pat_1a.add_labs(
        functionality.Lab(
            pat_id="1A",
            name="POTASSIUM",
            value="37",
            units="mg/dL",
            time="2001-07-01 03:20:24.070",
        )
    )

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
        output = functionality.parse_data(sub_filenames, test_filenames)
        assert output["1A"].get_lab_test_values(
            "POTASSIUM"
        ) == pat_1a.get_lab_test_values("POTASSIUM")


def test_patient_age_general() -> None:
    """Test general example of get age."""

    pat_1a = functionality.Patient(
        pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )
    assert pat_1a.age == 22


def test_patient_age_wrong_format_dob() -> None:
    """Test wrong format error for date of birth in data input."""
    with pytest.raises(ValueError):
        pat_1a = functionality.Patient(
            pat_id="1A", gender="Male", dob="2000-06-15", race="White"
        )


def test_patient_sick() -> None:
    """Test (1) general get if sick patient example & not a patient error."""
    pat_1a = functionality.Patient(
        pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )
    pat_1a.add_labs(
        functionality.Lab(
            pat_id="1A",
            name="POTASSIUM",
            value="37",
            units="mg/dL",
            time="2001-07-01 03:20:24.070",
        )
    )

    # test general
    assert pat_1a.is_sick(lab_name="POTASSIUM", operator=">", value=36) is True


def test_patient_sick_non_numeric_error() -> None:
    """Test error for patient lab value not numeric."""
    with pytest.raises(ValueError):
        pat_1a = functionality.Patient(
            pat_id="1A",
            gender="Male",
            dob="2000-06-15 02:45:40.547",
            race="White",
        )
        pat_1a.add_labs(
            functionality.Lab(
                pat_id="1A",
                name="POTASSIUM",
                value="37a",
                units="mg/dL",
                time="2001-07-01 03:20:24.070",
            )
        )
        pat_1a.is_sick(lab_name="POTASSIUM", operator=">", value=3)


def test_get_patient_age_first_lab_general() -> None:
    """Tests function to get age at first patient lab"""
    pat_1a = functionality.Patient(
        pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )
    pat_1a.add_labs(
        functionality.Lab(
            pat_id="1A",
            name="POTASSIUM",
            value="37",
            units="mg/dL",
            time="2020-07-01 03:20:24.070",
        )
    )

    pat_age_first_lab = pat_1a.get_age_at_first_lab()
    assert pat_age_first_lab == 20
