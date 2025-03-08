from flask import Flask, request
from src.api.videos import videos
import logging
import datetime

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d")

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"logs/{run_date}.log",
    format="%(asctime)s %(message)s",
    filemode="w",
    level=logging.INFO,
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/videos")
def rename_videos():
    logger.info("Getting new names for videos...")
    return videos(request.get_json())


@app.route("/books")
def rename_books():
    return "<p>Renaming books...</p>"


if __name__ == "__main__":
    app.run(debug=True)
