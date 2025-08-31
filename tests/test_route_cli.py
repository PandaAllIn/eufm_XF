import json
import subprocess
import sys
from pathlib import Path


def test_route_cli_outputs_json():
    result = subprocess.run(
        [sys.executable, "-m", "scripts.route", "research EU projects"],
        capture_output=True,
        text=True,
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    data = json.loads(lines[-1])
    assert data["chosen_agent"] == "research"
    for field in ["run_id", "prompt_hash", "reason", "ts"]:
        assert field in data
