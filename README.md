# task-api
The api for the task application.  Based off of https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way.

# Setup
Ensure you have `virtualenv`. Then:

```
$ git clone git@github.com:chrisworman/task-api.git
$ cd task-api
$ virtualenv env
$ source env/bin/activate
$ env/bin/pip install -r requirements.txt
$ flask run
$ # ... api server should be listening now! ...
$ deactivate
```

TODO: talk about exporting environment variables, or even better, figure out a better way of dealing with environment variables.
