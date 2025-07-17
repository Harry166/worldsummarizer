"""
WorldSummarize Combined Runner
Runs both the news scraper scheduler and web server concurrently
"""

import subprocess
import threading
import logging
import time
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_scheduler():
    """Run the scheduler in a subprocess"""
    try:
        logger.info("Starting scheduler process...")
        process = subprocess.Popen([sys.executable, "scheduler.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   bufsize=1)
        
        # Read output in real-time
        for line in process.stdout:
            if line:
                logger.info(f"[Scheduler] {line.strip()}")
                
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")

def run_web_server():
    """Run the Flask web server in a subprocess"""
    try:
        logger.info("Starting web server process...")
        process = subprocess.Popen([sys.executable, "app.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   bufsize=1)
        
        # Read output in real-time
        for line in process.stdout:
            if line:
                logger.info(f"[Web Server] {line.strip()}")
                
    except Exception as e:
        logger.error(f"Web server error: {str(e)}")

def main():
    """Main function to run both services"""
    logger.info("=== WorldSummarize Starting ===")
    logger.info("This will run both the scheduler and web server")
    logger.info("Press Ctrl+C to stop both services")
    
    # Create threads for each service
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    web_server_thread = threading.Thread(target=run_web_server, daemon=True)
    
    # Start both threads
    scheduler_thread.start()
    time.sleep(2)  # Give scheduler a moment to start
    web_server_thread.start()
    
    logger.info("Both services started successfully!")
    logger.info("Access the web interface at: http://localhost:5000")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down WorldSummarize...")
        sys.exit(0)

if __name__ == "__main__":
    main()
