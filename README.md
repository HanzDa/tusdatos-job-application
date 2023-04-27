# tusdatos-job-application
This project consist in 2 parts, the API written in python using fastAPI framework
and the scraper which works with selenium and beautifulsoup4

## Project setup

### Install browser driver
Before start the project you will need to install a chrome driver
you can download it from https://sites.google.com/chromium.org/driver/downloads?authuser=0
Once you have the driver extract it a root folder so that the scraper can find it.
(alternative you can change the path at line 129 in scraper.py file)

### Install dependencies

    `pip install -r requirements.txt`


### Start the API
Got to API folder and run
    `uvicorn main:app --reload --port 8000`

Alternative you can run 
    `uvicorn API.main:app --reload --port 8000`


### Run scraper.py file
Please note that you must have the server running before run the scraper
since it will send the scraped data to the API

`python3 scraper.py`


### Got to API documentation
    http://127.0.0.1:8000/docs#/
