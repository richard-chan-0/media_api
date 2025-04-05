import logging
import datetime
from src.api import create_app
from dotenv import load_dotenv

load_dotenv()

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d-%H-%M-%S")

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"logs/{run_date}.log",
    format="%(asctime)s %(message)s",
    filemode="w",
    level=logging.INFO,
)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
