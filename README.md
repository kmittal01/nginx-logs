# Column: Nginx Logs

Mini Project to check nginx logs of the system, where it's deployed.

## Features

- **FastAPI** with Python 3.8
- MongoDB
- Docker compose for easier development

### Run with Docker

Starting the project with hot-reloading enabled
(the first time it will take a while):

```bash
docker-compose up -d
```

And navigate to http://localhost:8014/api/docs

## Generating Credentials for Local Env:
There is no api to create user, so in order to create user, edit `initial_data.py` 
with your own credentials and run the following command:
`docker-compose run backend_column python3 column/initial_data.py`.
Default Credentials  in this file are `kshitij.mittal01@gmail.com` and `password`.
`
## Navigating Through APIs

 * Open Swagger Docs and click on Authorize button. Enter the Credentials provided through Email.
 * Under Nginx Logs, there are 3 APIs.
 * First - `api/v1/nginx-logs-raw` - fetches all logs from nginx logs file. User can use this to go through logs.
 * Second Inserts Last `n` Logs into the database from nginx logs file. `n` is optional parameter, default being 100.
   To be noted, sha_256 hash value is created and saved with every log as a unique identifier, so that the same log is never saved again.
 * Third API gets paginated the logs from the database, in a readable format.

## Accessing Database:
* On Local, database can be accessed at http://localhost:8085/db/column/. 
*  On Production, database can be accessed through ssh port forwarding of port 8085.


### Rebuilding containers:

```
docker-compose build
```

### Restarting containers:

```
docker-compose restart
```

### Bringing containers down:

```
docker-compose down
```


## Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # backend_column|mongo_column
```