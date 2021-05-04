![CD](https://github.com/Soufiane-Fartit/MySocial/workflows/CD/badge.svg)


# MySocial

A mini social network built using flask.

## Run :

To run the application you simply have to :

- spin an sql database and create a configuration file (example shown below)

- build the docker image ```docker-compose build```

- run the docker image ``` docker-compose up -d --scale gunicorn=3 ```

- go to : `localhost`

___

## Configuration File :

create a file : `mySocial/mySocial/config.ini` that holds configuration for the application

Example :

```
[Database]
USER_NAME : admin
PASSWORD : 123456789
IP : mysocial.blablabla.eu-west-3.rds.amazonaws.com
DB_NAME : mySocial

[App]
secret_key : somesecretkeyhere
SQLALCHEMY_TRACK_MODIFICATIONS : False
```
___

## TODO

<input type="checkbox" disabled /> detect remote webrtc connection closed

___

## Improvement ideas

None for the moment