import logging
import datetime
from src.api import create_app
from dotenv import load_dotenv

load_dotenv()

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d-%H-%M-%S")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
