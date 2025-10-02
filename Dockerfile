FROM python:3.11-slim
WORKDIR /app
RUN echo 'print("Hello, world!")' > app.py
CMD ["python", "app.py"]