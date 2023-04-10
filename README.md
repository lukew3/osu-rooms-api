# osu-rooms-api
An json API for getting information about classrooms at the Ohio State University. 

## Setup
### Install requirements
You should set up a venv and install requirements with:
```
pip install -r requirements.txt
```
### Setup db
Run
```
python makeDb.py
```
to create the `roomMatrix.db` sqlite database.
### Scrape data
Run
```
python scraper.py
```
to get data
### Start server
```
python server.py
```
You can test by going to http://localhost:5000/classroom/DL0369 to see how long Dreese 369 is available for
