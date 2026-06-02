# TextPulse

Lightweight Text Analytics & Visualization Engine.

## Features

- Sentiment Analysis
- Readability Scoring (Flesch, Gunning Fog, Coleman-Liau)
- Text Statistics
- Word Frequency Analysis
- Pattern Detection
- Terminal-based Visualization
- Zero External Dependencies

## Installation

```bash
pip install .
```

## Usage

```bash
textpulse "Your text here"
textpulse -f document.txt
echo "Analyze this" | textpulse --stdin
textpulse -f doc.txt --format json
textpulse -f doc.txt -m sentiment
```

## License

MIT License - see [LICENSE](LICENSE) for details.
