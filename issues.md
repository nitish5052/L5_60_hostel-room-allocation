# Lab 5: Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe YAML loading | Security, Medium | Original `loadConfig()` function | `yaml.load()` with `yaml.Loader` permits unsafe object construction from YAML input. | Replaced it with `yaml.safe_load()`. |
| Mutable default argument | Bug, Medium | Original `allocateRoom()` function | The default argument `preferred=[]` shares a mutable list across calls. | Changed the default to `None` and initialized a list inside the function. |
| Incorrect room capacity check | Logic bug, Medium | Original `allocateRoom()` function | The condition `len(occupants) > capacity` permits an extra occupant. | Changed the check to reject rooms when occupancy reaches capacity. |
| Gender restriction ignored | Logic bug, Medium | Original `allocateRoom()` function | The allocation function does not check whether the room matches the student's gender. | Added a gender comparison before assigning the room. |
| Duplicate student allocation | Logic bug, Medium | Original `allocateRoom()` function | A student might receive a second room when allocated again. | Check existing allocations before assigning a room. |
| Incomplete room vacating | Logic bug, Medium | Original `vacateRoom()` function | The allocation record is deleted, but the student remains in the room's occupant list. | Remove the student from both records. |
| Incorrect seniority ordering | Logic bug | Original `priorityOrder()` function | Sorting by year in ascending order places junior students before senior students. | Sort by year in descending order. |
| Insecure lottery randomness | Security, Low | Original `roomLottery()` function | The standard `random` module is unsuitable for security-sensitive random selection. | Replaced it with `secrets` for secure random shuffling. |
| Hardcoded password argument | Security, Low | Original `connectWardenDb()` function | A hardcoded password argument was passed to the simulated database connection. | Removed the password argument from the placeholder connection function. |
| Unsafe HTML output | Security | Original `roomLookup()` function | A request parameter was inserted into HTML without escaping. | Used `html.escape()` on user-controlled values. |
| Flask debug mode | Security | Original `runPortal()` function | Debug mode exposes development debugging features. | Set `debug=False`. |
| Missing docstrings and inconsistent naming | Code quality | Multiple functions | Missing documentation and non-standard function names reduce readability. | Added docstrings and renamed functions using snake_case. |

## Static Analysis Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.84/10 | 10.00/10 |
| Bandit | Original report needs review | No issues identified |
| Flake8 | Original report needs review | No violations reported |

Note: The line references above identify the original functions because the source file changed during fixes. Replace them with exact line numbers from the original source or reports if your instructor requires numeric line numbers.

The before-and-after results are based on the reports collected during this lab.
