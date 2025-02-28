FROM python:3.12-slim

WORKDIR /app

COPY import_csv.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "import_csv.py"]
