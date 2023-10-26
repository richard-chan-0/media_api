from dotenv import load_dotenv
import os
from src.run_utility import main

load_dotenv()

if __name__ == "__main__":
    directory_in = os.getenv("DIRECTORY_IN")
    directory_out = os.getenv("DIRECTORY_OUT")
    main(directory_in, directory_out)
