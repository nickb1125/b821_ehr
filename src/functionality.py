"""EHR module."""

# import dependencies
import datetime

# Data Parsing
# Description: Nested dicitonary
#   L1 Keys: (SubjectId1, SubjectId2, ...)
#           L2 Keys: ("General", "METABOLIC: ALBUMIN", ...)
#                   Returns tuple of tuples containing all labs collected

# Assumptions:
# (1) Column names are the same as in files provided (order will not matter)
# (2) File is tab delimited

# Let...
# N = Number of columns in lab file
# M = Number of columns in subjects file
# I = Number of rows in lab file
# J = Number of rows in subjects file

lab_col_order = [
    "PatientID",
    "AdmissionID",
    "LabName",
    "LabValue",
    "LabUnits",
    "LabDateTime",
]  # O(1)

subjects_col_order = [
    "PatientID",
    "PatientGender",
    "PatientDateOfBirth",
    "PatientRace",
    "PatientMaritalStatus",
    "PatientLanguage",
    "PatientPopulationPercentageBelowPoverty",
]  # O(1)

list_of_list = list[list[str]]  # O(1)
# need to use "..."" due to varying cases for varying functions
nested_dict_type = dict[str, dict[str, list[list[str]]]]  # O(1)


# Big O:  O(I) for subjects file, O(J) for labs file.
# Explain: File is opened O(1), file lines are each read O(# of lines in file),
# and file is closed O(1). Simplifies to O(# of lines in file)
# How to improve: Can't because readlines() must be O(# of rows)
def read_data(filename: str) -> list[str]:
    """Read in data file."""
    file = open(filename, mode="r", encoding="utf-8-sig")  # O(1)
    lines = file.readlines()  # O(NI) for subjects file, O(MJ) for labs file
    file.close()  # O(1)
    return lines


# Big O: O(MJ) for subjects file or O(NI) for labs file
# Explain: O(# of cols) for strip, O(number of rows) for split. Since
# simplifies to O(# of cols * # of rows)
# How to imrpove: We may be able to improve best case complexity with some
# brainstorming, but worst case will remain O(# of columns * # of rows)
def seperate_lines(row_list: list[str]) -> list_of_list:
    """Seperate Lines.

    Split list of full string data rows to reuturn a list (rows) of lists.
    (values) of each individual entry.
    """
    return [row.strip().split("\t") for row in row_list]
    # O(MJ) for subjects file
    # O(NI) for labs file


# Big O: O(NI) for labs and O(MJ) for subjects
# Explain: header columns are found as first list in list of lists O(1).
# reorder_dict is created using dictionary comp O(# columns)
# index_header is created using list comp O(# columns)
# If error is raised additional O(1)
# Reordering is done using nested list comprehension O(# rows * # cols)
# Simplifies to O(# rows * # cols)
# How to improve: We can (1) improve code readability using the enumerate
# function. I don't think we can improve complexity easily.
def reorder_columns(
    column_order: list[str], list_of_list: list_of_list
) -> list_of_list:
    """Reorder Columns.

    Reorders "columns" in list of list based on predisposed proper order
    (column_order).
    """
    header = list_of_list[0]  # O(1)
    col_order_greater_than_header = list(
        set(column_order) - set(header)
    )  # O(N)/O(M)
    header_greater_than_col_order = list(
        set(header) - set(column_order)
    )  # O(N)/O(M)
    if (len(col_order_greater_than_header)) != 0 or (
        len(header_greater_than_col_order) != 0
    ):
        raise ValueError(
            f"Column order and true headers dont match. Add \
                {header_greater_than_col_order} to column order \
                    and remove {header_greater_than_col_order} \
                        from column order."
        )  # O(1)
    reorder_dict = {header[i]: i for i in range(len(header))}
    # O(# of columns): O(N) for labs and O(M) for subjects
    index_header = [
        reorder_dict[column_order[i]] for i in range(len(column_order))
    ]  # O(# of columns): O(N) for labs and O(M) for subjects
    if not any(item is None for item in index_header):  # O(N)
        reorder = [
            [row[idx] for idx in index_header] for row in list_of_list
        ]  # O(# columns * # Rows) = O(NI) for labs and O(MJ) for subjects
    return reorder


# Big O: O(J) for subjects and O(I) for labs
# Explain: (1) For each list in the list, we create a list
# after indexing each nested list by
# column index for individual rows. Therefore,
# Big O: O(#row)


# How to improve: If we remove list to tuple conversions,
# we can improve the complexity here to O(#row)
# This would be changed to filter_list_of_lists.
def filter_list_of_list(
    filter_value: str,
    values: list_of_list,
    column_index: int,
    check_index: int,
) -> list_of_list:
    """Filter Tuple of Tuple.

    Helper function to take a tuple of tuples of strings (values) and
    filter to only tuples of strings in which entry in index (check_index)
    is equal to a specific value (filter_value). We return such columns after
    the column_index in a tuple of tuples.
    """
    dat = [
        general[column_index:]  # tuple(list) is O(length of list)
        for general in values
        if general[check_index] == filter_value
    ]  # O(#row)
    return dat


# Big O: O(N * # unique tests * # unique subject)


# Explain: if we change tuple_of_tuple to list_of_list then we have
# read_data: O(#row)
# reorder columns: O(#row*#col)
# seperate_lines: O(#row*#col)
# filter_tuple_of_tuple -> filter_list_of_lists: O(#row)
# Therefore our bigO is
# O(N * # unique tests * # unique subject)
def parse_data(patient_filename: str, lab_filename: str) -> nested_dict_type:
    """Organize Lab and Subject Data into Nested Dictionary."""
    # reads subject file
    subject_data = read_data(patient_filename)  # O(MJ)
    lab_data = read_data(lab_filename)  # O(NI)

    # seperate lines of read file, reorder columns to proper, and convert
    # from list of lists to tuple of tuples for immutability. Complete
    # for both lab and general data
    subject_values = reorder_columns(
        column_order=subjects_col_order,
        list_of_list=seperate_lines(subject_data),  # O(MJ) + O(MJ)
    )[
        1:
    ]  # O(1)
    lab_values = reorder_columns(
        column_order=lab_col_order,
        list_of_list=seperate_lines(lab_data),  # O(NI) + O(NI)
    )[
        1:
    ]  # O(1)

    # get unique subjects
    subjects = set(
        record[0] for record in subject_values
    )  # O(J) + O(J) -> O(J)

    # make nested dict
    nested_dict = {}  # O(1)
    for subject in subjects:
        subject_general = filter_list_of_list(
            subject, subject_values, 0, 0
        )  # O(J) * O(# unique subjects)
        subject_lab_values = filter_list_of_list(
            subject, lab_values, 1, 0
        )  # O(I) * O(# unique subjects)
        unique_test_list = set(
            record[1] for record in subject_lab_values
        )  # O(I) * O(# unique subjects) + O(I) * O(# unique subjects) ->
        # O(I) * O(# unique subjects)

        nested_dict[subject] = {"General": subject_general}
        # O(1) * O(# unique subjects)
        for test in unique_test_list:
            test_this_value = filter_list_of_list(
                test, subject_lab_values, 0, 1
            )  # O(I) * O(# unique tests) * O(# unique subject)
            nested_dict[subject][test] = test_this_value
            # O(# unique tests) * O(# unique subject)

            # -> entire nested for loop simplifies to
            # O(NI) * O(# unique tests) * O(# unique subject)

    return nested_dict


# Worst Case: O(1)
# Explain: datetime operations are O(1), and record indexing is
# O(1) since we are functioning in a nested_dictionary.
# Division is also O(1)
# How to improve: Can't
def patient_age(records: nested_dict_type, patient_id: str) -> int:
    """Return Patient Age."""
    dob = records[patient_id]["General"][0][2]  # O(1)
    time_since_birth = datetime.datetime.now() - datetime.datetime.strptime(
        dob, "%Y-%m-%d %H:%M:%S.%f"
    )  # O(1)
    time_since_birth_years = (
        time_since_birth.total_seconds() / 60 / 60 / 24 / 365.25
    )  # O(1)
    return int(time_since_birth_years)


# Big O:  O(H) where H is # of tests patient has for lab & H = I/J on average
# Explain: Getting all tests for patient of lab name is O(1)
# since we are indexing nested dict. List comprehension to get the
# sick results list is O(H). any() funcition to see if any sick tests
# is O(H). simplifies to big O of O(H)
# How to improve: We can improve time complexity by
# terminating the for loop once a true is reached (best time O(1)) but
# worst case will remain the same
def patient_is_sick(
    records: nested_dict_type,
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """Return Whether Patient is Sick."""
    # get all tests of lab_name
    lab_values = records[patient_id][lab_name]  # O(1)
    if any(list(map(lambda x: x[2].isdigit() is False, lab_values))):
        raise ValueError(
            "Some test labs are not numeric! Check your data source"
        )
    sick_list = [
        eval(lab_value[2] + operator + str(value)) for lab_value in lab_values
    ]  # O(#Patient tests for that lab)
    return any(sick_list)  # O(#Patient tests for that lab)


def main() -> None:
    """Test Functions."""
    pass
