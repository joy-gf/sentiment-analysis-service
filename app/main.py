"""
FastAPI application for sentiment analysis microservice
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import AnalysisRequest, SentimentResult, EnhancedSentimentResult, HealthResponse
from app.analyzer import get_analyzer
from app.emotion_detector import EmotionDetector
from app.keyword_extractor import KeywordExtractor
from app.alert_generator import AlertGenerator
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


@app.post("/analyze/enhanced", response_model=EnhancedSentimentResult)
async def analyze_sentiment_enhanced(request: AnalysisRequest):
    """
    Analyze sentiment with enhanced features: emotion detection, keywords, and alerts

    Args:
        request: AnalysisRequest with text to analyze

    Returns:
        EnhancedSentimentResult with sentiment, emotion, keywords and alerts
    """
    try:
        # Análisis de sentimiento base
        analyzer = get_analyzer()
        base_result = analyzer.analyze(request.text)

        # Detectar emoción predominante
        emotion_detector = EmotionDetector()
        emotion = emotion_detector.detect_emotion(
            request.text,
            base_result.sentimiento_general
        )

        # Extraer palabras clave
        keyword_extractor = KeywordExtractor()
        keywords = keyword_extractor.extract_keywords(request.text, top_n=8)

        # Generar alertas
        alert_generator = AlertGenerator()
        alerts = alert_generator.generate_alerts(
            request.text,
            base_result.sentimiento_general,
            emotion,
            base_result.confianza
        )

        logger.info(
            f"Enhanced analysis complete - "
            f"Sentiment: {base_result.sentimiento_general}, "
            f"Emotion: {emotion}, "
            f"Alerts: {len(alerts)}"
        )

        return EnhancedSentimentResult(
            sentimiento_general=base_result.sentimiento_general,
            score_positivo=base_result.score_positivo,
            score_negativo=base_result.score_negativo,
            score_neutral=base_result.score_neutral,
            confianza=base_result.confianza,
            modelo_usado=base_result.modelo_usado,
            emocion_predominante=emotion,
            palabras_clave=keywords,
            alertas=alerts
        )

    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
