import pandas as pd
import os

from h5py import File


def load_time_grades(filepath) -> pd.DataFrame:
    _filename, file_extension = os.path.splitext(filepath)
    if file_extension == ".csv":
        return pd.read_csv(filepath)
    elif file_extension == ".h5":
        return load_from_h5(filepath)
    else:
        print(f"file not csv or h5 format: {filepath}")
        return pd.DataFrame()


def load_from_h5(filepath) -> pd.DataFrame:
    recording = File(filepath)

    with File(filepath) as recording:
        description = recording["/time_grades/text"]
        onset = recording["/time_grades/time"]
        dur = recording["/time_grades/duration"]

        time_grades = pd.DataFrame(
            {"Description": description, "Onset": onset, "Duration": dur}
        )
        time_grades["Description"] = time_grades["Description"].str.decode("utf-8")

        return time_grades
