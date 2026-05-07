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
            # Ansiedad
            "ansioso", "ansiosa", "ansiedad", "ansié", "me angustié",
            # Angustia
            "angustiado", "angustiada", "angustia", "angustié", "angustiarme",
            # Nervios
            "nervioso", "nerviosa", "nerviosismo", "nervios", "nerviosidad",
            "estoy nervioso", "me puse nervioso", "me pongo nervioso",
            # Preocupación
            "preocupado", "preocupada", "preocupación", "preocupaciones",
            "preocupé", "me preocupé", "preocuparme", "preocupante",
            "me preocupa", "me tiene preocupado",
            # Inquietud
            "inquieto", "inquieta", "inquietud", "inquieté",
            # Intranquilidad
            "intranquilo", "intranquila", "intranquilidad",
            # Miedo / susto
            "miedo", "miedoso", "miedosa", "le tengo miedo", "tengo miedo",
            "asustado", "asustada", "susto", "asusté", "me asusté",
            "me asusta", "me aterra", "aterrado", "aterrada",
            # Temor
            "temor", "temeroso", "temerosa", "temo", "temía",
            # Pánico / terror
            "pánico", "ataque de pánico", "crisis de ansiedad",
            "terror", "pavor", "pavor", "aterrorizado",
            # Síntomas físicos de ansiedad
            "taquicardia", "palpitaciones", "me tiemblan", "temblor", "temblando",
            "me falta el aire", "no puedo respirar", "opresión en el pecho",
            "el pecho apretado", "pecho cerrado", "me oprime el pecho",
            "sudor frío", "manos sudadas", "me sudan las manos",
            # Rumiación / pensamientos en loop
            "vueltas en la cabeza", "no puedo parar de pensar",
            "dando vueltas", "mente no para", "no para de dar vueltas",
            "no puedo dejar de pensar",
            # Incertidumbre
            "incertidumbre", "incerteza", "no sé qué va a pasar",
            "no sé qué hacer", "no sé cómo",
            # Timidez / dificultad social (relevante para diarios)
            "shock", "en shock", "quedé en shock",
            "complicado abrirme", "difícil abrirme", "no puedo abrirme",
            "me cuesta abrirme", "me cuesta relacionarme",
            "no sé cómo actuar", "no fluidez",
        ],
        "Tranquilo": [
            # Tranquilidad
            "tranquilo", "tranquila", "tranquilidad", "tranquilizó", "tranquilicé",
            "me tranquilicé", "me tranquilizó", "tranquilizarme", "tranquilizarse",
            # Calma
            "calma", "calmado", "calmada", "calmé", "me calmé",
            "me calmó", "calmarme", "calmarse",
            # Paz
            "en paz", "paz interior", "me siento en paz",
            "serenidad", "sereno", "serena", "me sentí sereno",
            # Relajación
            "relajado", "relajada", "relajé", "me relajé",
            "relajación", "relajarme", "relajante", "me relajó",
            # Sosiego / alivio
            "sosiego", "sosegado", "sosegada", "plácido", "apacible",
            "aliviado", "aliviada", "alivio", "alivié", "me alivié",
            "me dio alivio", "qué alivio",
            # Descanso
            "descansé", "descansado", "descansada", "descanso",
            "dormí bien", "descansé bien", "pude descansar",
            # Respiración / liberación
            "respiré", "pude respirar", "respiré profundo",
            "suspiré", "suspiro de alivio", "soltó tension",
            "liberado", "liberada", "me liberé", "me solté",
            # Quietud
            "quieto", "quieta", "reposado", "reposada",
        ],
        "Feliz": [
            # Felicidad base
            "feliz", "felicidad", "fui feliz", "me sentí feliz",
            "me hizo feliz", "qué felicidad",
            # Alegría
            "alegre", "alegría", "me alegré", "me alegró", "qué alegría",
            "alegrías", "me llené de alegría",
            # Contento / satisfecho
            "contento", "contenta", "contentó", "muy contento",
            "satisfecho", "satisfecha", "satisfacción", "me sentí satisfecho",
            # Disfrute
            "disfruté", "disfrutar", "lo disfruté", "pude disfrutar",
            "divertido", "divertida", "diversión", "me divertí",
            "lo pasé bien", "lo pasamos bien",
            # Emoción positiva
            "emocionado", "emocionada", "emoción", "me emocioné",
            "ilusionado", "ilusionada", "ilusión", "qué ilusión",
            # Risa / sonrisa
            "reí", "nos reímos", "risas", "me reí",
            "sonreí", "sonrisa", "me sacó una sonrisa",
            # Logro / orgullo
            "orgulloso", "orgullosa", "orgullo", "me siento orgulloso",
            "logré", "lo logré", "pude lograrlo", "alcancé",
            "me salió bien", "resultó bien", "salió perfecto",
            # Otros
            "dichoso", "dichosa", "radiante", "gozoso", "jubiloso",
            "eufórico", "eufórica", "excelente día", "qué buen día",
            "genial", "maravilloso", "maravillosa", "fantástico",
        ],
        "Estresado": [
            # Estrés base
            "estrés", "estresado", "estresada", "estresé", "me estresé",
            "muy estresado", "demasiado estrés",
            # Agobio
            "agobiado", "agobiada", "agobio", "agobié", "me agobié",
            "me agobia", "qué agobio",
            # Presión
            "presionado", "presionada", "presión", "bajo presión",
            "me siento presionado", "demasiada presión",
            # Tensión
            "tenso", "tensa", "tensión", "muy tenso",
            # Abrumado
            "abrumado", "abrumada", "me siento abrumado", "me abrumó",
            "sobrepasado", "sobrepasada", "me sobrepasó",
            "desbordado", "desbordada", "me desbordé",
            # Saturado / agotado
            "saturado", "saturada", "saturación",
            "exhausto", "exhausta", "agotado", "agotada",
            "agotamiento", "cansancio extremo",
            # No dar más
            "no doy más", "no puedo más", "llegué al límite",
            "estoy al límite", "al borde del colapso",
            "colapso", "colapsé", "me colapsé",
            # Quemado / desgaste
            "quemado", "quemada", "burnout", "desgastado", "desgastada",
            "desgaste", "sin fuerzas", "sin energía", "me falta energía",
            # Acumulación de cosas
            "tantas cosas", "demasiadas cosas", "muchas cosas pendientes",
            "todo junto", "todo al mismo tiempo",
        ],
        "Triste": [
            # Tristeza base
            "triste", "tristeza", "me sentí triste", "muy triste",
            "qué tristeza", "me puse triste", "me puso triste",
            # Depresión / decaimiento
            "deprimido", "deprimida", "depresión", "caído", "caída",
            "decaído", "decaída", "decaimiento",
            # Melancolía
            "melancólico", "melancólica", "melancolía",
            "nostálgico", "nostálgica", "nostalgia", "extraño",
            # Desánimo
            "desanimado", "desanimada", "desánimo", "sin ánimo",
            "sin ganas", "no tengo ganas", "no me dan ganas",
            "desganas", "desmotivado", "desmotivación",
            # Llanto
            "lloré", "llorando", "llanto", "lloro", "llorosa",
            "quiero llorar", "ganas de llorar", "me dieron ganas de llorar",
            "se me escaparon las lágrimas", "lágrimas",
            # Dolor emocional
            "dolor", "sufrimiento", "sufrí", "pena", "me da pena",
            "me duele", "duele mucho",
            # Vacío
            "vacío", "vacía", "vacío interior", "me siento vacío",
            "hueco", "huecos",
            # Pérdida / abandono
            "pérdida", "perdí", "perder", "abandono", "abandonado",
            "abandonada", "desolado", "desolada", "desolación",
            # Decepción
            "decepción", "decepcionado", "decepcionada", "decepcioné",
            "me decepcionó", "desilusionado", "desilusionada", "desilusión",
            # Sin esperanza
            "desesperanza", "desesperanzado", "sin esperanza",
            "no hay salida", "no veo salida", "amargado", "amargura",
            "hundido", "hundida", "me hundí",
        ],
        "Molesto": [
            # Molestia base
            "molesto", "molesta", "molestia", "molestó", "me molestó",
            "me molesta", "me molestó mucho",
            # Enojo
            "enojado", "enojada", "enojo", "enojé", "me enojé",
            "me enojó", "muy enojado",
            # Irritación
            "irritado", "irritada", "irritación", "me irritó", "me irrita",
            # Frustración
            "frustrado", "frustrada", "frustración", "frustré", "me frustré",
            "me frustró", "qué frustración", "muy frustrante",
            # Enfado / furia
            "enfadado", "enfadada", "enfado", "furioso", "furiosa",
            "furia", "explosión de ira", "no aguanté",
            # Rabia
            "rabia", "rabioso", "rabiosa", "me dio rabia", "con rabia",
            # Indignación
            "indignado", "indignada", "indignación", "me indignó",
            "no puede ser", "es un colmo",
            # Disgusto / hartazgo
            "disgustado", "disgustada", "disgusto", "fastidiado", "fastidio",
            "hastiado", "hartazgo", "harto", "harta", "me hartó",
            "me tiene harto", "ya no aguanto", "no soporto",
            # Bronca (latinoamericanismo muy común)
            "bronca", "me da bronca", "me causó bronca",
            "coraje", "me da coraje",
            # Reacción
            "reaccioné mal", "me salí de las casillas", "estallé",
            "exploté", "me sacó", "me sacó de quicio",
        ],
        "Motivado": [
            # Motivación base
            "motivado", "motivada", "motivación", "motivé", "me motivé",
            "me motivó", "muy motivado",
            # Entusiasmo
            "entusiasmado", "entusiasmada", "entusiasmo", "con entusiasmo",
            "me entusiasmó", "qué entusiasmo",
            # Energía
            "energizado", "energizada", "energía", "con energía",
            "lleno de energía", "llena de energía", "me siento con energía",
            # Inspiración
            "inspirado", "inspirada", "inspiración", "me inspiró",
            "me sentí inspirado",
            # Decisión / determinación
            "decidido", "decidida", "determinado", "determinada",
            "con determinación", "decidí hacer", "tomé la decisión",
            # Ganas / empuje
            "con ganas", "tengo ganas", "muchas ganas", "ganas de hacer",
            "me dieron ganas", "empuje", "con empuje",
            "impulsado", "impulso", "me impulsó",
            # Confianza
            "confiado", "confiada", "confianza", "confianza en mí",
            "me siento capaz", "soy capaz", "puedo hacerlo",
            "voy a poder", "seguro de mí", "segura de mí",
            # Optimismo / esperanza
            "optimista", "optimismo", "esperanzado", "esperanzada",
            "esperanza", "con esperanza", "positivo en lo que viene",
            # Productividad / logro
            "productivo", "productiva", "productividad",
            "logré", "alcancé", "pude", "avancé",
            "progresé", "progreso", "crecí", "crecimiento",
            "me salió bien", "lo hice", "terminé",
            # Animoso
            "animoso", "animosa", "vigoroso", "vigorosa",
        ],
        "Agradecido": [
            # Agradecimiento base
            "agradecido", "agradecida", "agradecimiento", "agradezco",
            "te agradezco", "le agradezco", "muy agradecido",
            # Gratitud
            "gratitud", "grato", "grata", "con gratitud",
            "siento gratitud", "lleno de gratitud",
            # Afortunado / bendecido
            "afortunado", "afortunada", "qué suerte", "tengo suerte",
            "bendecido", "bendecida", "me siento bendecido",
            # Valorar / apreciar
            "valoro", "lo valoro", "aprecio", "lo aprecio",
            "apreciado", "apreciada", "me sentí apreciado",
            "me valoraron", "me lo reconocieron",
            # Reconocimiento
            "reconocido", "reconocida", "me reconocieron",
            "me lo agradecieron", "gracias",
            # Plenitud
            "pleno", "plena", "plenitud", "me siento pleno",
            "lleno", "llena", "me siento lleno",
            "completo", "completa", "me siento completo",
        ],
        "Solitario": [
            # Soledad base
            "solo", "sola", "soledad", "me sentí solo", "me sentí sola",
            "estoy solo", "quedé solo", "me dejaron solo",
            "me siento solo", "muy solo",
            # Aislamiento
            "aislado", "aislada", "aislamiento", "me aislé",
            "me aisló", "me encerré", "encerrado", "encerrada",
            "apartado", "apartada", "me aparté", "me alejé",
            # Incomprendido
            "incomprendido", "incomprendida", "nadie me entiende",
            "no me entienden", "no me comprenden",
            "me siento incomprendido",
            # Desconexión
            "desconectado", "desconectada", "desconexión",
            "no encajo", "no pertenezco", "no soy parte",
            "me cuesta conectar", "difícil conectar con",
            "no sé relacionarme", "me cuesta relacionarme",
            # Extrañar
            "extraño", "extrañé", "extrañar", "extraño mucho",
            "echo de menos",
        ],
        "Confundido": [
            # Confusión base
            "confundido", "confundida", "confusión", "me confundí",
            "me confundió", "muy confundido", "qué confusión",
            # Perdido / sin rumbo
            "perdido", "perdida", "me siento perdido",
            "sin rumbo", "no sé para dónde ir",
            "no sé qué camino tomar",
            # Duda
            "dudo", "dudé", "duda", "muchas dudas", "no sé si",
            "no sé qué pensar", "no sé qué hacer",
            "dudoso", "dudosa", "indeciso", "indecisa", "indecisión",
            # Desorientación
            "desorientado", "desorientada", "desorientación",
            "no entiendo", "no entendí", "no comprendo",
            "no sé por qué", "no encuentro sentido",
            # Conflicto interno
            "conflicto interno", "no sé qué quiero",
            "cabeza hecha un lío", "todo revuelto",
            "no tengo claro", "no lo tengo claro",
            "no sé cómo me siento",
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
