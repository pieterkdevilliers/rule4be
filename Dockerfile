# Declare the build argument that will receive the secret
# ARG DATABASE_URL_ARG
# ARG AWS_ACCESS_KEY_ID_ARG
# ARG AWS_SECRET_ACCESS_KEY_ARG
# ARG AWS_STORAGE_BUCKET_NAME_ARG
# ARG AWS_S3_REGION_NAME_ARG
# ARG AWS_S3_CUSTOM_DOMAIN_ARG
# ARG AWS_CLOUDFRONT_KEY_ID_ARG
# ARG AWS_CLOUDFRONT_KEY_ARG

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

# Set the  environment variable FROM the build argument
# ENV DATABASE_URL=${DATABASE_URL_ARG}
# ENV Use_S3=True
# ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID_ARG}
# ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY_ARG}
# ENV AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME_ARG}
# ENV AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME_ARG}
# ENV AWS_S3_CUSTOM_DOMAIN=${AWS_S3_CUSTOM_DOMAIN_ARG}
# ENV AWS_CLOUDFRONT_KEY_ID=${AWS_CLOUDFRONT_KEY_ID_ARG}
# ENV AWS_CLOUDFRONT_KEY=${AWS_CLOUDFRONT_KEY_ARG}

# --- Static Files ---
# RUN python manage.py collectstatic --noinput --clear

# --- Runtime Configuration ---
EXPOSE 8000

# --- Define the entrypoint and default command ---
ENTRYPOINT ["/entrypoint.sh"]

# CMD provides the default command that entrypoint.sh will 'exec'
# This should be your Gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rule4be.wsgi:application"]