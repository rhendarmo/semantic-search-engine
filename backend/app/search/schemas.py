from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User search query")
    top_k: int = Field(10, ge=1, le=50, description="Number of results to return")
    model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", description="Embedding model name")
