# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron and vim
RUN apt-get update && apt-get install -y cron vim

# Add the cron job to the crontab and ensure it ends with a newline
COPY cron-tab /etc/cron.d/cron-tab
RUN echo "" >> /etc/cron.d/cron-tab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-tab

# Create a script to set up the environment and run cron
RUN echo '#!/bin/bash\n\
PATH=/usr/local/bin:$PATH\n\
printenv >> /etc/environment\n\
cron -f' > /app/start-cron.sh && chmod +x /app/start-cron.sh

# Apply the cron job
RUN crontab /etc/cron.d/cron-tab

# Create the log file for cron
RUN touch /var/log/cron.log

# Command to run the cron service
CMD ["/app/start-cron.sh"]