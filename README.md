# WorldSummarize

A Python application that automatically scrapes news from various sources every hour and generates a 2-page PDF summary of current world events.

## Features

- **Automated News Scraping**: Collects news from multiple RSS feeds including BBC, CNN, Reuters, NYT, The Guardian, and more
- **Smart Categorization**: Automatically categorizes news into World News, Business & Economy, Technology, Politics, and Other
- **PDF Generation**: Creates a well-formatted 2-page PDF document with the latest news
- **Hourly Updates**: Runs automatically every hour to keep you updated
- **Archive System**: Automatically archives previous summaries
- **Comprehensive Logging**: Tracks all operations for debugging and monitoring

## Installation

1. Make sure you have Python 3.8+ installed
2. Create and activate a virtual environment using `uv`:
   ```bash
   uv venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Run Once
To generate a single news summary PDF:
```bash
python worldsummerize.py
```

### Run Continuously (Hourly Updates)
To start the scheduler that updates every hour:
```bash
python scheduler.py
```

The scheduler will:
- Generate an initial summary immediately
- Continue running and update the summary every hour
- Archive previous summaries in the `archive/` folder

### Output

- **Main Summary**: `world_summary.pdf` - Always contains the latest news
- **Archives**: `archive/world_summary_YYYYMMDD_HHMMSS.pdf` - Historical summaries
- **Log File**: `worldsummerize.log` - Detailed operation logs

## Configuration

Edit `config.py` to customize:

- **News Sources**: Add or remove RSS feeds and websites
- **Update Interval**: Change how often the summary updates
- **PDF Settings**: Adjust page layout, fonts, and formatting
- **Article Limits**: Control how many articles per source

## News Sources

Currently configured sources include:
- BBC World News
- CNN Top Stories
- Reuters Top News
- New York Times World
- The Guardian World
- Al Jazeera
- NPR News
- Washington Post World
- Bloomberg Markets
- Financial Times
- Ars Technica
- Wired

## Project Structure

```
WorldSummerize/
├── worldsummerize.py    # Main scraping and PDF generation logic
├── scheduler.py         # Hourly scheduling script
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── world_summary.pdf  # Latest news summary (generated)
├── archive/           # Historical summaries (created automatically)
└── worldsummerize.log # Application logs (created automatically)
```

## Troubleshooting

- **SSL Errors**: Some news sites may have SSL certificate issues. The application will skip these and continue with other sources.
- **Empty PDFs**: Check the log file for errors. Some RSS feeds may be temporarily unavailable.
- **Memory Usage**: The application is designed to be lightweight, but processing many articles may use significant memory temporarily.

## Future Enhancements

Potential improvements:
- Add more sophisticated NLP for better article summarization
- Include sentiment analysis
- Add email delivery of summaries
- Create a web interface
- Support for multiple languages
- Custom news source filtering based on interests
