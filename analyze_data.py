
import numpy as np
import pandas as pd

def get_columns(all_scores):
    cols,  = set(tuple(sorted(x)) for x in all_scores.values())
    return cols

def sanitize_scores(cols, scores):
    results = np.zeros(len(cols))
    for k, v in scores.items():
        results[cols.index(k)] = max(v.get('total', 0), v.get('effort', 0))
    return results

def remove_all_0s(data):
    return data.drop(data.agg('max')[data.agg('max') == 0].keys(), axis=1)

def to_frame(all_scores):
    cols = get_columns(all_scores)
    sanitized_scores = [(student, sanitize_scores(cols, scores)) for student, scores in all_scores.items()]
    data = pd.DataFrame([scores for _, scores in sanitized_scores],
                        index=[student for student, _ in sanitized_scores],
                        columns=cols)
    return remove_all_0s(data)

def by_cat(assign_type):
    return lambda x, cols: sum(val for col, val in zip(cols, x) if col.startswith(assign_type))

def recent_effort(row, cols):
    lab = hw = disc = 0
    for col, val in zip(cols, row):
        if col.startswith("disc"):
            disc = val
        if col.startswith("lab"):
            lab = val
        if col.startswith("hw"):
            hw = val
    return 2 * (disc + lab) + hw

def for_assignment(assign):
    def query(x, cols):
        if assign in cols:
            return x[cols.index(assign)]
        else:
            return 0
    return query

QUERIES = [
    ("score", lambda x, cols: sum(val for col, val in zip(cols, x) if not col[:3] in ("lab", "dis"))),
    ("disc", by_cat("disc")),
    ("lab", by_cat("lab")),
    ("hw", by_cat("hw")),
    ("proj", by_cat("proj")),
    ("midterm 1", for_assignment("midterm1")),
    ("midterm 2", for_assignment("midterm2")),
    ("final", for_assignment("final")),
    ("recent effort", recent_effort)
]

def run_queries(data):
    frame = pd.DataFrame(np.array([list(data.apply(lambda x: fn(x, list(data.columns)), axis=1)) for _, fn in QUERIES]).T,
                         index=data.index, columns=[x for x, _ in QUERIES])
    frame = remove_all_0s(frame)
    return frame.sort_values(list(frame.columns))
