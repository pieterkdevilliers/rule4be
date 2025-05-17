
# --- Base Image ---
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-buster

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- System Dependencies ---
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        # Add any other system dependencies required by your app
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install uv ---
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && echo "Verifying uv installation in /root/.local/bin" \
    && /root/.local/bin/uv --version

# Add the CORRECT directory to the PATH
ENV PATH="/root/.local/bin:${PATH}"

# --- Application Setup ---
WORKDIR /app

# --- Python Dependencies (using uv) ---
# Ensure django-storages and boto3 (or your S3 backend) are in requirements.txt
COPY requirements.txt .
RUN /root/.local/bin/uv pip install --system --no-cache -r requirements.txt

# --- Application Code & Entrypoint ---
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# --- Runtime Configuration ---
EXPOSE 8000

# --- Define the entrypoint and default command ---
ENTRYPOINT ["/entrypoint.sh"]

# CMD provides the default command that entrypoint.sh will 'exec'
# This should be your Gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rule4be.wsgi:application"]