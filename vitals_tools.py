"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Returns the recorded systolic blood pressure from each unique AND valid visit."""
    readings = []
    for encounter in encounters:
            readings.append(encounter["systolic"])
    return readings
    pass


def mean_systolic(readings):
    """Returns the mean value of the systolic blood pressure among all visits if readings exist. If not, returns None."""
    if not readings:
        return None
    return sum(readings) / len(readings)
    pass


def count_patients(encounters):
    """Reads the patient IDs saved in encounters, saves them to a list if they are unique, and returns that list of unique IDs seen."""
    output = []
    for encounter in encounters:
         if encounter not in output:
            output.append(encounter["patient_id"])
    return output
    pass


def patients_at_or_above(encounters, cutoff):
    """Return patient IDs if the recorded systolic pressure is higher than the cutoff."""
    output = []
    for encounter in encounters:
        if encounter["systolic"] > cutoff:
            output.append(encounter["patient_id"])
    return output
    pass
