FROM ubuntu

MAINTAINER Prasad Dalavi "prasad01dalavi@gmail.com"

RUN apt-get update -y && apt-get upgrade -y 

RUN apt-get install python3-dev -y

RUN apt-get install python3-pip -y

# Create app folder
WORKDIR /app

# Copy project files to app directory
COPY ./ /app

# User upgraded pip version
RUN pip3 install --upgrade pip

# Install the project dependencies
RUN pip3 install -r requirements.txt

# Run the flask server
ENTRYPOINT ["python3"]
CMD ["main.py"] 
