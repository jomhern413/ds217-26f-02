#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")

def read_encounters(data_path):
    """TODO: A usuable encounter has exactly three comma-separated fields with an integer as the third value that is between 60 mmHg and 250 mmHg.
    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # read the rows and skip the header line.
    with data_path.open("r", encoding="utf-8") as data_file: # read the input as a data file
        rows = data_file.readlines() 
        encounters = []                       # this is where we're storing things
        skipped = []
    for row in rows[1:]:                      # ignore the headers pls
        if not row.strip():                   
            print("BLANK")                    # ignore not rows
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:                  # ignore rows with too many things
            skipped.append({"patient_id": patient_id, "systolic": systolic})
            print(f"WRONG AMT. OF FIELDS. {len(fields)} FIELDS. {row.strip()}")
            continue
        patient_id, visit_date, systolic = fields
        try:
            systolic = int(systolic)      # if something is weird ignore it
        except ValueError as error:
            skipped.append({"patient_id": patient_id, "systolic": systolic})
            print(f"SKIP {patient_id}. ERROR: {error}. {row.strip()}")
            continue
        if 60 > int(systolic):
            skipped.append({"patient_id": patient_id, "systolic": systolic})
            print(f"SKIP {patient_id}. ERROR IN SYSTOLIC BLOOD PRESSURE READING. LOW.")
            continue
        if int(systolic)>250:
                    skipped.append({"patient_id": patient_id, "systolic": systolic})
                    print(f"SKIP {patient_id}. ERROR IN SYSTOLIC BLOOD PRESSURE READING. HIGH.")
                    continue
        else:
            encounters.append({"patient_id": patient_id, "systolic": systolic})
            print(f"{patient_id} ADDED.") # add if things worked out
    return encounters, skipped


def main():
    """This returns the count of usuable encounters and skipped lines."""
    encounters, skipped = read_encounters(DATA_PATH)
    # Building the report lines.
    usable = len(encounters)
    unusable = len(skipped)
    patnum = count_patients(encounters)
    meansys = mean_systolic(systolic_readings(encounters))
    maxsys = max(systolic_readings(encounters))
    minsys = min(systolic_readings(encounters))
    
    # Saving the vitals report as output
    OUTPUT_DIR.mkdir(exist_ok=True)           # no error when output/ already exists
    reportPath = OUTPUT_DIR / "vitals_report.txt"
    with open(reportPath, "w", encoding="utf-8") as coolReportFile:
        coolReportFile.write("")
        print("Usable encounters:", usable, "\n"+"Skipped rows:", unusable, "\n"+"Patients seen:", len(patnum),"\n"+"Mean systolic:", meansys,"\n"+"Highest systolic:", maxsys, "\n"+"Lowest systolic:",minsys, file = coolReportFile)
    
    # Cutoff decision, and follow-up writing setup
    cutoff = 130
    cutpatlist = patients_at_or_above(encounters,cutoff) # making list of cutoffs 
    cutpatslines = "\n".join(cutpatlist) + "\n"
    followupPath = OUTPUT_DIR / "followup_list.txt"
    with open(followupPath, "w", encoding="utf-8") as coolFollowupFile:
        coolFollowupFile.write("")
        print("Cutoff:", cutoff, "\n"+"Reason: I chose a systolic blood pressure of 130 mmHg because it is the lowest possible systolic blood pressure value where level 1 hypertension is diagnosed."
            , "\n"+cutpatslines,file = coolFollowupFile)
    
    
    return None



if __name__ == "__main__":
    main()