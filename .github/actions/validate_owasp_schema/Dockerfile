# Start with an official Python slim image. It's lightweight and has Python and pip.
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install the necessary Python packages directly without a requirements.txt file
# --no-cache-dir keeps the image layer smaller.
RUN pip install --no-cache-dir owasp-schema PyYAML

# Copy the validation script and the entrypoint script into the container's working directory
COPY validate.py entrypoint.sh ./

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

# This is the command that will be run when the container starts
ENTRYPOINT ["/app/entrypoint.sh"]