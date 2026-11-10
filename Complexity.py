"""Sync ClickUp client complexity.

For every task in the Client's complexity view:
  1. Set its Client Complexity dropdown from its Total Complexity Score.
  2. Copy that Client Complexity onto the linked client record.
  3. Copy CM and DM from the linked client record onto the complexity task.

Usage:
  python Complexity.py           -> dry run (logs what would change)
  python Complexity.py --apply   -> actually write to ClickUp

Every run is logged to complexity_changes.log next to this file.
"""

import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv


# --- ClickUp connection -------------------------------------------------------

load_dotenv()
API = "https://api.clickup.com/api/v2"
TOKEN = os.getenv("CLICKUP_TOKEN")
if not TOKEN:
    raise SystemExit("CLICKUP_TOKEN is not set - add it to your .env file")
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}


# --- Logging ------------------------------------------------------------------

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "complexity_changes.log")

log = logging.getLogger("complexity")
log.setLevel(logging.INFO)
_formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%Y-%m-%d %H:%M:%S")
for _handler in (logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()):
    _handler.setFormatter(_formatter)
    log.addHandler(_handler)


# --- ClickUp IDs --------------------------------------------------------------

SOURCE_VIEW = "8ccv77e-43891"  # Client's complexity view, from .../v/gr/8ccv77e-43891
LIST_ID = "901112212244"       # Client's complexity list, from .../v/l/6-901112212244-1

# Custom fields
SCORE_FIELD = "409ec9ce-c401-40f6-9ac7-aa0722ebf717"     # Total Complexity Score (formula)
DROPDOWN_FIELD = "123cc1b6-b79e-4a1e-ba14-111333e75731"  # Client Complexity (drop_down)
CLIENT_FIELD = "c5fa7c66-f150-4595-a8f7-dc510320249a"    # Client Name (link to client record)
CM_FIELD = "4b234a38-2cf8-401c-9dda-350305458b70"        # CM (users)
DM_FIELD = "d02807f7-f2b0-457a-8a47-eaa5123c6e24"        # DM (users)
PEOPLE_FIELDS = {"CM": CM_FIELD, "DM": DM_FIELD}         # copied client record -> complexity task

# ClickUp's API can return stale formula values. Re-saving this field (with the same
# webhook URL every task already has) makes ClickUp recalculate the task's formulas.
RECALC_FIELD = "08913302-f377-4bf7-8193-86db221339bd"  # Trigger recalculation (url)
RECALC_URL = "https://maxidroms83.app.n8n.cloud/webhook/d4bfadd2-bd8a-4b21-98fc-66756cb8ea20"
RECALC_WAIT = 3  # seconds to give ClickUp to finish recalculating

# Client Complexity dropdown options, in the same order as in ClickUp
# (ClickUp reports a dropdown's current value as its position in this order).
VERY_EASY = "c18c0d96-1142-4b46-a5b0-dea3be63c275"
EASY = "f8e142d8-2eef-41d2-9e59-c3fe2418bd84"
MODERATE = "577a56b6-9c67-4eb0-9497-8fb06f0f9d6a"
DIFFICULT = "b849fbbd-7dd3-43e6-9155-1ffe90145a02"
VERY_DIFFICULT = "d7a5cde1-dd86-44d2-8db0-50844efb902b"

OPTION_NAMES = {
    VERY_EASY: "Very Easy",
    EASY: "Easy",
    MODERATE: "Moderate",
    DIFFICULT: "Difficult",
    VERY_DIFFICULT: "Very Difficult",
}
OPTION_ORDER = list(OPTION_NAMES)

# (max score, option) - the first row whose max >= score wins.
CUTOFFS = [
    (20, VERY_EASY),
    (35, EASY),
    (50, MODERATE),
    (65, DIFFICULT),
    (float("inf"), VERY_DIFFICULT),
]


# --- ClickUp API calls --------------------------------------------------------

def call(method, path, **kwargs) -> dict:
    """Make a ClickUp API call. If ClickUp says we're going too fast (HTTP 429),
    wait until the limit resets and try again instead of crashing."""
    for _ in range(5):
        r = requests.request(method, f"{API}{path}", headers=HEADERS, timeout=30, **kwargs)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        reset = r.headers.get("X-RateLimit-Reset")
        wait = max(1, int(reset) - int(time.time()) + 1) if reset else 60
        log.info(f"ClickUp rate limit hit - waiting {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"ClickUp kept rate-limiting {method} {path} after 5 tries")


def get_custom_fields(list_id):
    """Custom fields on a list (id, name, type). Handy for looking up new field IDs."""
    return call("GET", f"/list/{list_id}/field")["fields"]


def get_view_tasks(view_id):
    """Every task in a view, following pagination. Formula values here can be stale."""
    tasks, page = [], 0
    while True:
        data = call("GET", f"/view/{view_id}/task", params={"page": page})
        tasks += data["tasks"]
        if data.get("last_page", True):
            return tasks
        page += 1


def get_task(task_id):
    """One task with fresh values (unlike the view)."""
    return call("GET", f"/task/{task_id}")


def set_field(task_id, field_id, value):
    """Write a custom field value on a task."""
    call("POST", f"/task/{task_id}/field/{field_id}", json={"value": value})


# --- Reading task values ------------------------------------------------------

def field_value(task, field_id):
    """A custom field's value on a task, or None if it isn't set."""
    for f in task.get("custom_fields", []):
        if f["id"] == field_id:
            return f.get("value")
    return None


def current_option(task):
    """The task's current Client Complexity option ID, or None if blank."""
    current = field_value(task, DROPDOWN_FIELD)
    return OPTION_ORDER[current] if isinstance(current, int) else current


def user_ids(task, field_id):
    """IDs of the people in a users field (CM / DM)."""
    return {u["id"] for u in (field_value(task, field_id) or [])}


def user_names(task, field_id):
    """Names of the people in a users field, for logging."""
    return ", ".join(u["username"] for u in (field_value(task, field_id) or [])) or "(empty)"


def score_to_option(score):
    """Map a score to a dropdown option ID. Score 0 or missing -> None (leave blank)."""
    if score in (None, ""):
        return None
    score = float(score)
    if score <= 0:
        return None
    for max_score, option in CUTOFFS:
        if score <= max_score:
            return option


# --- Steps --------------------------------------------------------------------

def refresh_scores(tasks):
    """Make ClickUp recalculate each task's formulas, then re-read the tasks."""
    log.info(f"Recalculating scores on {len(tasks)} tasks...")
    for t in tasks:
        set_field(t["id"], RECALC_FIELD, RECALC_URL)
    time.sleep(RECALC_WAIT)

    fresh = [get_task(t["id"]) for t in tasks]
    for old, new in zip(tasks, fresh):
        before, after = field_value(old, SCORE_FIELD), field_value(new, SCORE_FIELD)
        if before != after:
            log.info(f'Recalculated {new["name"]}: score {before} -> {after}')
    return fresh


def linked_client(task):
    """The client record this complexity task links to (Client Name field), or None."""
    links = field_value(task, CLIENT_FIELD) or []
    if not links:
        return None
    if len(links) > 1:
        log.warning(f'{task["name"]}: linked to {len(links)} client records, using the first')
    return get_task(links[0]["id"])


def sync_task(task, verb, apply):
    """Bring one complexity task and its client record up to date.
    Returns how many changes were made (or would be made in a dry run)."""
    changes = 0
    name = task["name"]
    score = field_value(task, SCORE_FIELD)
    option = score_to_option(score)

    # 1. Complexity task's dropdown from its score (score 0 -> left blank)
    if option and current_option(task) != option:
        log.warning(f"{verb}: {name} complexity task (score {score}) -> {OPTION_NAMES[option]}")
        if apply:
            set_field(task["id"], DROPDOWN_FIELD, option)
        changes += 1

    client = linked_client(task)
    if client is None:
        log.warning(f"{name}: no linked client record found, skipping client/CM/DM")
        return changes

    # 2. Client record's dropdown from the complexity task
    if option and current_option(client) != option:
        log.warning(f'{verb}: {client["name"]} client record ({client.get("custom_id")}) '
                    f"Client Complexity -> {OPTION_NAMES[option]}")
        if apply:
            set_field(client["id"], DROPDOWN_FIELD, option)
        changes += 1

    # 3. CM / DM from the client record onto the complexity task
    #    (only when the client record has someone; an empty field is not copied)
    for label, field_id in PEOPLE_FIELDS.items():
        want, have = user_ids(client, field_id), user_ids(task, field_id)
        if not want or want == have:
            continue
        log.warning(f"{verb}: {name} complexity task {label}: "
                    f"{user_names(task, field_id)} -> {user_names(client, field_id)}")
        if apply:
            set_field(task["id"], field_id, {"add": sorted(want - have), "rem": sorted(have - want)})
        changes += 1

    return changes


def sync_complexity(apply=False):
    """Run the sync on every task in the view.
    apply=False is a dry run: it logs what would change. It still re-saves the
    Trigger recalculation field so the preview uses real scores."""
    log.info(f"===== {'APPLY' if apply else 'DRY RUN'} started (all clients) =====")
    verb = "SET" if apply else "WOULD SET"

    tasks = refresh_scores(get_view_tasks(SOURCE_VIEW))
    changes = sum(sync_task(t, verb, apply) for t in tasks)

    log.info(f"{len(tasks)} tasks | {changes} {'changes made' if apply else 'changes to make'}")


if __name__ == "__main__":
    try:
        sync_complexity(apply="--apply" in sys.argv)
    except Exception:
        log.exception("Run stopped with an error")
        raise
