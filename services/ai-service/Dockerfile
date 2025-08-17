FROM python:3.10

# It sets the working directory inside the container to /app.
# Any files copied or commands run after this will happen inside this folder.
WORKDIR /app

# It copies everything from your current folder on your computer (where the Dockerfile is) into the /app folder inside the container.
COPY . .

# It tells Docker to run a command: install Python packages listed in requirements.txt using pip.
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt -i https://pypi.org/simple


# This tells Docker what command to run when the container starts.
# uvicorn: a lightweight web server for Python (often used with FastAPI).
# "app.main:app": means go into the file app/main.py and run the FastAPI app named app.
# --host 0.0.0.0: makes the app accessible from outside the container.
# --port 8000: runs the app on port 8000.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
