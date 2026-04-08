"""Write initial admin credentials to a restricted file instead of logs.

Logging secrets to stdout/stderr is a well-known CodeQL finding
(py/clear-text-logging-sensitive-data) — in production those logs
get collected into ELK/Splunk/etc and become a secret sprawl
source. This helper writes the credential to a 0600 file that only
the process user can read, and returns the path so the caller can
log **the path** (not the password) for the operator to pick up.
"""

from __future__ import annotations

import os
from pathlib import Path

_CREDENTIAL_FILE = Path(".deer-flow") / "admin_initial_credentials.txt"


def write_initial_credentials(email: str, password: str, *, label: str = "initial") -> Path:
    """Write the admin email + password to ``.deer-flow/admin_initial_credentials.txt``.

    Creates the parent directory if it does not exist. Sets the file
    mode to 0600 so only the owning process user can read it.

    ``label`` distinguishes "initial" (fresh creation) from "reset"
    (password reset) in the file header, so an operator picking up
    the file after a restart can tell which event produced it.

    Returns the absolute :class:`Path` to the file.
    """
    _CREDENTIAL_FILE.parent.mkdir(parents=True, exist_ok=True)

    content = (
        f"# DeerFlow admin {label} credentials\n# This file is generated on first boot or password reset.\n# Change the password after login via Settings -> Account,\n# then delete this file.\n#\nemail: {email}\npassword: {password}\n"
    )
    _CREDENTIAL_FILE.write_text(content)
    os.chmod(_CREDENTIAL_FILE, 0o600)
    return _CREDENTIAL_FILE.resolve()
