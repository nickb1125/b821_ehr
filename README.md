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

Functions include:
parse_data(lab_file_name, subject_file_name) : parses lab and subject files to reorganize data. Note this is done during initialization but can be redone if neccecary.


**Useful Classes**

*Lab*

Attributes include:
- pat_id : Patient ID.
- name : Lab name.
- value : Lab value.
- units : Lab units.
- time : Time lab was taken.


*Patient*

Attributes include:
- pat_id : Patient ID.
- gender : Patient gender.
- dob : Patient date of birth.
- race : Patient Race.
- age : (not input by user) Patient Age.
- labs: (not input at initialization) Dictionary of lab object lists for lab name keys.

Frontend Methods Include:
- is_sick(lab_name, operator, value) : 
Returns whether or not patient is sick from a particular disease or lab name (lab_name),
a lab value indicating threshold of sickness (value), an operator (operator).
- add_labs(lab_object) :
Adds labs to patient.labs attribute given a Lab object.
- get_age_at_first_lab() : 
Gets patient age at first lab.
- get_lab_test_values(lab_name) :
Gets all values for a particular lab test name for patient.


**Example usage**

import functionality


pat_1a = functionality.Patient(
    pat_id="1A", gender="Male", dob="2000-06-15 02:45:40.547", race="White"
    )

patient_age(records = parsed_data, patient_id: "PATID") -> Age at first lab


pat_1a.add_labs(
        functionality.Lab(
            pat_id="1A",
            name="POTASSIUM",
            value="37",
            units="mg/dL",
            time="2001-07-01 03:20:24.070",
        )
    )


pat_1a.age -> Age


pat_1a.is_sick(lab_name = "DISEASE", operator = ">", value = "100") -> TRUE / FALSE


## For contributors:

For testing, with current tests or adding additional tests for your lab / subjects
files...

(1) (Optional) Add tests to tests/test_functionality.py file

(2) Run "pytest tests/test_functionality.py" in terminal (install pytest)

(3) To check coverage run "coverage report" (install coverage)
