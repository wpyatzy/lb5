FROM python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt && rm -rf $(pip cache dir)

# Copy source
WORKDIR /app
COPY src .

# Run App
ENTRYPOINT [ "python", "main.py" ]