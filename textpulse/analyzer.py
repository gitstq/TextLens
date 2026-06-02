"""
TextLens Core Text Analysis Engine
文本分析核心引擎
"""

import re
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# ============================================================
# Data Classes
# ============================================================

@dataclass
class SentimentResult:
    """Sentiment analysis result."""
    text: str
    score: float  # -1.0 to 1.0
    label: str  # positive / negative / neutral
    confidence: float
    word_count: int
    sentence_count: int


@dataclass
class ReadabilityResult:
    """Readability analysis result."""
    text: str
    avg_sentence_length: float
    avg_word_length: float
    syllable_count: int
    flesch_score: float
    gunning_fog: float
    coleman_liau: float
    grade_level: str


@dataclass
class TextStats:
    """Basic text statistics."""
    char_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    line_count: int
    avg_word_length: float
    unique_word_count: int
    lexical_diversity: float
    reading_time_minutes: float


@dataclass
class FrequencyResult:
    """Word frequency analysis result."""
    word_frequencies: Dict[str, int]
    top_n: List[Tuple[str, int]]
    total_unique_words: int


@dataclass
class PatternResult:
    """Text pattern analysis result."""
    questions: int
    exclamations: int
    passive_voice: int
    avg_sentence_complexity: float


# ============================================================
# Sentiment Analyzer
# ============================================================

class SentimentAnalyzer:
    """Sentiment analysis using a lexicon-based approach."""

    POSITIVE_WORDS = frozenset([
        "good", "great", "excellent", "amazing", "wonderful", "fantastic",
        "beautiful", "love", "happy", "joy", "brilliant", "outstanding",
        "superb", "perfect", "awesome", "nice", "pleasant", "delightful",
        "magnificent", "marvelous", "incredible", "remarkable", "exceptional",
        "splendid", "terrific", "glorious", "supreme", "triumphant",
        "positive", "success", "best", "better", "improve", "enjoy",
        "pleased", "glad", "satisfied", "grateful", "thankful", "hopeful",
        "optimistic", "confident", "proud", "excited", "thrilled",
        "enthusiastic", "passionate", "inspired", "motivated", "creative",
        "innovative", "impressive", "extraordinary",
    ])

    NEGATIVE_WORDS = frozenset([
        "bad", "terrible", "horrible", "awful", "poor", "worst", "hate",
        "ugly", "disgusting", "dreadful", "miserable", "painful", "sad",
        "angry", "disappointed", "frustrated", "annoyed", "boring", "useless",
        "worthless", "pathetic", "failure", "broken", "damaged", "destroyed",
        "ruined", "toxic", "harmful", "dangerous", "threatening", "aggressive",
        "violent", "cruel", "evil", "wicked", "corrupt", "unfair", "unjust",
        "dishonest", "greedy", "selfish", "lazy", "stupid", "ignorant",
        "incompetent", "inefficient", "unreliable", "unstable", "insecure",
        "vulnerable", "weak", "helpless", "hopeless", "desperate", "depressed",
        "anxious", "worried", "fearful", "stressed", "confused", "lost",
    ])

    INTENSIFIERS = frozenset([
        "very", "extremely", "incredibly", "absolutely", "totally",
        "completely", "utterly", "highly", "deeply", "truly", "really",
        "so", "quite", "rather", "fairly", "somewhat", "slightly",
        "barely", "hardly",
    ])

    NEGATORS = frozenset([
        "not", "no", "never", "neither", "nobody", "nothing", "nowhere",
        "nor", "cannot", "can't", "don't", "doesn't", "didn't", "won't",
        "wouldn't", "shouldn't", "couldn't", "isn't", "aren't", "wasn't",
        "weren't",
    ])

    def analyze(self, text: str) -> SentimentResult:
        """Analyze sentiment of a text string."""
        words = re.findall(r"[a-zA-Z']+", text.lower())
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        word_count = len(words)
        sentence_count = max(len(sentences), 1)

        positive_score = 0.0
        negative_score = 0.0

        i = 0
        while i < len(words):
            word = words[i]

            # Check for intensifier preceding a sentiment word
            if word in self.INTENSIFIERS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in self.POSITIVE_WORDS:
                    positive_score += 1.5
                    i += 2
                    continue
                elif next_word in self.NEGATIVE_WORDS:
                    negative_score += 1.5
                    i += 2
                    continue

            # Check for negator preceding a sentiment word
            if word in self.NEGATORS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in self.POSITIVE_WORDS:
                    negative_score += 1.0
                    i += 2
                    continue
                elif next_word in self.NEGATIVE_WORDS:
                    positive_score += 1.0
                    i += 2
                    continue

            if word in self.POSITIVE_WORDS:
                positive_score += 1.0
            elif word in self.NEGATIVE_WORDS:
                negative_score += 1.0

            i += 1

        # Normalize score to -1.0 to 1.0
        total = positive_score + negative_score
        if total == 0:
            score = 0.0
            confidence = 0.0
        else:
            score = (positive_score - negative_score) / total
            confidence = total / max(word_count, 1)
            confidence = min(confidence, 1.0)

        if score > 0.05:
            label = "positive"
        elif score < -0.05:
            label = "negative"
        else:
            label = "neutral"

        return SentimentResult(
            text=text,
            score=round(score, 4),
            label=label,
            confidence=round(confidence, 4),
            word_count=word_count,
            sentence_count=sentence_count,
        )

    def analyze_sentences(self, text: str) -> List[SentimentResult]:
        """Analyze sentiment of each sentence individually."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return [self.analyze(s) for s in sentences]

    def batch_analyze(self, texts: List[str]) -> List[SentimentResult]:
        """Analyze sentiment of multiple texts."""
        return [self.analyze(t) for t in texts]


# ============================================================
# Readability Analyzer
# ============================================================

class ReadabilityAnalyzer:
    """Readability scoring using multiple established formulas."""

    def count_syllables(self, word: str) -> int:
        """Count syllables in a word."""
        word = word.lower().strip()
        if not word:
            return 0

        # Special common words
        special_syllables = {
            "the": 1, "apple": 2, "water": 2, "fire": 1, "every": 3,
            "beautiful": 3, "wonderful": 3, "simple": 2, "people": 2,
            "little": 2, "middle": 2, "table": 2, "bottle": 2,
        }
        if word in special_syllables:
            return special_syllables[word]

        # Remove trailing 'e' (silent e) but not for short words
        if word.endswith('e') and len(word) > 3:
            word = word[:-1]

        # Remove trailing 'es' if it doesn't add a syllable
        if word.endswith('es') and len(word) > 4:
            word = word[:-2]
        # Remove trailing 'ed' if it doesn't add a syllable
        elif word.endswith('ed') and len(word) > 4:
            word = word[:-2]

        if not word:
            return 1

        # Count vowel groups (consecutive vowels count as one syllable)
        vowel_groups = re.findall(r'[aeiouy]+', word)
        count = len(vowel_groups)

        return max(count, 1)

    def analyze(self, text: str) -> ReadabilityResult:
        """Analyze readability of text."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = re.findall(r"[a-zA-Z']+", text)
        total_words = len(words)
        total_sentences = max(len(sentences), 1)

        # Count syllables
        total_syllables = sum(self.count_syllables(w) for w in words)

        # Average sentence length
        avg_sentence_length = total_words / total_sentences

        # Average word length
        avg_word_length = sum(len(w) for w in words) / max(total_words, 1)

        # Flesch Reading Ease
        # 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        if total_words > 0 and total_sentences > 0:
            flesch = (206.835
                      - 1.015 * (total_words / total_sentences)
                      - 84.6 * (total_syllables / total_words))
            flesch = max(0.0, min(100.0, flesch))
        else:
            flesch = 0.0

        # Gunning Fog Index
        # 0.8 * (total_words / total_sentences) + 100 * (complex_words / total_words)
        complex_words = sum(1 for w in words if self.count_syllables(w) >= 3)
        if total_words > 0 and total_sentences > 0:
            gunning_fog = (0.8 * (total_words / total_sentences)
                           + 100.0 * (complex_words / total_words))
        else:
            gunning_fog = 0.0

        # Coleman-Liau Index
        # 0.0588 * L - 0.296 * S - 15.8
        # L = avg letters per 100 words, S = avg sentences per 100 words
        total_letters = sum(len(w) for w in words)
        if total_words > 0:
            L = (total_letters / total_words) * 100.0
            S = (total_sentences / total_words) * 100.0
            coleman_liau = 0.0588 * L - 0.296 * S - 15.8
        else:
            coleman_liau = 0.0

        # Determine grade level based on Flesch score
        if flesch >= 90:
            grade_level = "Very Easy (5th grade)"
        elif flesch >= 80:
            grade_level = "Easy (6th grade)"
        elif flesch >= 70:
            grade_level = "Fairly Easy (7th grade)"
        elif flesch >= 60:
            grade_level = "Standard (8th-9th grade)"
        elif flesch >= 50:
            grade_level = "Fairly Difficult (10th-12th grade)"
        elif flesch >= 30:
            grade_level = "Difficult (College)"
        else:
            grade_level = "Very Difficult (Graduate)"

        return ReadabilityResult(
            text=text,
            avg_sentence_length=round(avg_sentence_length, 2),
            avg_word_length=round(avg_word_length, 2),
            syllable_count=total_syllables,
            flesch_score=round(flesch, 2),
            gunning_fog=round(gunning_fog, 2),
            coleman_liau=round(coleman_liau, 2),
            grade_level=grade_level,
        )


# ============================================================
# Text Statistics
# ============================================================

class TextStatistics:
    """Basic text statistics computation."""

    def analyze(self, text: str) -> TextStats:
        """Compute basic statistics for text."""
        char_count = len(text)

        words = re.findall(r"[a-zA-Z']+", text)
        word_count = len(words)

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        paragraphs = re.split(r'\n\s*\n', text.strip())
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        paragraph_count = max(len(paragraphs), 1)

        lines = text.split('\n')
        line_count = len(lines)

        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)

        unique_words = set(w.lower() for w in words)
        unique_word_count = len(unique_words)

        lexical_diversity = unique_word_count / max(word_count, 1)

        # Reading time at 200 words per minute
        reading_time_minutes = word_count / 200.0

        return TextStats(
            char_count=char_count,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            line_count=line_count,
            avg_word_length=round(avg_word_length, 2),
            unique_word_count=unique_word_count,
            lexical_diversity=round(lexical_diversity, 4),
            reading_time_minutes=round(reading_time_minutes, 2),
        )


# ============================================================
# Frequency Analyzer
# ============================================================

class FrequencyAnalyzer:
    """Word frequency analysis with stop word filtering."""

    STOP_WORDS = frozenset([
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "shall",
        "should", "may", "might", "must", "can", "could", "of", "in", "to",
        "for", "with", "on", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "above", "below", "between", "out",
        "off", "over", "under", "again", "further", "then", "once", "here",
        "there", "when", "where", "why", "how", "all", "both", "each", "few",
        "more", "most", "other", "some", "such", "no", "nor", "not", "only",
        "own", "same", "so", "than", "too", "very", "just", "because", "but",
        "and", "or", "if", "while", "about", "against", "between", "through",
        "during", "before", "after", "it", "its", "this", "that", "these",
        "those", "i", "me", "my", "we", "our", "you", "your", "he", "him",
        "his", "she", "her", "they", "them", "their", "what", "which", "who",
        "whom",
    ])

    def analyze(self, text: str, top_n: int = 20) -> FrequencyResult:
        """Analyze word frequency, excluding stop words."""
        words = re.findall(r"[a-zA-Z']+", text.lower())
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 1]

        freq: Dict[str, int] = {}
        for w in filtered:
            freq[w] = freq.get(w, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        top = sorted_words[:top_n]

        return FrequencyResult(
            word_frequencies=freq,
            top_n=top,
            total_unique_words=len(freq),
        )

    def analyze_ngrams(self, text: str, n: int = 2, top_n: int = 10) -> FrequencyResult:
        """Analyze n-gram frequency."""
        words = re.findall(r"[a-zA-Z']+", text.lower())
        filtered = [w for w in words if w not in self.STOP_WORDS and len(w) > 1]

        ngrams: Dict[str, int] = {}
        for i in range(len(filtered) - n + 1):
            gram = " ".join(filtered[i:i + n])
            ngrams[gram] = ngrams.get(gram, 0) + 1

        sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
        top = sorted_ngrams[:top_n]

        return FrequencyResult(
            word_frequencies=ngrams,
            top_n=top,
            total_unique_words=len(ngrams),
        )


# ============================================================
# Pattern Analyzer
# ============================================================

class PatternAnalyzer:
    """Text pattern detection and analysis."""

    # Passive voice helper verbs
    PASSIVE_HELPERS = frozenset([
        "is", "was", "are", "were", "be", "been", "being",
        "has", "have", "had",
    ])

    # Common past participles
    PAST_PARTICIPLES = frozenset([
        "done", "made", "taken", "given", "written", "spoken", "broken",
        "chosen", "known", "grown", "shown", "thrown", "drawn", "driven",
        "born", "worn", "torn", "sworn", "borne", "eaten", "beaten",
        "fallen", "stolen", "hidden", "ridden", "bidden", "forgotten",
        "frozen", "shaken", "risen", "written", "seen", "been", "gone",
        "built", "sent", "spent", "left", "felt", "kept", "meant", "met",
        "hit", "put", "run", "cut", "set", "read", "led", "heard",
        "loved", "hated", "wanted", "needed", "used", "found", "told",
        "asked", "called", "tried", "helped", "started", "played",
        "moved", "lived", "believed", "held", "brought", "caught",
        "taught", "bought", "fought", "thought", "sought", "worked",
        "created", "destroyed", "developed", "produced", "received",
        "considered", "required", "reported", "included", "designed",
        "established", "described", "completed", "accepted", "affected",
        "decided", "recognized", "replaced", "reduced", "formed",
        "continued", "provided", "determined", "prepared", "applied",
        "announced", "suggested", "supported", "controlled", "managed",
        "treated", "involved", "carried", "performed", "planned",
        "changed", "based", "caused", "contained", "reached",
        "remained", "occurred", "achieved", "allowed", "added",
        "appeared", "followed", "began", "became",
    ])

    def analyze(self, text: str) -> PatternResult:
        """Analyze text patterns."""
        # Use findall to preserve sentence-ending punctuation
        sentences = re.findall(r'[^.!?]*[.!?]', text)
        if not sentences:
            # Fall back to treating entire text as one sentence
            sentences = [text] if text.strip() else []

        questions = 0
        exclamations = 0
        passive_voice = 0
        total_complexity = 0.0

        for sentence in sentences:
            stripped = sentence.strip()
            if not stripped:
                continue

            # Count questions and exclamations
            if stripped.endswith('?'):
                questions += 1
            if stripped.endswith('!'):
                exclamations += 1

            # Detect passive voice: helper + past participle
            words = re.findall(r"[a-zA-Z']+", stripped.lower())
            for i in range(len(words) - 1):
                if words[i] in self.PASSIVE_HELPERS and words[i + 1] in self.PAST_PARTICIPLES:
                    passive_voice += 1
                    break

            # Sentence complexity: clause density (commas + conjunctions per sentence)
            clauses = stripped.count(',') + stripped.count(';')
            conjunctions = len(re.findall(
                r'\b(and|but|or|nor|for|yet|so|although|because|since|unless|while|whereas|if|when|where|after|before|though|even|whether)\b',
                stripped.lower()
            ))
            complexity = (clauses + conjunctions + 1) / max(len(words), 1)
            total_complexity += complexity

        avg_complexity = total_complexity / max(len(sentences), 1)

        return PatternResult(
            questions=questions,
            exclamations=exclamations,
            passive_voice=passive_voice,
            avg_sentence_complexity=round(avg_complexity, 4),
        )


# ============================================================
# TextLens Engine (Main Orchestrator)
# ============================================================

class TextLensEngine:
    """Main orchestrator combining all analyzers."""

    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.readability_analyzer = ReadabilityAnalyzer()
        self.text_statistics = TextStatistics()
        self.frequency_analyzer = FrequencyAnalyzer()
        self.pattern_analyzer = PatternAnalyzer()

    def analyze(
        self,
        text: str,
        include_sentiment: bool = True,
        include_readability: bool = True,
        include_stats: bool = True,
        include_frequency: bool = True,
        include_patterns: bool = True,
    ) -> dict:
        """Run full or partial analysis on text."""
        result = {}

        if include_sentiment:
            result["sentiment"] = self.sentiment_analyzer.analyze(text)

        if include_readability:
            result["readability"] = self.readability_analyzer.analyze(text)

        if include_stats:
            result["stats"] = self.text_statistics.analyze(text)

        if include_frequency:
            result["frequency"] = self.frequency_analyzer.analyze(text)

        if include_patterns:
            result["patterns"] = self.pattern_analyzer.analyze(text)

        return result

    def analyze_file(self, path: str, encoding: str = 'utf-8') -> dict:
        """Analyze text from a file."""
        with open(path, 'r', encoding=encoding) as f:
            text = f.read()
        return self.analyze(text)

    def quick_summary(self, text: str) -> str:
        """Generate a one-line summary of text."""
        stats = self.text_statistics.analyze(text)
        sentiment = self.sentiment_analyzer.analyze(text)
        readability = self.readability_analyzer.analyze(text)

        return (
            f"{stats.word_count} words, {stats.sentence_count} sentences, "
            f"sentiment: {sentiment.label} ({sentiment.score:.2f}), "
            f"readability: {readability.grade_level}"
        )

    def compare_texts(self, texts: List[str]) -> dict:
        """Compare multiple texts side by side."""
        results = []
        for i, text in enumerate(texts):
            analysis = self.analyze(text)
            analysis["index"] = i
            results.append(analysis)

        # Compute comparison metrics
        comparison = {
            "texts": results,
            "sentiment_range": None,
            "readability_range": None,
        }

        sentiments = [r["sentiment"].score for r in results]
        readabilities = [r["readability"].flesch_score for r in results]

        if sentiments:
            comparison["sentiment_range"] = {
                "min": min(sentiments),
                "max": max(sentiments),
                "avg": sum(sentiments) / len(sentiments),
            }

        if readabilities:
            comparison["readability_range"] = {
                "min": min(readabilities),
                "max": max(readabilities),
                "avg": sum(readabilities) / len(readabilities),
            }

        return comparison
