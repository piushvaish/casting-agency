# Casting Agency Flask Application
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. An Executive Producer within the company is creating a system to simplify and streamline your process. This project uses Heroku for deployment.

## Application is available at 

https://pv-casting-agency.herokuapp.com/

Please let me know what you think

## Getting Started

### Installing Dependencies

#### Python 3.7

We recommend working with a python version which is less than 3.8 because SQLAlchemy doesnot support python version 3.8. 

#### Anaconda Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. This project is using windows operating system. 

* Create a conda environment with python version 3.7
```
conda create env --name py37 python=3.7
```
* To activate the environment
```
conda activate py37
```

#### PIP Dependencies

Once we have our virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Getting Started on Heroku

We need to create an account with Heroku here and then we need to download the Heroku CLI (Command Line Interface) in order to run commands from the terminal that enable us to create a Heroku application and manage it.

Once we have the Heroku CLI we can start to run Heroku commands! Enter heroku login and then provide authentication information. Now we can start running Heroku commands for our account and applications.

### Installing Dependencies
Deploying an application to Heroku is as simple as pushing that repository to Heroku, just like Github. Heroku does a lot of things behind the scenes for us when we push a repository - including installing dependencies. For a Python application, Heroku looks for a **requirements.txt** file that needs to include all of your dependencies.

### Environment Configuration
Most of the work we do for Heroku will be in our application files or the command line. In order to give you some familiarity with the web interface, we'll set up the environment variables there, after we deploy our application. For now, check out the screenshot below to get used to the interface. Once you're in a project's settings, you'll see an option to Reveal Config Vars. Once you click on that, a table similar to that you see below will appear. 

### Gunicorn
Gunicorn is a pure-Python HTTP server for WSGI applications. We'll be deploying our applications using the Gunicorn webserver. 

First, we need to install gunicorn using pip install gunicorn. 

Procfile is exceedingly simple. It only needs to include one line to instruct Heroku correctly for us: web: gunicorn app:app. Just make sure your app is housed in app.py

## Database Setup

* Movies with attributes title and release date
* Actors with attributes name, age and gender

### Database Manage & Migrations on Heroku

Heroku can run all migrations to the database hosted on the platform, but in order to do so, the application needs to include a manage.py file.

The manage.py file will contain the following code:
```
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

Now we run our local migrations using our manage.py file, to mirror how Heroku will run behind the scenes for us when we deploy our application with the following commands

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Those last commands are the essential process that Heroku will run to ensure our database is architected properly. We, however, won't need to run them again unless we're testing the app locally.

The local database is created using Postgres.
![image](images/postgres.png)

To establish a psql session with your remote database, use
```
heroku pg:psql
```
If you have more than one database, specify the database to connect to (just the color works as a shorthand) as the first argument to the command (the database located at DATABASE_URL is used by default).
```
heroku pg:psql BLACK_URL
```
Postgres Commands 
- movies
```
INSERT INTO movies(title, release_date)
VALUES
('Joker', '2019-10-04'),
('Her', '2013-02-14');
```
- actors
```
INSERT INTO actors(name,age,gender, movie_id)
VALUES
('Joaquin Phoenix',45,'M', 2),
('Amy Adam', 40, 'F', 2);
```


##### References for building model

* To use Heroku postgres table - https://devcenter.heroku.com/articles/heroku-postgresql
* http://zetcode.com/db/sqlalchemy/orm/ 
* https://www.sqlalchemy.org/library.html#tutorials
* https://stackoverflow.com/questions/25375179/one-to-many-flask-sqlalchemy
* https://www.postgresql.org/docs/12/index.html




### Deploying to Heroku
#### Clone the repository
Use Git to clone pv-casting-agency's source code to our local machine.
```
$ heroku git:clone -a pv-casting-agency
$ cd pv-casting-agency
```
#### Deploy our changes

Make some changes to the code we just cloned and deploy them to Heroku using Git.

```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
#### Add postgresql add on for our database
Heroku has an addon for apps for a postgresql database instance. Run this code in order to create our database and connect it to our application: 
'''
heroku addons:create heroku-postgresql:hobby-dev --app pv-casting-agency
'''

Breaking down the heroku-postgresql:hobby-dev section of this command, heroku-postgresql is the name of the addon. hobby-dev on the other hand specifies the tier of the addon, in this case the free version which has a limit on the amount of data it will store, albeit fairly high.

Run 
```
heroku config --app pv-casting-agency
```
in order to check your configuration variables in Heroku. We will see DATABASE_URL and the URL of the database we just created. That's excellent, but there were a lot more environment variables our apps use. 

#### Fix our configurations in Heroku
In the browser, go to Heroku Dashboard and access application's settings. Reveal config variables and start adding all the required environment variables for the project. 
![config_vars](images/config.png)

#### Running the server
$ heroku ps:scale web=1

##### Refrences for Heroku

https://devcenter.heroku.com/articles/heroku-postgresql

## Endpoints:

GET /movies
* Handle Get requests for all movies
* Arguments: None
* Returns
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Fri, 04 Oct 2019 00:00:00 GMT",
      "title": "Joker"
    },
    {
      "id": 2,
      "release_date": "Thu, 14 Feb 2013 00:00:00 GMT",
      "title": "Her"
    }
  ],
  "success": true
}
```
GET /actors
* Handle Get requests for all actors
* Arguments: None
* Returns
```
{
  "actors": [
    {
      "age": 45,
      "gender": "M",
      "id": 1,
      "movie_id": 2,
      "name": "Joaquin Phoenix"
    },
    {
      "age": 40,
      "gender": "F",
      "id": 2,
      "movie_id": 2,
      "name": "Amy Adam"
    }
  ],
  "success": true
}
```

GET '/movies/int:id'
* Handle Get requests for a specific movie
* Arguments: id
* Returns
```
{
  "movie": [
    {
      "id": 1,
      "release_date": "Fri, 04 Oct 2019 00:00:00 GMT",
      "title": "Joker"
    }
  ],
  "success": true
}
```
GET '/actors/int:id'
* Handle Get requests for a specific actor
* Arguments: id
* Returns
```
{
  "actor": [
    {
      "age": 45,
      "gender": "M",
      "id": 1,
      "movie_id": 2,
      "name": "Joaquin Phoenix"
    }
  ],
  "success": true
}
```
POST '/movies'
* POST a new movie, which will require title and realease_date 
* Arguments: title, release_date (using Postman Body -> raw -> JSON)
    
Returns a new movie to the database
```
{
  "movie": {
    "id": 4,
    "release_date": "Tue, 03 Dec 2013 00:00:00 GMT",
    "title": "American Hustle"
  },
  "success": true
}
```
POST '/actors'
* POST a new actor, which will require name, age and gender 
* Arguments: name, age, gender, movie_id
Returns a new actor to the database
```
{
  "actor": {
    "age": 76,
    "gender": "M",
    "id": 3,
    "movie_id": 1,
    "name": "Robert De Niro"
  },
  "success": true
}
```
PATCH '\movies\int:id'
* Update a movie
* Arguments: id
* Returns
```
{
  "movie": {
    "id": 4,
    "release_date": "Wed, 04 Dec 2013 00:00:00 GMT",
    "title": "American Hustle"
  },
  "success": true
}
```
PATCH '\actors\int:id'
* Update an actor
* Arguments: id
* Returns
```
{
  "actor": {
    "age": 45,
    "gender": "F",
    "id": 2,
    "movie_id": 2,
    "name": "Amy Adams"
  },
  "success": true
}
```

DELETE '\movies\int:id'
* Delete a movie
* Arguments: id
* Returns
```
{
  "deleted movie id": 5,
  "deleted movie title": "American Hustle",
  "success": true
}
```

DELETE '\actors\int:id'
* Delete an actor
* Arguments: id
* Returns
```
{
  "deleted actor id": 3,
  "deleted actor name": "Robert De Niro",
  "success": true
}
```
## Errors

### Bad Request: 400
```
"success": False,
"error": 400,
"message": "Bad Request"
```

### Not Found: 404
```
"success": False,
"error": 404,
"message": "Resource Not Found"
```
### Unprocessable request: 422
```
"success": False,
"error": 422,
"message": "Unprocessable"
```
### Internal Server Error: 500
```
"success": False,
"error": 500,
"message": "An error has occured, please try again"

```
#### References for Postman
* https://documenter.getpostman.com/view/631643/JsLs/?version=latest


## Roles:

### AUTH0

The complete documentation for the authorization code flow can be found in [Auth0's Documentation](https://auth0.com/docs/api/authentication#authorize-application).

It may help to fill in the url in the textbox below before copying it into the browser:
```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```
For this project
```
https://dev-pv.eu.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=F8RXCBpavu4G2Hdo3YtoLu0nQ0RDd7Mc&redirect_uri=https://pv-casting-agency.herokuapp.com/movies

```
![auth0](images/auth0.png)

### Integrating Auth0 With Your Frontend
To integrate Auth0 with frontend we simply need to redirect our user to our Auth0 hosted login page and include a url to redirect them to upon completion. This can be done using a simple html anchor link:
```
<a href="{{AUTH0_AUTHORIZE_URL}}">Login</a>
```

##### Casting Assistant - Can view actors and movies
'''
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp4NEZBWkpMQWpsUFdrOXRyUm4weCJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5YjM3ZGY2N2U4NzQwYzFlZGNkMDcwIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1ODcyMzExNjcsImV4cCI6MTU4NzMxNzU2NywiYXpwIjoiRjhSWENCcGF2dTRHMkhkbzNZdG9MdTBuUTBSRGQ3TWMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.J7Peh_ZPiS5PLtfDbiXBxx1bjUJFrY0UPJkogHX8t911Vou8x9GaVXWKARdM6HMk11wxQ7YIpQH8mMBhzfHlyqiIrnIGzd9ExUB61-QsiZkGMR-uWdxxO5jDTMXoms6ERcCafsA9EeTZ-avq1xGclBRLVZTYacOv-50HArxCB-pj1FeydmKEHW3tYxtJBYD5tc3e9ZzgwqciaLWrD-JOn_gDuLUfiYwoOe4NaZ5TD6Q7ApMhNAZegae0WVDn5KVHtjZ26GfF_2SvYZoRjfJdU6ysurqweqzTYu7jYBW_SFH_VUEnyHPclUUi_DTYDsKys2lPF7BIgKyoIFPQmIgH2g
'''
Visit https://jwt.io/ to verify the payload
```
{
  "iss": "https://dev-pv.eu.auth0.com/",
  "sub": "auth0|5e9b37df67e8740c1edcd070",
  "aud": "casting-agency",
  "iat": 1587231167,
  "exp": 1587317567,
  "azp": "F8RXCBpavu4G2Hdo3YtoLu0nQ0RDd7Mc",
  "scope": "",
  "permissions": [
    "view:actors",
    "view:movies"
  ]
}
``` 

##### Casting Director - All permissions a Casting Assistant has and Add or delete an actor from the database, Modify actors or movies
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp4NEZBWkpMQWpsUFdrOXRyUm4weCJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5YjM4OTM2ODRhMDEwYzIyODg0OGI4IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1ODcyMzE0OTgsImV4cCI6MTU4NzMxNzg5OCwiYXpwIjoiRjhSWENCcGF2dTRHMkhkbzNZdG9MdTBuUTBSRGQ3TWMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.O1FO0OppV3W1f0Rgidn_2J25fhwZ-ZZIAi8pJVL-Os7TRuitfx8RKd6sOBeSfMytC1xfKJWHElu442QJoG40pj3doUZKsmCdl5T5qvIejka8C9IZxn1KE0gpYrqKhbJCy9StkN0Bl7q4hgupQhpWl_GkafO4EkIMPN7Anka2ZdmhiaEhKNsiqW8ODe4CUyUVjZgkuPY7uV0OpI_UPI9lO6xce7RHvGMJJ1_9KH4yp_pnkCCQRy9gmGplqa_iNLH-2jjlAtV2onbEHnctFLxrPF7yL7jtpZ-QmmzpDnttbjfgn5qns3s55nhQisdG4Kd-skNJN1h8HbpQEOBXqP0Piw
```

```
{
  "iss": "https://dev-pv.eu.auth0.com/",
  "sub": "auth0|5e9b3893684a010c228848b8",
  "aud": "casting-agency",
  "iat": 1587231498,
  "exp": 1587317898,
  "azp": "F8RXCBpavu4G2Hdo3YtoLu0nQ0RDd7Mc",
  "scope": "",
  "permissions": [
    "delete:actors",
    "patch:actors",
    "patch:movies",
    "post:actors",
    "view:actors",
    "view:movies"
  ]
}
```
##### Executive Producer - All permissions a Casting Director has and Add or delete a movie from the database
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inp4NEZBWkpMQWpsUFdrOXRyUm4weCJ9.eyJpc3MiOiJodHRwczovL2Rldi1wdi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5YjM4Y2E2ODRhMDEwYzIyODg0OGVmIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE1ODcyMzE2OTQsImV4cCI6MTU4NzMxODA5NCwiYXpwIjoiRjhSWENCcGF2dTRHMkhkbzNZdG9MdTBuUTBSRGQ3TWMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.q3Zdozz-vAqt0ZfgA7_y35IrXv2sbIXAjPGCA9Hct1hJWyFf13lmPByA1BxZqLYyevbhHhVL69jbDtZkaWEyW_IvE3aW2RtQRgz7KZS10owugMs0B-O2cYki5zEhwTgxnOHrhHEHpDnKkDvnfUKhnP8ZnileAxW4qt4UbNAT7eLXAJiEqf1TsPO2rn1KnuuSvMjkEFbVz_G1s32sU1q87bmT6tnLSoZSJAevTgAxyeMjeNxHRuI-u1pT9VFj8vGWa1ssvqY33pNoRWgbv3jth9WosC6Kk8Y8hxo67E0Cz6P03nq7iJiUl8nxSX2r8tBaqiRvZHh0G_U7TRRXZMN81w
```
```
{
    [
     "iss": "https://dev-pv.eu.auth0.com/",
  "sub": "auth0|5e9b38ca684a010c228848ef",
  "aud": "casting-agency",
  "iat": 1587231694,
  "exp": 1587318094,
  "azp": "F8RXCBpavu4G2Hdo3YtoLu0nQ0RDd7Mc",
  "scope": "",
  "permissions": [
    "delete:actors",
    "delete:movies",
    "patch:actors",
    "patch:movies",
    "post:actors",
    "post:movies",
    "view:actors",
    "view:movies"
  ]
}
```

#### References for AUTH0
* https://github.com/auth0-samples/auth0-python-api-samples/blob/master/00-Starter-Seed/server.py
* https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
* https://auth0.com/docs/quickstart/backend/python/01-authorization

## Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role

## Testing
To run tests on a local database, run
```
python test_app.py
```

To run tests using Heroku endpoints, run

```
casting-agency.postman_collection.json
```


