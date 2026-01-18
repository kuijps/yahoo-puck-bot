FROM python:3.12

# Create a directory inside the container
WORKDIR /app

# Copy everything from your project folder into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your app
CMD ["python", "app.py"]

