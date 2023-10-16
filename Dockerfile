FROM ubuntu:18.04

# Install dependencies
RUN sudo apt-get python3-pip -y

RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Run app.py when the container launches
CMD ["flask", "--app", "src/api", "run"]
