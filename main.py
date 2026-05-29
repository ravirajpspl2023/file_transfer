import time
import signal
import sys
from downloader import S3Downloader
from utils import load_config, setup_logging

class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

def main():
    config = load_config()
    logger = setup_logging(config)
    killer = GracefulKiller()

    logger.info("🚀 S3 G-code Downloader Service Started")

    downloader = S3Downloader(config)

    while not killer.kill_now:
        try:
            downloader.download_new_files()
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        
        time.sleep(config['polling']['interval_seconds'])

    logger.info("🛑 Service stopped gracefully")

if __name__ == "__main__":
    main()