"""
TextLens CLI Entry Point
命令行入口
"""

import sys
import json
import argparse
from pathlib import Path

from . import __version__
from .analyzer import TextLensEngine
from .visualizer import TextLensDashboard


def _dataclass_to_dict(obj):
    """Convert a dataclass instance to a plain dict for JSON serialization."""
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name in obj.__dataclass_fields__:
            value = getattr(obj, field_name)
            result[field_name] = _dataclass_to_dict(value)
        return result
    elif isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_dataclass_to_dict(item) for item in obj]
    else:
        return obj


def _format_json(result: dict) -> str:
    """Format analysis result as JSON."""
    return json.dumps(_dataclass_to_dict(result), indent=2, ensure_ascii=False)


def _format_text(result: dict) -> str:
    """Format analysis result as plain text."""
    lines = []

    if "sentiment" in result:
        s = result["sentiment"]
        lines.append(f"Sentiment: {s.label} (score: {s.score:.4f}, confidence: {s.confidence:.4f})")
        lines.append(f"  Words: {s.word_count}, Sentences: {s.sentence_count}")

    if "stats" in result:
        st = result["stats"]
        lines.append(f"Statistics: {st.word_count} words, {st.sentence_count} sentences, "
                      f"{st.paragraph_count} paragraphs")
        lines.append(f"  Characters: {st.char_count}, Lines: {st.line_count}")
        lines.append(f"  Unique words: {st.unique_word_count}, "
                      f"Lexical diversity: {st.lexical_diversity:.4f}")
        lines.append(f"  Reading time: {st.reading_time_minutes:.2f} min")

    if "readability" in result:
        r = result["readability"]
        lines.append(f"Readability: Flesch={r.flesch_score:.2f}, "
                      f"Gunning Fog={r.gunning_fog:.2f}, Coleman-Liau={r.coleman_liau:.2f}")
        lines.append(f"  Grade level: {r.grade_level}")
        lines.append(f"  Avg sentence length: {r.avg_sentence_length}, "
                      f"Avg word length: {r.avg_word_length}")

    if "frequency" in result:
        f = result["frequency"]
        lines.append(f"Frequency: {f.total_unique_words} unique words")
        if f.top_n:
            top_words = ", ".join(f"{w}({c})" for w, c in f.top_n[:10])
            lines.append(f"  Top words: {top_words}")

    if "patterns" in result:
        p = result["patterns"]
        lines.append(f"Patterns: {p.questions} questions, {p.exclamations} exclamations, "
                      f"{p.passive_voice} passive voice")
        lines.append(f"  Avg complexity: {p.avg_sentence_complexity:.4f}")

    return "\n".join(lines)


def _format_markdown(result: dict) -> str:
    """Format analysis result as Markdown."""
    lines = ["# TextLens Analysis Report", ""]

    if "sentiment" in result:
        s = result["sentiment"]
        lines.append("## Sentiment")
        lines.append(f"- **Label:** {s.label}")
        lines.append(f"- **Score:** {s.score:.4f}")
        lines.append(f"- **Confidence:** {s.confidence:.4f}")
        lines.append(f"- **Words:** {s.word_count}, **Sentences:** {s.sentence_count}")
        lines.append("")

    if "stats" in result:
        st = result["stats"]
        lines.append("## Statistics")
        lines.append(f"- **Words:** {st.word_count}")
        lines.append(f"- **Sentences:** {st.sentence_count}")
        lines.append(f"- **Paragraphs:** {st.paragraph_count}")
        lines.append(f"- **Characters:** {st.char_count}")
        lines.append(f"- **Unique Words:** {st.unique_word_count}")
        lines.append(f"- **Lexical Diversity:** {st.lexical_diversity:.4f}")
        lines.append(f"- **Reading Time:** {st.reading_time_minutes:.2f} min")
        lines.append("")

    if "readability" in result:
        r = result["readability"]
        lines.append("## Readability")
        lines.append(f"- **Flesch Score:** {r.flesch_score:.2f}")
        lines.append(f"- **Gunning Fog:** {r.gunning_fog:.2f}")
        lines.append(f"- **Coleman-Liau:** {r.coleman_liau:.2f}")
        lines.append(f"- **Grade Level:** {r.grade_level}")
        lines.append("")

    if "frequency" in result:
        f = result["frequency"]
        lines.append("## Word Frequency")
        lines.append(f"**Total unique words:** {f.total_unique_words}")
        lines.append("")
        lines.append("| Word | Count |")
        lines.append("|------|-------|")
        for word, count in f.top_n:
            lines.append(f"| {word} | {count} |")
        lines.append("")

    if "patterns" in result:
        p = result["patterns"]
        lines.append("## Patterns")
        lines.append(f"- **Questions:** {p.questions}")
        lines.append(f"- **Exclamations:** {p.exclamations}")
        lines.append(f"- **Passive Voice:** {p.passive_voice}")
        lines.append(f"- **Avg Complexity:** {p.avg_sentence_complexity:.4f}")
        lines.append("")

    return "\n".join(lines)


def _format_csv(result: dict) -> str:
    """Format analysis result as CSV."""
    lines = []

    if "sentiment" in result:
        s = result["sentiment"]
        lines.append("sentiment_label,sentiment_score,confidence,word_count,sentence_count")
        lines.append(f"{s.label},{s.score},{s.confidence},{s.word_count},{s.sentence_count}")

    if "stats" in result:
        st = result["stats"]
        lines.append("char_count,word_count,sentence_count,paragraph_count,line_count,"
                      "avg_word_length,unique_word_count,lexical_diversity,reading_time_minutes")
        lines.append(f"{st.char_count},{st.word_count},{st.sentence_count},"
                      f"{st.paragraph_count},{st.line_count},{st.avg_word_length},"
                      f"{st.unique_word_count},{st.lexical_diversity},{st.reading_time_minutes}")

    if "readability" in result:
        r = result["readability"]
        lines.append("flesch_score,gunning_fog,coleman_liau,avg_sentence_length,"
                      "avg_word_length,syllable_count,grade_level")
        lines.append(f"{r.flesch_score},{r.gunning_fog},{r.coleman_liau},"
                      f"{r.avg_sentence_length},{r.avg_word_length},"
                      f"{r.syllable_count},{r.grade_level}")

    if "frequency" in result:
        f = result["frequency"]
        lines.append("word,count")
        for word, count in f.top_n:
            lines.append(f"{word},{count}")

    if "patterns" in result:
        p = result["patterns"]
        lines.append("questions,exclamations,passive_voice,avg_sentence_complexity")
        lines.append(f"{p.questions},{p.exclamations},{p.passive_voice},"
                      f"{p.avg_sentence_complexity}")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="textpulse",
        description="TextLens - Lightweight Text Analytics & Visualization Engine",
    )

    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to analyze, or a file path if -f is used",
    )

    parser.add_argument(
        "-f", "--file",
        action="store_true",
        default=False,
        help="Treat input as a file path",
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        default=False,
        help="Read text from stdin",
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path",
    )

    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="full",
        choices=["full", "quick", "sentiment", "readability", "stats",
                 "frequency", "patterns", "compare"],
        help="Analysis mode (default: full)",
    )

    parser.add_argument(
        "--format",
        type=str,
        default="dashboard",
        choices=["dashboard", "text", "json", "markdown", "csv"],
        help="Output format (default: dashboard)",
    )

    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Top N words for frequency analysis (default: 20)",
    )

    parser.add_argument(
        "--no-visual",
        action="store_true",
        default=False,
        help="Disable terminal visualization",
    )

    parser.add_argument(
        "--lang",
        type=str,
        default="auto",
        choices=["en", "zh", "auto"],
        help="Language hint (default: auto)",
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        default=False,
        help="Suppress progress messages",
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"TextLens {__version__}",
    )

    return parser


def main(argv=None):
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Determine input text
    text = None

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        if args.text:
            path = args.text
        else:
            parser.error("Please provide a file path when using -f/--file")
            return 1
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {path}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    elif args.text:
        text = args.text
    else:
        parser.error("Please provide text to analyze, use -f for a file, or --stdin")
        return 1

    if not text.strip():
        print("Error: Empty text provided", file=sys.stderr)
        return 1

    engine = TextLensEngine()

    # Determine analysis mode
    if args.mode == "quick":
        output = engine.quick_summary(text)
    elif args.mode == "sentiment":
        result = engine.analyze(
            text,
            include_sentiment=True,
            include_readability=False,
            include_stats=False,
            include_frequency=False,
            include_patterns=False,
        )
        output = _format_result(result, args)
    elif args.mode == "readability":
        result = engine.analyze(
            text,
            include_sentiment=False,
            include_readability=True,
            include_stats=False,
            include_frequency=False,
            include_patterns=False,
        )
        output = _format_result(result, args)
    elif args.mode == "stats":
        result = engine.analyze(
            text,
            include_sentiment=False,
            include_readability=False,
            include_stats=True,
            include_frequency=False,
            include_patterns=False,
        )
        output = _format_result(result, args)
    elif args.mode == "frequency":
        result = engine.analyze(
            text,
            include_sentiment=False,
            include_readability=False,
            include_stats=False,
            include_frequency=True,
            include_patterns=False,
        )
        output = _format_result(result, args)
    elif args.mode == "patterns":
        result = engine.analyze(
            text,
            include_sentiment=False,
            include_readability=False,
            include_stats=False,
            include_frequency=False,
            include_patterns=True,
        )
        output = _format_result(result, args)
    elif args.mode == "compare":
        # Split text by double newline for comparison
        texts = [t.strip() for t in text.split("\n\n") if t.strip()]
        if len(texts) < 2:
            print("Error: Need at least 2 texts separated by blank lines for comparison",
                  file=sys.stderr)
            return 1
        result = engine.compare_texts(texts)
        output = _format_json(result)
    else:
        # Full mode
        result = engine.analyze(text)
        output = _format_result(result, args)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
                f.write("\n")
            if not args.quiet:
                print(f"Output written to {args.output}")
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            return 1
    else:
        print(output)

    return 0


def _format_result(result: dict, args) -> str:
    """Format a result dict based on args."""
    fmt = args.format

    if args.no_visual and fmt == "dashboard":
        fmt = "text"

    if fmt == "dashboard":
        return TextLensDashboard.render_dashboard(result)
    elif fmt == "text":
        return _format_text(result)
    elif fmt == "json":
        return _format_json(result)
    elif fmt == "markdown":
        return _format_markdown(result)
    elif fmt == "csv":
        return _format_csv(result)
    else:
        return _format_text(result)


if __name__ == "__main__":
    sys.exit(main())
