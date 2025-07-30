from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
from cneura_ai.shell import ShellSessionManager 
from cneura_ai.logger import logger
from dotenv import load_dotenv

load_dotenv()

REMOTE_URL = os.getenv("REMOTE_URL") 
MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
manager = ShellSessionManager(remote_url=REMOTE_URL, mongo_uri=MONGO_URI)


class CommandRequest(BaseModel):
    agent_id: str
    command: List[str]


class SessionRequest(BaseModel):
    agent_id: str


class FileRequest(BaseModel):
    agent_id: str
    path: str


class FolderRequest(BaseModel):
    agent_id: str
    container_path: str
    local_path: str


@app.post("/session/create")
def create_session(request: SessionRequest):
    try:
        session = manager.get_session(request.agent_id)
        return {"message": f"Session created or resumed for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error in {request}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/session/stop")
def stop_session(request: SessionRequest):
    try:
        manager.stop_session(request.agent_id)
        return {"message": f"Session stopped for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error in {request}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/command/run")
def run_command(request: CommandRequest):
    try:
        result = manager.run_command(request.agent_id, request.command)
        return result
    except Exception as e:
        logger.error(f"Error in {request}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/file/get")
def get_file(request: FileRequest):
    try:
        session = manager.get_session(request.agent_id)
        file_data = session.get_file(request.path)
        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found in container")
        return {"content": file_data.decode("utf-8")}
    except Exception as e:
        logger.error(f"Error in {request}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/folder/get")
def get_folder(request: FolderRequest):
    try:
        session = manager.get_session(request.agent_id)
        result = session.get_folder(request.container_path, request.local_path)
        if not os.path.exists(request.local_path):
            raise HTTPException(status_code=500, detail="Folder not downloaded correctly")
        return {"message": result}
    except Exception as e:
        logger.error(f"Error in {request}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/folder/download")
def download_folder(local_path: str):
    if not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(local_path, filename=os.path.basename(local_path), media_type='application/octet-stream')
