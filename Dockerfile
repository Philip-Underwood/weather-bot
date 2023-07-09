# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Set timezone & discord webhook url
ENV TZ=America/Chicago
ENV DISCORD_WEBHOOK https://discord.com/api/webhooks/

# Install python requrements
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install cron
RUN apt-get update && apt-get install -y cron

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/cron-hello

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-hello

# Apply cron job
RUN crontab /etc/cron.d/cron-hello

# Create the log file to be able to run tail
RUN touch /usr/src/app/cron.log

# Run the command on container startup
CMD service cron start && tail -f /usr/src/app/cron.log