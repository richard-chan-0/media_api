import logging
import datetime
from src.api import create_app
from dotenv import load_dotenv
from debugpy import listen
from os import getenv

load_dotenv()

# if getenv("FLASK_ENV") == "development":
#     listen(("0.0.0.0", 5003))

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d-%H-%M-%S")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = create_app()


@app.route("/", methods=["GET"])
def home():
    return "media api is running"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)
