# Lab 5: Static Code Analysis Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security weaknesses, poor coding practices, and style violations. In this lab, static analysis helped identify issues in the hostel room allocation system before submitting the final code.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified code quality issues, including missing docstrings, inconsistent function names, unused imports, and a mutable default argument. Bandit identified security concerns related to YAML loading, random number generation, and a hardcoded password argument. Flake8 checked Python formatting and style rules.

## 3. What changes did you make to improve the program?

I replaced unsafe YAML loading with `yaml.safe_load()`, corrected the room capacity check, prevented duplicate allocations, and fixed the room vacating logic. I also added gender checks, corrected seniority ordering, escaped HTML output, disabled Flask debug mode, and replaced the standard random generator with `secrets` for the lottery.

## 4. What did you learn from this lab?

I learned that a program might run successfully while still containing logic bugs and security risks. Static analysis tools help identify different categories of problems. After making changes, I reran the tools and obtained a Pylint score of 10.00/10, no Bandit findings, and an empty Flake8 report. I also learned to verify program behavior because static analysis does not detect every functional bug.
