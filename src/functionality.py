"""EHR module."""

# import dependencies and create needed types

import datetime
from dataclasses import dataclass

list_of_list = list[list[str]]

# create helper functions

# Let...
# N = Number of columns in lab file
# M = Number of columns in subjects file
# I = Number of rows in lab file
# J = Number of rows in subjects file


def read_data(filename: str) -> list[str]:
    """Read in data file."""
    file = open(filename, mode="r", encoding="utf-8-sig")  # O(1)
    lines = file.readlines()  # O(NI) for subjects file, O(MJ) for labs file
    file.close()  # O(1)
    return lines


def seperate_lines(row_list: list[str]) -> list_of_list:
    """Seperate Lines.

    Split list of full string data rows to reuturn a list (rows) of lists.
    (values) of each individual entry.
    """
    return [row.strip().split("\t") for row in row_list]
    # O(MJ) for subjects file
    # O(NI) for labs file


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
    )  # O(N) / O(M)
    header_greater_than_col_order = list(
        set(header) - set(column_order)
    )  # O(N) / O(M)
    if (len(col_order_greater_than_header)) != 0 or (
        len(header_greater_than_col_order) != 0
    ):  # O(1)
        raise ValueError(  # O(1)
            f"Column order and true headers dont match. Add \
                {header_greater_than_col_order} to column order \
                    and remove {header_greater_than_col_order} \
                        from column order."
        )  # O(1)
    reorder_dict = {header[i]: i for i in range(len(header))}  # O(N) / O(M)
    index_header = [
        reorder_dict[column_order[i]] for i in range(len(column_order))
    ]  # O(# of columns): O(N) for labs and O(M) for subjects
    if not any(item is None for item in index_header):
        reorder = [[row[idx] for idx in index_header] for row in list_of_list]
        # O(# columns * # Rows) = O(NI) for labs and O(MJ) for subjects
    return reorder[1:]  # remove column row


@dataclass
class Lab:
    """Lab class."""

    pat_id: str
    name: str
    value: str | float
    units: str
    time: str


class Patient:
    """Patient Class."""

    def __init__(
        self, pat_id: str, gender: str, dob: str, race: str
    ) -> None:  # O(1)
        """Initialize patient class."""
        self.labs: dict[str, list[Lab]] = dict({})  # O(1)
        try:
            self.dob = datetime.datetime.strptime(
                dob, "%Y-%m-%d %H:%M:%S.%f"
            )  # O(1)
        except ValueError:
            raise ValueError(
                f"DOB '{dob}' for patient {pat_id} is incorrectly formatted"
            )
        self.gender = gender  # O(1)
        self.race = race  # O(1)
        self.pat_id = pat_id  # O(1)

    @property
    def age(self) -> int:  # O(1)
        """Get patient age."""
        time_since_birth = datetime.datetime.now() - self.dob  # O(1)
        time_since_birth_years = (
            time_since_birth.total_seconds() / 60 / 60 / 24 / 365.25
        )  # O(1)
        return int(time_since_birth_years)  # O(1)

    def is_sick(
        self, lab_name: str, operator: str, value: float
    ) -> bool:  # O(J)
        """Check if patient is sick."""
        lab_values = self.labs[lab_name]  # O(1)
        try:
            sick_list = [
                eval(str(lab_value.value) + operator + str(value))  # O(J)
                for lab_value in lab_values
            ]
        except SyntaxError:
            raise ValueError(
                "Lab values for patient '{self.pat_id}' lab '{lab_name}' are \
                    not validly formatted."
            )  # O(1)
        return any(sick_list)  # O(1)

    def add_labs(self, lab: Lab) -> None:  # O(1)
        """Add lab to patient profile."""
        if lab.name not in self.labs.keys():  # O(1)
            self.labs[lab.name] = [lab]  # O(1)
        else:
            self.labs[lab.name].append(lab)  # O(1)

    def get_age_at_first_lab(self) -> int:  # O(J)
        """Get patient age at first lab."""
        times = []
        for key, item in self.labs.items():  # O(J)
            try:
                times.extend(
                    [
                        datetime.datetime.strptime(
                            lab.time, "%Y-%m-%d %H:%M:%S.%f"
                        )
                        for lab in item
                    ]
                )  # O(J)
            except ValueError:
                raise ValueError(
                    "Lab time values for patient {self.pat_id} \
                        lab {key} are not validly formatted."
                )  # O(1)
        min_lab_date = min(times)  # O(J)
        pat_age_at_first = (
            (min_lab_date - self.dob).total_seconds() / 60 / 60 / 24 / 365.25
        )  # O(1)
        return int(pat_age_at_first)  # O(1)

    def get_lab_test_values(self, lab_name: str) -> str | list[float]:  # O(J)
        """Get patient lab for specific test if exists."""
        if lab_name in self.labs.keys():
            try:
                return [
                    float(info.value) for info in self.labs[lab_name]
                ]  # O(J)
            except ValueError:
                raise ValueError(
                    "Lab values for patient '{self.pat_id}' lab '{lab_name}' \
                        are not validly formatted."
                )  # O(1)
        else:
            return f"Patient has no tests for {lab_name}"  # O(1)


# Big O: O(MJ + NI + J^2)
def parse_data(
    subjects_file_name: str, labs_file_name: str
) -> dict[str, Patient]:
    """Parse read files into dictionary of patient classes."""
    # reads data files
    try:
        subject_data = read_data(subjects_file_name)  # O(MJ)
    except ValueError:
        ValueError("Incorrect subjects file path.")
    try:
        lab_data = read_data(labs_file_name)  # O(NI)
    except ValueError:
        ValueError("Incorrect labs file path.")

    # reorders columns for proper variable assignent
    subject_values = reorder_columns(
        column_order=[
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        list_of_list=seperate_lines(subject_data),
    )  # O(MJ) + O(MJ)
    lab_values = reorder_columns(
        column_order=[
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        list_of_list=seperate_lines(lab_data),
    )  # O(NI) + O(NI)

    # creates patients dirictory
    subjects = dict(
        {
            patient_info[0]: Patient(
                pat_id=patient_info[0],
                gender=patient_info[1],
                dob=patient_info[2],
                race=patient_info[3],
            )
            for patient_info in subject_values
        }
    )  # O(J)

    # adds lab classes for each patient
    for lab in lab_values:
        lab_class = Lab(
            pat_id=lab[0],
            name=lab[2],
            value=lab[3],
            units=lab[4],
            time=lab[5],
        )  # O(1)
        patient = subjects.get(lab_class.pat_id)  # O(J)
        if patient is not None:
            patient.add_labs(lab_class)  # O(J)
        else:
            raise ValueError("Patient in this lab is not in records.")
    return subjects
