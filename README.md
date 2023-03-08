# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

## For end users:

To setup install: Download project folder & complete funciton import as follows:

import [folder name].functionality.py

**Expected files needed:**

(1) Lab file ["lab file name"]: .csv file formatted exclusively to some or all of the following columns:

*Columns* : "PatientID", "PatientGender", "PatientDateOfBirth", "PatientRace" "PatientMaritalStatus", "PatientLanguage", PatientPopulationPercentageBelowPoverty"

(2) Subject file ["subject file name"]: .csv file formatted exclusively to some or all of the following columns:

*Columns* : "PatientID", "PatientGender", "PatientDateOfBirth", "PatientRace", "PatientMaritalStatus", "PatientLanguage", "PatientPopulationPercentageBelowPoverty"

**Useful Functions**

*parse_data(subject_file_name, lab_file_name):*
Takes in lab file and subject file names and organizes into a nested dictionary
suitable for filtering. Takes in subject_file_name (subject file name) and
lab_file_name (lab file name).

*patient_age(records, patient_id):*
Takes in records (parsed data files from parse_data function) and patient id
to return patient age of particular patient.

*patient_is_sick(records, patient_id, lab_name, operator, value)*
Returns whether or not patient is sick from a particular disease or lab name (lab_name),
a lab value indicating threshold of sickness (value), an operator (operator) indicating 
whether sickness defined as above or below threshold value, a patient id (patient_id),
and a records file from parse_data function (records).



**Example usage**

import functionality

parsed_data = functionality.parse_data("subject file name", "lab file name")

patient_age(records = parsed_data, patient_id: "PATID") -> Age

patient_is_sick(
    records = parsed_data
    patient_id = "PATID"
    lab_name = "DISEASE"
    operator = ">"
    value = "100"
) -> TRUE / FALSE



## For contributors:

For testing, with current tests or adding additional tests for your lab / subjects
files...

(1) (Optional) Add tests to tess/test_functionality.py file

(2) Run "pytest tests/test_functionality.py" in terminal (install pytest)

(3) To check coverage run "coverage report" (install coverage)
