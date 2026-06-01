FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build demo DB into image so no runtime generation needed
RUN python3 demo_setup.py

EXPOSE 7860

CMD ["chainlit", "run", "agent_ui.py", "--host", "0.0.0.0", "--port", "7860"]
