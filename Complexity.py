"""Client complexity scoring.

Loads client data into a DataFrame, runs each category scorer, and combines
the results into a single complexity score.

NOTE: the calculations inside each scorer are still placeholders. They will be
replaced once the real scoring rules are decided.
"""

import argparse
import math

import pandas as pd

DEFAULT_DATA_PATH = "data.csv"


def initial_data_complexity(df: pd.DataFrame) -> float:
    """Score how complex a dataset is.

    Placeholder: total number of unique values across all columns.
    """

    return float(df.nunique().sum())


def size_score(df: pd.DataFrame) -> float:
    """Score based on the amount of people (size of the data). Need to make a key that identifies the people in the data. For now, just return 0.3 times the number of rows."""
    
    "How the people are counted"
    num_rows, num_cols = df.shape
    people = 0
    baseScore = 0.3
        
    return float(people * baseScore)


def base_score(df: pd.DataFrame) -> float:
    """Score based on the data once it is processed.

    Placeholder: mean of the means of the numeric columns.
    Returns 0 when there are no numeric columns.
    """
    numeric_cols = df.select_dtypes(include="number")
    if numeric_cols.empty:
        return 0.0
    value = numeric_cols.mean().mean()
    return 0.0 if math.isnan(value) else float(value)


def manual_changes_score(df: pd.DataFrame) -> float:
    """Score based on the amount of manual changes."""

    """ The Math of this"""
    manual_changes = input("Enter the number of manual changes made to the data: ")
    cost = 0.5  # Placeholder cost per manual change
    try:
        manual_changes = int(manual_changes)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of manual changes.")
        return 0.0

    return float(manual_changes * cost)


def conflict_score(df: pd.DataFrame) -> float:
    """Score based on the amount of conflicts."""

    """The Math of this"""

    manual_conflicts = input("Enter the number of conflicts in the data: ")
    cost = 30  # Conflicts per point (rounded up to the next whole number)
    try:
        manual_conflicts = int(manual_conflicts)
    except ValueError:
        print("Invalid input. Please enter a valid integer for the number of conflicts.")
        return 0.0

    return float(math.ceil(manual_conflicts / cost))


def monthly_loader_score(df: pd.DataFrame) -> float:
    """Additional score based on the effort to load clients through the monthly loader."""

    """ The Math"""
    lastMonthsPeople = int(input("Enter the number of people loaded in the last month: "))
    people = int(input("Enter the number of people loaded this month: "))
    cost = 0.001

    if lastMonthsPeople == 0:
        return float(people * cost)
    else:
        return float((people - lastMonthsPeople) * cost)

# Every category scorer, in the order it is reported.
SCORERS = {
    "initial_data_complexity": initial_data_complexity,
    "size": size_score,
    "base": base_score,
    "manual_changes": manual_changes_score,
    "conflicts": conflict_score,
    "monthly_loader": monthly_loader_score,
}


def load_data(path: str) -> pd.DataFrame:
    """Load client data from a CSV file."""
    return pd.read_csv(path)


def score_breakdown(df: pd.DataFrame) -> dict[str, float]:
    """Run every scorer and return each category's score."""
    return {name: scorer(df) for name, scorer in SCORERS.items()}


def complexity_score(df: pd.DataFrame) -> float:
    """Combine every category score into one complexity score."""
    return sum(score_breakdown(df).values())


def main() -> None:
    """What runs the whole thing."""
    parser = argparse.ArgumentParser(description="Score client complexity.")
    parser.add_argument(
        "path",
        nargs="?",
        default=DEFAULT_DATA_PATH,
        help=f"CSV file to score (default: {DEFAULT_DATA_PATH})",
    )
    args = parser.parse_args()

    df = load_data(args.path)
    breakdown = score_breakdown(df)

    for name, value in breakdown.items():
        print(f"{name:>24}: {value:,.2f}")
    print(f"{'Complexity Score':>24}: {sum(breakdown.values()):,.2f}")


if __name__ == "__main__":
    main()
