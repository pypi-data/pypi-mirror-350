import os
import docker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cneura_ai.tool_registry import ToolRegistry
from cneura_ai.memory import AbilitiesMemory
from bson.errors import InvalidId
from dotenv import load_dotenv

load_dotenv()

REMOTE_URL = os.getenv("REMOTE_URL")
MONGO_URI = os.getenv("MONGO_URI")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
TOOL_MEMORY_NAMESPACE = os.getenv("TOOL_MEMORY_NAMESPACE", "tool")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()
docker_client = docker.DockerClient(base_url=REMOTE_URL)

abilities_memory = AbilitiesMemory(host=CHROMA_HOST, port=CHROMA_PORT, namespace=TOOL_MEMORY_NAMESPACE)
registry = ToolRegistry(mongo_uri=MONGO_URI, memory=abilities_memory)


class QueryModel(BaseModel):
    query: str
    top_k: int = 3



@app.get("/tools")
def list_tools():
    return registry.list_tools()

@app.get("/tools/{container_name}")
def get_tool(container_name: str):
    tool = registry.get_tool(container_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@app.get("/tools/id/{tool_id}")
def get_tool_by_id(tool_id: str):
    try:
        tool = registry.get_tool_by_id(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return tool
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid tool ID format")

@app.post("/tools/query")
async def query_tools(query_model: QueryModel):
    try:
        results = await registry.find_similar_tools(query_model.query, top_k=query_model.top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop/{container_name}")
def stop_container(container_name: str):
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
        return {"message": f"{container_name} stopped"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")

@app.post("/remove/{container_name}")
def remove_container(container_name: str):
    try:
        container = docker_client.containers.get(container_name)
        container.remove(force=True)
        registry.remove_tool(container_name)
        return {"message": f"{container_name} removed"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")
