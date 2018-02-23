GENERAL INFORMATION
===================

*REST-Flask-boostrap* is a generic Flask boilerplate(?)code for rapid development of REST interfaces. We have very good flask resources online:

[https://github.com/humiaozuzu/awesome-flask](https://github.com/humiaozuzu/awesome-flask)

But, sometimes putting everything together can be cumbersome, this is a bootstrap code to get you goin on develop your own REST, also as study material(?)

The project uses the following packages:

 - Flask==0.12.2
 - Flask_RESTful==0.3.6
 - Flask_SQLAlchemy==2.1
 - SQLAlchemy==1.1.10
 - marshmallow==2.13.5
 - webargs==1.7.0
 - flasgger==0.8.0
 - Flask_Env==1.0.1

Python version: 3.6

The code here presented is 1 way to put it together, if you think something is not ok or could be improved please fork and make a pull request.

The main object is for presented code to be simple, straight forward and pythonic. **Let the code speak by it self**

Setup and run
=============

Clone the repository to your local computer:

```
https://github.com/GeoCat/REST-Flask-boostrap.git 
```

To run the code just call **app.py**

```
cd  REST-Flask-boostrap.git
pip3 install -r requirements.txt
python3 app.py
```

The *app.py* will start the Flask server with contents

To evalute the REST API, check the openAPI docs: 

```
http://127.0.0.1:5001/api/v1.0/apidocs#/default
```

Flasgger is able to do REST calls to the different end points, with example data. If necessary there are text files for testing in folder `tests/data`

Package Integration
===================

The following packages/frameworks are part of the code:

**[Flask-Restful](https://flask-restful.readthedocs.io)** Functions/Classes for REST API.
**[webargs](https://github.com/sloria/webargs)** Argument validation and check
**[Flask_Env](https://github.com/brettlangdon/flask-env)** Flask configuration using classes
**[Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)** SQLAlchemy for database access and record control
**[flasgger](https://github.com/rochacbruno/flasgger)** Testing REST and documenting functionality


app.py
======

This is the python file from where we start Flask REST api, read it first 


REST structure
==============

Restful uses a very straight foward class struture read the docs to understand it: ([here](https://flask-restful.readthedocs.io)).

Each endpoint is represented as class locate in folder 

```./resources/v1``` 


the good thing about Flask-Restful is that each HTTP Verb is a simple class method, example for a HTTP GET
```
class Welcome(Resource):
   def get(self):
       now = datetime.datetime.now()
       app.logger.debug("Time of request {}".format(now))
       return jsonify({"message":"Lekker!!!", "version": app.config["VERSION"], "date": now})
```


The end points are register on the file: *app.py* e.g:
```
    from resources.v1.welcome import Welcome
    ....
    API10.add_resource(Welcome, '/welcome')
```

The rest end point */welcome/* is now mapped to class Welcome. Notice in the code that we use blueprints

```
APP = Flask(__name__)
BLUEPRINT = Blueprint('tree', __name__)
PREFIX = "/api/v1.0"
API10 = Api(BLUEPRINT, prefix=PREFIX)
```

Therefore the actual URL for the end point will be something like `http://localhost:5001/api/v1.0/welcome`

For more information about blueprints read: ([here](http://flask.pocoo.org/docs/0.12/blueprints/))

Webargs
=======

There is 10 milion ways to checks the arguments and requests being passed to Flask, even Flask-Restufull has amazing stuff but Webargs is very simple and gets the job done integrated on the classes from Flask-Restful

Webargs docs ([here](https://webargs.readthedocs.io/en/latest/))

The idea is to use webargs as class variables (code in classes of folder `./resources/v1/`)
```
class Query(Resource):
    """Query class testing 2 inputs one numerical other string"""
    args = {
        'number': fields.Float( #pylint: disable=E1101
            required=True,
            validate=lambda x: -1.0 <= x <= 1.0
        ),
        'string' : fields.Str( #pylint: disable=E1101
            required=False,
            validate=lambda x: x in ["dog", "cat"]
        )
    }
    @use_kwargs(args)
    @swag_from("swagger/query.yml")
    def get(self, number, string): #pylint: disable=R0201
        """Method returning input"""
        return jsonify(number=number, string=string)
```

Look with attention between Class Query and the get method we have definiion of 2 inputs: **number** and **string**

Number will validate if it is between -1.0 and 1.0 while the string has to be **dog** or **cat**

The decorator `@use_kwargs` is from package webargs


OpenAPI Flasgger
================

OpenAPI (Swagger) is an open spec for describing, consuming and generate contents for REST webservices,for more information:([link](https://github.com/OAI/OpenAPI-Specification)).

Normally we have tools like postman for testing REST points since it is simple to make the an HTTP call from your browser, but when run swagger we have a dedicated website for testing and documenting the API (e.g what does it do when an argument is invalid, with default data and explanations)

REST needs to be described as a yml document, for each endpoint we have a yml file describing it located on folder: `/resources/v1/swagger` 

Again the idea is that docs should be the closest possible to the class running the end point. 

Please read the Flasgger docs: ([here](https://github.com/rochacbruno/flasgger))

Each Flask-REST class has a decorator pointing to the documentation:

```
from flasgger import swag_from
class Welcome(Resource):
    """Welcome class for testing REST"""
    @swag_from('swagger/welcome.yml')
    def get(self):
        now = datetime.datetime.now()
        app.logger.debug("Time of request {}".format(now))
        return jsonify({"message":"Lekker!!!", "version": app.config["VERSION"], "date": now})
```

Each method can have a different file, at the end the Flagger module will bundle everything and make a full website that will run in:

```
http://127.0.0.1:5001/api/v1.0/apidocs#/default
```

You will learn alot by playing with the system :)

CONFIG
======

Configuration classes are in folder `etc/__init__.py`

Flask can be configured using yml files, classes, dictionarties etc etc. Major problem is to diferenciate between production and development. Using classes we can use inheritance for configuration (one base class with everything and other child classes with the necessary modifications)

Flask configuration docs ([here](http://flask.pocoo.org/docs/0.12/config/))

In the docs we have something "ugly"
```
app.config.from_object('configmodule.ProductionConfig')
```

The config module is imported as a string, bit strange

**Flask**_Env allows loading a class as configuration

In **app.py**
```
from etc import DevelopmentConfig as Config
APP.config.from_object(Config)
```

And in the **__init__** in folder etc/
```
from flask_env import MetaFlaskEnv
import os, tempfile

from __init__ import __version__

# pylint: disable=too-few-public-methods
class BaseConfig(metaclass=MetaFlaskEnv):
    """BaseClass from where other configurations will de derived"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Just to remove the warning and tracking of SQLALCHEMY 
    DBPATH= os.path.join(".", "task_database.db")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DBPATH)
    LOG_FILE = "flask.log"
    UPLOAD_FOLDER = tempfile.mkdtemp(prefix="rest_api") 
    PORT = 5001
    MAX_UPLOAD = 100
    VERSION = __version__
    HOST = "0.0.0.0"
```

The advantage of class config is that we can use python code to set parameters e.g: `UPLOAD_FOLDER = tempfile.mkdtemp(prefix="rest_api")`

Flask_SQLAlchemy
================


SQLAlchemy (and Flask_SQLAlchemy) has lots and lots of docs online start with the generic docs ([here](http://flask-sqlalchemy.pocoo.org/2.3/))

SQLAlchemy is a programatically way to deal with SQL (normally refered as object relational mapping), the idea is that the database structure is mapped as classes, atributes, methods etc etc. 

REST end point `/tasks` is a classic text book example of SQLAlchemy, the models are in `models.py`.

This topic is to extensive to be described in a  *README.md* 

  

Contact
=======

- [Jorge S. Mendes de Jesus](https://github.com/jorgejesus)
- [Anton Bakker](https://github.com/arbakker) 
