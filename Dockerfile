FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (best practice for caching)
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Install Playwright dependencies (browsers not needed locally, but system deps are)
RUN playwright install --with-deps

# Copy project files
COPY . .

# Set default environment variable for browser
ENV BROWSER=chromium

# Run pytest with Allure results
CMD ["pytest", "-s", "--alluredir=allure-results", "Tests/"]
