FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN mkdir input

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "media_utility.py"]



