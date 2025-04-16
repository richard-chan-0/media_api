import logging
import datetime
from src.api import create_app
from dotenv import load_dotenv
import debugpy

load_dotenv()

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d-%H-%M-%S")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
)

app = create_app()


@app.route("/", methods=["GET"])
def home():
    return "media api is running"


if __name__ == "__main__":
    debugpy.listen(("0.0.0.0", 5678))
    debugpy.wait_for_client()
    print("Debugger attached")
    app.run(debug=False, host="0.0.0.0")
