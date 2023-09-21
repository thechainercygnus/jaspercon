# Use the official Python 3 image as the base image
FROM python:3

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | sh

# Set up the work directory
WORKDIR /workspace

# Copy the project files into the container
COPY . .

# Install project dependencies with Poetry
RUN poetry install

# Set the default shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Start a bash shell by default
CMD ["bash"]
