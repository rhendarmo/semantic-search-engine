from pydantic import BaseModel, Field

class QARequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question to answer")
    query: str = Field(..., min_length=1, description="Search query used to retrieve evidence")
    top_k: int = Field(10, ge=1, le=20, description="Number of retrieved docs to ground the answer")
    model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", description="Embedding model")
    llm_model: str = Field("gpt-5.2", description="LLM model name (OpenAI Responses API)")
