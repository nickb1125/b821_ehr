"""EHR module."""

import datetime

# Data Parsing
# Description: Nested dicitonary
#   L1 Keys: (SubjectId1, SubjectId2, ...)
#           L2 Keys: ("General", "METABOLIC: ALBUMIN", ...)
#                   Returns tuple of tuples containing all labs collected

# Assumptions:
# (1) Column names are the same as in files provided (order will not matter)
# (2) File is tab delimited


lab_col_order = [
    "PatientID",
    "AdmissionID",
    "LabName",
    "LabValue",
    "LabUnits",
    "LabDateTime",
]

subjects_col_order = [
    "PatientID",
    "PatientGender",
    "PatientDateOfBirth",
    "PatientRace",
    "PatientMaritalStatus",
    "PatientLanguage",
    "PatientPopulationPercentageBelowPoverty",
]

list_of_list = list[list[str]]
tuple_of_tuple = tuple[
    tuple[str, ...], ...
]  # need to use "..."" due to varying cases for varying functions
nested_dict_type = dict[str, dict[str, tuple[tuple[str, ...], ...]]]


def read_data(filename: str) -> list[str]:
    """Read in data file."""
    file = open(filename, mode="r", encoding="utf-8-sig")
    lines = file.readlines()
    file.close()
    return lines


def seperate_lines(row_list: list[str]) -> list_of_list:
    """Seperate Lines.

    Split list of full string data rows to reuturn a list (rows) of lists.
    (values) of each individual entry.
    """
    return [row.strip().split("\t") for row in row_list]


def reorder_columns(
    column_order: list[str], list_of_list: list_of_list
) -> list_of_list:
    """Reorder Columns.

    Reorders "columns" in list of list based on predisposed proper order
    (column_order).
    """
    header = list_of_list[0]
    reorder_dict = {header[i]: i for i in range(len(header))}
    try:
        index_header = [
            reorder_dict[column_order[i]] for i in range(len(column_order))
        ]
    except KeyError:
        print("List of list column names do not match column order list.")
        raise KeyError
    if not any(item is None for item in index_header):
        reorder = [[row[idx] for idx in index_header] for row in list_of_list]
    return reorder


def list_of_list_to_tuple_of_tuple(
    list_of_list: list_of_list,
) -> tuple_of_tuple:
    """List of Lists -> Tuple of Tuples.

    Converts a list of lists to tuple of tuples; for purposes of
    tuples being immutable
    """
    to_tuple = tuple([tuple(row) for row in list_of_list])
    return to_tuple


def filter_tuple_of_tuple(
    filter_value: str,
    values: tuple_of_tuple,
    column_index: int,
    check_index: int,
) -> tuple_of_tuple:
    """Filter Tuple of Tuple.

    Helper function to take a tuple of tuples of strings (values) and
    filter to only tuples of strings in which entry in index (check_index)
    is equal to a specific value (filter_value). We return such columns after
    the column_index in a tuple of tuples.
    """
    dat = tuple(
        [
            tuple(general[column_index:])
            for general in values
            if general[check_index] == filter_value
        ]
    )  # consider using next() here as patrick suggested
    # (may need to ask for elaboration)
    return dat


def parse_data(patient_filename: str, lab_filename: str) -> nested_dict_type:
    """Organize Lab and Subject Data into Nested Dictionary."""
    # reads subject file
    subject_data = read_data(patient_filename)
    lab_data = read_data(lab_filename)

    # seperate lines of read file, reorder columns to proper, and convert
    # from list of lists to tuple of tuples for immutability. Complete
    # for both lab and general data
    subject_values = list_of_list_to_tuple_of_tuple(
        list_of_list=reorder_columns(
            column_order=subjects_col_order,
            list_of_list=seperate_lines(subject_data),
        )
    )[1:]
    lab_values = list_of_list_to_tuple_of_tuple(
        list_of_list=reorder_columns(
            column_order=lab_col_order,
            list_of_list=seperate_lines(lab_data),
        )
    )[1:]

    # get unique subjects
    subjects = set(record[0] for record in subject_values)

    # make nested dict
    nested_dict = {}
    for subject in subjects:
        subject_general = filter_tuple_of_tuple(subject, subject_values, 0, 0)
        subject_lab_values = filter_tuple_of_tuple(subject, lab_values, 1, 0)
        unique_test_list = set(record[1] for record in subject_lab_values)

        nested_dict[subject] = {"General": subject_general}
        for test in unique_test_list:
            test_this_value = filter_tuple_of_tuple(
                test, subject_lab_values, 0, 1
            )
            nested_dict[subject][test] = test_this_value

    return nested_dict


def patient_age(records: nested_dict_type, patient_id: str) -> int:
    """Return Patient Age."""
    dob = records[patient_id]["General"][0][2]
    time_since_birth = datetime.datetime.now() - datetime.datetime.strptime(
        dob, "%Y-%m-%d %H:%M:%S.%f"
    )
    time_since_birth_years = (
        time_since_birth.total_seconds() / 60 / 60 / 24 / 365.25
    )
    return int(time_since_birth_years)


def patient_is_sick(
    records: nested_dict_type,
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return Whether Patient is Sick."""
    # get all tests of lab_name
    lab_values = records[patient_id][lab_name]
    sick_list = [
        eval(lab_value[2] + operator + str(value)) for lab_value in lab_values
    ]
    return any(sick_list)


def main() -> None:
    """Test Functions."""
    records = parse_data(
        patient_filename="/Users/nickbachelder/Downloads/"
        "PatientCorePopulatedTable.txt",
        lab_filename="/Users/nickbachelder/Downloads/"
        "LabsCorePopulatedTable.txt",
    )
    age_example_result = patient_age(
        records, patient_id="1A8791E3-A61C-455A-8DEE" "-763EB90C9B2C"
    )
    sick_example_result = patient_is_sick(
        records,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "METABOLIC: ALBUMIN",
        ">",
        4.0,
    )
    if (age_example_result == 49) & (sick_example_result):
        print("Module is loaded and passes example tests.")
    else:
        print("Module is loaded and but fails at least 1 example test.")


if __name__ == "__main__":
    main()
