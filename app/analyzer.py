"""
Sentiment analysis logic.
- If HF_API_TOKEN is set: uses HuggingFace Inference API (lightweight, for cloud demo).
- If HF_API_TOKEN is not set: loads model locally via transformers (for local development).
"""
import logging
from app.config import settings
from app.models import SentimentResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:

    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.pipeline = None
        self._use_api = bool(settings.HF_API_TOKEN)

        if self._use_api:
            self._setup_api()
        else:
            self._load_local_model()

    def _setup_api(self):
        import requests as _requests
        self._requests = _requests
        self._api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self._headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        self.pipeline = True  # flag for health check
        logger.info(f"Analyzer ready (HuggingFace API): {self.model_name}")

    def _load_local_model(self):
        try:
            from transformers import pipeline as hf_pipeline
            logger.info(f"Loading local model: {self.model_name}")
            self.pipeline = hf_pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=-1,
            )
            logger.info("Local model loaded successfully")
        except ImportError:
            raise RuntimeError(
                "transformers/torch not installed. "
                "Run: pip install -r requirements-local.txt"
            )

    def analyze(self, text: str) -> SentimentResult:
        if self._use_api:
            return self._analyze_api(text)
        return self._analyze_local(text)

    def _analyze_api(self, text: str) -> SentimentResult:
        payload = {"inputs": text, "options": {"wait_for_model": True}}

        try:
            response = self._requests.post(
                self._api_url,
                headers=self._headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
        except self._requests.exceptions.Timeout:
            raise RuntimeError("HuggingFace API timeout — model may be loading, retry in a moment")
        except self._requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HuggingFace API error: {e.response.status_code} {e.response.text}")

        data = response.json()
        items = data[0] if isinstance(data[0], list) else data
        return self._build_result(items)

    def _analyze_local(self, text: str) -> SentimentResult:
        if not self.pipeline:
            raise RuntimeError("Local model not loaded")
        result = self.pipeline(text)[0]
        label = result["label"]
        confidence = result["score"]
        scores = {"POS": 0.0, "NEG": 0.0, "NEU": 0.0}
        scores[label] = confidence
        items = [{"label": k, "score": v} for k, v in scores.items()]
        return self._build_result(items)

    def _build_result(self, items: list) -> SentimentResult:
        scores = {"POS": 0.0, "NEG": 0.0, "NEU": 0.0}
        for item in items:
            label = item["label"]
            if label in scores:
                scores[label] = item["score"]

        dominant = max(scores, key=scores.get)
        confidence = scores[dominant]
        sentiment_map = {"POS": "positivo", "NEG": "negativo", "NEU": "neutral"}

        logger.info(f"Analysis complete — {sentiment_map[dominant]} ({confidence:.2f})")

        return SentimentResult(
            sentimiento_general=sentiment_map[dominant],
            score_positivo=scores["POS"],
            score_negativo=scores["NEG"],
            score_neutral=scores["NEU"],
            confianza=confidence,
            modelo_usado=self.model_name,
        )


# Global singleton
analyzer = None


def get_analyzer() -> SentimentAnalyzer:
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()
    return analyzer
