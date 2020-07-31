# REST API with Flask and Python
## Credit: Jose Salvatierra - Teclado

### About this repo:
This simple REST API serves as my own springboard for other projects.  It implements Flask, RESTful architecture, user authentication, SQL and SQLAlchemy, Heroku, nginx, DNS, SSL, and token refreshing.  Features will be added to different branches and merged to master when complete.  Check branch history for most recent commits.  Dependencies will be automated at some point.

### Native environment:
All code has been written and tested in Ubuntu 20.04 and macOS Catalina V 10.15.6.  Any similar Linux distro based on Ubuntu should have no issues with this project.  As I continue my personal journey into software development, I'd like to 'dockerize' this project at some point.

### Setting things up:

Using PIPENV virtual environment with the following dependencies:
1. `$ pipenv install Flask`
2. `$ pipenv install Flask-RESTful`
3. `$ pipenv install Flask-JWT`

Once virtual environment is initialized and set up with our dependancies, remember to launch the environment to ensure global packages aren't changed:

`$ pipenv shell`

If using VSCode text editor, ensure correct Python interpreter is selected for your virtual environment or packages will not be found.