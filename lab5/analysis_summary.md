\# Lab 5: Static Code Analysis — Issue and Fix Summary



\## 1. Issues and Fixes



| Tool | Issue identified | Fix applied |

|---|---|---|

| Pylint | Missing function docstring and unused import | Added docstrings and removed unused imports |

| Pylint | Function naming convention violation | Renamed `bookRoom` to `book\_room` |

| Bandit | Unsafe use of `eval()` | Replaced with restricted arithmetic-expression evaluation |

| Bandit | Weak MD5 hashing | Replaced with SHA-256 |

| Bandit | Insecure random booking reference | Used the `secrets` module |

| Bandit | Shell command execution using `os.system()` | Removed shell execution |

| Bandit | Hardcoded secret | Read the secret from an environment variable |

| Flake8 | Unused imports and variables | Removed unused code |

| Flake8 | Exception handling, comparison, and formatting problems | Corrected exception handling, used `is None`, and fixed formatting |



\## 2. Final Results



\- \*\*Pylint:\*\* 10.00/10

\- \*\*Bandit:\*\* No issues identified

\- \*\*Flake8:\*\* No reported violations



\## 3. Reflection



\*\*Why is static code analysis useful?\*\*



Static code analysis helps identify code quality, style, and potential security problems without executing the program.



\*\*What did Bandit help identify?\*\*



Bandit identified potentially unsafe practices such as unsafe expression evaluation, weak hashing, insecure randomness, shell command execution, and a hardcoded secret.



\*\*Why should the tools be run again after fixes?\*\*



Rerunning the tools verifies whether the reported problems have been addressed and whether any issues remain.



\*\*What did this lab teach me?\*\*



This lab demonstrated how automated tools can improve Python code quality, consistency, and security.

