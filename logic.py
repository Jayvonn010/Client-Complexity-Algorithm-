"""Complexity scoring functions.

The scoring rules are intentionally left as placeholders until the business
rules for size and processing complexity are finalized.
"""


def size_score() -> float:
    """Calculate workload based on the number of people in the client file."""

    raise NotImplementedError("The size scoring rules have not been defined.")


def processing_score() -> float:
    """Calculate complexity from client processing requirements."""

    raise NotImplementedError("The processing scoring rules have not been defined.")


def manual_change_score() -> float:
    """Calculate effort caused by manual changes."""

    raise NotImplementedError("The manual-change inputs have not been connected.")


def conflict_score() -> float:
    """Calculate effort caused by data conflicts."""

    raise NotImplementedError("The conflict inputs have not been connected.")


def monthly_loaded_score() -> float:
    """Calculate additional effort for clients using the monthly loader."""

    raise NotImplementedError("The monthly-loader inputs have not been connected.")


def total_score() -> float:
    """Return the sum of all client complexity score components."""

    return (
        size_score()
        + processing_score()
        + manual_change_score()
        + conflict_score()
        + monthly_loaded_score()
    )
