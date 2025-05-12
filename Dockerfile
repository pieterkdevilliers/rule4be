# --- Base Image ---
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-buster

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- System Dependencies ---
# Install curl (needed to download uv) and other system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \ 
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install uv ---
# Download and install the latest stable version of uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
# Make uv available in the PATH
ENV PATH="/root/.cargo/bin:${PATH}" # Adjust if running as non-root or if install location differs

# --- Application Setup ---
WORKDIR /app

# --- Python Dependencies (using uv) ---
# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies using uv
# --no-cache prevents caching downloads/builds within the layer, similar to pip's --no-cache-dir
# Using 'uv pip install' for compatibility with pip commands/requirements.txt format
RUN uv pip install --no-cache -r requirements.txt

# --- Application Code ---
COPY . .

# --- Static Files ---
RUN python manage.py collectstatic --noinput

# --- Runtime Configuration ---
EXPOSE 8000

# --- Run the Application ---
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

# --- Optional: Non-root user ---
# (If using a non-root user, ensure uv is installed for that user or globally,
# and adjust PATH and permissions accordingly)
# RUN useradd --system --create-home appuser
# USER appuser
# WORKDIR /app
# (Potentially copy uv binary or install it for the user)
# RUN chown -R appuser:appuser /app/static /app/media # Adjust paths
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]