# Engine 
FROM python:3.10-slim

# Working Directory
WORKDIR /app

# Copying files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Command that runs the bot
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
