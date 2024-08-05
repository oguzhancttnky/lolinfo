
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Installing dependencies to install Google Chrome and Chromedriver to our container
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Adding Google Chrome official repositories (installing the gpg key) to get the latest stable version
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Installing Chromedriver to be able to use Selenium in our Python code with Google Chrome
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -N http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -P ~ \
    && unzip ~/chromedriver_linux64.zip -d ~ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files to the containers /app directory
COPY . /app

# Set our working directory to /app
WORKDIR /app

# Run the main.py file when the container launches with the command python main.py as the entrypoint
ENTRYPOINT ["python", "main.py"]
