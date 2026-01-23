"""
FastAPI application for sentiment analysis microservice
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import AnalysisRequest, SentimentResult, HealthResponse
from app.analyzer import get_analyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analysis Service",
    description="AI-powered sentiment analysis for emotional diary entries",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load ML model on startup"""
    logger.info("Starting sentiment analysis service...")
    try:
        get_analyzer()  # This will load the model
        logger.info("Service ready!")
    except Exception as e:
        logger.error(f"Failed to start service: {str(e)}")
        raise


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "service": "Sentiment Analysis API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        analyzer = get_analyzer()
        return HealthResponse(
            status="healthy",
            model_loaded=analyzer.pipeline is not None,
            model_name=analyzer.model_name
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@app.post("/analyze", response_model=SentimentResult)
async def analyze_sentiment(request: AnalysisRequest):
    """
    Analyze sentiment of provided text

    Args:
        request: AnalysisRequest with text to analyze

    Returns:
        SentimentResult with sentiment scores
    """
    try:
        analyzer = get_analyzer()
        result = analyzer.analyze(request.text)

        logger.info(f"Analysis complete - Sentiment: {result.sentimiento_general} (confidence: {result.confianza:.2f})")

        return result

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
