FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY servidor.py .

EXPOSE 8000

CMD ["uvicorn", "servidor:app", "--host", "0.0.0.0", "--port", "8000"]