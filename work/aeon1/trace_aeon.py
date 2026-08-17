"""Send a minimal local AEON validation trace without printing credentials."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langfuse import Langfuse

DESKTOP_ENV = Path(r"C:\Users\agenc\OneDrive\Desktop\AEON1\.env")
load_dotenv(DESKTOP_ENV, override=True)


def send_validation_trace() -> str:
    client = Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        base_url=os.environ.get("LANGFUSE_BASE_URL", "http://127.0.0.1:3001"),
    )
    with client.start_as_current_observation(
        name="aeon-1.0-validation",
        as_type="span",
        metadata={"source": "local-loop"},
        output={"status": "validated"},
    ) as trace:
        trace_id = trace.trace_id
    client.flush()
    return trace_id


if __name__ == "__main__":
    trace_id = send_validation_trace()
    print(f"Langfuse trace created: {trace_id}")
