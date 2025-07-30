import os
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from cneura_ai.shell import ShellSessionManager
from cneura_ai.logger import logger
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/shell", tags=["Shell"])


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


async def get_shell_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> ShellSessionManager:
    await db_hub.load_config()
    remote_url = db_hub.config.get("REMOTE_URL")
    mongo_uri = db_hub.config.get("MONGO_URI")

    if not remote_url or not mongo_uri:
        raise HTTPException(status_code=500, detail="REMOTE_URL or MONGO_URI missing in DB config")

    return ShellSessionManager(remote_url=remote_url, mongo_uri=mongo_uri)


@router.post("/session/create")
def create_session(
    request: SessionRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        manager.get_session(request.agent_id)
        return {"message": f"Session created or resumed for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/stop")
def stop_session(
    request: SessionRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        manager.stop_session(request.agent_id)
        return {"message": f"Session stopped for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error stopping session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/command/run")
def run_command(
    request: CommandRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        result = manager.run_command(request.agent_id, request.command)
        return result
    except Exception as e:
        logger.error(f"Error running command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file/get")
def get_file(
    request: FileRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        session = manager.get_session(request.agent_id)
        file_data = session.get_file(request.path)
        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found in container")
        return {"content": file_data.decode("utf-8")}
    except Exception as e:
        logger.error(f"Error getting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/folder/get")
def get_folder(
    request: FolderRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        session = manager.get_session(request.agent_id)
        result = session.get_folder(request.container_path, request.local_path)
        if not os.path.exists(request.local_path):
            raise HTTPException(status_code=500, detail="Folder not downloaded correctly")
        return {"message": result}
    except Exception as e:
        logger.error(f"Error getting folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/folder/download")
def download_folder(local_path: str = Query(..., description="Path to the folder or file to download")):
    if not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(local_path, filename=os.path.basename(local_path), media_type='application/octet-stream')
