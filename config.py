"""
Configuration file for WorldSummerize
Contains news sources and application settings
"""

# News sources configuration
NEWS_SOURCES = {
    'rss_feeds': [
        # Major International News
        'https://feeds.bbci.co.uk/news/world/rss.xml',
        'https://rss.cnn.com/rss/cnn_topstories.rss',
        'https://feeds.reuters.com/reuters/topNews',
        'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        'https://www.theguardian.com/world/rss',
        
        # Regional News
        'https://www.aljazeera.com/xml/rss/all.xml',
        'https://feeds.npr.org/1001/rss.xml',
        'https://feeds.washingtonpost.com/rss/world',
        
        # Business & Economics
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.ft.com/rss/home',
        
        # Technology
        'https://feeds.arstechnica.com/arstechnica/index',
        'https://www.wired.com/feed/rss',
    ],
    
    'news_websites': [
        # Additional websites for direct scraping if needed
        'https://www.bbc.com/news',
        'https://www.reuters.com/',
        'https://apnews.com/',
    ]
}

# Application settings
SETTINGS = {
    'update_interval_hours': 1,
    'max_articles_per_source': 10,  # Increased to get more content
    'summary_length': 400,  # Much longer summaries
    'pdf_output_path': 'world_summary.pdf',
    'archive_path': 'archive/',
    'enable_logging': True,
    'log_file': 'worldsummerize.log',
    'target_word_count': 2000,  # Target word count for the document
    'max_pages': 12  # Allow many more pages for 10 articles × 200 words each
}

# PDF settings
PDF_SETTINGS = {
    'page_size': 'A4',
    'margin_top': 50,  # Smaller margins for more content
    'margin_bottom': 50,
    'margin_left': 40,
    'margin_right': 40,
    'title_font_size': 24,
    'heading_font_size': 14,
    'body_font_size': 10,
    'line_spacing': 12  # Tighter line spacing
}
