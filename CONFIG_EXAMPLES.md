# Configuration Examples

This document provides ready-to-use configuration examples for common OCR workflows.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Google Drive Examples](#google-drive-examples)
3. [RClone Examples](#rclone-examples)
4. [Transformation Examples](#transformation-examples)
5. [Complete Workflows](#complete-workflows)

---

## Basic Examples

### 1. Simplest Setup

Process local images, no transformations:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt
```

### 2. Separate Files Per Page

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=separate \
  --output.output-directory=./output_pages
```

### 3. High-Speed Processing

Process with 20 concurrent tasks:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --text-extractor.n-tasks=20 \
  --output.type=combined \
  --output.file=./output.txt
```

---

## Google Drive Examples

### 4. Read from Google Drive

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=1ABC123XYZ789 \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt
```

### 5. Write to Google Drive

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=google-drive \
  --output.credentials-path=./drive-access-key.json \
  --output.directory-id=1XYZ789ABC123 \
  --output.filename=my_book.txt
```

### 6. Google Drive to Google Drive

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=1ABC123INPUT \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=google-drive \
  --output.credentials-path=./drive-access-key.json \
  --output.directory-id=1XYZ789OUTPUT \
  --output.filename=processed_book.txt
```

### 7. Auto-Detect Latest Folder

Process the most recently modified subfolder:

```bash
python -m ocr \
  --input.type=google-drive-directory \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=1PARENT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt
```

---

## RClone Examples

### 8. Sync to Google Drive with RClone

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books/OCR \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

### 9. RClone with Separate Files

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books/OCR \
  --output.local-output.type=separate \
  --output.local-output.output-directory=./ocr_results
```

### 10. RClone to Dropbox

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=dropbox:/Documents/Books \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

### 11. RClone to Amazon S3

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=s3:my-bucket/books \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

---

## Transformation Examples

### 12. LLM Cleanup with Anthropic

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
  --output.transformations.0.llm-provider.model=claude-3-5-sonnet-20241022
```

### 13. LLM Cleanup with OpenAI

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=openai \
  --output.transformations.0.llm-provider.api-key=YOUR_OPENAI_KEY \
  --output.transformations.0.llm-provider.model=gpt-4o
```

### 14. Split Long Words (Polish)

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=split-long-words \
  --output.transformations.0.max-syllable-group-length=9 \
  --output.transformations.0.separator=" " \
  --output.transformations.0.lang=pl_PL
```

### 15. Split Long Words (English)

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=split-long-words \
  --output.transformations.0.max-syllable-group-length=8 \
  --output.transformations.0.separator=" " \
  --output.transformations.0.lang=en_US
```

### 16. Duplicate Long Words

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=duplicate-long-words \
  --output.transformations.0.max-syllable-group-length=9
```

### 17. Word Centering for Speed Reading

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=join-words-moving-center \
  --output.transformations.0.sequence-length=30 \
  --output.transformations.0.word-separator="⠀"
```

### 18. Chained Transformations: Cleanup + Split

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
  --output.transformations.1.type=split-long-words \
  --output.transformations.1.max-syllable-group-length=9
```

### 19. Triple Chain: Cleanup + Split + Center

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
  --output.transformations.1.type=split-long-words \
  --output.transformations.1.max-syllable-group-length=9 \
  --output.transformations.2.type=join-words-moving-center \
  --output.transformations.2.sequence-length=30
```

---

## Complete Workflows

### 20. Production Pipeline: Google Drive → Cleanup → RClone

```bash
python -m ocr \
  --input.type=google-drive-directory \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=1PARENT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --text-extractor.n-tasks=16 \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books/Processed \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt \
  --output.local-output.transformations.0.type=llm-cleanup \
  --output.local-output.transformations.0.llm-provider.type=anthropic \
  --output.local-output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
  --output.local-output.transformations.1.type=split-long-words \
  --output.local-output.transformations.1.max-syllable-group-length=9
```

### 21. Speed Reading Pipeline

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --text-extractor.n-tasks=12 \
  --output.type=combined \
  --output.file=./speed_reading.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
  --output.transformations.1.type=join-words-moving-center \
  --output.transformations.1.sequence-length=30
```

### 22. Archive Pipeline: Local → Separate Files → S3

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=rclone \
  --output.shared-directory=./archive \
  --output.output-path=s3:my-bucket/book-archive \
  --output.local-output.type=separate \
  --output.local-output.output-directory=./archive \
  --output.local-output.transformations.0.type=llm-cleanup \
  --output.local-output.transformations.0.llm-provider.type=openai \
  --output.local-output.transformations.0.llm-provider.api-key=YOUR_OPENAI_KEY
```

### 23. Minimal Processing (Fast, No AI)

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --text-extractor.n-tasks=24 \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=split-long-words \
  --output.transformations.0.max-syllable-group-length=9
```

### 24. Debug Mode with Logging

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.logging-level=10 \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY
```

---

## Using Configuration Files

### Create a Shell Script

Save as `run_ocr.sh`:

```bash
#!/bin/bash

VISION_KEY="your_vision_key"
ANTHROPIC_KEY="your_anthropic_key"

python -m ocr \
  --input.type=google-drive-directory \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id="$1" \
  --text-extractor.vision-client.token="$VISION_KEY" \
  --output.type=combined \
  --output.file="$2" \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key="$ANTHROPIC_KEY"
```

Usage:
```bash
chmod +x run_ocr.sh
./run_ocr.sh FOLDER_ID output.txt
```

### Using .env File

Create `.env`:

```bash
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=your_vision_key
INPUT__TYPE=directory
INPUT__INPUT_DIRECTORY=./input_images
OUTPUT__TYPE=combined
OUTPUT__FILE=./output.txt
OUTPUT__TRANSFORMATIONS__0__TYPE=split-long-words
OUTPUT__TRANSFORMATIONS__0__MAX_SYLLABLE_GROUP_LENGTH=9
```

Then run simply:

```bash
python -m ocr
```

---

## Tips for Complex Configurations

1. **Use environment variables for secrets**:
   ```bash
   export VISION_KEY=your_key
   --text-extractor.vision-client.token=$VISION_KEY
   ```

2. **Test transformations separately**:
   ```bash
   # First run without transformations
   python -m ocr ... --output.file=./raw.txt

   # Then add transformations one by one
   python -m ocr ... --output.transformations.0.type=llm-cleanup
   ```

3. **Start with low n-tasks**:
   ```bash
   # Test with 2 tasks first
   --text-extractor.n-tasks=2

   # Then scale up
   --text-extractor.n-tasks=16
   ```

4. **Use separate output for large books**:
   - Reduces memory usage
   - Easier to debug specific pages
   - Can resume processing if interrupted

5. **Monitor API costs**:
   - Vision API: ~$1.50 per 1000 images
   - LLM cleanup: varies by provider
   - RClone: free (storage costs apply)

---

For more details, see [README.md](./README.md).