# Use an official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables
ENV INSTANCE_NUMBER=1
ENV NVM_DIR=/root/.nvm
ENV GO_VERSION=1.20.6
ENV NODE_VERSION=v18.16.1
ENV PYTHON_VENV=/root/.venv
ENV DEBIAN_FRONTEND=noninteractive

# Payloads used for checking success of SQL Injection and XSS
ENV PAYLOAD_ONE="' and 1=1 --"
ENV PAYLOAD_TWO="<script>alert(document.cookie)</script>"


# Update and upgrade the base system
RUN apt update -y && \
    apt dist-upgrade -y && \
    apt autoremove -y && \
    apt autoclean -y && \
    apt install -y curl wget zip unzip python3.10-venv php-cli php-xml php-curl openjdk-21-jdk openjdk-21-jre \
                   git gcc g++ make build-essential golang-go composer

# Install NVM, Node.js, and PM2
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default && \
    npm install -g pm2

# Add NVM to PATH
ENV PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

# Install Go
RUN curl -OL https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz

# Add Go to PATH
ENV PATH="/usr/local/go/bin:$PATH"

# Install Composer for PHP
RUN curl -sS https://getcomposer.org/installer -o /tmp/composer-setup.php && \
    php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    composer --version

# Install SDKMAN and Gradle
RUN curl -s "https://get.sdkman.io" | bash && \
    bash -c "source /root/.sdkman/bin/sdkman-init.sh && sdk install gradle 8.6"

# Install Python libraries for Flask and FastAPI
RUN apt install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install flask fastapi "uvicorn[standard]" xmltodict python-multipart

###
# Clone repositories and prepare apps (assuming each framework has its own directory structure)
###
WORKDIR /root
COPY webservers /root/

# Set up the webservers as per the script and install dependencies
COPY setup_servers.sh /root/setup_servers.sh
RUN chmod +x /root/setup_servers.sh && /bin/sh /root/setup_servers.sh
COPY processes.json /root/processes.json

# Expose the necessary ports for the services
EXPOSE 8630 8631 8632 8633 8634 8635 8621 8611

# Start all services using PM2
CMD ["pm2-runtime", "start", "/root/processes.json"]
# CMD ["pm2", "ls"]
# CMD ["pm2-runtime", "list"]

