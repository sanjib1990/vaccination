import os

from dotenv import load_dotenv

path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    ".env")
)
load_dotenv(dotenv_path=path)

SLACK_HOOK_URL = os.getenv('SLACK_HOOK_URI')
AGES = [int(x.strip()) for x in os.getenv('AGES').strip().split(",") if x.strip()]
PINCODES = [int(x.strip()) for x in os.getenv('PINCODES').strip().split(",") if x.strip()]
DAYS = int(os.getenv('DAYS', 1))
