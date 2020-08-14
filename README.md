# REST API with Flask and Python
## Credit: Jose Salvatierra - Teclado

### About this repo:
This simple store REST API serves as my own springboard for other projects.  It was built alongside Jose Salvatierra's REST API tutorial hosted on Udemy, [which can be found here.](https://www.udemy.com/course/rest-api-flask-and-python) It introduces Flask, RESTful architecture, user authentication, SQL and SQLAlchemy, Heroku, nginx, DNS, SSL, and token refreshing.  The virtual environment was set up slightly different than instructed (see below).  Each section of the tutorial was completed on a seperate branch with the final section merged at the end.  You can review the branch history to see the different steps leading up to the most recent changes seen here.

### Native environment:
All code has been written and tested in Ubuntu 20.04 and macOS Catalina V 10.15.6.  Any similar Linux distro based on Ubuntu should have no issues with this project.

### Setting things up:

Using PIPENV virtual environment with the following dependencies:
1. `$ pipenv install Flask`
2. `$ pipenv install Flask-RESTful`
3. `$ pipenv install Flask-JWT`
4. `$ pipenv install Flask-SQLAlchemy`

Once virtual environment is initialized and set up with our dependancies, remember to launch the environment to ensure global packages aren't changed:

`$ pipenv shell`

If using VSCode text editor, ensure correct Python interpreter is selected for your virtual environment or packages will not be found.