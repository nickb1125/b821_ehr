"""Tests for funcitionality.py."""
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
        ["b", "a", "d", "c"],
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


def test_filter_list_of_list() -> None:
    """Test general filter of list of list."""
    input_list = [
        ["a", "b", "c", "d"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]

    output = functionality.filter_list_of_list(
        filter_value="1", values=input_list, column_index=1, check_index=0
    )

    assert output == [
        ["2", "3", "4"],
        ["2", "3", "4"],
    ]


def test_filter_list_of_list_incorrect_check_index() -> None:
    """Test error for column index out of range."""
    input_list = [
        ["a", "b", "c", "d"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]
    with pytest.raises(IndexError):
        functionality.filter_list_of_list(
            filter_value="1", values=input_list, column_index=1, check_index=5
        )


def test_parse_data_general() -> None:
    """Test parge data general example."""
    expect_output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                ["1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"]
            ],
        }
    }

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
        assert output == expect_output


def test_parse_data_input_wrong_column_order() -> None:
    """Test parse data with switched up column order input."""
    expect_output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                ["1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"]
            ],
        }
    }

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
        assert output == expect_output


def test_patient_age_general() -> None:
    """Test general example of get age."""

    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                ["1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"]
            ],
        }
    }
    assert functionality.patient_age(records=output, patient_id="1A") == 22


def test_patient_age_wrong_format_dob() -> None:
    """Test wrong format error for date of birth in data input."""
    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                ["1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"]
            ],
        }
    }
    with pytest.raises(ValueError):
        functionality.patient_age(records=output, patient_id="1A")


def test_patient_sick_multiple() -> None:
    """Test (1) general get if sick patient example &(2)not a patient error."""
    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                ["1", "POTASSIUM", "37", "mg/dL", "2001-07-01 03:20:24.070"]
            ],
        }
    }

    # test general
    assert (
        functionality.patient_is_sick(
            records=output,
            patient_id="1A",
            lab_name="POTASSIUM",
            operator=">",
            value=36,
        )
        is True
    )
    # test no matching patient
    with pytest.raises(KeyError):
        functionality.patient_is_sick(
            records=output,
            patient_id="2A",
            lab_name="POTASSIUM",
            operator=">",
            value=36,
        )


def test_patient_sick_non_numeric_error() -> None:
    """Test error for patient lab value not numeric."""
    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "2000-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                [
                    "1",
                    "POTASSIUM",
                    "BAD_VALUE",
                    "mg/dL",
                    "2001-07-01 03:20:24.070",
                ]
            ],
        }
    }
    # test no matching patient
    with pytest.raises(ValueError):
        functionality.patient_is_sick(
            records=output,
            patient_id="1A",
            lab_name="POTASSIUM",
            operator=">",
            value=36,
        )


def test_get_patient_age_first_lab_general() -> None:
    """Tests function to get age at first patient lab"""
    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "1980-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                [
                    "1A",
                    "POTASSIUM",
                    "10",
                    "mg/dL",
                    "2001-07-01 03:20:24.070",
                ]
            ],
            "A1C": [
                [
                    "1A",
                    "A1C",
                    "15",
                    "mg/dL",
                    "2000-07-01 03:20:24.070",
                ]
            ],
        }
    }

    pat_age_first_lab = functionality.get_age_at_first_lab(output, "1A")
    assert pat_age_first_lab == 20


def test_get_patient_age_first_lab_non_data_error() -> None:
    """Tests function error when non-date format exists for patient"""
    output = {
        "1A": {
            "General": [
                [
                    "1A",
                    "Male",
                    "1980-06-15 02:45:40.547",
                    "White",
                    "Single",
                    "English",
                    "12.2",
                ]
            ],
            "POTASSIUM": [
                [
                    "1A",
                    "POTASSIUM",
                    "10",
                    "mg/dL",
                    "2001-07-01 03:20:24.070",
                ]
            ],
            "A1C": [
                [
                    "1A",
                    "A1C",
                    "15",
                    "mg/dL",
                    "WRONG",
                ]
            ],
        }
    }
    with pytest.raises(ValueError):
        functionality.get_age_at_first_lab(output, "1A")
