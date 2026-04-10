from fastapi import FastAPI, HTTPException, Query

from app.config import ALLOWED_LIST
from app.schemas import ServiceRequest, ServiceRequestLogs, CommandResponse
from app.services import run_command

app = FastAPI()

#POST

@app.post("/service/status", response_model=CommandResponse)
def service_status_post(data: ServiceRequest):

    if data.service_name not in ALLOWED_LIST:
        raise HTTPException(status_code=403, detail="service not allowed!")

    result = run_command(["systemctl", "is-active", data.service_name])
    
    return CommandResponse(
        service_name=data.service_name,
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
        returncode=result.returncode
    )

@app.post("/service_logs", response_model=CommandResponse)
def service_logs_post(data: ServiceRequestLogs):
    
    if data.service_name not in ALLOWED_LIST:
        raise HTTPException(status_code=403, detail="service not allowed!")

    result = run_command(["journalctl", "-u", data.service_name, "-n", str(data.lines), "--no-pager"], timeout=10)

    return CommandResponse(
       service_name=data.service_name,
       stdout=result.stdout.strip(),
       stderr=result.stderr.strip(),
       returncode=result.returncode
       )

#GET

@app.get("/")
def root():
    return {
        "message": "root path"
    }

@app.get("/service_status/{service_name}")
def service_status(service_name: str):

    if service_name not in ALLOWED_LIST:
        raise HTTPException(status_code=403, detail = "service is not in allow list")

    result = run_command(["systemctl", "is-active", service_name]) 
    return {
        "message": service_name,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }


@app.get("/service_status/{service_name}/logs")
def service_logs(service_name: str, lines: int = Query(20, ge = 1, le = 200)):

    if service_name not in ALLOWED_LIST:
        raise HTTPException(status_code=403, detail = "service is not in allow list")

    result = run_command(["journalctl", "-u", service_name, "-n", str(lines), "--no-pager"]) 
    return {
        "message": service_name,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }

@app.get("/run_cmd/{cmd}")
def run_cmd(cmd: str):

    result = run_command([cmd]) 
    return {
        "message": cmd,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }
