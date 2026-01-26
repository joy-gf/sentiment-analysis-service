"""
Extractor de palabras clave en español
"""
import re
from collections import Counter
from typing import List, Dict

# Stopwords comunes en español
SPANISH_STOPWORDS = {
    'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
    'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
    'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
    'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
    'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
    'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
    'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
    'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
    'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
    'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar',
    'dejar', 'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo',
    'solo', 'decir', 'salir', 'volver', 'tomar', 'conocer', 'vivir', 'sentir',
    'tratar', 'mirar', 'contar', 'empezar', 'esperar', 'buscar', 'existir',
    'entrar', 'trabajar', 'escribir', 'perder', 'producir', 'ocurrir', 'entender',
    'pedir', 'recibir', 'recordar', 'terminar', 'permitir', 'aparecer', 'conseguir',
    'comenzar', 'servir', 'sacar', 'necesitar', 'mantener', 'resultar', 'leer',
    'caer', 'cambiar', 'presentar', 'crear', 'abrir', 'considerar', 'oír', 'acabar',
    'mil', 'seis', 'veinte', 'ciudad', 'ciento', 'cierto', 'cerca', 'segundo',
    'lado', 'hoy', 'durante', 'contra', 'tres', 'menos', 'puede', 'fueron',
    'había', 'esa', 'estos', 'estas', 'soy', 'eres', 'son', 'somos', 'estoy',
    'está', 'están', 'estamos', 'tengo', 'tiene', 'tienen', 'tenemos', 'ha',
    'han', 'hemos', 'fue', 'era', 'eran', 'éramos', 'sea', 'sean', 'seamos',
    'aunque', 'quien', 'cual', 'cuál', 'cuáles', 'cuyo', 'cuya', 'cuyos', 'cuyas',
}

class KeywordExtractor:
    """
    Extrae palabras clave frecuentes de textos en español
    """

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, any]]:
        """
        Extrae las palabras clave más frecuentes de un texto

        Args:
            text: Texto a analizar
            top_n: Número de palabras clave a retornar

        Returns:
            Lista de diccionarios con word y frequency
        """
        # Limpiar y tokenizar
        words = re.findall(r'\b\w+\b', text.lower())

        # Filtrar stopwords y palabras muy cortas
        filtered_words = [
            word for word in words
            if word not in SPANISH_STOPWORDS and len(word) > 3
        ]

        # Contar frecuencias
        word_freq = Counter(filtered_words)

        # Retornar top N palabras
        return [
            {"word": word, "frequency": freq}
            for word, freq in word_freq.most_common(top_n)
        ]

    def extract_keywords_from_multiple(
        self,
        texts: List[str],
        top_n: int = 10
    ) -> List[Dict[str, any]]:
        """
        Extrae palabras clave de múltiples textos

        Args:
            texts: Lista de textos
            top_n: Número de palabras clave a retornar

        Returns:
            Lista de diccionarios con word y frequency
        """
        all_words = []

        for text in texts:
            # Limpiar y tokenizar
            words = re.findall(r'\b\w+\b', text.lower())
            # Filtrar stopwords y palabras cortas
            filtered = [
                w for w in words
                if w not in SPANISH_STOPWORDS and len(w) > 3
            ]
            all_words.extend(filtered)

        # Contar frecuencias globales
        word_freq = Counter(all_words)

        # Retornar top N palabras
        return [
            {"word": word, "frequency": freq}
            for word, freq in word_freq.most_common(top_n)
        ]
