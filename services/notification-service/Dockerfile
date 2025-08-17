FROM python:3.10
WORKDIR /app
COPY . .
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt -i https://pypi.org/simple

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]