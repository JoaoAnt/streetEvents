# Street Occurrences
One weekend backend django with PostGis Project.

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs
* [Docker](https://www.docker.com/): Empowering App Development for Developers


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* Turn on Docker on your local machine.
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/JoaoAnt/streetEvents
    ```
* To build the containers
    ```bash
        $ docker-compose build
    ```
* To have the docker up and running:
    ```bash
        $ docker-compose up
    ```
* You can now access the file api service on your browser by using
    ```
        http://localhost:8000/
    ```

## Testing
* Run the command:
    ```bash
        $ docker-compose run web python manage.py test
    ```

## Database Related commands
* Make Migrations:
    ```bash
        $ docker-compose run web python manage.py magemigrations
    ```
* Migrate:
    ```bash
        $ docker-compose run web python manage.py magemigrations
    ```
## API Endpoints
* Dynamic documentation
- '/swagger'
- '/redoc'

* Static Documentation
- '/swagger.json'
- '/swagger.yaml'

* Authentication
- '/api-auth'

* Events Endpoints
- '/events'
- '/events/pk'
