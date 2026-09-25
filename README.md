# Client Complexity Algorithm

A Python scoring tool for estimating the effort required to process a client's data. The planned algorithm combines client size, processing complexity, manual corrections, data conflicts, and monthly-loader volume into one complexity score.

## Project status

This project is currently a work in progress. [`logic.py`](./logic.py) defines the structure of the scoring model, but the individual scoring functions have not been implemented yet. Running the file completes without producing a score.

## Planned scoring model

The total complexity score will be the sum of five components:

| Component | Purpose | Planned calculation |
| --- | --- | --- |
| Size score | Measures workload based on the number of people in the input data | To be determined |
| Processing score | Measures the complexity of processing the client's data | To be determined |
| Manual change score | Accounts for manual data changes | `ceil(manual changes / 5)` |
| Conflict score | Accounts for conflicts found in the data | `ceil(conflicts / 30)` |
| Monthly-loaded score | Adds effort for clients processed through the monthly loader | `number of people * 0.001` |

The processing score is intended to consider:

- Demographic processing complexity
- Whether ACA status must be calculated
- ACA status changes and processing complexity
- Benefit group status changes and processing complexity
- Transfers
- Employment processing complexity
- Enrollment processing complexity
- COBRA processing complexity
- Dependent processing complexity
- Data quality

The planned total is:

```text
total score = size score
            + processing score
            + manual change score
            + conflict score
            + monthly-loaded score
```

## Requirements

- Python 3
- No third-party packages are currently required

## Running the current file

From the project directory, run:

```bash
python logic.py
```

The current implementation does not accept input or print output. Those behaviors can be added after the scoring rules and input format are finalized.

## Project structure

```text
.
├── logic.py   # Scoring model skeleton
└── README.md  # Project documentation
```

## Next steps

1. Define the size and processing scoring rules.
2. Decide how client data will be supplied to the algorithm.
3. Implement each scoring function.
4. Return or display the total score.
5. Add tests for score boundaries and rounding behavior.

