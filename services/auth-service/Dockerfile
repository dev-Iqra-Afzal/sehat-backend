FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

# Copy app files
COPY . .

RUN pip install --upgrade pip setuptools wheel


# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt -i https://pypi.org/simple

# Start the FastAPI server
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]



