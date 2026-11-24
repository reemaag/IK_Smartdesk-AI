from fastapi import (
    FastAPI
)

from app.models.schemas import (
    ChatRequest,
    ChatResponse
)

from app.agents.graph import (
    agent_graph
)


app = FastAPI(
    title="SmartDesk AI",
    version="1.0.0"
)


@app.get("/")
def health():

    return {
        "status": "running"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    response = (
        agent_graph.process_query(
            session_id=
            request.session_id,

            query=
            request.query
        )
    )

    return ChatResponse(
        response=response
    )