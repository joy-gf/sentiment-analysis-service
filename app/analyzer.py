"""
Sentiment analysis logic.
- Default: loads the model locally via transformers (used in local dev and on HF Spaces deploy).
- Optional: if HF_API_TOKEN is set, calls the HuggingFace Inference Providers router.
  Note: pysentimiento/robertuito-sentiment-analysis is not currently served by any provider,
  so the API path only works if MODEL_NAME is switched to a provider-supported model.
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
        self._api_url = f"https://router.huggingface.co/hf-inference/models/{self.model_name}"
        self._headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        self.pipeline = True  # flag for health check
        logger.info(f"Analyzer ready (HuggingFace API): {self.model_name}")

    def _load_local_model(self):
        try:
            from pysentimiento import create_analyzer
            logger.info(f"Loading pysentimiento analyzer: {self.model_name}")
            self.pipeline = create_analyzer(task="sentiment", lang="es")
            logger.info("pysentimiento analyzer loaded successfully")
        except ImportError:
            raise RuntimeError(
                "pysentimiento not installed. "
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
        result = self.pipeline.predict(text)
        items = [{"label": k, "score": v} for k, v in result.probas.items()]
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
