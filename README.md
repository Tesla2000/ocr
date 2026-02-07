# OCR Book Page Processor

A Python-based OCR (Optical Character Recognition) system for processing book pages using Google Cloud Vision API. The system supports multiple input sources (local directories, Google Drive), customizable text transformations, and flexible output options including RClone for cloud storage synchronization.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Google Cloud Setup](#google-cloud-setup)
- [Google Drive Setup](#google-drive-setup)
- [RClone Setup](#rclone-setup)
- [Configuration](#configuration)
- [Input Options](#input-options)
- [Text Transformations](#text-transformations)
- [Output Options](#output-options)
- [Usage Examples](#usage-examples)
- [Advanced Usage](#advanced-usage)

## Features

- **Multiple Input Sources**:
  - Local directory scanning
  - Google Drive folder access
  - Google Drive with automatic latest folder detection

- **Powerful Text Processing**:
  - OCR text extraction via Google Cloud Vision API
  - Syllable-based word splitting for long words
  - Word centering for improved readability
  - AI-powered text cleanup (OCR error correction, header/footer removal)

- **Flexible Output Options**:
  - Combined text file output
  - Separate files per page
  - Direct Google Drive upload
  - RClone synchronization to cloud storage

## Prerequisites

- Python 3.11 or higher
- Google Cloud account with Vision API enabled
- (Optional) Google Drive service account for Drive integration
- (Optional) RClone for cloud storage synchronization
- (Optional) OpenAI or Anthropic API key for LLM-based text cleanup

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd OCR
```

### 2. Install dependencies using uv

```bash
make uv
```

Or manually:

```bash
uv sync
```

### 3. Install optional dependency groups

Depending on your needs, install additional dependency groups:

```bash
# For Google Drive integration
uv sync --group google-drive

# For syllable splitting (Polish language support)
uv sync --group sylable-splitting

# For LLM cleanup with Anthropic Claude
uv sync --group llm-cleanup-anthropic

# For LLM cleanup with OpenAI
uv sync --group llm-cleanup-openai

# Install all optional dependencies
uv sync --all-groups
```

## Google Cloud Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID

### 2. Enable Vision API

1. Navigate to "APIs & Services" > "Library"
2. Search for "Cloud Vision API"
3. Click "Enable"

### 3. Create API Credentials

#### Option A: API Key (Simplest)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy the generated API key
4. (Recommended) Click "Restrict Key" and limit it to Vision API only

#### Option B: Service Account (For production)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details
4. Grant the "Cloud Vision API User" role
5. Create and download the JSON key file

### 4. Store Your Credentials

Create a `.env` file in the project root:

```bash
# For API Key approach
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=your_api_key_here
```

## Google Drive Setup

If you want to read images from or write results to Google Drive, follow these steps:

### 1. Create a Service Account

1. In Google Cloud Console, go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "ocr-drive-access")
4. Grant it the "Editor" role (or more restrictive permissions)
5. Click "Create Key" and choose JSON format
6. Save the file as `drive-access-key.json` in your project root

### 2. Enable Google Drive API

1. Go to "APIs & Services" > "Library"
2. Search for "Google Drive API"
3. Click "Enable"

### 3. Share Folders with Service Account

1. Open Google Drive
2. Find the folder you want to process
3. Right-click > "Share"
4. Add the service account email (found in the JSON file: `client_email`)
5. Grant appropriate permissions:
   - "Viewer" for input folders
   - "Editor" for output folders
6. Note the folder ID from the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

## RClone Setup

RClone allows you to sync OCR results to various cloud storage providers.

### 1. Install RClone

#### Linux/Mac:
```bash
curl https://rclone.org/install.sh | sudo bash
```

#### Windows:
Download from [rclone.org/downloads](https://rclone.org/downloads/)

### 2. Configure RClone Remote

Configure a remote storage provider:

```bash
rclone config
```

Follow the interactive prompts. Common examples:

#### Google Drive:
```
n) New remote
name> gdrive
Storage> drive
client_id> (leave empty or use custom)
client_secret> (leave empty or use custom)
scope> 1 (Full access)
# Follow browser authentication
```

#### Dropbox:
```
n) New remote
name> dropbox
Storage> dropbox
# Follow browser authentication
```

#### Amazon S3:
```
n) New remote
name> s3
Storage> s3
provider> AWS
env_auth> false
access_key_id> YOUR_ACCESS_KEY
secret_access_key> YOUR_SECRET_KEY
region> us-east-1
```

### 3. Test Your Configuration

```bash
# List remotes
rclone listremotes

# Test connection
rclone ls gdrive:
```

## Configuration

The application uses Pydantic Settings for configuration, supporting:
- Command-line arguments (kebab-case: `--input-directory`)
- Environment variables (with `__` as nested delimiter)
- `.env` file

### Environment Variables

Create a `.env` file:

```bash
# Google Cloud Vision API Token
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=your_vision_api_key

# Optional: OpenAI API Key for LLM cleanup
OUTPUT__TRANSFORMATIONS__0__LLM_PROVIDER__API_KEY=your_openai_key

# Optional: Anthropic API Key for LLM cleanup
OUTPUT__TRANSFORMATIONS__0__LLM_PROVIDER__API_KEY=your_anthropic_key

# Optional: Number of concurrent OCR tasks (default: 12)
TEXT_EXTRACTOR__N_TASKS=12
```

## Input Options

### 1. Local Directory Input

Process images from a local directory:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=/path/to/images \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=output.txt
```

**Supported image formats**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.webp`

Files are processed in order of modification time.

### 2. Google Drive Folder Input

Process images from a specific Google Drive folder:

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=drive-access-key.json \
  --input.directory-id=YOUR_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=output.txt
```

**Features**:
- Downloads images to `/dev/shm` (RAM disk) for faster processing
- Processes files in alphabetical order by name
- Only downloads supported image formats

### 3. Google Drive Directory (Latest Folder)

Automatically finds and processes the most recently modified subfolder:

```bash
python -m ocr \
  --input.type=google-drive-directory \
  --input.credentials-path=drive-access-key.json \
  --input.directory-id=PARENT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=output.txt
```

**Use case**: When you regularly add new folders with scanned pages, and always want to process the latest one.

## Text Transformations

Transformations are applied sequentially to the OCR output before saving. They can be chained together.

### 1. Split Long Words

Splits long words into manageable chunks based on syllable boundaries.

```bash
--output.transformations.0.type=split-long-words \
--output.transformations.0.max-syllable-group-length=9 \
--output.transformations.0.separator=" " \
--output.transformations.0.lang=pl_PL
```

**Parameters**:
- `max-syllable-group-length` (default: 9): Maximum characters per syllable group
- `separator` (default: " "): Separator between syllable groups
- `lang` (default: "pl_PL"): Language for syllable detection

**Example**:
```
Input:  "międzynarodowy"
Output: "między naro dowy"
```

### 2. Duplicate Long Words

Duplicates long words multiple times based on their length to improve readability for speed reading applications.

```bash
--output.transformations.0.type=duplicate-long-words \
--output.transformations.0.max-syllable-group-length=9
```

**Parameters**:
- `max-syllable-group-length` (default: 9): Maximum characters per syllable group

**How it works**:
- Words are duplicated based on `ceil(word_length / max_syllable_group_length)`
- Helps with speed reading by repeating longer words

**Example**:
```
Input:  "internationalization"
Output: "internationalization internationalization internationalization"
```

### 3. Join Words Moving Center

Centers words within fixed-width lines for improved readability (useful for speed reading):

```bash
--output.transformations.0.type=join-words-moving-center \
--output.transformations.0.sequence-length=30 \
--output.transformations.0.word-separator="⠀"
```

**Parameters**:
- `sequence-length` (default: 30): Fixed line width
- `word-separator` (default: "⠀" - Braille blank): Character between words

**Example output**:
```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀The⠀quick⠀
⠀⠀⠀⠀⠀The⠀quick⠀brown⠀
⠀⠀quick⠀brown⠀fox⠀jumps⠀
```

### 4. LLM Cleanup

Uses AI to clean up OCR errors, remove headers/footers, and improve text quality.

#### Using Anthropic Claude:

```bash
--output.transformations.0.type=llm-cleanup \
--output.transformations.0.llm-provider.type=anthropic \
--output.transformations.0.llm-provider.api-key=YOUR_ANTHROPIC_KEY \
--output.transformations.0.llm-provider.model=claude-3-5-sonnet-20241022
```

#### Using OpenAI:

```bash
--output.transformations.0.type=llm-cleanup \
--output.transformations.0.llm-provider.type=openai \
--output.transformations.0.llm-provider.api-key=YOUR_OPENAI_KEY \
--output.transformations.0.llm-provider.model=gpt-4
```

**Parameters**:
- `logging-level` (default: INFO): Logging verbosity
- `llm-provider.type`: "anthropic" or "openai"
- `llm-provider.api-key`: Your API key
- `llm-provider.model`: Model to use
- `system-prompt`: (optional) Custom system prompt

**What it does**:
- Fixes OCR mistakes and typos
- Removes page numbers
- Removes chapter titles and headers
- Removes footers and repeated elements
- Preserves actual content and paragraph structure
- Fixes formatting issues

### Chaining Transformations

You can chain multiple transformations:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=output.txt \
  --output.transformations.0.type=llm-cleanup \
  --output.transformations.0.llm-provider.type=anthropic \
  --output.transformations.0.llm-provider.api-key=YOUR_KEY \
  --output.transformations.1.type=split-long-words \
  --output.transformations.1.max-syllable-group-length=9
```

## Output Options

### 1. Combined Output

Saves all OCR results into a single text file:

```bash
--output.type=combined \
--output.file=/path/to/output.txt
```

Pages are joined with newlines.

### 2. Separate Output

Saves each page as a separate file:

```bash
--output.type=separate \
--output.output-directory=/path/to/output/
```

Files are named sequentially: `1.txt`, `2.txt`, `3.txt`, etc.

### 3. Google Drive Output

Uploads the combined result directly to Google Drive:

```bash
--output.type=google-drive \
--output.credentials-path=drive-access-key.json \
--output.directory-id=OUTPUT_FOLDER_ID \
--output.filename=ocr_result.txt
```

**Note**: The service account must have write access to the folder.

### 4. RClone Output

Saves locally first, then syncs to cloud storage using RClone:

```bash
--output.type=rclone \
--output.shared-directory=/path/to/local/dir \
--output.output-path=gdrive:/remote/path \
--output.local-output.type=combined \
--output.local-output.file=/path/to/local/dir/output.txt
```

**Parameters**:
- `shared-directory`: Local directory to sync
- `output-path`: RClone remote path (format: `remote_name:/path`)
- `local-output`: Nested local output configuration (can be `combined` or `separate`)

**Important**: Transformations are applied at the `local-output` level, not at the RClone level.

**Example with separate files**:

```bash
--output.type=rclone \
--output.shared-directory=/tmp/ocr_output \
--output.output-path=gdrive:/OCR/Results \
--output.local-output.type=separate \
--output.local-output.output-directory=/tmp/ocr_output \
--output.local-output.transformations.0.type=split-long-words
```

## Usage Examples

### Example 1: Basic Local Processing

Process local images and save to a single file:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=./output/result.txt
```

### Example 2: Google Drive to Google Drive

Read from Google Drive, process, and write back to Drive:

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=INPUT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=google-drive \
  --output.credentials-path=./drive-access-key.json \
  --output.directory-id=OUTPUT_FOLDER_ID \
  --output.filename=processed_book.txt
```

### Example 3: Complete Processing Pipeline

Latest Google Drive folder → OCR → LLM cleanup → Word splitting → RClone to cloud:

```bash
python -m ocr \
  --input.type=google-drive-directory \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=PARENT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_VISION_KEY \
  --text-extractor.n-tasks=16 \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books/Processed \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt \
  --output.local-output.transformations.0.type=llm-cleanup \
  --output.local-output.transformations.0.llm-provider.type=anthropic \
  --output.local-output.transformations.0.llm-provider.api-key=YOUR_CLAUDE_KEY \
  --output.local-output.transformations.1.type=split-long-words \
  --output.local-output.transformations.1.max-syllable-group-length=9
```

### Example 4: Speed Reading Format

Generate centered text for speed reading apps:

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./input_images \
  --text-extractor.vision-client.token=YOUR_API_KEY \
  --output.type=combined \
  --output.file=./output/speed_read.txt \
  --output.transformations.0.type=join-words-moving-center \
  --output.transformations.0.sequence-length=30
```

### Example 5: Using Environment Variables

Create a `.env` file:

```bash
TEXT_EXTRACTOR__VISION_CLIENT__TOKEN=your_vision_key
INPUT__TYPE=directory
INPUT__INPUT_DIRECTORY=/home/user/scans
OUTPUT__TYPE=combined
OUTPUT__FILE=/home/user/output.txt
OUTPUT__TRANSFORMATIONS__0__TYPE=split-long-words
```

Then run simply:

```bash
python -m ocr
```

## Advanced Usage

### Adjusting Concurrency

Control the number of parallel OCR requests:

```bash
--text-extractor.n-tasks=20
```

Higher values = faster processing but more API quota usage.

### Custom LLM System Prompt

Modify the cleanup behavior:

```bash
--output.transformations.0.type=llm-cleanup \
--output.transformations.0.system-prompt="Fix OCR errors only, keep all formatting"
```

### Debugging Transformations

Enable debug logging for LLM cleanup:

```bash
--output.transformations.0.type=llm-cleanup \
--output.transformations.0.logging-level=10
```

Logging levels:
- `50`: CRITICAL
- `40`: ERROR
- `30`: WARNING
- `20`: INFO (default)
- `10`: DEBUG

### Processing Specific Image Formats

The system auto-detects supported formats. To process only specific types, filter your input directory:

```bash
# Process only PNG files
find ./input_images -type f ! -name "*.png" -delete
```

### RClone Advanced Options

For more complex RClone configurations, you can run RClone separately after processing:

```bash
# Use combined output without rclone wrapper
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=combined \
  --output.file=./result.txt

# Then sync with custom rclone flags
rclone sync ./result.txt gdrive:/Books/ \
  --progress \
  --transfers 4 \
  --checkers 8
```

### Batch Processing Multiple Folders

Create a bash script:

```bash
#!/bin/bash

for folder in /path/to/scans/*/; do
  folder_name=$(basename "$folder")
  python -m ocr \
    --input.type=directory \
    --input.input-directory="$folder" \
    --text-extractor.vision-client.token="$VISION_KEY" \
    --output.type=combined \
    --output.file="./output/${folder_name}.txt"
done
```

## Troubleshooting

### Vision API Quota Exceeded

**Error**: `Resource has been exhausted`

**Solution**:
- Reduce `--text-extractor.n-tasks`
- Request quota increase in Google Cloud Console
- Enable billing for higher limits

### Google Drive Permission Denied

**Error**: `Insufficient Permission`

**Solution**:
- Ensure the folder is shared with the service account email
- Check the service account has the correct scopes
- Verify the folder ID is correct

### RClone Not Found

**Error**: `rclone: command not found`

**Solution**:
- Install RClone: `curl https://rclone.org/install.sh | sudo bash`
- Ensure RClone is in your PATH

### LLM Cleanup API Errors

**Error**: `API key invalid` or `Rate limit exceeded`

**Solution**:
- Verify your API key is correct
- Check your API quota/billing
- Consider using a different model or reducing request rate

### Memory Issues

**Error**: Out of memory during processing

**Solution**:
- Reduce `--text-extractor.n-tasks`
- Process in smaller batches
- Use separate output instead of combined for large books

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please submit issues and pull requests.

## Support

For issues or questions, please open an issue on GitHub.