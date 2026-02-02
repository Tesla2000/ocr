# RClone Integration Guide

Complete guide for setting up and using RClone with the OCR system to sync your processed text to cloud storage.

## What is RClone?

RClone is a command-line program to manage files on cloud storage. It supports over 40 cloud storage providers including:
- Google Drive
- Dropbox
- Amazon S3
- Microsoft OneDrive
- Box
- Backblaze B2
- And many more

The OCR system integrates RClone to automatically sync your processed OCR results to your preferred cloud storage.

## Installation

### Linux

```bash
curl https://rclone.org/install.sh | sudo bash
```

### macOS

```bash
brew install rclone
```

Or using the install script:

```bash
curl https://rclone.org/install.sh | sudo bash
```

### Windows

Download from [rclone.org/downloads](https://rclone.org/downloads/) and add to PATH, or use:

```powershell
choco install rclone
```

### Verify Installation

```bash
rclone version
```

## Configuration

### Interactive Configuration

```bash
rclone config
```

This launches an interactive wizard. Below are detailed examples for popular providers.

---

## Google Drive Setup

### Step 1: Start Configuration

```bash
rclone config
```

### Step 2: Create New Remote

```
n) New remote
name> gdrive
```

### Step 3: Choose Google Drive

```
Storage> drive
```

### Step 4: Configure OAuth (Recommended)

```
client_id> (press Enter to use default)
client_secret> (press Enter to use default)
scope> 1    # Full access to all files
```

### Step 5: Advanced Config

```
Edit advanced config? n
```

### Step 6: Auto Config

```
Use auto config? y    # Opens browser for authentication
```

### Step 7: Shared Drive (Optional)

```
Configure this as a Shared Drive? n    # Unless using Team Drive
```

### Step 8: Confirm

```
y) Yes this is OK
q) Quit config
```

### Test Google Drive

```bash
# List root directory
rclone ls gdrive:

# Create test file
echo "test" > test.txt
rclone copy test.txt gdrive:/OCR/test/

# Verify
rclone ls gdrive:/OCR/test/
```

---

## Dropbox Setup

### Step 1: Start Configuration

```bash
rclone config
```

### Step 2: Create New Remote

```
n) New remote
name> dropbox
```

### Step 3: Choose Dropbox

```
Storage> dropbox
```

### Step 4: OAuth Configuration

```
client_id> (press Enter)
client_secret> (press Enter)
```

### Step 5: Auto Config

```
Use auto config? y    # Opens browser
```

### Step 6: Confirm

```
y) Yes this is OK
q) Quit config
```

### Test Dropbox

```bash
rclone ls dropbox:
```

---

## Amazon S3 Setup

### Step 1: Get AWS Credentials

1. Log into AWS Console
2. Go to IAM → Users → Your User → Security Credentials
3. Create Access Key
4. Note the Access Key ID and Secret Access Key

### Step 2: Start Configuration

```bash
rclone config
```

### Step 3: Create New Remote

```
n) New remote
name> s3
```

### Step 4: Choose S3

```
Storage> s3
provider> AWS
```

### Step 5: Enter Credentials

```
env_auth> false
access_key_id> YOUR_ACCESS_KEY_ID
secret_access_key> YOUR_SECRET_ACCESS_KEY
region> us-east-1    # Or your preferred region
```

### Step 6: Endpoint and Location

```
endpoint> (press Enter for default)
location_constraint> (press Enter)
acl> private
```

### Step 7: Confirm

```
Edit advanced config? n
y) Yes this is OK
q) Quit config
```

### Test S3

```bash
# List buckets
rclone lsd s3:

# List bucket contents
rclone ls s3:my-bucket/
```

---

## Microsoft OneDrive Setup

### Step 1: Start Configuration

```bash
rclone config
```

### Step 2: Create New Remote

```
n) New remote
name> onedrive
```

### Step 3: Choose OneDrive

```
Storage> onedrive
```

### Step 4: OAuth

```
client_id> (press Enter)
client_secret> (press Enter)
```

### Step 5: Region

```
region> 1    # Microsoft Cloud Global
```

### Step 6: Auto Config

```
Use auto config? y    # Opens browser
```

### Step 7: Drive Type

```
Type of connection> 1    # OneDrive Personal or Business
```

### Step 8: Choose Drive

```
# Select your drive from the list
0    # Usually your main drive
```

### Step 9: Confirm

```
y) Yes this is OK
q) Quit config
```

---

## Using RClone with OCR

### Basic Syntax

```bash
python -m ocr \
  --output.type=rclone \
  --output.shared-directory=LOCAL_DIR \
  --output.output-path=REMOTE:PATH \
  --output.local-output.type=TYPE \
  --output.local-output.PARAMS
```

### Key Parameters

- `shared-directory`: Local directory where files are saved before syncing
- `output-path`: RClone remote path (format: `remote_name:/path`)
- `local-output`: Configuration for the local output (combined or separate)

---

## Common Usage Patterns

### 1. Combined File to Google Drive

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=gdrive:/Books/Processed \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

### 2. Separate Files to Dropbox

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=dropbox:/Documents/OCR \
  --output.local-output.type=separate \
  --output.local-output.output-directory=./ocr_results
```

### 3. With Transformations to S3

```bash
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=s3:my-bucket/books \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt \
  --output.local-output.transformations.0.type=llm-cleanup \
  --output.local-output.transformations.0.llm-provider.type=anthropic \
  --output.local-output.transformations.0.llm-provider.api-key=YOUR_KEY
```

### 4. Google Drive Input → Process → OneDrive Output

```bash
python -m ocr \
  --input.type=google-drive \
  --input.credentials-path=./drive-access-key.json \
  --input.directory-id=INPUT_FOLDER_ID \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=rclone \
  --output.shared-directory=./ocr_results \
  --output.output-path=onedrive:/Documents/Books \
  --output.local-output.type=combined \
  --output.local-output.file=./ocr_results/book.txt
```

---

## Advanced RClone Options

If you need more control over the sync process, you can run RClone separately after OCR processing:

### 1. Sync with Progress

```bash
# Run OCR first
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=combined \
  --output.file=./result.txt

# Then sync with progress
rclone sync ./result.txt gdrive:/Books/ --progress
```

### 2. Copy with Bandwidth Limit

```bash
rclone copy ./ocr_results gdrive:/Books/ \
  --bwlimit 1M \
  --progress
```

### 3. Sync with Filters

```bash
# Only sync .txt files
rclone sync ./ocr_results gdrive:/Books/ \
  --include "*.txt" \
  --progress
```

### 4. Sync with Encryption

```bash
# Configure encrypted remote first
rclone config
# Then sync
rclone sync ./ocr_results encrypted_remote:/Books/
```

### 5. Verify Sync

```bash
rclone check ./ocr_results gdrive:/Books/
```

---

## RClone Commands Reference

### List Operations

```bash
# List directories only
rclone lsd gdrive:

# List all files
rclone ls gdrive:/path

# List with details
rclone lsl gdrive:/path

# Tree view
rclone tree gdrive:/path
```

### Copy vs Sync

```bash
# Copy (one-way, additive)
rclone copy source dest

# Sync (one-way, mirror - deletes files not in source)
rclone sync source dest

# Two-way sync (bidirectional)
rclone bisync source dest
```

### Other Useful Commands

```bash
# Check file integrity
rclone check local_path remote:path

# Delete empty directories
rclone rmdirs remote:path

# Get total size
rclone size remote:path

# Move files
rclone move source dest

# Delete files
rclone delete remote:path
```

---

## Troubleshooting

### Error: "Command not found: rclone"

**Solution**: Install RClone or add to PATH

```bash
# Linux/Mac
which rclone

# If not found, reinstall
curl https://rclone.org/install.sh | sudo bash
```

### Error: "Failed to configure token"

**Solution**: Use manual authentication

```bash
rclone config
# When asked "Use auto config?" choose "n"
# Follow the manual authentication flow
```

### Error: "Didn't find section in config file"

**Solution**: Check remote name

```bash
# List configured remotes
rclone listremotes

# Use exact name from list
rclone ls EXACT_NAME:
```

### Error: "Directory not found"

**Solution**: Create remote directory first

```bash
rclone mkdir gdrive:/Books/OCR
```

### Slow Transfers

**Solution**: Increase transfers and checkers

```bash
rclone copy source dest \
  --transfers 8 \
  --checkers 16 \
  --progress
```

### Token Expired

**Solution**: Re-authenticate

```bash
rclone config reconnect REMOTE_NAME:
```

---

## Performance Tips

### 1. Use Fast Storage for Local Directory

```bash
# Use /dev/shm (RAM disk) for temporary files
--output.shared-directory=/dev/shm/ocr_results
```

### 2. Increase Concurrency

```bash
# In RClone command
rclone sync source dest --transfers 16 --checkers 32
```

### 3. Use Compression (for compatible remotes)

```bash
rclone copy source dest --compress
```

### 4. Cache Configuration

```bash
# Add to rclone config
[gdrive]
type = drive
# ... other config ...
chunk_size = 64M
upload_cutoff = 8M
```

---

## Security Best Practices

### 1. Use Encrypted Remotes

Configure an encrypted remote for sensitive data:

```bash
rclone config
# Choose: crypt
# Encrypt filenames: yes
# Encrypt directory names: yes
```

### 2. Restrict Permissions

For OAuth remotes, use restricted scopes when possible.

### 3. Separate Service Accounts

Use separate service accounts for different projects.

### 4. Regular Credential Rotation

```bash
# Delete and recreate OAuth tokens periodically
rclone config delete REMOTE
rclone config    # Reconfigure
```

### 5. Backup Configuration

```bash
# Backup rclone config
cp ~/.config/rclone/rclone.conf ~/.config/rclone/rclone.conf.backup
```

---

## Integration Examples

### Automated Daily OCR + Sync

Create `daily_ocr.sh`:

```bash
#!/bin/bash

DATE=$(date +%Y%m%d)
INPUT_DIR="/path/to/daily/scans"
OUTPUT_DIR="/tmp/ocr_$DATE"

python -m ocr \
  --input.type=directory \
  --input.input-directory="$INPUT_DIR" \
  --text-extractor.vision-client.token="$VISION_KEY" \
  --output.type=rclone \
  --output.shared-directory="$OUTPUT_DIR" \
  --output.output-path="gdrive:/Books/$DATE" \
  --output.local-output.type=combined \
  --output.local-output.file="$OUTPUT_DIR/book.txt" \
  --output.local-output.transformations.0.type=llm-cleanup \
  --output.local-output.transformations.0.llm-provider.type=anthropic \
  --output.local-output.transformations.0.llm-provider.api-key="$ANTHROPIC_KEY"

# Cleanup
rm -rf "$OUTPUT_DIR"
```

Schedule with cron:

```bash
crontab -e
# Add: 0 2 * * * /path/to/daily_ocr.sh
```

### Multi-Destination Sync

Process once, sync to multiple locations:

```bash
# Run OCR
python -m ocr \
  --input.type=directory \
  --input.input-directory=./images \
  --text-extractor.vision-client.token=YOUR_KEY \
  --output.type=combined \
  --output.file=./result.txt

# Sync to multiple destinations
rclone copy ./result.txt gdrive:/Books/ &
rclone copy ./result.txt dropbox:/Documents/ &
rclone copy ./result.txt s3:my-bucket/books/ &
wait
```

---

## Additional Resources

- [RClone Official Documentation](https://rclone.org/docs/)
- [RClone Forum](https://forum.rclone.org/)
- [Supported Storage Providers](https://rclone.org/#providers)
- [RClone GitHub](https://github.com/rclone/rclone)

---

For general OCR usage, see [README.md](./README.md).