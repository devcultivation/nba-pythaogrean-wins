##### Base Setup #####

# Apply python base image
FROM python:3.9.4-buster as python-base

# Install extra libraries
RUN apt-get update -yqq \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    build-essential \
    libssl-dev \
    libboost-all-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

##### App Environment Setup #####

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.1.12 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install Poetry (uses $POETRY_HOME & $POETRY_VERSION environment variables)
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# Copy Python requirements and install only runtime dependencies
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

# Set active directory
WORKDIR /app

# Add non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy application code dependencies
COPY /conf/start.sh /conf/test_runner.sh ./
COPY /app ./app

# Assign non-root user permissions
RUN chown appuser /app /app/*

# Assign start shell script permission privilege to non-root user
RUN chmod +x /app/start.sh /app/test_runner.sh

# Constrain application layer to setting non-root and default command
FROM python-base as application

# Set non-root user
USER appuser

# Set default command to start app shell
CMD ["/app/start.sh"]

###### Test-Builder Layer #####

# "testing" stage uses "python-base" stage and adds test dependencies to execute test script
FROM python-base as testing

# Install full poetry environment including dev-dependencies for test libraries
WORKDIR $PYSETUP_PATH
RUN poetry install

# Set active directory and copy test dependencies
WORKDIR /app
COPY /tests ./tests

# Set non-root user
USER appuser

# Set default command to run tests
CMD ["/app/test_runner.sh"]
