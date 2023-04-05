"""EHR module."""

# import dependencies and create needed types

import datetime
from dataclasses import dataclass
import sqlite3

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

    lab_id: str

    @property
    def time(self) -> str:
        """Get lab value."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT LabID, LabDateTime
            FROM Labs
            WHERE LabID= ?""",
            (self.lab_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        time = str(recieved[0][1])
        return time

    @property
    def value(self) -> float:
        """Get lab value."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT LabID, LabValue
            FROM Labs
            WHERE LabID = ?""",
            (self.lab_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        value = float(recieved[0][1])
        return value

    @property
    def units(self) -> str:
        """Get unit."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT LabID, LabUnits
            FROM Labs
            WHERE LabID = ?""",
            (self.lab_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        units = str(recieved[0][1])
        return units

    @property
    def name(self) -> str:
        """Get lab name."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT LabID, LabUnits
            FROM Labs
            WHERE LabID = ?""",
            (self.lab_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        name = str(recieved[0][1])
        return name


@dataclass
class Patient:
    """Patient Class."""

    pat_id: str

    @property
    def dob(self) -> datetime.datetime:
        """Pateint DOB."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT PatientDateOfBirth
            FROM Patients
            WHERE PatientID = ?""",
            (self.pat_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        dob = recieved[0][0]
        try:
            return datetime.datetime.strptime(dob, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            raise ValueError(
                f"DOB '{dob}' for patient {self.pat_id} is incorrectly \
                    formatted"
            )

    @property
    def gender(self) -> str:
        """Patient gender."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT PatientGender
            FROM Patients
            WHERE PatientID = ?""",
            (self.pat_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        gender = str(recieved[0][0])
        return gender

    @property
    def race(self) -> str:
        """Patient race."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        pat_dob_info = cursor.execute(
            f"""SELECT PatientRace
            FROM Patients
            WHERE PatientID = ?""",
            (self.pat_id,),
        )
        recieved = pat_dob_info.fetchall()
        connection.close()
        race = str(recieved[0][0])
        return race

    @property
    def age(self) -> int:  # O(1)
        """Get patient age."""
        time_since_birth = datetime.datetime.now() - self.dob  # O(1)
        time_since_birth_years = (
            time_since_birth.total_seconds() / 60 / 60 / 24 / 365.25
        )  # O(1)
        return int(time_since_birth_years)  # O(1)

    @property
    def labs(self) -> dict[str, list[Lab]]:
        """Get patient labs and organize into dictionary by lab name."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        lab_info_ex = cursor.execute("""SELECT LabID, LabName FROM Labs""")
        lab_info = lab_info_ex.fetchall()
        connection.close()
        pat_labs: dict[str, list[Lab]] = dict()
        for lab in lab_info:
            lab_id = lab[0]
            lab_name = lab[1]
            if lab_name in pat_labs.keys():
                pat_labs[lab_name].append(Lab(lab_id))
            else:
                pat_labs[lab_name] = [Lab(lab_id)]
        return pat_labs

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

    def add_labs(
        self, lab_name: str, value: float, units: str, time: str
    ) -> None:  # O(1)
        """Add lab to patient profile."""
        connection = sqlite3.connect("ehr.db")
        cursor = connection.cursor()
        lab_ids_ex = cursor.execute("""SELECT LabID FROM Labs""")
        lab_ids = lab_ids_ex.fetchall()
        try:
            max_lab_id = max([lab_id[0] for lab_id in lab_ids])
        except ValueError:
            max_lab_id = 0
        cursor.execute(
            """INSERT INTO Labs VALUES (?, ?, ?, ?, ?, ?)""",
            (
                max_lab_id + 1,
                self.pat_id,
                lab_name,
                value,
                units,
                time,
            ),
        )
        connection.commit()
        connection.close()

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
def parse_data(subjects_file_name: str, labs_file_name: str) -> None:
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

    # creates sql database
    connection = sqlite3.connect("ehr.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Patients")
    cursor.execute("DROP TABLE IF EXISTS Labs")
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
        """CREATE TABLE Patients(
                PatientID VARCHAR PRIMARY KEY,
                PatientGender VARCHAR,
                PatientDateOfBirth TIMESTAMP,
                PatientRace VARCHAR)"""
    )

    # adds patient for each patient

    for patient_info in subject_values:
        cursor.execute(
            "INSERT INTO Patients VALUES(?, ?, ?, ?)",
            (
                patient_info[0],  # ID
                patient_info[1],  # Gender
                patient_info[2],  # DOB
                patient_info[3],  # Race
            ),
        )

    # add lab for each lab
    unique_id = 0
    for lab in lab_values:
        cursor.execute(
            "INSERT INTO Labs VALUES(?, ?, ?, ?, ?, ?)",
            (
                unique_id,  # lab_id
                lab[0],  # ID
                lab[2],  # LabName
                lab[3],  # LabValue
                lab[4],  # LabUnits
                lab[5],  # LabTime
            ),
        )
        unique_id += 1
    connection.commit()
    connection.close()
