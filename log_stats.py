from src.metrics import get_system_stats
from src.logger import log_stats
from dotenv import load_dotenv
import os

load_dotenv()

CSV_PATH = os.getenv('LOG_CSV', 'stats_log.csv')

stats = get_system_stats()
log_stats(CSV_PATH, stats)
