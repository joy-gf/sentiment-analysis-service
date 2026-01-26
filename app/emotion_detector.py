"""
Detector de emociones específicas basado en palabras clave
"""
from typing import Dict, List

class EmotionDetector:
    """
    Detecta emociones específicas analizando palabras clave en el texto
    """

    # Mapeo de emociones a palabras clave (en español)
    EMOTION_KEYWORDS = {
        "Ansioso": [
            "ansioso", "ansiedad", "nervios", "nervioso", "preocupado", "preocupación",
            "inquieto", "intranquilo", "angustia", "temor", "miedo", "pánico"
        ],
        "Tranquilo": [
            "tranquilo", "calma", "paz", "relajado", "sereno", "sosiego",
            "plácido", "apacible", "quieto", "reposado"
        ],
        "Feliz": [
            "feliz", "alegre", "contento", "alegría", "satisfecho", "dichoso",
            "animado", "radiante", "gozoso", "jubiloso", "eufórico"
        ],
        "Estresado": [
            "estrés", "estresado", "agobiado", "presionado", "tensión", "tenso",
            "abrumado", "sobrepasado", "saturado", "exhausto"
        ],
        "Triste": [
            "triste", "tristeza", "deprimido", "melancólico", "desanimado",
            "apesadumbrado", "afligido", "apenado", "abatido", "decaído"
        ],
        "Molesto": [
            "molesto", "enojado", "irritado", "frustrado", "enfadado", "furioso",
            "rabioso", "indignado", "airado", "disgustado"
        ],
        "Motivado": [
            "motivado", "entusiasmado", "energizado", "inspirado", "decidido",
            "determinado", "impulsado", "animoso", "vigoroso"
        ],
        "Agradecido": [
            "agradecido", "gratitud", "afortunado", "bendecido", "reconocido",
            "grato", "satisfecho", "apreciativo"
        ],
    }

    def detect_emotion(self, text: str, sentiment: str) -> str:
        """
        Detecta la emoción predominante en el texto

        Args:
            text: Texto a analizar
            sentiment: Sentimiento general (positivo, negativo, neutral)

        Returns:
            Emoción predominante como string
        """
        text_lower = text.lower()

        # Contar coincidencias para cada emoción
        emotion_scores: Dict[str, int] = {}

        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score

        # Si hay coincidencias, retornar la emoción con más matches
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)

        # Fallback basado en sentimiento general
        fallback_map = {
            "positivo": "Feliz",
            "negativo": "Ansioso",
            "neutral": "Tranquilo"
        }

        return fallback_map.get(sentiment, "Tranquilo")

    def get_emotion_distribution(self, texts: List[str]) -> Dict[str, int]:
        """
        Obtiene la distribución de emociones en múltiples textos

        Args:
            texts: Lista de textos a analizar

        Returns:
            Diccionario con conteo de cada emoción
        """
        distribution: Dict[str, int] = {}

        for text in texts:
            # Detectar sin sentimiento previo ("neutral" como default)
            emotion = self.detect_emotion(text, "neutral")
            distribution[emotion] = distribution.get(emotion, 0) + 1

        return distribution
