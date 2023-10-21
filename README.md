# PostPay Back-end Assessment

## Instructions
For this assignment we are making use of the star wars api (swapi.dev)
For the purpose of this assignment we are going to assume that there is a cost to using the api and
that in order to save costs we are going to create a cache of the data and only call the actual
endpoint every 5 minutes (but this value must be configurable so we can change it at will)
We are interested in the people API and the aim of the project is to use django and/or django rest to
have the following endpoints
1. provide a list of characters to the consumer which can be filtered by a search eg
GET /people?search=lu
and thus get back luke skywalker etc
2. an endpoint to allow the consumer to provide a vote from 1-5 to vote on their favourite character
(5 being highest)
3. a top 10 endpoint to give back the ranked top ten favourite characters
Please include a single unit test of your

## Solution
We will be building a django backed lightweight consumer for the SWAPI Api.
Some assumptions were made for this assessment:
1. No front facing presentation. Purely api
2. Redis cache is used for all local storage, No need for a database

### 1. Stack
Docker is the only prerequisite to get this application up and running.
Please make sure you have it installed
```bash
$ docker --version
Docker version 24.0.6, build ed223bc
```

The application stack looks like this:

- Python 3.10.13
- Django 4.2
- Redis 7.2

### 2. Local Development

From your terminal, clone the project:
```bash
# SSH
$ git clone git@github.com:pstevek/swapi-consumer.git

# HTTPS
$ git clone https://github.com/pstevek/swapi-consumer.git
```

Navigate to the root project and run the application containers via Docker:
```bash
$ cd swapi-consumer
$ ./start.sh
```

The above `start.sh` script creates an environment based on the sample one provided and launches the required docker containers on your local network
```
NOTE: Caching TTL is set to 5ms (300s). It can be changed via the `.env.sample` file to any desired value
```

### 3. Endpoints

### GET /people/{id}
`localhost:8000/people/1`
```json
{
    "success": true,
    "data": [
        {
            "id": "1",
            "name": "Luke Skywalker",
            "vote": 0
        }
    ]
}
```

### GET /people?search={string_search}
`localhost:8000/people?search=lu`
````json
{
    "success": true,
    "data": [
        {
            "id": "1",
            "name": "Luke Skywalker",
            "vote": 0
        },
        {
            "id": "64",
            "name": "Luminara Unduli",
            "vote": 0
        }
    ]
}
````

### POST /people/{id}
`localhost:8000/people/7`

`body`
````json
{
    "vote": "3"
}
````

`response`
```json
{
    "success": true,
    "data": [
        {
            "id": "7",
            "name": "Beru Whitesun lars",
            "vote": 3
        }
    ]
}
```

### GET /people/votes
````json
{
    "success": true,
    "data": [
        {
            "id": "2",
            "name": "C-3PO",
            "vote": 4
        },
        {
            "id": "7",
            "name": "Beru Whitesun lars",
            "vote": 3
        },
        {
            "id": "1",
            "name": "Luke Skywalker",
            "vote": 0
        },
        {
            "id": "64",
            "name": "Luminara Unduli",
            "vote": 0
        }
    ]
}
````


### 4. Unit Test
In order to run the available unit test in the people app, run the following command from your terminal in the root directory of the project:
```bash
docker compose run --rm app sh -c "python manage.py test"
```
You should get something similar to this:
```bash
[+] Building 0.0s (0/0)                                                                                                                                                                        docker:desktop-linux
[+] Creating 1/0
 ✔ Container postpay-db  Running                                                                                                                                                                               0.0s
[+] Building 0.0s (0/0)                                                                                                                                                                        docker:desktop-linux
Found 1 test(s).
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
```