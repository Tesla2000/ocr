# Quick Start Guide

Get up and running with OCR in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Google Cloud account
- [ ] Vision API enabled
- [ ] API key or service account created

## Step 1: Install

```bash
cd OCR
make uv
# Or: uv sync
```

## Step 2: Get Your Vision API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Credentials"
3. Click "Create Credentials" > "API Key"
4. Copy the key

## Step 3: Create .env File

```bash
cat > .env << 'EOF'
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=paste_your_api_key_here
EOF
```

## Step 4: Prepare Your Images

Put your scanned book pages in a folder:

```bash
mkdir -p input_images
# Copy your images (.jpg, .png, etc.) to input_images/
```

## Step 5: Run OCR

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --output.type=combined \
  --output.file=./output.txt
```

## Step 6: Check Results

```bash
cat output.txt
```

Done! Your book pages are now OCR'd into text.

## Next Steps

### Add Text Cleanup

Install AI cleanup dependencies:

```bash
uv sync --group llm-cleanup-anthropic
```

Get Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)

Run with cleanup:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY
```

### Add Word Splitting

Install syllable splitting:

```bash
uv sync --group sylable-splitting
```

Run with word splitting:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --output.type=combined \
  --output.file=./output.txt \
  --output.transformations.0.type=split-long-words \
  --output.transformations.0.max-syllable-group-length=9
```

### Use Google Drive

Install Google Drive support:

```bash
uv sync --group google-drive
```

1. Create service account and download JSON key (see main README)
2. Share your Drive folder with the service account email
3. Get folder ID from URL

Run with Google Drive:

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=YOUR_FOLDER_ID \
  --output.type=combined \
  --output.file=./output.txt
```

### Sync to Cloud with RClone

Install RClone:

```bash
curl https://rclone.org/install.sh | sudo bash
rclone config  # Configure your remote
```

Run with RClone sync:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

## Common Issues

### "Vision API not enabled"
- Go to Cloud Console > APIs & Services > Library
- Search for "Cloud Vision API"
- Click Enable

### "Permission denied" for Google Drive
- Make sure you shared the folder with the service account email
- Check that the email in drive-access-key.json matches

### "Command not found: rclone"
- Install RClone: `curl https://rclone.org/install.sh | sudo bash`

### Out of memory
- Reduce concurrent tasks: `--text-extractor.n-tasks=4`

## Tips

1. **Test with a few images first** before processing a whole book
2. **Use environment variables** for repeated configurations (see .env.example)
3. **Chain transformations** to get the best results (cleanup → split words)
4. **Separate output** is better for large books (less memory usage)
5. **Monitor API quota** in Google Cloud Console

## Full Documentation

See [README.md](./README.md) for complete documentation.
