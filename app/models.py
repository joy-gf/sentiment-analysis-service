"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional


class AnalysisRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str = Field(..., min_length=1, description="Text to analyze")
    diario_id: Optional[str] = Field(None, description="Associated diary entry ID")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hoy me siento muy feliz porque logré terminar mi proyecto",
                "diario_id": "uuid-123"
            }
        }


class SentimentResult(BaseModel):
    """Response model for sentiment analysis results"""
    sentimiento_general: str = Field(..., description="Overall sentiment: positivo, negativo, neutral")
    score_positivo: float = Field(..., ge=0, le=1, description="Positive sentiment score (0-1)")
    score_negativo: float = Field(..., ge=0, le=1, description="Negative sentiment score (0-1)")
    score_neutral: float = Field(..., ge=0, le=1, description="Neutral sentiment score (0-1)")
    confianza: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    modelo_usado: str = Field(..., description="Model used for analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "sentimiento_general": "positivo",
                "score_positivo": 0.85,
                "score_negativo": 0.10,
                "score_neutral": 0.05,
                "confianza": 0.85,
                "modelo_usado": "pysentimiento/robertuito-sentiment-analysis"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_name: str
