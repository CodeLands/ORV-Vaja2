FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary libraries for GUI support and OpenCV
RUN apt-get update && apt-get install -y \
    python3-tk \
    libopencv-core-dev \
    libopencv-imgproc-dev \
    libopencv-highgui-dev \
    libopencv-imgcodecs-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "naloga2.py"]
