# NodeJS Streams Client UAT
## Setup
To run the scripts you will need to install both the Python Streams Client and NodeJS Streams Client
### NodeJS Setup
To install the required libraries for NodeJS run
~~~~
npm install .
~~~~
### Python Setup
To install the required libraries for Python run
~~~~
pip install -r requirements.txt
~~~~
### Environment variables
To run the scripts you should set the following environment variables:
- **USER_KEY**: A valid FA user_key
- **SUBSCRIPTION_ID**: The subscription id that NodeJS will consume
- **SUBSCRIPTION_ID_PYTHON**: The subscription id that python will consume
## Running the scripts
### NodeJS
To run you should execute
~~~~
node index.js
~~~~
### Python
~~~~
python streams.py
~~~~