FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    procps \
    python3 \
    python3-pip \
    python3-venv \
    iptables \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    # Install specific version of Docker known to work better with read-only filesystems
    && apt-get install -y docker-ce=5:20.10.13~3-0~debian-bullseye docker-ce-cli=5:20.10.13~3-0~debian-bullseye containerd.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Create directories that Docker might need
    && mkdir -p /var/lib/docker /var/run/docker /etc/docker

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Make the scripts executable
COPY start.sh /start.sh
COPY fallback.sh /app/fallback.sh
RUN chmod +x /start.sh /app/fallback.sh

# Expose the gateway service port
EXPOSE 8000

# Start all services using Docker Compose
CMD ["/start.sh"]
