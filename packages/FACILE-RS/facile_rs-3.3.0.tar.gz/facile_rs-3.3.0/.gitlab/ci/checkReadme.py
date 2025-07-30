#!/usr/bin/env python
import os
import sys

if (
    (not os.path.exists("README.md"))
    and (not os.path.exists("README.txt"))
    and (not os.path.exists("README"))
):
    print(
        "Your repository does not contain a README file on the top level. Please consider adding one."
    )
    sys.exit(2)
else:
    print("README found.")
