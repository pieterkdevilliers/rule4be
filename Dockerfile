# --- Base Image ---
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-buster

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- System Dependencies (Run as root) ---
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        # Add any other system dependencies required by your app
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install uv (Run as root, but will be used by non-root later if possible) ---
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && uv --version
ENV PATH="/usr/local/bin:${PATH}"

# --- Create a non-root user and group ---
RUN groupadd --system appgroup --gid 1001 && \
    useradd --system --create-home --uid 1001 --gid appgroup --shell /bin/bash appuser

# --- Application Setup (Still as root to create directories and set ownership) ---
WORKDIR /app

# --- Python Dependencies (using uv) ---
# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies using uv
RUN uv pip install --system --no-cache -r requirements.txt

# --- Application Code & Entrypoint ---
# Copy the rest of the application code
COPY . .

# Change ownership of the /app directory to the non-root user
# Do this *after* all files are copied into /app
RUN chown -R appuser:appgroup /app

# Copy entrypoint and ensure it's executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# --- Switch to non-root user ---
# All subsequent commands will run as 'appuser'
USER appuser

# --- Runtime Configuration ---
EXPOSE 8000

# --- Define the entrypoint and default command ---
ENTRYPOINT ["/entrypoint.sh"]

# CMD provides the default command that entrypoint.sh will 'exec'

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rule4be.wsgi:application"]