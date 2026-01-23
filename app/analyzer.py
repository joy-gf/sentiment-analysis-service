"""
Sentiment analysis logic using Hugging Face Transformers
"""
from transformers import pipeline
from app.config import settings
from app.models import SentimentResult
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment analyzer using pysentimiento/robertuito model
    Specialized for Spanish text sentiment analysis
    """

    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.device = 0 if settings.DEVICE == "cuda" else -1
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        """Load the sentiment analysis model"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=self.device
            )
            logger.info(f"Model loaded successfully on device: {settings.DEVICE}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def analyze(self, text: str) -> SentimentResult:
        """
        Analyze sentiment of given text

        Args:
            text: Spanish text to analyze

        Returns:
            SentimentResult with sentiment scores
        """
        if not self.pipeline:
            raise RuntimeError("Model not loaded")

        try:
            # Get prediction from model
            result = self.pipeline(text)[0]

            # pysentimiento returns labels: POS, NEG, NEU
            label = result["label"]
            confidence = result["score"]

            # Initialize scores
            scores = {
                "POS": 0.0,
                "NEG": 0.0,
                "NEU": 0.0
            }

            # Assign confidence to corresponding label
            scores[label] = confidence

            # Map to Spanish sentiment names
            sentiment_map = {
                "POS": "positivo",
                "NEG": "negativo",
                "NEU": "neutral"
            }

            return SentimentResult(
                sentimiento_general=sentiment_map[label],
                score_positivo=scores["POS"],
                score_negativo=scores["NEG"],
                score_neutral=scores["NEU"],
                confianza=confidence,
                modelo_usado=self.model_name
            )

        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise


# Global analyzer instance (loaded once at startup)
analyzer = None


def get_analyzer() -> SentimentAnalyzer:
    """Get or create the global analyzer instance"""
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()
    return analyzer
