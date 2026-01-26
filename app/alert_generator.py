"""
Generador de alertas basadas en el análisis de sentimientos
"""
from typing import List, Dict

class AlertGenerator:
    """
    Genera alertas automáticas basadas en patrones detectados
    """

    # Palabras que indican riesgo o preocupación severa
    HIGH_RISK_KEYWORDS = [
        "suicidio", "suicidar", "matarme", "morir", "muerte", "acabar",
        "terminar", "desaparecer", "no aguanto", "no puedo más",
        "insoportable", "desesperado", "sin salida"
    ]

    # Emociones negativas que justifican alerta
    NEGATIVE_EMOTIONS_THRESHOLD = ["Ansioso", "Estresado", "Triste", "Molesto"]

    def generate_alerts(
        self,
        text: str,
        sentiment: str,
        emotion: str,
        confidence: float
    ) -> List[Dict[str, str]]:
        """
        Genera alertas basadas en el contenido del texto

        Args:
            text: Texto analizado
            sentiment: Sentimiento general
            emotion: Emoción predominante
            confidence: Confianza del modelo

        Returns:
            Lista de alertas detectadas
        """
        alerts = []
        text_lower = text.lower()

        # Alerta de alto riesgo (palabras críticas)
        for keyword in self.HIGH_RISK_KEYWORDS:
            if keyword in text_lower:
                alerts.append({
                    "type": "critical",
                    "text": f"⚠️ ALERTA CRÍTICA: Se detectaron indicadores de riesgo. Se recomienda atención profesional inmediata."
                })
                break  # Solo una alerta crítica

        # Alerta por sentimiento negativo con alta confianza
        if sentiment == "negativo" and confidence > 0.75:
            alerts.append({
                "type": "warning",
                "text": f"Se detecta sentimiento negativo persistente (confianza: {confidence:.0%})"
            })

        # Alerta por emoción negativa específica
        if emotion in self.NEGATIVE_EMOTIONS_THRESHOLD and confidence > 0.6:
            if emotion == "Ansioso":
                alerts.append({
                    "type": "warning",
                    "text": "Se identifica ansiedad en el contenido. Considere técnicas de relajación."
                })
            elif emotion == "Estresado":
                alerts.append({
                    "type": "warning",
                    "text": "Se detectan signos de estrés. Priorice el autocuidado y descanso."
                })
            elif emotion == "Triste":
                alerts.append({
                    "type": "info",
                    "text": "Se percibe tristeza en la entrada. Es importante expresar las emociones."
                })

        return alerts

    def generate_pattern_alerts(
        self,
        emotions: Dict[str, int],
        total_entries: int
    ) -> List[Dict[str, str]]:
        """
        Genera alertas basadas en patrones de múltiples entradas

        Args:
            emotions: Distribución de emociones
            total_entries: Total de entradas analizadas

        Returns:
            Lista de alertas de patrones
        """
        alerts = []

        if total_entries == 0:
            return alerts

        # Alerta por alta frecuencia de ansiedad
        ansioso_count = emotions.get("Ansioso", 0)
        ansioso_percentage = (ansioso_count / total_entries) * 100

        if ansioso_percentage > 40:
            alerts.append({
                "type": "warning",
                "text": f"Alta frecuencia de ansiedad detectada ({ansioso_percentage:.0f}% de las entradas)"
            })

        # Alerta por alta frecuencia de estrés
        estresado_count = emotions.get("Estresado", 0)
        estresado_percentage = (estresado_count / total_entries) * 100

        if estresado_percentage > 30:
            alerts.append({
                "type": "warning",
                "text": f"Niveles elevados de estrés ({estresado_percentage:.0f}% de las entradas)"
            })

        # Alerta por alta frecuencia de tristeza
        triste_count = emotions.get("Triste", 0)
        triste_percentage = (triste_count / total_entries) * 100

        if triste_percentage > 35:
            alerts.append({
                "type": "info",
                "text": f"Patrón de tristeza frecuente ({triste_percentage:.0f}% de las entradas)"
            })

        return alerts
