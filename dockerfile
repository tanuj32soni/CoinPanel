# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /coinpanel

# copy the dependencies file to the working directory
COPY data_feeders/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY data_feeders/ .

# command to run on container start
CMD [ "python", "data_feeder.py" ]