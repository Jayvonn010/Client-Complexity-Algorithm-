import os, sys, requests
from dotenv import load_dotenv


#Getting access to ClickUp's API
load_dotenv()
API = "https://api.clickup.com/api/v2"
TOKEN = os.getenv("CLICKUP_TOKEN")
if not TOKEN:
    raise SystemExit("CLICKUP_TOKEN is not set - add it to your .env file")
H = {"Authorization": TOKEN, "Content-Type": "application/json"}

#Seeing what list we are working with
SOURCE_VIEW = "8ccv77e-43891"   # view ID, from .../v/gr/8ccv77e-43891
LIST_ID     = "901112212244"    # list ID, from .../v/l/6-901112212244-1
DESTINATION_VIEW = "8ccv77e-43891"  # view ID, from .../v/gr/8ccv77e-43891

SCORE_FIELD    = "409ec9ce-c401-40f6-9ac7-aa0722ebf717"   # Total Complexity Score (formula)
DROPDOWN_FIELD = "123cc1b6-b79e-4a1e-ba14-111333e75731"   # Client Complexity (drop_down)

# Dropdown option IDs
VERY_EASY      = "c18c0d96-1142-4b46-a5b0-dea3be63c275"
EASY           = "f8e142d8-2eef-41d2-9e59-c3fe2418bd84"
MODERATE       = "577a56b6-9c67-4eb0-9497-8fb06f0f9d6a"
DIFFICULT      = "b849fbbd-7dd3-43e6-9155-1ffe90145a02"
VERY_DIFFICULT = "d7a5cde1-dd86-44d2-8db0-50844efb902b"

# TODO: placeholder cutoffs - replace with the real ones.
# (max score, option) - first row whose max >= score wins.
CUTOFFS = [
    (20,  VERY_EASY),
    (35,  EASY),
    (50,  MODERATE),
    (65,  DIFFICULT),
    (float("inf"), VERY_DIFFICULT),
]
OPTION_NAMES = {VERY_EASY: "Very Easy", EASY: "Easy", MODERATE: "Moderate",
                DIFFICULT: "Difficult", VERY_DIFFICULT: "Very Difficult"}


def get_custom_fields(list_id):
    """Return the custom fields available on a list (id, name, type)."""
    r = requests.get(f"{API}/list/{list_id}/field", headers=H)
    r.raise_for_status()
    return r.json()["fields"]

# Seeing each task in the view, following pagination
def get_view_tasks(view_id):
    """Return every task in a view, following pagination."""
    tasks, page = [], 0
    while True:
        r = requests.get(f"{API}/view/{view_id}/task", headers=H, params={"page": page})
        r.raise_for_status()
        data = r.json()
        tasks += data["tasks"]
        if data.get("last_page", True):
            return tasks
        page += 1

#Seeing the value of a custom field on a task
def field_value(task, field_id):
    for f in task.get("custom_fields", []):
        if f["id"] == field_id:
            return f.get("value")
    return None

#Mapping the score that we get from the formula to the dropdown option ID
def score_to_option(score):
    """Map a score to a dropdown option ID. Score 0 / missing -> None (leave blank)."""
    if score in (None, ""):
        return None
    score = float(score)
    if score <= 0:
        return None
    for max_score, option in CUTOFFS:
        if score <= max_score:
            return option

# Setting the dropdown value on a task
def set_dropdown(task_id, option_id):
    r = requests.post(f"{API}/task/{task_id}/field/{DROPDOWN_FIELD}",
                      headers=H, json={"value": option_id})
    r.raise_for_status()

# Syncing the complexity scores to the dropdowns
def sync_complexity(apply=False):
    """Set each task's Client Complexity dropdown from its Total Complexity Score.
    apply=False is a dry run: prints what would change, writes nothing."""
    tasks = get_view_tasks(SOURCE_VIEW)
    changed = skipped = 0
    for t in tasks:
        option = score_to_option(field_value(t, SCORE_FIELD))
        if option is None:
            skipped += 1
            continue
        current = field_value(t, DROPDOWN_FIELD)
        # ClickUp returns the dropdown's current value as the option's orderindex
        current_id = list(OPTION_NAMES)[current] if isinstance(current, int) else current
        if current_id == option:
            continue
        print(f'{"SET" if apply else "WOULD SET"}: {t["name"]} '
              f'(score {field_value(t, SCORE_FIELD)}) -> {OPTION_NAMES[option]}')
        if apply:
            set_dropdown(t["id"], option)
        changed += 1
    print(f"\n{len(tasks)} tasks | {changed} {'updated' if apply else 'to update'} "
          f"| {skipped} left blank (score 0)")


if __name__ == "__main__":
    # python Complexity.py          -> dry run
    # python Complexity.py --apply  -> actually write to ClickUp
    sync_complexity(apply="--apply" in sys.argv)
