# AI Learning Log - Engineer A (Elijah Mamodu)

## Interaction 1: Validating Input Type and Value Checking
* **What I understood before:** I knew that Python can verify integers using conditions like `if type(x) is int`.
* **What I was unsure about:** I was unsure about the cleanest pattern to catch negative integers, empty string inputs, and floats (like `3.5`) in a single pass without crashing the validation loop.
* **AI Explanation Summary:** The AI demonstrated using strict type isolation (`type(affected_users) is not int`) combined with value evaluations (`affected_users <= 0`) alongside `.strip()` checking methods for strings to isolate empty whitespaces before raising formal `ValueError` exceptions.
* **My Experiment & Verification:** I wrote a localized function verification that isolated string inputs and float variables. I predicted it would trigger a `ValueError`, which was confirmed when my unit tests executed with an `ok` status.
* **How this helped my feature:** This allowed me to build the validation layer for `create_ticket()` that completely rejects zeroes, string variables, or decimal values for affected users while preserving the internal dictionary matrix.

## Interaction 2: Managing JSON De-serialization Safely
* **What I understood before:** I knew Python's built-in `json.dump()` and `json.load()` could serialize and deserialize dictionary tracking objects to text files.
* **What I was unsure about:** How to handle the system gracefully if a database file does not exist yet on a completely fresh initialization without throwing a missing file crash error.
* **AI Explanation Summary:** The AI explained utilizing `os.path.exists()` to safely verify a file path's presence before execution, returning an empty list array placeholder `[]` if missing, and wrapping execution runs in a `try...except json.JSONDecodeError` block.
* **My Experiment & Verification:** I tested a temporary setup where an intentionally malformed JSON string (`{ invalid json ... [`) was placed inside a mock path file. The loader raised a `ValueError` exactly as predicted rather than clearing out or corrupting our list.
* **How this helped my feature:** This provided the foundation for `campusflow/storage.py`, ensuring a clean user experience on fresh deployments while protecting against database corruption.

## Interaction 3: AI Suggestion Independently Corrected and Rejected
* **What I understood before:** I knew our sprint project was explicitly divided into separate assignments between Engineer A and Engineer B to ensure unique development logs and branch separation.
* **What I was unsure about:** I needed clarification on mapping my finished validation code into our project's broader sequence.
* **The AI Suggestion:** The AI provided a broad implementation layout that generated complete placeholder features belonging to Engineer B (such as `workflow.py`, `reports.py`, and menu controllers inside `main.py`).
* **My Correction and Rejection:** I independently flagged and **rejected** this structural suggestion. I instructed the AI that I am strictly Engineer A, and generating or adapting code inside Engineer B's files would cause file duplication, redundancy, and merge conflicts.
* **How this helped my feature:** By rejecting the automated block, I successfully maintained strict branch separation (`feat/6-json-persistence`), ensuring that my work stayed entirely within my personal domain checklist while keeping our codebase clean for the upcoming peer code review.


# AI Learning Log

## Fellow: Engineer B (Okefu Enyitobi)

### Interaction #1 - Do my tests catch real bugs?

**Problem:** 31 tests passed, but that doesn't prove they would fail on a bug.

**My initial understanding:** "All tests pass" meant the code was correct.

**Prompt to AI:** I wrote 7 unittest tests for my build_report function and they all pass. How can I check that my tests would actually catch a bug? Give me an example of a small change I can make on purpose, and explain FAIL vs ERROR. I want to write the changes myself.

**Useful AI guidance:** Break one line on purpose, predict which test fails, run, restore. FAIL is a wrong assertion; ERROR is an unexpected exception.

**My independent experiment/test:**
1. `+= 1` to `+= 2`: `test_counts_by_status_and_priority` and `test_totals_match_sums` failed (`6 != 3`).
2. Edited `ALLOWED_TRANSITIONS`: `test_reopen_resolved` raised an ERROR.
3. `by_status = {}`: 2 failures and 4 errors (`Unknown status in ticket T1: open`).

Each line restored; 31 passing again.

**Verification source or result:** Unittest output compared with my predictions.

**Decision:** Improved. AI predicted 1 failure (2 happened) and 3 errors (4 happened). I trusted my output.

**Related file/commit:** `tests/test_reports.py`, `campusflow/reports.py`, <PR link>

**What I can now explain without AI:** Passing tests don't prove good tests, so I break the code on purpose. FAIL = wrong assertion; ERROR = unexpected crash.

---

### Interaction #2 - Matching the agreed field name

**Problem:** My `assign_ticket` and `change_status` had to fit the ticket shape from Engineer A's `create_ticket`.

**My initial understanding:** Any field name would work if I used it consistently.

**Prompt to AI:** Here is my workflow.py for the CampusFlow project (assign_ticket, change_status, get_work_queue). Please review it against the requirements and tell me what is wrong or missing. Don't rewrite it for me, because I want to fix it myself.

**Useful AI guidance:** I used `assignee`, but the design file says `assigned_to`, so my "unassigned can't start" check would read the wrong field.

**My independent experiment/test:** Replaced all three uses with `assigned_to`; my `make_ticket` helper and tests use it too. 23 tests passed.

**Verification source or result:** Checked against `docs/design-decisions.md` myself.

**Decision:** Accepted, after checking the design file.

**Related file/commit:** `campusflow/workflow.py`, `tests/test_workflow.py`, <PR link>

**What I can now explain without AI:** Modules from two people only fit if they share exact field names, and test helpers must follow the agreed shape.

---

### Interaction #3 - Dict vs set order

**Problem:** I wasn't sure the report order from `ALLOWED_TRANSITIONS` was guaranteed.

**My initial understanding:** I believed `ALLOWED_TRANSITIONS` had no guaranteed order.

**Prompt to AI:** In build_report I reuse ALLOWED_TRANSITIONS to get the list of statuses, but I think its order isn't guaranteed. Which is best to use: ALLOWED_TRANSITIONS, VALID_STATUSES, or something else, and why?

**Useful AI guidance:** Dicts keep insertion order (Python 3.7+); sets don't. `ALLOWED_TRANSITIONS` is a dict, `VALID_STATUSES` is a set.

**My independent experiment/test:** <python3 -c lines, prediction, what you saw>. Wrote `test_keys_are_in_workflow_order`; 31 tests passed.

**Verification source or result:** Test output.

**Decision:** Corrected my own misunderstanding; kept the dicts and added the test.

**Related file/commit:** `campusflow/reports.py`, `tests/test_reports.py`, <PR link>

**What I can now explain without AI:** Dicts keep order, sets don't, and `assertEqual` on dicts ignores order, so an order test compares lists of keys.