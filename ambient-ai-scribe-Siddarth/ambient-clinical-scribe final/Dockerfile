FROM python:3.11-slim

WORKDIR /app

# Install system deps (ffmpeg for whisper; build-essential for any package
# that needs to compile). No GTK/Pango/Cairo needed - PDF export uses
# fpdf2 (pure Python), not WeasyPrint.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
