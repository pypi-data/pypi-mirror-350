FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Copy the application into the container.
COPY . /application

# Install the application dependencies.
WORKDIR /application
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["uv", "run", "python-app-boilerplate-25-d"]
