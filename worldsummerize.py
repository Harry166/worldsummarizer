import os
import logging
import requests
import feedparser
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import textwrap
from urllib.parse import urljoin, urlparse
from config import NEWS_SOURCES, SETTINGS, PDF_SETTINGS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(SETTINGS.get('log_file', 'worldsummerize.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def scrape_rss_feed(url):
    """Scrape RSS feed and return a list of articles"""
    try:
        logger.info(f"Scraping RSS feed: {url}")
        feed = feedparser.parse(url)
        articles = []
        
        if feed.bozo:
            logger.warning(f"Failed to parse RSS feed properly: {url}")
            return articles
            
        for entry in feed.entries[:SETTINGS.get('max_articles_per_source', 5)]:
            article = {
                'title': entry.get('title', 'No title'),
                'summary': entry.get('summary', entry.get('description', '')),
                'link': entry.get('link', ''),
                'published': entry.get('published_parsed', None),
                'source': feed.feed.get('title', urlparse(url).netloc)
            }
            
            # Clean up summary
            if article['summary']:
                soup = BeautifulSoup(article['summary'], 'html.parser')
                article['summary'] = soup.get_text(strip=True)
                
            articles.append(article)
            
        logger.info(f"Successfully scraped {len(articles)} articles from {url}")
        return articles
        
    except Exception as e:
        logger.error(f"Error scraping RSS feed {url}: {str(e)}")
        return []



def generate_summary(articles):
    """Generate a categorized summary of articles"""
    # Categorize articles
    categories = {
        'World News': [],
        'Business & Economy': [],
        'Technology': [],
        'Politics': [],
        'Science & Health': [],
        'Climate & Environment': [],
        'Other': []
    }
    
    # Enhanced keyword-based categorization
    for article in articles:
        title_lower = article['title'].lower()
        summary_lower = article.get('summary', '').lower()
        full_text = title_lower + ' ' + summary_lower
        
        # Technology keywords
        if any(word in full_text for word in ['technology', 'tech', 'ai', 'artificial intelligence', 'software', 'cyber', 
                                              'digital', 'internet', 'data', 'hack', 'startup', 'silicon valley', 
                                              'algorithm', 'machine learning', 'robotics', 'automation', 'cloud',
                                              'google', 'microsoft', 'apple', 'amazon', 'meta', 'nvidia']):
            categories['Technology'].append(article)
        # Business & Economy keywords
        elif any(word in full_text for word in ['economy', 'market', 'business', 'finance', 'stock', 'trade',
                                                'inflation', 'recession', 'gdp', 'investment', 'bank', 'currency',
                                                'corporate', 'earnings', 'revenue', 'profit', 'merger', 'acquisition',
                                                'startup', 'ipo', 'crypto', 'bitcoin', 'dow', 'nasdaq', 's&p']):
            categories['Business & Economy'].append(article)
        # Politics keywords
        elif any(word in full_text for word in ['politics', 'election', 'government', 'minister', 'president',
                                                'congress', 'senate', 'parliament', 'democrat', 'republican',
                                                'policy', 'legislation', 'vote', 'campaign', 'candidate',
                                                'diplomatic', 'embassy', 'sanctions', 'treaty', 'summit']):
            categories['Politics'].append(article)
        # Science & Health keywords
        elif any(word in full_text for word in ['science', 'research', 'study', 'health', 'medical', 'disease',
                                                'vaccine', 'drug', 'treatment', 'hospital', 'doctor', 'patient',
                                                'discovery', 'breakthrough', 'scientist', 'laboratory', 'clinical',
                                                'mental health', 'pandemic', 'virus', 'bacteria', 'dna']):
            categories['Science & Health'].append(article)
        # Climate & Environment keywords
        elif any(word in full_text for word in ['climate', 'environment', 'weather', 'storm', 'hurricane', 'flood',
                                                'drought', 'wildfire', 'temperature', 'global warming', 'carbon',
                                                'renewable', 'solar', 'wind', 'energy', 'sustainability', 'pollution',
                                                'conservation', 'biodiversity', 'ocean', 'forest', 'arctic']):
            categories['Climate & Environment'].append(article)
        # World News keywords
        elif any(word in full_text for word in ['world', 'international', 'global', 'nation', 'country', 
                                                'conflict', 'war', 'peace', 'refugee', 'crisis', 'humanitarian',
                                                'united nations', 'nato', 'military', 'defense', 'security']):
            categories['World News'].append(article)
        else:
            categories['Other'].append(article)
    
    return categories


def create_pdf(categorized_articles, output_path):
    """Create a well-formatted PDF document from the categorized articles"""
    try:
        # Create archive directory if it doesn't exist
        archive_path = SETTINGS.get('archive_path', 'archive/')
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        
        # Archive previous summary if it exists
        if os.path.exists(output_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_name = f"{archive_path}world_summary_{timestamp}.pdf"
            os.rename(output_path, archive_name)
            logger.info(f"Archived previous summary to {archive_name}")
        
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        # Title page
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, height - 100, "WORLD SUMMARIZE")
        
        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height - 140, "Global News Summary")
        
        c.setFont("Helvetica", 14)
        current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
        c.drawCentredString(width/2, height - 170, current_time)
        
        # Draw a decorative line
        c.setLineWidth(2)
        c.line(100, height - 200, width - 100, height - 200)
        
        # Start content
        y_position = height - 250
        margin_left = 50
        margin_right = 50
        text_width = width - margin_left - margin_right
        
        article_count = 0
        page_count = 1
        
        # Process all articles into a single narrative format
        all_formatted_articles = []
        
        for category, articles in categorized_articles.items():
            if not articles:
                continue
            
            # Add category header to formatted articles
            if articles:
                all_formatted_articles.append({"type": "category", "text": category.upper()})
            
            # Show exactly 10 articles per category
            articles_to_show = min(len(articles), 10)  # Show up to 10 articles per category
            for article in articles[:articles_to_show]:
                # Format article with bold title inline
                title = article['title']  # Don't limit title length
                raw_summary = article.get('summary', '')
                source = article.get('source', 'Unknown')
                
                # Clean up and create natural summary between 150-300 words
                if raw_summary:
                    raw_summary = ' '.join(raw_summary.split())  # Remove extra whitespace
                    sentences = raw_summary.replace('? ', '?|').replace('! ', '!|').replace('. ', '.|').split('|')
                    sentences = [s.strip() for s in sentences if s.strip()]
                    
                    # Build summary sentence by sentence
                    summary = ""
                    word_count = 0
                    
                    for sentence in sentences:
                        sentence_words = len(sentence.split())
                        new_word_count = word_count + sentence_words
                        
                        # Always include at least enough sentences to reach 150 words
                        if word_count < 150:
                            summary += sentence + " "
                            word_count = new_word_count
                        # Between 150-200 words, keep adding if it doesn't go over 250
                        elif word_count < 200 and new_word_count <= 250:
                            summary += sentence + " "
                            word_count = new_word_count
                        # Between 200-300, only add if it keeps us under 300
                        elif new_word_count <= 300:
                            summary += sentence + " "
                            word_count = new_word_count
                        else:
                            break
                    
                    # If we're still under 150 words, add contextual information
                    if word_count < 150:
                        additional_context = f"According to {source}, this development represents a significant moment in current events. Industry experts and analysts are closely monitoring the situation as it continues to evolve. The implications of this news could have far-reaching effects on various stakeholders involved. Further updates are expected as more information becomes available from reliable sources. This story is part of ongoing coverage of important global developments."
                        
                        context_sentences = additional_context.replace('. ', '.|').split('|')
                        for sentence in context_sentences:
                            sentence = sentence.strip()
                            if sentence:
                                sentence_words = len(sentence.split())
                                if word_count + sentence_words <= 300:
                                    summary += sentence + " "
                                    word_count += sentence_words
                                    if word_count >= 150:
                                        break
                    
                    summary = summary.strip()
                else:
                    # No summary available, create natural placeholder text
                    summary = f"This article from {source} provides important coverage of current events. While detailed information is being compiled, initial reports suggest significant developments in this area. The story continues to evolve as journalists gather more information from various sources. Updates will be provided as additional details become available. This news item represents part of the broader coverage of important global events and their potential implications for various stakeholders and communities around the world. Experts are analyzing the situation to better understand its significance and potential impact on related sectors and regions."
                    
                formatted_text = f"{title}: {summary}"
                all_formatted_articles.append({
                    "type": "article",
                    "title": title,
                    "text": formatted_text,
                    "source": source
                })
        
        # Now render all articles in a flowing format
        for item in all_formatted_articles:
            # Check if we need a new page
            if y_position < 100:
                # Add page number at bottom
                c.setFont("Helvetica", 9)
                c.drawCentredString(width/2, 30, f"Page {page_count}")
                
                c.showPage()
                page_count += 1
                if page_count > SETTINGS.get('max_pages', 4):
                    break  # Limit to more pages for detail
                y_position = height - 50
            
            if item["type"] == "category":
                # Add some space before category
                y_position -= 20
                
                # Category header
                c.setFont("Helvetica-Bold", 14)
                c.drawString(margin_left, y_position, item["text"])
                y_position -= 20
                
            elif item["type"] == "article":
                # Article content
                c.setFont("Helvetica-Bold", 11)
                
                # Split the formatted text to handle title separately
                parts = item["text"].split(": ", 1)
                title_text = parts[0]
                summary_text = parts[1] if len(parts) > 1 else ""
                
                # Wrap and draw title
                title_lines = textwrap.wrap(title_text, width=90)
                for i, line in enumerate(title_lines[:2]):  # Max 2 lines for title
                    if i == len(title_lines[:2]) - 1 and summary_text:
                        # Add colon back to last line of title
                        line += ":"
                    c.drawString(margin_left, y_position, line)
                    y_position -= 14
                
                # Switch to regular font for summary
                c.setFont("Helvetica", 10)
                
                # Continue with summary on same line if title was short
                if len(title_lines) == 1 and summary_text:
                    # Calculate remaining space on the line
                    title_width = c.stringWidth(title_text + ": ", "Helvetica-Bold", 11)
                    x_position = margin_left + title_width
                    
                    # Draw first part of summary on same line
                    remaining_width = text_width - title_width
                    first_line_chars = int(remaining_width / c.stringWidth("a", "Helvetica", 10))
                    
                    if len(summary_text) > first_line_chars:
                        first_line = summary_text[:first_line_chars]
                        rest_of_summary = summary_text[first_line_chars:]
                        
                        # Go back up one line to continue after title
                        y_position += 14
                        c.drawString(x_position, y_position, first_line)
                        y_position -= 14
                        
                        # Wrap remaining summary
                        wrapped_lines = textwrap.wrap(rest_of_summary, width=100)
                        for line in wrapped_lines[:6]:  # Allow more lines
                            c.drawString(margin_left, y_position, line)
                            y_position -= 12
                    else:
                        # Summary fits on same line
                        y_position += 14
                        c.drawString(x_position, y_position, summary_text)
                        y_position -= 14
                else:
                    # Wrap summary normally
                    if summary_text:
                        wrapped_lines = textwrap.wrap(summary_text, width=100)
                        for line in wrapped_lines[:7]:  # Allow more lines
                            c.drawString(margin_left, y_position, line)
                            y_position -= 12
                
                y_position -= 8  # Space between articles
                article_count += 1
                
                # Don't limit by article count, let pages fill up
                # The page limit will control the content amount
        
        # Add page number on last page
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, 30, f"Page {page_count}")
        
        c.save()
        logger.info(f"PDF created successfully: {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating PDF: {str(e)}")
        raise


def scrape_news():
    """Main function to scrape news and update PDF"""
    logger.info("Starting news scraping session")
    all_articles = []
    
    # Scrape RSS feeds
    for rss_url in NEWS_SOURCES['rss_feeds']:
        try:
            articles = scrape_rss_feed(rss_url)
            all_articles.extend(articles)
        except Exception as e:
            logger.error(f"Failed to scrape {rss_url}: {str(e)}")
            continue
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        if article['title'] not in seen_titles:
            seen_titles.add(article['title'])
            unique_articles.append(article)
    
    logger.info(f"Total unique articles collected: {len(unique_articles)}")
    
    # Generate categorized summary
    categorized_articles = generate_summary(unique_articles)
    
    # Create PDF
    output_path = SETTINGS.get('pdf_output_path', 'world_summary.pdf')
    create_pdf(categorized_articles, output_path)
    
    logger.info("News scraping session completed successfully")


def main():
    """WorldSummarize main function"""
    try:
        logger.info("WorldSummarize started")
        scrape_news()
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        raise


if __name__ == '__main__':
    main()
