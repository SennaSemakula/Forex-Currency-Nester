-----------
This file entails instructions required to run nest.py and server.py. 
Scripts have been implemented to log results to standard output. 

Pre-requisites:
- Python3.6 is required
- Ensure that all python dependencies are installed with pip3. Requirements file has been provided.
- Running server.py will require you to be on your local machine e.g. preferably do not attempt to run this over ssh as it defaults to localhost

1. Install dependencies
Run 'pip3 install -r requirements.txt'

-----------------------
- Running python nest script
-- Ensure that you're in the take_home_task directory. 
-- To view technical command line usage help, execute the following command:
python nest.py -h
-- Successfully running the script requires valid JSON to be stored in an array and passed as standard input. 
   A sample JSON file is provided in this directory to make demonstration purposes easier.

EXAMPLE: Running the script:
cat input.json | python nest.py country currency

NOTE: Nested dictionary result will be printed to standard output. I have deliberately chose to implement empty keys in the case where the maximum number of keys are specified as arguments. 

REST API
-----------------------
- Start up the server by running: 'python server.py'. A log should be displayed notifying when the server is running
- Authentication:
1. Go to localhost:8080
2. Enter username 'admin' and password 'challenge123'

NOTE: if you enter the wrong credentials you will be redirected to the login page. 

Issuing POST requests
1. Issue a POST request to localhost:8080/nest

Usage:
POST /nest?param1=<country>&param2=<city>

Example of POST request:
curl -X POST -H "Content-Type: application/json" \
-d '[{"country":"US","currency":"USD"}, {"country": "UK", "currency": "GBP"}]' \
"localhost:8080/nest?param1=country&param2=currency"

NOTE: Nested dictionary result will be printed to standard output under an INFO log. 

Unit tests
---------
There are two unit test modules located under the tests directory: test_nest.py and test_server.py
To run the tests do the following:
'pytest test_nest.py'
'pytest test_server.py'
