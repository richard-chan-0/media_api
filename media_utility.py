from flask import Flask, request
from src.api.videos import get_jellyfin_names, update_video_names
import logging
import datetime

today_date = datetime.datetime.now()
run_date = today_date.strftime("%Y-%m-%d-%H-%M-%S")

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


@app.route("/videos", methods=["GET", "POST"])
def rename_videos():
    if request.method == "GET":
        logger.info("Getting new names for videos...")
        return get_jellyfin_names(request.get_json())

    try:
        logger.info("Updating video names...")
        update_video_names(request.get_json())
        return "Successfully renamed videos to Jellyfin format."
    except Exception as e:
        logger.error(f"Error renaming videos: {e}")
        return "Error renaming videos."


@app.route("/books")
def rename_books():
    return "<p>Renaming books...</p>"


if __name__ == "__main__":
    app.run(debug=True)
