FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    # Install specific version of Docker known to work on Render
    && apt-get install -y docker-ce=5:20.10.24~3-0~debian-bullseye docker-ce-cli=5:20.10.24~3-0~debian-bullseye containerd.io docker-compose-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Make the startup script executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose the gateway service port
EXPOSE 8000

# Start all services using Docker Compose
CMD ["/start.sh"]
