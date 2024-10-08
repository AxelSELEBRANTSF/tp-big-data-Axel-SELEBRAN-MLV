# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Add the cron job to the crontab
COPY cron-tab /etc/cron.d/cron-tab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-tab

# Apply the cron job
RUN crontab /etc/cron.d/cron-tab

# Create the log file for cron
RUN touch /var/log/cron.log

# Command to run the cron service
CMD ["cron", "-f"]
