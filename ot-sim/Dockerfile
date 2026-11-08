FROM python:3.12-slim
RUN pip install --no-cache-dir pymodbus==3.6.9
WORKDIR /app
COPY plc_sim.py .
EXPOSE 502
CMD ["python", "plc_sim.py"]
