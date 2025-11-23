FROM python:3.11-slim
WORKDIR /app
COPY game_service.py /app/
RUN pip install flask flask-cors
EXPOSE 5000
CMD ["python", "game_service.py"]
