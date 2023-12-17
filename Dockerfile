# Use an official Python runtime as a parent image
FROM python:3.12

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies for Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    && rm -rf /var/lib/apt/lists/*

#Download Google Chrome dependencies
# Chrome dependency Instalation
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libgtk-4-1 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1

#Download Google Chrome
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i ./google-chrome-stable_current_amd64.deb 

#Display the path to google chrome
RUN which google-chrome

# Download and install Chromedriver
RUN wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.71/linux64/chromedriver-linux64.zip && \
   unzip /tmp/chromedriver.zip -d /usr/bin/ && \
   rm /tmp/chromedriver.zip


# Set the PATH environment variable
ENV PATH="/usr/local/bin:${PATH}"

# Mount the application code to the image
COPY . /code/fyp_project/
WORKDIR /code

EXPOSE 8000

# Run the production server
ENTRYPOINT ["python", "fyp_project/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

