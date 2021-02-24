# Data Feeder

Data Feeder(DF) is a python script to get trading data of differnet symbols from Binance market and then feeding that data into the database(MongoDB).

### Installation Steps

After taking pull of the repositiry, things that are needed to be done are:-

1. Create a python virtual environmet.
2. Install the packages from requirements.txt file.
3. You need to set up Mongodb database using Username and Password and provide this information in constants file.


### Following are the Steps to Run trading script:

1. Goto the folder "data_feeders"
2. Run command "python data_feeder.py"
3. First - Input the symbol/symbols name, for which we need to fetch and store the trade streams.
4. Second - Input the price value for which we need to check the price rise.

After running the command, the response will show on your screen and the trade stream data will be stored in MongoDB. 


### Following are the Steps to Build and Run docker image:

1. Goto the folder "data_feeders"
2. Add the required values in constants.py file. (SYMBOL_LIST, PRICE_INPUT)
3. First install docker into your machine. can take help from "https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04".
4. Now build the docker image by " docker build -t coinpanel ." 
5. Now run the docker image from "docker run -p 5000:5000 coinpanel" command .
