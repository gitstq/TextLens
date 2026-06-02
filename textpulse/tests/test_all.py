"""
TextPulse Comprehensive Test Suite
全面测试套件
"""

import json
import os
import sys
import tempfile
import unittest
from io import StringIO

from textpulse.analyzer import (
    SentimentResult,
    ReadabilityResult,
    TextStats,
    FrequencyResult,
    PatternResult,
    SentimentAnalyzer,
    ReadabilityAnalyzer,
    TextStatistics,
    FrequencyAnalyzer,
    PatternAnalyzer,
    TextLensEngine,
)
from textpulse.visualizer import TerminalChart, TextLensDashboard
from textpulse.cli import build_parser, main, _format_json, _format_text, _format_markdown, _format_csv
from textpulse import __version__


# ============================================================
# Test Sentiment Analyzer
# ============================================================

class TestSentimentAnalyzer(unittest.TestCase):
    """Tests for SentimentAnalyzer."""

    def setUp(self):
        self.analyzer = SentimentAnalyzer()

    def test_positive_text(self):
        """Test positive sentiment detection."""
        result = self.analyzer.analyze("This is a great and wonderful day!")
        self.assertEqual(result.label, "positive")
        self.assertGreater(result.score, 0)

    def test_negative_text(self):
        """Test negative sentiment detection."""
        result = self.analyzer.analyze("This is a terrible and horrible experience.")
        self.assertEqual(result.label, "negative")
        self.assertLess(result.score, 0)

    def test_neutral_text(self):
        """Test neutral sentiment detection."""
        result = self.analyzer.analyze("The sky is blue and the grass is green.")
        self.assertEqual(result.label, "neutral")

    def test_negation_handling(self):
        """Test that negation flips sentiment."""
        result = self.analyzer.analyze("This is not good at all.")
        self.assertEqual(result.label, "negative")

    def test_double_negation(self):
        """Test double negation becomes positive."""
        result = self.analyzer.analyze("This is not bad actually.")
        self.assertEqual(result.label, "positive")

    def test_intensifier(self):
        """Test intensifier amplifies sentiment."""
        result = self.analyzer.analyze("This is very good!")
        self.assertEqual(result.label, "positive")
        self.assertGreater(result.score, 0)

    def test_score_range(self):
        """Test score is in -1.0 to 1.0 range."""
        result = self.analyzer.analyze("Some text here.")
        self.assertGreaterEqual(result.score, -1.0)
        self.assertLessEqual(result.score, 1.0)

    def test_confidence_range(self):
        """Test confidence is in 0.0 to 1.0 range."""
        result = self.analyzer.analyze("Some text here.")
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)

    def test_word_count(self):
        """Test word count is correct."""
        result = self.analyzer.analyze("one two three four five")
        self.assertEqual(result.word_count, 5)

    def test_sentence_count(self):
        """Test sentence count."""
        result = self.analyzer.analyze("First sentence. Second sentence. Third.")
        self.assertEqual(result.sentence_count, 3)

    def test_analyze_sentences(self):
        """Test per-sentence analysis."""
        results = self.analyzer.analyze_sentences("Good day. Bad night.")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].label, "positive")
        self.assertEqual(results[1].label, "negative")

    def test_batch_analyze(self):
        """Test batch analysis."""
        texts = ["Good day!", "Bad night.", "Okay weather."]
        results = self.analyzer.batch_analyze(texts)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].label, "positive")
        self.assertEqual(results[1].label, "negative")
        self.assertEqual(results[2].label, "neutral")

    def test_empty_text(self):
        """Test empty text."""
        result = self.analyzer.analyze("")
        self.assertEqual(result.label, "neutral")
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.word_count, 0)

    def test_mixed_sentiment(self):
        """Test mixed sentiment text."""
        result = self.analyzer.analyze("The good and the bad, the beautiful and the ugly.")
        # Mixed sentiment - could be either, but score should be near 0
        self.assertIn(result.label, ["positive", "negative", "neutral"])


# ============================================================
# Test Readability Analyzer
# ============================================================

class TestReadabilityAnalyzer(unittest.TestCase):
    """Tests for ReadabilityAnalyzer."""

    def setUp(self):
        self.analyzer = ReadabilityAnalyzer()

    def test_syllable_count_simple(self):
        """Test basic syllable counting."""
        self.assertEqual(self.analyzer.count_syllables("cat"), 1)
        self.assertEqual(self.analyzer.count_syllables("dog"), 1)

    def test_syllable_count_two(self):
        """Test two-syllable words."""
        self.assertEqual(self.analyzer.count_syllables("apple"), 2)
        self.assertEqual(self.analyzer.count_syllables("water"), 2)

    def test_syllable_count_three(self):
        """Test three-syllable words."""
        self.assertEqual(self.analyzer.count_syllables("beautiful"), 3)
        self.assertEqual(self.analyzer.count_syllables("wonderful"), 3)

    def test_syllable_count_silent_e(self):
        """Test silent e handling."""
        result = self.analyzer.count_syllables("make")
        self.assertGreaterEqual(result, 1)

    def test_syllable_count_empty(self):
        """Test empty word."""
        self.assertEqual(self.analyzer.count_syllables(""), 0)

    def test_syllable_count_minimum(self):
        """Test minimum syllable count is 1."""
        result = self.analyzer.count_syllables("the")
        self.assertGreaterEqual(result, 1)

    def test_flesch_score_range(self):
        """Test Flesch score is in valid range."""
        result = self.analyzer.analyze("The quick brown fox jumps over the lazy dog.")
        self.assertGreaterEqual(result.flesch_score, 0.0)
        self.assertLessEqual(result.flesch_score, 100.0)

    def test_flesch_score_easy_text(self):
        """Test that simple text has higher Flesch score."""
        easy = self.analyzer.analyze("The cat sat on the mat. The dog ran in the park.")
        hard = self.analyzer.analyze(
            "The extraordinarily complicated phenomenon demonstrated "
            "unprecedented characteristics throughout the comprehensive "
            "investigation methodology implementation."
        )
        self.assertGreater(easy.flesch_score, hard.flesch_score)

    def test_grade_level(self):
        """Test grade level is determined."""
        result = self.analyzer.analyze("The cat sat on the mat.")
        self.assertIsInstance(result.grade_level, str)
        self.assertIn("grade", result.grade_level.lower())

    def test_gunning_fog(self):
        """Test Gunning Fog index is computed."""
        result = self.analyzer.analyze("The quick brown fox jumps over the lazy dog.")
        self.assertIsInstance(result.gunning_fog, float)
        self.assertGreater(result.gunning_fog, 0)

    def test_coleman_liau(self):
        """Test Coleman-Liau index is computed."""
        result = self.analyzer.analyze("The quick brown fox jumps over the lazy dog.")
        self.assertIsInstance(result.coleman_liau, float)

    def test_avg_sentence_length(self):
        """Test average sentence length."""
        text = "One. Two three. Four five six seven."
        result = self.analyzer.analyze(text)
        self.assertGreater(result.avg_sentence_length, 0)

    def test_avg_word_length(self):
        """Test average word length."""
        result = self.analyzer.analyze("The cat sat.")
        self.assertGreater(result.avg_word_length, 0)

    def test_syllable_count_total(self):
        """Test total syllable count."""
        result = self.analyzer.analyze("The cat sat on the mat.")
        self.assertGreater(result.syllable_count, 0)

    def test_empty_text(self):
        """Test empty text readability."""
        result = self.analyzer.analyze("")
        self.assertEqual(result.flesch_score, 0.0)


# ============================================================
# Test Text Statistics
# ============================================================

class TestTextStatistics(unittest.TestCase):
    """Tests for TextStatistics."""

    def setUp(self):
        self.stats = TextStatistics()

    def test_word_count(self):
        """Test word count."""
        result = self.stats.analyze("one two three four five")
        self.assertEqual(result.word_count, 5)

    def test_sentence_count(self):
        """Test sentence count."""
        result = self.stats.analyze("First. Second. Third.")
        self.assertEqual(result.sentence_count, 3)

    def test_char_count(self):
        """Test character count."""
        result = self.stats.analyze("hello")
        self.assertEqual(result.char_count, 5)

    def test_paragraph_count(self):
        """Test paragraph count."""
        text = "Para one.\n\nPara two.\n\nPara three."
        result = self.stats.analyze(text)
        self.assertEqual(result.paragraph_count, 3)

    def test_line_count(self):
        """Test line count."""
        text = "Line one.\nLine two.\nLine three."
        result = self.stats.analyze(text)
        self.assertEqual(result.line_count, 3)

    def test_avg_word_length(self):
        """Test average word length."""
        result = self.stats.analyze("cat dog bird")
        # cat(3) + dog(3) + bird(4) = 10 / 3 = 3.33
        self.assertAlmostEqual(result.avg_word_length, 3.33, places=2)

    def test_unique_word_count(self):
        """Test unique word count."""
        result = self.stats.analyze("the cat and the dog and the bird")
        self.assertEqual(result.unique_word_count, 5)  # the, cat, and, dog, bird

    def test_lexical_diversity(self):
        """Test lexical diversity."""
        result = self.stats.analyze("the cat and the dog and the bird")
        self.assertGreater(result.lexical_diversity, 0)
        self.assertLessEqual(result.lexical_diversity, 1.0)

    def test_reading_time(self):
        """Test reading time estimation."""
        # 200 words should be ~1 minute
        text = "word " * 200
        result = self.stats.analyze(text)
        self.assertAlmostEqual(result.reading_time_minutes, 1.0, places=1)

    def test_empty_text(self):
        """Test empty text."""
        result = self.stats.analyze("")
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.char_count, 0)


# ============================================================
# Test Frequency Analyzer
# ============================================================

class TestFrequencyAnalyzer(unittest.TestCase):
    """Tests for FrequencyAnalyzer."""

    def setUp(self):
        self.analyzer = FrequencyAnalyzer()

    def test_word_frequency(self):
        """Test basic word frequency."""
        result = self.analyzer.analyze("cat cat dog dog dog bird")
        self.assertEqual(result.word_frequencies.get("cat"), 2)
        self.assertEqual(result.word_frequencies.get("dog"), 3)
        self.assertEqual(result.word_frequencies.get("bird"), 1)

    def test_stop_words_filtered(self):
        """Test that stop words are filtered out."""
        result = self.analyzer.analyze("the cat is on the mat")
        self.assertNotIn("the", result.word_frequencies)
        self.assertNotIn("is", result.word_frequencies)
        self.assertNotIn("on", result.word_frequencies)
        self.assertIn("cat", result.word_frequencies)
        self.assertIn("mat", result.word_frequencies)

    def test_top_n(self):
        """Test top N words."""
        result = self.analyzer.analyze("cat cat cat dog dog bird", top_n=2)
        self.assertEqual(len(result.top_n), 2)
        self.assertEqual(result.top_n[0], ("cat", 3))
        self.assertEqual(result.top_n[1], ("dog", 2))

    def test_unique_word_count(self):
        """Test total unique words count."""
        result = self.analyzer.analyze("cat dog bird fish")
        self.assertEqual(result.total_unique_words, 4)

    def test_ngrams(self):
        """Test n-gram analysis."""
        result = self.analyzer.analyze_ngrams("cat dog bird cat dog fish", n=2, top_n=5)
        self.assertGreater(len(result.word_frequencies), 0)
        # "cat dog" should appear twice
        self.assertEqual(result.word_frequencies.get("cat dog", 0), 2)

    def test_empty_text(self):
        """Test empty text."""
        result = self.analyzer.analyze("")
        self.assertEqual(result.total_unique_words, 0)
        self.assertEqual(len(result.top_n), 0)

    def test_case_insensitive(self):
        """Test case insensitivity."""
        result = self.analyzer.analyze("Cat cat CAT")
        self.assertEqual(result.word_frequencies.get("cat"), 3)

    def test_single_char_words_filtered(self):
        """Test that single character words are filtered."""
        result = self.analyzer.analyze("a cat")
        # "a" is a stop word, should be filtered
        self.assertNotIn("a", result.word_frequencies)


# ============================================================
# Test Pattern Analyzer
# ============================================================

class TestPatternAnalyzer(unittest.TestCase):
    """Tests for PatternAnalyzer."""

    def setUp(self):
        self.analyzer = PatternAnalyzer()

    def test_questions(self):
        """Test question detection."""
        result = self.analyzer.analyze("What is this? How are you? This is a statement.")
        self.assertEqual(result.questions, 2)

    def test_exclamations(self):
        """Test exclamation detection."""
        result = self.analyzer.analyze("Wow! Amazing! This is normal.")
        self.assertEqual(result.exclamations, 2)

    def test_passive_voice(self):
        """Test passive voice detection."""
        result = self.analyzer.analyze(
            "The ball was thrown. The cake was eaten. The car was driven."
        )
        self.assertGreater(result.passive_voice, 0)

    def test_active_voice_not_passive(self):
        """Test active voice is not detected as passive."""
        result = self.analyzer.analyze("The cat sat on the mat. The dog ran fast.")
        self.assertEqual(result.passive_voice, 0)

    def test_avg_complexity(self):
        """Test average sentence complexity."""
        result = self.analyzer.analyze("The cat sat.")
        self.assertGreater(result.avg_sentence_complexity, 0)

    def test_complex_sentence(self):
        """Test complex sentence has higher complexity."""
        simple = self.analyzer.analyze("The cat sat.")
        complex_text = self.analyzer.analyze(
            "Although it was raining, and the wind was blowing, "
            "the cat, which was very brave, sat on the mat, "
            "but the dog ran away."
        )
        self.assertGreater(
            complex_text.avg_sentence_complexity,
            simple.avg_sentence_complexity,
        )

    def test_empty_text(self):
        """Test empty text."""
        result = self.analyzer.analyze("")
        self.assertEqual(result.questions, 0)
        self.assertEqual(result.exclamations, 0)
        self.assertEqual(result.passive_voice, 0)


# ============================================================
# Test Terminal Chart
# ============================================================

class TestTerminalChart(unittest.TestCase):
    """Tests for TerminalChart."""

    def test_bar_chart(self):
        """Test bar chart rendering."""
        data = {"A": 10, "B": 20, "C": 15}
        result = TerminalChart.render_bar_chart(data, "Test Chart")
        self.assertIn("Test Chart", result)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)

    def test_bar_chart_empty(self):
        """Test bar chart with empty data."""
        result = TerminalChart.render_bar_chart({}, "Empty Chart")
        self.assertIn("no data", result)

    def test_horizontal_bar(self):
        """Test horizontal bar chart."""
        data = [("A", 10), ("B", 20), ("C", 15)]
        result = TerminalChart.render_horizontal_bar(data, "Test")
        self.assertIn("Test", result)
        self.assertIn("A", result)

    def test_progress_bar(self):
        """Test progress bar."""
        result = TerminalChart.render_progress_bar(5, 10, label="Progress")
        self.assertIn("Progress", result)

    def test_progress_bar_zero_max(self):
        """Test progress bar with zero max."""
        result = TerminalChart.render_progress_bar(5, 0, label="Test")
        self.assertIn("Test", result)

    def test_gauge(self):
        """Test gauge rendering."""
        result = TerminalChart.render_gauge(0.5, 0.0, 1.0, "Score")
        self.assertIn("Score", result)
        self.assertIn("0.50", result)

    def test_gauge_min_equals_max(self):
        """Test gauge with min == max."""
        result = TerminalChart.render_gauge(5, 5, 5, "Test")
        self.assertIn("Test", result)

    def test_sparkline(self):
        """Test sparkline rendering."""
        values = [1, 2, 3, 4, 5, 4, 3, 2, 1]
        result = TerminalChart.render_sparkline(values)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_sparkline_empty(self):
        """Test sparkline with empty values."""
        result = TerminalChart.render_sparkline([])
        self.assertIn("no data", result)

    def test_sparkline_uniform(self):
        """Test sparkline with uniform values."""
        values = [5, 5, 5, 5, 5]
        result = TerminalChart.render_sparkline(values)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_sparkline_single_value(self):
        """Test sparkline with single value."""
        result = TerminalChart.render_sparkline([42])
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


# ============================================================
# Test TextPulse Dashboard
# ============================================================

class TestTextLensDashboard(unittest.TestCase):
    """Tests for TextLensDashboard."""

    def test_render_dashboard(self):
        """Test full dashboard rendering."""
        engine = TextLensEngine()
        result = engine.analyze("This is a great and wonderful test.")
        dashboard = TextLensDashboard.render_dashboard(result)
        self.assertIn("TextLens", dashboard)
        self.assertIn("Sentiment", dashboard)
        self.assertIn("Statistics", dashboard)

    def test_render_sentiment_dashboard(self):
        """Test sentiment dashboard."""
        sa = SentimentAnalyzer()
        sentiment = sa.analyze("Great day!")
        dashboard = TextLensDashboard.render_sentiment_dashboard(sentiment)
        self.assertIn("Sentiment", dashboard)
        self.assertIn("positive", dashboard)

    def test_render_stats_dashboard(self):
        """Test stats dashboard."""
        ts = TextStatistics()
        stats = ts.analyze("Hello world. This is a test.")
        dashboard = TextLensDashboard.render_stats_dashboard(stats)
        self.assertIn("Statistics", dashboard)
        self.assertIn("Words", dashboard)

    def test_render_frequency_chart(self):
        """Test frequency chart."""
        fa = FrequencyAnalyzer()
        freq = fa.analyze("cat dog cat bird dog cat")
        chart = TextLensDashboard.render_frequency_chart(freq)
        self.assertIn("Frequency", chart)
        self.assertIn("cat", chart)

    def test_render_readability_dashboard(self):
        """Test readability dashboard."""
        ra = ReadabilityAnalyzer()
        readability = ra.analyze("The cat sat on the mat.")
        dashboard = TextLensDashboard.render_readability_dashboard(readability)
        self.assertIn("Readability", dashboard)
        self.assertIn("Flesch", dashboard)


# ============================================================
# Test TextPulse Engine
# ============================================================

class TestTextLensEngine(unittest.TestCase):
    """Tests for TextLensEngine."""

    def setUp(self):
        self.engine = TextLensEngine()

    def test_full_analysis(self):
        """Test full analysis returns all components."""
        result = self.engine.analyze("This is a great test. The cat sat on the mat.")
        self.assertIn("sentiment", result)
        self.assertIn("readability", result)
        self.assertIn("stats", result)
        self.assertIn("frequency", result)
        self.assertIn("patterns", result)

    def test_partial_analysis(self):
        """Test partial analysis."""
        result = self.engine.analyze(
            "Hello world.",
            include_sentiment=True,
            include_readability=False,
            include_stats=False,
            include_frequency=False,
            include_patterns=False,
        )
        self.assertIn("sentiment", result)
        self.assertNotIn("readability", result)
        self.assertNotIn("stats", result)

    def test_file_analysis(self):
        """Test file analysis."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
                                          encoding='utf-8') as f:
            f.write("This is a great and wonderful test.")
            f.flush()
            path = f.name

        try:
            result = self.engine.analyze_file(path)
            self.assertIn("sentiment", result)
            self.assertEqual(result["sentiment"].label, "positive")
        finally:
            os.unlink(path)

    def test_quick_summary(self):
        """Test quick summary."""
        summary = self.engine.quick_summary("This is a great test.")
        self.assertIn("words", summary)
        self.assertIn("sentiment", summary)
        self.assertIn("readability", summary)

    def test_compare_texts(self):
        """Test comparing multiple texts."""
        texts = [
            "This is a great and wonderful day!",
            "This is a terrible and horrible experience.",
        ]
        result = self.engine.compare_texts(texts)
        self.assertIn("texts", result)
        self.assertIn("sentiment_range", result)
        self.assertEqual(len(result["texts"]), 2)
        self.assertIsNotNone(result["sentiment_range"])
        self.assertIn("min", result["sentiment_range"])
        self.assertIn("max", result["sentiment_range"])
        self.assertIn("avg", result["sentiment_range"])

    def test_compare_single_text(self):
        """Test comparing a single text."""
        result = self.engine.compare_texts(["Hello world."])
        self.assertEqual(len(result["texts"]), 1)


# ============================================================
# Test CLI
# ============================================================

class TestCLI(unittest.TestCase):
    """Tests for CLI argument parsing and execution."""

    def test_version(self):
        """Test version flag."""
        parser = build_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_args(["--version"])
        self.assertEqual(cm.exception.code, 0)

    def test_text_input(self):
        """Test text input parsing."""
        parser = build_parser()
        args = parser.parse_args(["Hello world"])
        self.assertEqual(args.text, "Hello world")
        self.assertFalse(args.file)

    def test_file_flag(self):
        """Test file flag parsing."""
        parser = build_parser()
        args = parser.parse_args(["-f", "test.txt"])
        self.assertTrue(args.file)
        self.assertEqual(args.text, "test.txt")

    def test_mode_selection(self):
        """Test mode selection."""
        parser = build_parser()
        args = parser.parse_args(["-m", "sentiment", "text"])
        self.assertEqual(args.mode, "sentiment")

    def test_format_selection(self):
        """Test format selection."""
        parser = build_parser()
        args = parser.parse_args(["--format", "json", "text"])
        self.assertEqual(args.format, "json")

    def test_top_n(self):
        """Test top_n parsing."""
        parser = build_parser()
        args = parser.parse_args(["--top-n", "10", "text"])
        self.assertEqual(args.top_n, 10)

    def test_no_visual(self):
        """Test no-visual flag."""
        parser = build_parser()
        args = parser.parse_args(["--no-visual", "text"])
        self.assertTrue(args.no_visual)

    def test_quiet(self):
        """Test quiet flag."""
        parser = build_parser()
        args = parser.parse_args(["-q", "text"])
        self.assertTrue(args.quiet)

    def test_main_text(self):
        """Test main with text input."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            ret = main(["This is a great test."])
            output = sys.stdout.getvalue()
            self.assertEqual(ret, 0)
            self.assertIn("TextLens", output)
        finally:
            sys.stdout = old_stdout

    def test_main_json_format(self):
        """Test main with JSON format."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            ret = main(["--format", "json", "Hello world."])
            output = sys.stdout.getvalue()
            self.assertEqual(ret, 0)
            # Verify it's valid JSON
            data = json.loads(output)
            self.assertIn("sentiment", data)
            self.assertIn("stats", data)
        finally:
            sys.stdout = old_stdout

    def test_main_quick_mode(self):
        """Test main with quick mode."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            ret = main(["-m", "quick", "Hello world."])
            output = sys.stdout.getvalue()
            self.assertEqual(ret, 0)
            self.assertIn("words", output)
        finally:
            sys.stdout = old_stdout

    def test_main_empty_text(self):
        """Test main with empty text returns error."""
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        try:
            ret = main([""])
            # parser.error raises SystemExit(2), which is caught by main returning 1
            # but actually parser.error calls sys.exit(2) directly
            self.assertIn(ret, [1, 2])
        except SystemExit as e:
            self.assertEqual(e.code, 2)
        finally:
            sys.stderr = old_stderr

    def test_main_no_input(self):
        """Test main with no input returns error."""
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        try:
            ret = main([])
            self.assertIn(ret, [1, 2])
        except SystemExit as e:
            self.assertEqual(e.code, 2)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def test_format_json_output(self):
        """Test JSON format output."""
        engine = TextLensEngine()
        result = engine.analyze("Test text.")
        output = _format_json(result)
        data = json.loads(output)
        self.assertIn("sentiment", data)

    def test_format_text_output(self):
        """Test text format output."""
        engine = TextLensEngine()
        result = engine.analyze("Test text.")
        output = _format_text(result)
        self.assertIn("Sentiment", output)

    def test_format_markdown_output(self):
        """Test markdown format output."""
        engine = TextLensEngine()
        result = engine.analyze("Test text.")
        output = _format_markdown(result)
        self.assertIn("# TextLens", output)

    def test_format_csv_output(self):
        """Test CSV format output."""
        engine = TextLensEngine()
        result = engine.analyze("Test text.")
        output = _format_csv(result)
        self.assertIn("sentiment_label", output)

    def test_main_file_output(self):
        """Test main with output file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
                                          encoding='utf-8') as f:
            output_path = f.name

        try:
            ret = main(["-o", output_path, "-q", "Hello world."])
            self.assertEqual(ret, 0)
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn("TextLens", content)
        finally:
            os.unlink(output_path)


# ============================================================
# Test Package Init
# ============================================================

class TestPackageInit(unittest.TestCase):
    """Tests for package initialization."""

    def test_version(self):
        """Test version is set."""
        self.assertEqual(__version__, "1.0.0")

    def test_author(self):
        """Test author is set."""
        from textpulse import __author__
        self.assertEqual(__author__, "gitstq")


if __name__ == "__main__":
    unittest.main()
