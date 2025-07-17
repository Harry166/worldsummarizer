import schedule
import time
import logging
from datetime import datetime
from worldsummerize import main

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_with_logging():
    """Wrapper function to run main with error handling"""
    try:
        logger.info("Starting scheduled news scraping...")
        main()
        logger.info("Scheduled news scraping completed successfully")
    except Exception as e:
        logger.error(f"Error during scheduled run: {str(e)}")

if __name__ == '__main__':
    logger.info("WorldSummarize Scheduler started")
    logger.info("Running initial news scraping...")
    
    # Run immediately on start
    run_with_logging()
    
    # Schedule to run every hour
    schedule.every(1).hour.do(run_with_logging)
    
    logger.info("Scheduler is now running. Will update every hour.")
    logger.info("Press Ctrl+C to stop.")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
