import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from cneura_ai.research import Research
from cneura_ai.llm import GeminiLLM
from cneura_ai.memory import MemoryManager
from cneura_ai.logger import logger

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
KNOWLEDGE_BASE_MEMORY_NAMESPACE = os.getenv("KNOWLEDGE_BASE_MEMORY_NAMESPACE", "knowledge")

if not BRAVE_API_KEY:
    raise RuntimeError("BRAVE_API_KEY must be set.")


app = FastAPI(title="Web Research API", version="1.0")
research_instance = Research(api_key=BRAVE_API_KEY)

class SearchRequest(BaseModel):
    agent_id: str
    query: str
    num_results: int = Field(default=1, ge=1, le=10)

class SearchResponse(BaseModel):
    task_id: str
    message: str = "Search started. Check result later using the task ID."

@app.post("/search")
async def search(request: SearchRequest):
    try:
        contents = research_instance.search_with_content(
            query=request.query,
            count=request.num_results
        )

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        summaries = []

        for content in contents:
            summarize_prompt = ("system", f"""
                You are a professional data analyst specializing in extracting key information and generating detailed, structured descriptions from web-scraped content.
                
                Given the user's query and the scraped content, your task is to produce a comprehensive, informative explanation that:
                - Directly addresses the user's intent.
                - Highlights all important points, facts, and insights.
                - Preserves the depth, structure, and nuance of the original content.
                - Avoids generalizations and includes specific, meaningful details.

                🔍 User Query: {request.query}

                Scrape result:
                🔗 Title: {content.get("title")}
                📝 Description: {content.get("description")}
                📄 Content: {content.get("content").strip()}
            """)
            response = llm.query(summarize_prompt)

            if response.get("success", False):
                summaries.append(response.get("data"))
                logger.info("Content summarized")
            else:
                logger.error("Summarization failed: %s", response)

        merge_prompt = ("system", f"""
            You are a professional data analyst and content synthesizer.
            Your task is to merge the following detailed descriptions into a single, cohesive, and comprehensive explanation.

            Requirements:
            - Preserve all important facts, insights, and nuances from each description.
            - Eliminate redundancy while retaining clarity and depth.
            - Ensure the merged result is well-structured and logically coherent.
            - Do not simplify the content — maintain detailed and informative tone throughout.

            Detailed Descriptions:
            {summaries}
        """)

        response = llm.query(merge_prompt)

        if response.get("success", False):
            logger.info("Content merged")
            memory_manager = MemoryManager(host=CHROMA_HOST, port=CHROMA_PORT, llm=llm)
            await memory_manager.store_to_knowledge_base(request.agent_id, str(uuid.uuid4()), response.get("data"))
            logger.info("Merged content added to Knowledge base")

            return JSONResponse(content={
                "status": "completed",
                "results": response.get("data")
            })
        else:
            logger.error("Merging failed: %s", response)
            return JSONResponse(content={
                "status": "failed",
                "error": "Merging LLM failed."
            }, status_code=500)

    except Exception as e:
        logger.exception("Exception during on-air search")
        return JSONResponse(content={
            "status": "failed",
            "error": str(e)
        }, status_code=500)


@app.get("/health")
async def health():
    try:
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Redis unavailable")

