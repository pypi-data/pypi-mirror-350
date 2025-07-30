from pathlib import Path


MODEL_PATH = Path("data/classifier.joblib")

# OParl API configuration
OPARL_BASE_URL = "https://www.bonn.sitzung-online.de/public/oparl"
OPARL_PAPERS_ENDPOINT = "/papers?body=1"
OPARL_MAX_PAGES = 5  # Limit number of pages to fetch (20 items per page)

# Application settings
USER_AGENT = "stadt-bonn-ratsinfo/0.1.0 (https://machdenstaat.de)"

CACHE_DIR = Path(".") / ".cache" / "oparl_responses"
