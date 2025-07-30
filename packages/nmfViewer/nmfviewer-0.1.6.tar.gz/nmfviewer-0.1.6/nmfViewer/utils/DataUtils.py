import pandas as pd
import numpy as np


def transform_time_grades(time_grades: pd.DataFrame, sampling_frequency=50):
    time_grades.loc[:, "Onset":"Duration"] = round(
        time_grades.loc[:, "Onset":"Duration"] * sampling_frequency
    )
    return time_grades


def transform_triggers(triggers: np.ndarray, sampling_frequency=50):
    triggers *= sampling_frequency
    return np.rint(triggers)
