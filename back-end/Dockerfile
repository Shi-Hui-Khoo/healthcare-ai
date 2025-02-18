FROM python:3.11-slim

WORKDIR /code

COPY ./healthcare /code/healthcare

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

RUN crewai install

RUN uv add ollama

RUN ollama pull llama3

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8080"]