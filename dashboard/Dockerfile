FROM python:3.12-slim
RUN pip install --no-cache-dir pymodbus==3.6.9 flask==3.0.3
WORKDIR /app
COPY app.py .
COPY static ./static
EXPOSE 8080
CMD ["python", "app.py"]
