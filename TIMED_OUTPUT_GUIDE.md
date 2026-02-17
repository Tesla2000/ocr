# Timed Output Guide

This guide explains how to use the timed output feature, which saves OCR results with duration information for each word and provides a GUI viewer.

## Overview

The timed output system consists of three main components:

1. **Duration Calculator**: Calculates duration values for each word
2. **Timed Output**: Saves words with their durations to a JSON file
3. **Timed Words Viewer** (GUI Output): Displays timed words directly in an interactive GUI

## Duration Calculator

### Default Duration Calculator

The default implementation assigns a duration of `1.0` to each word, representing a baseline equivalent of one word.

```json
{
  "type": "default"
}
```

### Creating Custom Duration Calculators

You can create custom duration calculators by extending the `DurationCalculator` base class:

```python
from typing import Literal
from ocr.output.duration._base import DurationCalculator


class CustomDurationCalculator(DurationCalculator):
    type: Literal["custom"] = "custom"

    def calculate_duration(self, word: str) -> float:
        return len(word) * 0.5
```

Don't forget to register your custom calculator in `/home/filip/PassionProjects/OCR/ocr/output/duration/__init__.py`.

## Timed Output Configuration

### Basic Configuration

```json
{
  "transformations": [],
  "outputs": [
    {
      "type": "timed",
      "path": "output/timed_words.json",
      "duration_calculator": {
        "type": "default"
      }
    }
  ]
}
```

### With Transformations

Transformations are now applied at the main level, before any outputs:

```json
{
  "transformations": [
    {
      "type": "split-long-words",
      "max_length": 15
    }
  ],
  "outputs": [
    {
      "type": "timed",
      "path": "output/timed_words.json",
      "duration_calculator": {
        "type": "default"
      }
    }
  ]
}
```

## Output Format

The timed output creates a JSON file with the following structure:

```json
[
  {
    "word": "example",
    "duration": 1.0
  },
  {
    "word": "text",
    "duration": 1.0
  }
]
```

## GUI Output (RSVP Viewer)

The `TimedWordsViewer` is an output type that displays results using Rapid Serial Visual Presentation (RSVP) - showing one word at a time in the center of the screen for its calculated duration.

### Configuration

```json
{
  "transformations": [],
  "outputs": [
    {
      "type": "timed-viewer",
      "timed_output": {
        "type": "timed",
        "path": "output/timed_words.json",
        "duration_calculator": {
          "type": "default"
        }
      },
      "reload": false
    }
  ]
}
```

The `reload` parameter controls whether to regenerate the timed output file or load from existing file.

### Features

The RSVP viewer:
- Displays words one at a time in the center of the screen
- Uses a large, readable font on a black background
- Adjustable reading speed from 100 to 1000 words per minute (WPM) with logarithmic slider
- Default speed: 300 WPM
- Provides Start, Pause, and Reset controls
- Supports spacebar to toggle play/pause
- Shows progress (current word / total words)

## Complete Examples

### Save to File Only

```bash
python -m ocr --input '{"type": "directory", "directory": "images"}' \
  --text-extractor '{"vision_client": {"type": "google", "credentials_path": "credentials.json"}}' \
  --outputs '[{"type": "timed", "path": "output/timed_words.json"}]'
```

### Display in GUI

```bash
python -m ocr --input '{"type": "directory", "directory": "images"}' \
  --text-extractor '{"vision_client": {"type": "google", "credentials_path": "credentials.json"}}' \
  --outputs '[{"type": "timed-viewer", "timed_output": {"type": "timed", "path": "output/timed_words.json"}}]'
```

### Multiple Outputs (Save to Multiple Files)

```bash
python -m ocr --input '{"type": "directory", "directory": "images"}' \
  --text-extractor '{"vision_client": {"type": "google", "credentials_path": "credentials.json"}}' \
  --outputs '[{"type": "combined", "file": "output/text.txt"}, {"type": "timed", "path": "output/timed.json"}]'
```

### With Frequency-Based Duration (Polish)

```bash
python -m ocr --input '{"type": "directory", "directory": "images"}' \
  --text-extractor '{"vision_client": {"type": "google", "credentials_path": "credentials.json"}}' \
  --outputs '[{"type": "timed-viewer", "timed_output": {"type": "timed", "path": "output/timed.json", "duration_calculator": {"type": "frequency", "language": "pl", "min_duration": 0.3, "max_duration": 2.0}}}]'
```

This will display rare Polish words for up to 2 seconds and common words for as little as 0.3 seconds.

## Duration Calculators

### Default Duration Calculator

Returns a fixed duration of 1.0 second for all words.

```json
{
  "type": "default"
}
```

### Frequency-Based Duration Calculator

Uses word frequency data to determine duration - rare words are displayed longer than common words. Requires the `wordfreq` package.

```bash
pip install wordfreq
```

Configuration:

```json
{
  "type": "frequency",
  "language": "pl",
  "min_duration": 0.5,
  "max_duration": 3.0,
  "base_frequency": 1e-5
}
```

**Parameters:**
- `language`: Language code (e.g., "pl" for Polish, "en" for English, "de" for German)
- `min_duration`: Minimum duration in seconds for very common words
- `max_duration`: Maximum duration in seconds for very rare/unknown words
- `base_frequency`: Reference frequency for normalization (adjust to tune the curve)

**How it works:**
- Common words (high frequency) → closer to `min_duration`
- Rare words (low frequency) → closer to `max_duration`
- Unknown words (zero frequency) → `max_duration`

### Custom Duration Calculators

You can create custom duration calculators based on:
- Word length
- Syllable count
- Character complexity
- Custom business logic

Example based on word length:

```python
from typing import Literal
from ocr.output.duration._base import DurationCalculator


class LengthBasedDurationCalculator(DurationCalculator):
    type: Literal["length-based"] = "length-based"
    base_duration: float = 0.5
    per_character_duration: float = 0.1

    def calculate_duration(self, word: str) -> float:
        return self.base_duration + (len(word) * self.per_character_duration)
```
