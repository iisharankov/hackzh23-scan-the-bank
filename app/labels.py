import pandas as pd

def load_labels(): 

    labels = pd.read_csv("../files/sorted/labels.csv")

    def split_filename(filename): 
        pair = filename.split(".")
        return tuple(pair) if len(pair) == 2 else (pair[0], "weird")
    
    labels[["name", "extension"]] = labels.apply(lambda row: split_filename(row["filename"]), result_type='expand', axis = 1)
    return labels

def create_summary(): 

    labels = load_labels()

    summary = pd.DataFrame()

    summary["count"] = labels.groupby(by = "extension")["filename"].count()
    summary["frequency"] = summary["count"] / summary["count"].sum()
    summary["perc sensitive"] = labels.groupby(by = ["extension"])["sensitive"].mean()

    summary = summary.sort_values(by = "frequency", ascending=False)
    summary = summary.reset_index(drop = False)

    return summary

