# Client Complexity ClickUp Sync

A Python tool for mapping ACA client data into a client complexity format and synchronizing the result with ClickUp.

## Project status

This project is currently a work in progress. The two data models and configurable field mapper have been scaffolded. The final model fields, complexity rules, and ClickUp API operations still need to be implemented.

## Goal

Keep the client list and relevant metadata in ClickUp synchronized with ACA client data. Two internal models have separate responsibilities:

| Model | Responsibility |
| --- | --- |
| ACA Client model | Represents each client's actual ACA data and metadata |
| Client Complexity model | Represents the mapped fields and calculated values that will be sent to ClickUp |

ClickUp is the synchronization destination where users can view and manage the resulting client records.

## Expected data flow

```text
ACA Client model
        |
        | Read client data
        v
Client Complexity model
        |
        | Map fields and calculate complexity
        v
ClickUp
        |
        | Create a new task or update an existing task
        v
Current client complexity record
```

The synchronization process should:

1. Read the current client list and client data from the ACA Client model.
2. Map the required ACA fields into the Client Complexity model.
3. Calculate the client's complexity values.
4. Find the corresponding client task in ClickUp using a stable client identifier.
5. Create a ClickUp task when the client has not been synchronized before.
6. Update the existing ClickUp task when mapped data or calculated values change.
7. Save or retain the ClickUp task ID so future runs update the same task.

This create-or-update behavior is an **upsert**. It prevents the synchronization process from creating a duplicate ClickUp task every time it runs.

## Field mapping

Each value sent to ClickUp needs an explicit mapping. For example:

| ACA Client data | Client Complexity field | ClickUp destination |
| --- | --- | --- |
| Client identifier | ACA client ID | Client ID custom field |
| Client name | Client name | Task name |
| Employee or member count | Number of people | Number of People custom field |
| Manual change count | Manual changes | Manual Changes custom field |
| Data conflict count | Conflict count | Conflict Count custom field |
| Calculated result | Total score | Total Complexity Score custom field |

These field names are examples. The final mapping must use the actual ACA model fields and ClickUp custom field IDs.

## Planned complexity scoring

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

## Running the current project

Run the current mapping test from the project directory with:

```bash
python -m unittest discover -s tests
```

The current implementation does not yet read ACA client records or make ClickUp API requests.

## Project structure

```text
.
|-- models/
|   |-- __init__.py
|   |-- aca_client.py          # Source ACA client model
|   `-- client_complexity.py   # Mapped ClickUp data model
|-- services/
|   |-- __init__.py
|   |-- client_mapper.py       # ACA-to-complexity field mapping
|   `-- clickup_sync.py        # ClickUp upsert service
|-- tests/
|   |-- test_logic.py
|   |-- test_client_mapper.py
|   `-- test_clickup_sync.py
|-- .env.example               # Required environment variables
|-- config.py                  # Application configuration
|-- logic.py                   # Complexity scoring functions
|-- requirements.txt           # Python dependencies
`-- README.md                  # Project documentation
```

## Next steps

1. Replace the generic metadata fields with the final ACA and Client Complexity schemas.
2. Document the mapping from model fields to ClickUp custom field IDs.
3. Choose the stable client identifier used to find the correct ClickUp task.
4. Obtain the ClickUp workspace, space, list, and custom field identifiers required by the integration.
5. Define how new, changed, inactive, missing, and deleted clients should be handled.
6. Implement ClickUp task creation and updates in `ClickUpSyncService`.
7. Define and implement the remaining complexity scoring rules.
8. Add integration and scoring tests.
