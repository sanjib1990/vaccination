import os

from dotenv import load_dotenv

path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    ".env")
)
load_dotenv(dotenv_path=path)

SLACK_HOOK_URL = os.getenv('SLACK_HOOK_URI')
AGES = [int(x.strip()) for x in os.getenv('AGES').strip().split(",")]
PINCODES = [int(x.strip()) for x in os.getenv('PINCODES').strip().split(",")]
