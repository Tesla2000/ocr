# Troubleshooting Guide

Common issues and solutions for the OCR system.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Google Cloud Vision API Issues](#google-cloud-vision-api-issues)
3. [Google Drive Issues](#google-drive-issues)
4. [RClone Issues](#rclone-issues)
5. [Processing Issues](#processing-issues)
6. [Transformation Issues](#transformation-issues)
7. [Performance Issues](#performance-issues)
8. [Configuration Issues](#configuration-issues)

---

## Installation Issues

### Error: "Python version not supported"

**Symptoms**: Installation fails with version error

**Cause**: Python version is too old

**Solution**:
```bash
python --version    # Should be 3.11 or higher

# Install Python 3.11+ if needed
# Ubuntu/Debian
sudo apt install python3.11

# macOS
brew install python@3.11
```

### Error: "uv: command not found"

**Symptoms**: `make uv` or `uv sync` fails

**Cause**: UV package manager not installed

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv

# Then run
uv sync
```

### Error: "No module named 'ocr'"

**Symptoms**: Import errors when running

**Cause**: Package not installed or wrong directory

**Solution**:
```bash
# Make sure you're in the project root
pwd    # Should end with /OCR

# Reinstall
uv sync

# Or activate venv
source .venv/bin/activate
```

### Error: "google-api-python-client not found"

**Symptoms**: Import error for Google Drive modules

**Cause**: Optional dependency not installed

**Solution**:
```bash
# Install Google Drive support
uv sync --group google-drive
```

---

## Google Cloud Vision API Issues

### Error: "Vision API not enabled"

**Symptoms**: `SERVICE_DISABLED` or "API not enabled" error

**Cause**: Cloud Vision API not enabled for project

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "APIs & Services" > "Library"
4. Search for "Cloud Vision API"
5. Click "Enable"

### Error: "Invalid API key"

**Symptoms**: `UNAUTHENTICATED` or "API key not valid" error

**Cause**: Incorrect or expired API key

**Solution**:
```bash
# Verify your API key
echo $TEXT_EXTRACTOR__VISION_CLIENT__TOKEN

# Create new API key if needed
# Go to: APIs & Services > Credentials > Create Credentials > API Key

# Update .env file
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=your_new_key
```

### Error: "Quota exceeded"

**Symptoms**: `RESOURCE_EXHAUSTED` or "Quota exceeded" error

**Cause**: API quota limit reached

**Solution**:
1. **Reduce concurrent tasks**:
   ```bash
   --text-extractor.n-tasks=4
   ```

2. **Check quota usage**:
   - Go to: APIs & Services > Dashboard > Vision API
   - View usage and limits

3. **Request quota increase**:
   - Click "Request quota increase"
   - Or enable billing for higher limits

4. **Wait for quota reset** (usually 24 hours)

### Error: "Vision API error: Image too large"

**Symptoms**: `INVALID_ARGUMENT` for large images

**Cause**: Image exceeds size limits (20MB)

**Solution**:
```bash
# Compress images before processing
find ./input_images -name "*.jpg" -exec mogrify -resize 80% {} \;

# Or use ImageMagick
for img in ./input_images/*.jpg; do
  convert "$img" -quality 85 -resize 4096x4096\> "$img"
done
```

### Error: "Permission denied on service account"

**Symptoms**: `PERMISSION_DENIED` with service account

**Cause**: Service account missing Vision API role

**Solution**:
1. Go to: IAM & Admin > IAM
2. Find your service account
3. Click "Edit"
4. Add role: "Cloud Vision API User"
5. Save

---

## Google Drive Issues

### Error: "Credentials file not found"

**Symptoms**: `ValueError: Credentials file does not exist`

**Cause**: Invalid path to credentials JSON

**Solution**:
```bash
# Check file exists
ls -la drive-access-key.json

# If not, download it again from Google Cloud Console
# Go to: IAM & Admin > Service Accounts > Your Account > Keys

# Use absolute path if needed
--input.credentials-path=/full/path/to/drive-access-key.json
```

### Error: "Insufficient Permission"

**Symptoms**: `HttpError 403: Insufficient Permission`

**Cause**: Folder not shared with service account

**Solution**:
1. Open Google Drive
2. Find the folder (check folder ID in URL)
3. Right-click > "Share"
4. Add service account email from JSON file (`client_email`)
5. Grant "Viewer" (for input) or "Editor" (for output)
6. Ensure "Notify people" is unchecked

### Error: "Invalid folder ID"

**Symptoms**: `HttpError 404: File not found`

**Cause**: Incorrect folder ID

**Solution**:
```bash
# Get folder ID from URL
# https://drive.google.com/drive/folders/1ABC123XYZ
# Folder ID: 1ABC123XYZ

# Verify folder exists and is shared
# Try listing contents with gcloud or check Drive web interface
```

### Error: "Google Drive API not enabled"

**Symptoms**: `SERVICE_DISABLED` for Drive API

**Cause**: Google Drive API not enabled

**Solution**:
1. Go to: APIs & Services > Library
2. Search for "Google Drive API"
3. Click "Enable"

### Error: "No images found in folder"

**Symptoms**: Empty tuple returned, no processing

**Cause**: No supported image formats or folder is empty

**Solution**:
```bash
# Check folder contents via web interface

# Verify file extensions
# Supported: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .webp

# Check if files are in subdirectories (not supported by default)
# Move all images to the main folder
```

### Error: "Token expired"

**Symptoms**: `HttpError 401: Invalid Credentials`

**Cause**: Service account key expired or revoked

**Solution**:
1. Go to: IAM & Admin > Service Accounts
2. Find your service account
3. Keys tab > Add Key > Create new key > JSON
4. Replace old JSON file
5. Retry

---

## RClone Issues

### Error: "rclone: command not found"

**Symptoms**: Shell can't find rclone

**Cause**: RClone not installed or not in PATH

**Solution**:
```bash
# Install RClone
curl https://rclone.org/install.sh | sudo bash

# Verify
rclone version

# If still not found, add to PATH
export PATH=$PATH:/usr/local/bin
```

### Error: "Remote not found"

**Symptoms**: `Failed to create file system for "REMOTE:"`

**Cause**: Remote not configured or wrong name

**Solution**:
```bash
# List configured remotes
rclone listremotes

# Reconfigure if needed
rclone config

# Use exact remote name (case-sensitive)
--output.output-path=gdrive:/path    # If remote is "gdrive"
```

### Error: "OAuth token expired"

**Symptoms**: `401 Unauthorized` during sync

**Cause**: OAuth token needs refresh

**Solution**:
```bash
# Reconnect the remote
rclone config reconnect gdrive:

# Or reconfigure
rclone config
# Choose the remote > reconnect
```

### Error: "Sync failed: directory not empty"

**Symptoms**: RClone refuses to sync

**Cause**: Using `sync` instead of `copy` incorrectly

**Solution**:
```bash
# The OCR system uses `copy` by default
# If you're running rclone manually, use:
rclone copy source dest    # Safer

# Only use sync if you want mirroring (deletes extra files)
rclone sync source dest --dry-run    # Test first
```

---

## Processing Issues

### Error: "No images to process"

**Symptoms**: Script exits immediately, no OCR performed

**Cause**:
- Empty input directory
- No supported image formats
- Wrong path

**Solution**:
```bash
# Check directory exists and contains images
ls -la ./input_images/

# Verify file extensions
# Supported: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .webp

# Check directory path is correct
--input.input-directory=/absolute/path/to/images
```

### Error: "OCR returns empty text"

**Symptoms**: Output files created but empty

**Cause**:
- Poor image quality
- Non-text images
- Wrong language detection

**Solution**:
1. **Improve image quality**:
   ```bash
   # Enhance contrast
   convert input.jpg -normalize -contrast enhanced.jpg
   ```

2. **Check image content**: Ensure images contain readable text

3. **Try different images**: Test with a known good image

### Error: "Out of memory"

**Symptoms**: `MemoryError` or system freeze

**Cause**: Too many concurrent tasks or large images

**Solution**:
```bash
# Reduce concurrent tasks
--text-extractor.n-tasks=4

# Use separate output instead of combined
--output.type=separate

# Process in smaller batches
# Split images into multiple folders

# Use /dev/shm for temp files (RAM disk)
--input.temp-directory=/dev/shm/ocr_temp
```

### Error: "Task timeout"

**Symptoms**: Processing hangs indefinitely

**Cause**: Network issues or API problems

**Solution**:
```bash
# Check network connectivity
ping google.com

# Check API status
# Visit: https://status.cloud.google.com/

# Reduce concurrent tasks to isolate issue
--text-extractor.n-tasks=1
```

---

## Transformation Issues

### Error: "Module 'pyphen' not found"

**Symptoms**: Import error when using split-long-words

**Cause**: Syllable splitting dependency not installed

**Solution**:
```bash
uv sync --group sylable-splitting
```

### Error: "Module 'anthropic' not found"

**Symptoms**: Import error when using LLM cleanup

**Cause**: LLM cleanup dependency not installed

**Solution**:
```bash
# For Anthropic
uv sync --group llm-cleanup-anthropic

# For OpenAI
uv sync --group llm-cleanup-openai
```

### Error: "API rate limit exceeded" (LLM)

**Symptoms**: `RateLimitError` during cleanup

**Cause**: Too many API requests

**Solution**:
1. **Reduce batch size**: Process fewer pages at once

2. **Add delays**: Process in multiple runs with time between

3. **Upgrade API tier**: Contact provider for higher limits

4. **Use separate output**: Process pages individually with delays

### Error: "LLM returns incomplete text"

**Symptoms**: Cleaned text is truncated

**Cause**: Model output token limit reached

**Solution**:
1. **Use separate output**: Process pages individually
   ```bash
   --output.type=separate
   ```

2. **Use a model with higher limits**:
   ```bash
   # For Anthropic
   --output.transformations.0.llm-provider.model=claude-3-opus-20240229

   # For OpenAI
   --output.transformations.0.llm-provider.model=gpt-4-turbo
   ```

3. **Split into smaller chunks**: Don't use combined output for large books

### Error: "Invalid language code"

**Symptoms**: `ValueError` in split-long-words

**Cause**: Unsupported language code

**Solution**:
```bash
# Use correct pyphen language codes
# Common codes:
# - en_US (English)
# - pl_PL (Polish)
# - de_DE (German)
# - fr_FR (French)
# - es_ES (Spanish)

# List available languages
python -c "from pyphen import LANGUAGES; print(list(LANGUAGES.keys()))"

# Use correct code
--output.transformations.0.lang=en_US
```

---

## Performance Issues

### Problem: Processing is too slow

**Symptoms**: Takes hours to process a book

**Solutions**:

1. **Increase concurrent tasks**:
   ```bash
   --text-extractor.n-tasks=20
   ```

2. **Use /dev/shm for temp files**:
   ```bash
   --input.temp-directory=/dev/shm/ocr
   ```

3. **Disable transformations for testing**:
   ```bash
   # Remove --output.transformations.* flags
   ```

4. **Process in parallel manually**:
   ```bash
   # Split images into folders
   # Run multiple OCR instances
   python -m ocr --input.input-directory=./batch1 ... &
   python -m ocr --input.input-directory=./batch2 ... &
   ```

5. **Use faster model** (if using LLM cleanup):
   ```bash
   --output.transformations.0.llm-provider.model=claude-3-haiku-20240307
   ```

### Problem: High API costs

**Symptoms**: Unexpected bills

**Solutions**:

1. **Monitor usage**:
   - Check Google Cloud Console for Vision API usage
   - Check LLM provider dashboard

2. **Reduce concurrent tasks**:
   ```bash
   --text-extractor.n-tasks=4
   ```

3. **Test with small batches first**

4. **Use cheaper LLM models**:
   ```bash
   # Anthropic Haiku (cheapest)
   --output.transformations.0.llm-provider.model=claude-3-haiku-20240307

   # OpenAI GPT-3.5 (cheaper than GPT-4)
   --output.transformations.0.llm-provider.model=gpt-3.5-turbo
   ```

5. **Skip LLM cleanup for simple texts**:
   - Only use cleanup when necessary
   - Use split-long-words alone for simple formatting

---

## Configuration Issues

### Error: "Unrecognized arguments"

**Symptoms**: `error: unrecognized arguments: --some-flag`

**Cause**: Typo or wrong parameter name

**Solution**:
```bash
# Check parameter names (case-sensitive, use kebab-case)
# Correct:
--input.type=directory
--input.input-directory=/path

# Incorrect:
--input.type=Directory          # wrong case
--input.input_directory=/path   # wrong separator
--inputType=directory            # wrong format
```

### Error: "Pydantic validation error"

**Symptoms**: `ValidationError` with detailed field errors

**Cause**: Invalid configuration values

**Solution**:
1. **Read error message carefully**: Shows which field is invalid

2. **Check types**:
   ```bash
   # Numbers shouldn't be quoted
   --text-extractor.n-tasks=12    # Correct
   --text-extractor.n-tasks="12"  # May cause issues
   ```

3. **Check required fields**: Ensure all mandatory fields are provided

4. **Check discriminators**:
   ```bash
   # Must specify type for polymorphic fields
   --input.type=directory
   --output.type=combined
   --output.transformations.0.type=split-long-words
   ```

### Error: "Environment variable not loaded"

**Symptoms**: Values from .env file not used

**Cause**:
- .env file in wrong location
- Wrong naming format

**Solution**:
```bash
# .env must be in the directory where you run the command
pwd
ls -la .env

# Use correct format (double underscore for nesting)
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=key
INPUT__TYPE=directory

# Not:
TEXT_EXTRACTOR.VISION_CLIENT.TOKEN=key    # Wrong separator
```

### Error: "Field required"

**Symptoms**: `Field required` for a configuration field

**Cause**: Missing required parameter

**Solution**:
```bash
# Check error message for which field is required
# Example: If "file" is required for combined output:

--output.type=combined \
--output.file=./output.txt    # Must specify file

# Example: If "directory-id" is required for Google Drive:

--input.type=google-drive \
--input.credentials-path=./key.json \
--input.directory-id=1ABC123    # Must specify ID
```

---

## Getting Help

### Enable Debug Logging

```bash
# For LLM cleanup
--output.transformations.0.logging-level=10

# For Python exceptions
python -m ocr ... 2>&1 | tee debug.log
```

### Check System Info

```bash
# Python version
python --version

# Installed packages
uv pip list

# RClone version
rclone version

# Disk space
df -h

# Memory
free -h
```

### Test Components Individually

```bash
# Test Vision API
python -c "
from ocr.vision_client import VisionClient
from pathlib import Path
client = VisionClient(token='YOUR_KEY')
text = client.extract_text(Path('./test.jpg'))
print(text)
"

# Test Google Drive
python -c "
from ocr.input.google_drive import GoogleDriveInput
from pathlib import Path
input_obj = GoogleDriveInput(
    credentials_path=Path('./drive-access-key.json'),
    directory_id='YOUR_FOLDER_ID'
)
images = input_obj.get_images()
print(f'Found {len(images)} images')
"

# Test RClone
rclone ls gdrive:
```

### Report Issues

If you can't resolve the issue:

1. Check existing issues on GitHub
2. Gather diagnostic info:
   - Python version
   - OS and version
   - Error message (full traceback)
   - Configuration used (remove secrets)
3. Create minimal reproduction example
4. Open new issue with all details

---

## Additional Resources

- [README.md](./README.md) - Main documentation
- [QUICKSTART.md](./QUICKSTART.md) - Quick start guide
- [CONFIG_EXAMPLES.md](./CONFIG_EXAMPLES.md) - Configuration examples
- [RCLONE_GUIDE.md](./RCLONE_GUIDE.md) - RClone detailed guide

---

**Still having issues?** Open an issue on GitHub with:
- Full error message
- Your configuration (remove API keys)
- Steps to reproduce
- System information
