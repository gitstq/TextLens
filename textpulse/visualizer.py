"""
TextLens Terminal-based Visualization
终端可视化模块
"""

import math
from typing import Dict, List, Tuple

from .analyzer import (
    SentimentResult,
    ReadabilityResult,
    TextStats,
    FrequencyResult,
    PatternResult,
)


# Unicode block characters for sparklines
SPARKLINE_CHARS = [' ', '\u2581', '\u2582', '\u2583', '\u2584',
                   '\u2585', '\u2586', '\u2587', '\u2588']


class TerminalChart:
    """Terminal-based chart rendering utilities."""

    @staticmethod
    def render_bar_chart(
        data: Dict[str, float],
        title: str,
        width: int = 50,
        char: str = "\u2588",
    ) -> str:
        """Render a vertical-style bar chart in the terminal."""
        lines = []
        lines.append(f"  {title}")
        lines.append("")

        if not data:
            lines.append("  (no data)")
            return "\n".join(lines)

        max_val = max(abs(v) for v in data.values()) if data else 1
        if max_val == 0:
            max_val = 1

        for label, value in data.items():
            bar_len = int((abs(value) / max_val) * width)
            bar = char * bar_len
            lines.append(f"  {label:<20} {bar} {value:.2f}")

        return "\n".join(lines)

    @staticmethod
    def render_horizontal_bar(
        data: List[Tuple[str, float]],
        title: str,
        max_width: int = 40,
    ) -> str:
        """Render a horizontal bar chart."""
        lines = []
        lines.append(f"  {title}")
        lines.append("")

        if not data:
            lines.append("  (no data)")
            return "\n".join(lines)

        max_val = max(abs(v) for _, v in data) if data else 1
        if max_val == 0:
            max_val = 1

        for label, value in data:
            bar_len = int((abs(value) / max_val) * max_width)
            bar = "\u2588" * bar_len
            lines.append(f"  {label:<20} {bar} {value:.2f}")

        return "\n".join(lines)

    @staticmethod
    def render_progress_bar(
        value: float,
        max_value: float,
        width: int = 30,
        label: str = "",
    ) -> str:
        """Render a progress bar."""
        if max_value == 0:
            ratio = 0
        else:
            ratio = min(value / max_value, 1.0)

        filled = int(ratio * width)
        empty = width - filled
        bar = "\u2588" * filled + "\u2591" * empty

        if label:
            return f"  {label:<20} [{bar}] {value:.1f}/{max_value:.1f}"
        return f"  [{bar}] {value:.1f}/{max_value:.1f}"

    @staticmethod
    def render_gauge(
        value: float,
        min_val: float,
        max_val: float,
        label: str,
        width: int = 20,
    ) -> str:
        """Render a gauge meter."""
        if max_val == min_val:
            ratio = 0.5
        else:
            ratio = (value - min_val) / (max_val - min_val)
        ratio = max(0.0, min(1.0, ratio))

        filled = int(ratio * width)
        empty = width - filled
        bar = "\u2588" * filled + "\u2591" * empty

        return f"  {label:<20} [{bar}] {value:.2f}"

    @staticmethod
    def render_sparkline(
        values: List[float],
        width: int = 40,
        height: int = 5,
    ) -> str:
        """Render a sparkline using Unicode block characters."""
        if not values:
            return "  (no data)"

        min_val = min(values)
        max_val = max(values)

        if max_val == min_val:
            # All values are the same
            rows = []
            for row in range(height):
                if row == height - 1:
                    rows.append("  " + "\u2588" * min(width, len(values)))
                else:
                    rows.append("  " + " " * min(width, len(values)))
            return "\n".join(rows)

        # Normalize values to 0..(height-1)
        normalized = []
        for v in values:
            ratio = (v - min_val) / (max_val - min_val)
            level = int(ratio * (height - 1))
            normalized.append(level)

        # Build the sparkline row by row (top to bottom)
        rows = []
        for row in range(height):
            line_chars = []
            for val in normalized:
                if val >= (height - 1 - row):
                    line_chars.append("\u2588")
                else:
                    line_chars.append(" ")
            rows.append("  " + "".join(line_chars[:width]))

        return "\n".join(rows)


class TextLensDashboard:
    """Full dashboard rendering combining multiple chart types."""

    @staticmethod
    def render_dashboard(analysis_result: dict) -> str:
        """Render a full analysis dashboard."""
        sections = []

        sections.append("=" * 60)
        sections.append("  TextLens Analysis Dashboard")
        sections.append("=" * 60)
        sections.append("")

        if "sentiment" in analysis_result:
            sections.append(
                TextLensDashboard.render_sentiment_dashboard(
                    analysis_result["sentiment"]
                )
            )
            sections.append("")

        if "stats" in analysis_result:
            sections.append(
                TextLensDashboard.render_stats_dashboard(analysis_result["stats"])
            )
            sections.append("")

        if "readability" in analysis_result:
            sections.append(
                TextLensDashboard.render_readability_dashboard(
                    analysis_result["readability"]
                )
            )
            sections.append("")

        if "frequency" in analysis_result:
            sections.append(
                TextLensDashboard.render_frequency_chart(analysis_result["frequency"])
            )
            sections.append("")

        if "patterns" in analysis_result:
            patterns = analysis_result["patterns"]
            sections.append("  --- Pattern Analysis ---")
            sections.append(f"  Questions:          {patterns.questions}")
            sections.append(f"  Exclamations:       {patterns.exclamations}")
            sections.append(f"  Passive Voice:       {patterns.passive_voice}")
            sections.append(
                f"  Avg Complexity:      {patterns.avg_sentence_complexity:.4f}"
            )
            sections.append("")

        return "\n".join(sections)

    @staticmethod
    def render_sentiment_dashboard(sentiment: SentimentResult) -> str:
        """Render sentiment analysis dashboard."""
        lines = []
        lines.append("  --- Sentiment Analysis ---")

        # Sentiment gauge (-1 to 1)
        gauge = TerminalChart.render_gauge(
            sentiment.score, -1.0, 1.0, "Sentiment Score"
        )
        lines.append(gauge)

        lines.append(f"  Label:              {sentiment.label}")
        lines.append(f"  Confidence:         {sentiment.confidence:.4f}")
        lines.append(f"  Word Count:         {sentiment.word_count}")
        lines.append(f"  Sentence Count:     {sentiment.sentence_count}")

        return "\n".join(lines)

    @staticmethod
    def render_stats_dashboard(stats: TextStats) -> str:
        """Render text statistics dashboard."""
        lines = []
        lines.append("  --- Text Statistics ---")
        lines.append(f"  Characters:         {stats.char_count}")
        lines.append(f"  Words:              {stats.word_count}")
        lines.append(f"  Sentences:          {stats.sentence_count}")
        lines.append(f"  Paragraphs:         {stats.paragraph_count}")
        lines.append(f"  Lines:              {stats.line_count}")
        lines.append(f"  Avg Word Length:    {stats.avg_word_length}")
        lines.append(f"  Unique Words:       {stats.unique_word_count}")
        lines.append(f"  Lexical Diversity:  {stats.lexical_diversity:.4f}")
        lines.append(f"  Reading Time:       {stats.reading_time_minutes:.2f} min")

        return "\n".join(lines)

    @staticmethod
    def render_frequency_chart(freq: FrequencyResult) -> str:
        """Render word frequency chart."""
        lines = []
        lines.append("  --- Word Frequency (Top Words) ---")
        lines.append(f"  Total Unique Words: {freq.total_unique_words}")
        lines.append("")

        if freq.top_n:
            max_count = max(count for _, count in freq.top_n)
            if max_count == 0:
                max_count = 1

            for word, count in freq.top_n:
                bar_len = int((count / max_count) * 30)
                bar = "\u2588" * bar_len
                lines.append(f"  {word:<20} {bar} {count}")

        return "\n".join(lines)

    @staticmethod
    def render_readability_dashboard(readability: ReadabilityResult) -> str:
        """Render readability analysis dashboard."""
        lines = []
        lines.append("  --- Readability Analysis ---")

        # Flesch gauge (0 to 100)
        flesch_gauge = TerminalChart.render_gauge(
            readability.flesch_score, 0, 100, "Flesch Score"
        )
        lines.append(flesch_gauge)

        lines.append(f"  Grade Level:        {readability.grade_level}")
        lines.append(f"  Avg Sentence Len:   {readability.avg_sentence_length}")
        lines.append(f"  Avg Word Length:    {readability.avg_word_length}")
        lines.append(f"  Syllable Count:     {readability.syllable_count}")
        lines.append(f"  Gunning Fog:        {readability.gunning_fog}")
        lines.append(f"  Coleman-Liau:       {readability.coleman_liau}")

        return "\n".join(lines)
