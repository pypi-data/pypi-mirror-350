# JRDB-Model
ORM for JRDB with flask-sqlalchemy.  
You can store jrdb dataset to your database.  
This repository does not have fetching scripts.

## Setup
set your environmental variable below.  
e.g.  
`DB="sqlite:///tmp/jrdb.db"`  
https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

## Usage
### Install
```
pip install jrdb_model
```

### Load dataset
```
from  jrdb_model import KaisaiData  
kaisais = KaisaiData.query.filter_by(ymd='20181118').all()  
```