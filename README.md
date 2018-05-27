![SP Group Logo](https://www.spgroup.com.sg/www/theme/logo.png)

# SP Group Full Stack Engineer Coding Test

## Background
For any application with a need to build its own social network, "Friends Management" is a common requirement
which usually starts off simple but can grow in complexity depending on the application's use case.

Usually, applications would start with features like "Friend", "Unfriend", "Block", "Receive Updates" etc.

## Task

Develop an API server that does simple "Friend Management" based on the User Stories below.

## Technologies chosen

* Python
* Django>2.0
* [Django Rest Framework](http://www.django-rest-framework.org/)
  * I had problems learning the framework while doing
* [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/)
* [Neo4j](https://neo4j.com/)
  * A graph database is probably best suited for this social network question
  * It did take some time to learn the cypher query format
* [django_neomodel](https://github.com/neo4j-contrib/django-neomodel)
  * I needed something that interfaced seamlessly with neo4j for django
* [neomodel](http://neomodel.readthedocs.io/en/latest/)

## TODO
- Actually leverage on Django Rest Framework's authentication service - No authentication at the moment
- My code is bad for situations where the number of data in the db is huge.  I will need to  optimize all the calls

## Installing / Getting started
- run the docker compose command to get the neo4j and django server up and running.
```shell
git clone https://github.com/stlimtat/sp-test.git
cd <path>/sp-test
docker-compose up
```
- Once the docker is running, you can browse to the link below to view the APIs
  - [http://localhost:8000/](http://localhost:8000/)

## Features

### APIs

1. Create Friends

```
POST /friends/
{
  friends:
    [
      'andy@example.com',
      'john@example.com'
    ]
}
```

This should create the entries andy@example.com and john@example.com, and then link them up as friends in the database

2. Get all persons recorded in system

```
GET /friends/
```

This provides a full list of all the persons recorded in the database

3. Get persons who are friends of specific user

```
GET /friends/
{
  email: 'andy@example.com'
}
```

Or

```
GET /friends/?email=andy@example.com
```

*I was not sure how to do this properly.  I can always handle this via a POST but just seems to contradict the REST 
requirements.  So in the end, I just left it as-is.  I will be happily using GET with a request body.*

This API returns the list of all friends of andy@example.com

4. Get common friends between 2 users

```
GET /friends/
{
  friends:
    [
      'andy@example.com',
      'john@example.com'
    ]
}
```

*Again the issue of how to handle JSON body with GET*
This API returns the list of all common friends of the listed email ids.

5. Subscribe to updates from an email address

```
POST /subscribe/
{
  "requestor": "lisa@example.com",
  "target": "john@example.com"
}
```

This should connect from the requestor to the target with a relationship of SUBSCRIBE.  
This relationship is directional.

The SUBSCRIBE relationship will need to be obtained later.

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under Apache 2.0 license.
