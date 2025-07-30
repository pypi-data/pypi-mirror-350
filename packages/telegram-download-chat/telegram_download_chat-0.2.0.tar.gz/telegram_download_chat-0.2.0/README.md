# Telegram Chat Downloader

[![PyPI](https://img.shields.io/pypi/v/telegram-download-chat)](https://pypi.org/project/telegram-download-chat/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/telegram-download-chat)](https://pypi.org/project/telegram-download-chat/)

A powerful command-line utility to download and analyze Telegram chat history in multiple formats.

## Features

- Download complete chat history from any Telegram chat, group, channel or Telegram export archive
- Save messages in JSON format with full message metadata
- Generate human and LLM readable TXT exports with user-friendly display names
- Filter messages by date range and specific users
- Extract sub-conversations from message threads
- Cross-platform support (Windows, macOS, Linux)


## Use Cases

### Learning and Research
- Download study group discussions for offline review
- Archive Q&A sessions for future reference
- Collect data for linguistic or social research

### Team Collaboration
- Archive work-related group chats
- Document important decisions and discussions
- Create searchable knowledge bases from team conversations

### Personal Use
- Backup important personal conversations
- Organize saved messages and notes
- Analyze your own communication patterns over time

### Data Analysis
- Export chat data for sentiment analysis
- Track topic trends in community groups
- Generate statistics on message frequency and engagement

### Content Creation
- Collect discussions for content inspiration
- Reference past conversations for accuracy
- Archive community feedback and suggestions


## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install from PyPI (recommended)

```bash
pip install telegram-download-chat
```

### Using uvx (alternative package manager)

```bash
uvx install git+https://github.com/popstas/telegram-download-chat.git
```

## Configuration

### API Credentials

To use this tool, you'll need to obtain API credentials from [my.telegram.org](https://my.telegram.org):

1. Go to [API Development Tools](https://my.telegram.org/apps)
2. Log in with your phone number
   - **Important**: Do not use a VPN when obtaining API credentials
3. Create a new application
4. Copy the `api_id` and `api_hash` to your `config.yml`

### Configuration File

The configuration file is automatically created on first run in your application data directory:
- **Windows**: `%APPDATA%\telegram-download-chat\config.yml`
- **macOS**: `~/Library/Application Support/telegram-download-chat/config.yml`
- **Linux**: `~/.local/share/telegram-download-chat/config.yml`

#### Example Configuration

```yaml
# Telegram API credentials (required)
settings:
  api_id: your_api_id       # Get from https://my.telegram.org
  api_hash: your_api_hash   # Get from https://my.telegram.org
  session_name: session     # Optional: Custom session file name
  request_delay: 1          # Delay between API requests in seconds
  max_retries: 5            # Maximum number of retry attempts
  log_level: INFO           # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  log_file: app.log        # Path to log file (relative to app dir or absolute)

# Map user IDs to display names for text exports
users_map:
  123456: "Alice"
  789012: "Bob"
```

You can also specify a custom config file location using the `--config` flag.

## Usage

For the first run, you will need to log in to your Telegram account. A browser window will open for authentication.

### Basic Commands

```bash
# Download chat by username
telegram-download-chat username

# Download chat by numeric ID (negative for groups/channels)
telegram-download-chat -123456789

# Download chat by invite link
telegram-download-chat https://t.me/+invite_code

# Download chat by phone number (must be in your contacts)
telegram-download-chat +1234567890
```

### Advanced Usage

```bash
# Download with a limit on number of messages
telegram-download-chat username --limit 1000

# Download messages until a specific date (YYYY-MM-DD)
telegram-download-chat username --until 2025-05-01

# Filter messages by specific user
telegram-download-chat group_username --user 123456

# Download messages from a specific thread/reply chain
telegram-download-chat group_username --subchat 12345

# Specify custom output file
telegram-download-chat username -o custom_output.json

# Enable debug logging
telegram-download-chat username --debug

# Show current configuration
telegram-download-chat --show-config
```

### Command Line Options

```
usage: telegram-download-chat [-h] [-o OUTPUT] [--limit LIMIT] [--until DATE] [--subchat SUBCHAT] 
                            [--subchat-name NAME] [--user USER] [--config CONFIG] [--debug] 
                            [--show-config] [-v]
                            [chat]

Download Telegram chat history to JSON and TXT formats.

positional arguments:
  chat                  Chat identifier (username, phone number, chat ID, or URL)

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT    Output file path (default: chat_<chat_id>.json)
  -l, --limit LIMIT     Maximum number of messages to download (default: 0 - no limit)
  --until DATE          Only download messages until this date (format: YYYY-MM-DD)
  --subchat SUBCHAT     Filter messages by thread/reply chain (message ID or URL)
  --subchat-name NAME   Custom name for subchat directory
  --user USER           Filter messages by sender ID
  -c, --config CONFIG   Path to config file
  --debug               Enable debug logging
  --show-config         Show config file location and exit
  -v, --version         Show program's version number and exit
```

## Advanced Features

### Extract Messages from Telegram Archive

You can extract messages from a Telegram export archive (`result.json`) that you've downloaded from Telegram Desktop:

```bash
# Extract all messages from all chats
telegram-download-chat "/path/to/Telegram Desktop/DataExport/result.json"

# Extract only messages from a specific user (by their Telegram ID)
telegram-download-chat "/path/to/Telegram Desktop/DataExport/result.json" --user 123456

# Save to a custom output file
telegram-download-chat "/path/to/Telegram Desktop/DataExport/result.json" -o my_exported_chats.json
```

This feature is particularly useful for:
- Processing your full Telegram data export
- Extracting specific conversations from the export
- Converting the export to a more readable format
- Filtering messages by user or date range (using `--until`)

The tool will process the archive and generate both JSON and TXT files with the exported messages.

### Resuming Interrupted Downloads
If the download is interrupted, you can simply run the same command again to resume from where it left off. The tool automatically saves progress to a temporary file.

### User Mapping
Edit the `users_map` section in your config file to map Telegram user IDs to display names in the TXT output:

```yaml
users_map:
  123456: "Alice Smith"
  789012: "Bob Johnson"
```

### Subchat Extraction
Extract conversations from specific threads or reply chains:

```bash
# Extract messages from a specific thread
telegram-download-chat group_username --subchat 12345 --subchat-name "Important Discussion"

# Or use a direct message URL
telegram-download-chat group_username --subchat "https://t.me/c/123456789/12345"
```

## Output Formats

The tool generates the following files for each chat:

### JSON Output (`[chat_name].json`)
Contains complete message data including metadata like:
- Message IDs and timestamps
- Sender information
- Message content (including formatting)
- Reply information
- Media and file attachments
- Reactions and views

### Text Output (`[chat_name].txt`)
A human-readable version of the chat with:
- Formatted timestamps
- Display names from your `users_map`
- Message content with basic formatting
- Reply indicators

### Example Output Structure

```
2025-05-25 10:30:15 Alice:
Hello everyone! 👋

2025-05-25 10:31:22 Bob (replying to Alice):
Hi Alice! How are you?

2025-05-25 10:32:45 Charlie:
Welcome to the group!
```

## Troubleshooting

### Common Issues

1. **API Errors**
   - Ensure your API credentials are correct
   - Try disabling VPN if you're having connection issues
   - Check if your account is not restricted

2. **Missing Messages**
   - Some messages might be deleted or restricted
   - Check if you have the necessary permissions in the chat
   - Try with a smaller limit first

3. **Slow Downloads**
   - The tool respects Telegram's rate limits
   - Increase `request_delay` in config for more reliable downloads
   - Consider using a smaller `limit` parameter

### Getting Help

If you encounter any issues, please:
1. Check the logs in `app.log` (by default in the application directory)
2. Run with `--debug` flag for detailed output
3. Open an issue on [GitHub](https://github.com/popstas/telegram-download-chat/issues)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
