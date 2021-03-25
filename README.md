# capstone
Capstone is the last project of my Udacity Full Stack Nanodegree Course. In this project I developed a platform for Casting Agency.
The Casting Agency models a company that is responsible for creating movies and managing actors. 

Heroku App Url: (https://capstone-nitin15067.herokuapp.com).

Authorization Tokens are present in constants.py for different user types.

Code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

Featuring functionalities like:
1) Managing Movies by using CRUD api's.
2) Managing Actors by usig CRUD api's.
3) Authentication via Auth0.
4) Unit Testing of the api's.
5) Deployment on Heroku

## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machine.

### Installing dependencies
To install the dependencies, run the following command:
```pip install requirements.txt```
All required packages are included in the requirements file.

### Setting up environment variables
Required Environment variables:
DATABASE_URL, AUTH0_DOMAIN, API_AUDIENCE, ALGORITHMS

Get you postgres connection string and insert it into database url in env variables.
To setup environment variables, run the following command:
```export DATABASE_URL="{postgresConnectionString}"```

Similarly add env variables for domain, api audience and algorithms used for auth0.

### Starting Application
To run the application, run the following commands:
```export FLASK_APP=app.py
python -m flask run
```

These commands put the application in development and directs our application to use the `app.py` file in our project. 

The applicaiton will run on `http://127.0.0.1:5000` by default.

## Tests
In order to run tests, run the following commands:
```
python -m test_app.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http:127.0.0.1:5000/`
* Authentication: Auth0 is used for authentication.
* Authorization Tokens are present in constants.py for different user types.
#### Models:
* Movies with attributes title and release date
* Actors with attributes name, age and gender

#### Endpoints:
* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/

#### Roles:
* Casting Assistant
  * Can view actors and movies
* Casting Director
  * All permissions a Casting Assistant has and…
  * Add or delete an actor from the database
  * Modify actors or movies
* Executive Producer
  * All permissions a Casting Director has and…
  * Add or delete a movie from the database


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 404,
  "message": "Not found"
}
```

The API will return these error types when requests fail:
* 400: Bad Request
* 401: UnAuthorized
* 403: Permission not found
* 404: Not Found
* 405: Method Not Allowed
* 422: Unprocessable
* 500: Server Error

### Endpoints
##### GET /actors
* General:
  * Returns a list of actors, success, and message.
  * Sample: `curl http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer {token}"` 
 ```
   {
      "actors": [
          {
              "age": 24,
              "gender": "male",
              "id": 1,
              "name": "new Actor"
          }
      ],
      "success": true
  }
 ```
  
##### GET /actors/<actor_id>
* General:
  * Return details of an actor.
  * Sample: `curl http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer {token}"` 
```
  {
      "actor": {
          "age": 24,
          "gender": "male",
          "id": 1,
          "name": "new Actor"
      },
      "success": true
  }
```

##### POST /actors
* General:
  * Add Actor.
  * Sample: `curl http://127.0.0.1:5000/actors/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "New Actor", "age": 24, "gender": "male"}'` 
```
  {
      "actors": [
          {
              "age": 24,
              "gender": "male",
              "id": 1,
              "name": "new Actor"
          },
          {
              "age": 24,
              "gender": "male",
              "id": 2,
              "name": "New Actor"
          }
      ],
      "message": "Actor added successfully",
      "success": true
  }
```

##### PATCH /actors/<actor_id>
* General:
  * Update Actor Details.
  * Sample: `curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d '{"name": "New Actor", "age": 24, "gender": "male"}'` 
```
  {
    "actors": [
        {
            "age": 24,
            "gender": "male",
            "id": 2,
            "name": "New Actor"
        },
        {
            "age": 24,
            "gender": "male",
            "id": 1,
            "name": "New Actor"
        }
    ],
    "message": "Actor details updated successfully",
    "success": true
  }
```

##### DELETE /actors/<actor_id>
* General:
  * Delete Actor.
  * Sample: `curl http://127.0.0.1:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {token}"'` 
```
  {
    "message": "Actor deleted successfully",
    "success": true
  }
```

Similarly, same api's are implemented for movies also.

 ### Authors
 Nitin Yadav
 
 ### Acknowledgements
 Udacity Full Stack Nanodegree Program
