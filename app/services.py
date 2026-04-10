import subprocess
from fastapi import HTTPException

def run_command(cmd: list[str], timeout: int = 5) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="cmd timeout")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Cmd failed: {exc}")  