FROM python:3.7-slim
COPY setup.py /setup.py
COPY app.py /app.py
RUN python3.7 -m pip install -e .

CMD ["python", "app.py"]
