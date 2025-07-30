import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.errors import InvalidId
from dotenv import load_dotenv
from cneura_ai.agent_registry import AgentRegistry
from cneura_ai.memory import AgentsMemory
from cneura_ai.agent_deploy import AgentDeployer

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
AGENT_MEMORY_NAMESPACE = os.getenv("AGENT_MEMORY_NAMESPACE", "agent")
DEPLOY_OUTPUT_DIR = "./output"

app = FastAPI()


agents_memory = AgentsMemory(host=CHROMA_HOST, port=CHROMA_PORT, namespace=AGENT_MEMORY_NAMESPACE)
registry = AgentRegistry(mongo_uri=MONGO_URI, memory=agents_memory)
deployer = AgentDeployer(agent_registry=registry)

# Request Models
class AgentInfoModel(BaseModel):
    agent: dict
    env: dict

class QueryModel(BaseModel):
    query: str
    top_k: int = 3

# Endpoints

@app.get("/agents")
def list_agents():
    return registry.list_agents()

@app.get("/agents/{agent_name}")
def get_agent(agent_name: str):
    agent = registry.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.get("/agents/id/{agent_id}")
def get_agent_by_id(agent_id: str):
    try:
        agent = registry.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid agent ID format")



@app.post("/agents/query")
async def query_agents(query_model: QueryModel):
    try:
        results = await registry.find_similar_agents(query_model.query, top_k=query_model.top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/agents/{agent_name}")
def remove_agent(agent_name: str):
    try:
        registry.remove_agent(agent_name)
        return {"message": f"{agent_name} removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/create")
async def create_agent(context: AgentInfoModel):
    try:
        agent_id = str(uuid.uuid4())
        output_dir = os.path.join(DEPLOY_OUTPUT_DIR, agent_id)

        
        image_tag = f"{context.agent_name.lower()}:{agent_id[:8]}"
        container_name = f"{context.agent_name.lower()}-container-{agent_id[:6]}"

        container, deployed_agent_id = deployer.deploy(  
            output_path=output_dir,        
            image_tag=image_tag,
            container_name=container_name,
            context=context,  
        )

        return {
            "message": "Agent created and deployed successfully.",
            "agent_id": deployed_agent_id,
            "container_id": container.id,
            "image_tag": image_tag
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))