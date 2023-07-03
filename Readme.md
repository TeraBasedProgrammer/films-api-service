# Films api service
This RESTful API service is a part of the training project Cinotes (currently unavailable).
* [Full backend repository](https://github.com/anton-uvarenko/cinema)
* [Frontend repository](https://github.com/YarikShaman/Project_pratice)

## Technologies used
* [Django](https://docs.djangoproject.com/en/4.2/): The web framework for perfectionists with deadlines
* [Django Rest Framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs
* [Docker](https://docs.docker.com/get-started/): Develop faster. Run anywhere
* [Docker compose](https://docs.docker.com/compose/): Tool for defining and running multi-container Docker applications
* [PostgreSQL](https://www.postgresql.org/): The world's most advanced open source database
* [Amazon S3](https://aws.amazon.com/ru/s3/): Cloud object storage with industry-leading scalability, data availability, security, and performance
## Installation
* If you wish to run your own build, first ensure you have installed [Python](https://www.python.org/downloads/release/python-3106/) and [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) (docker engine and docker compose for Linux)
* If everything is installed, clone this repository to your computer:

  ```
  git clone https://github.com/TeraBasedProgrammer/films-api-service.git
  ```
* Setup dependencies
  1. Cd into the project directory
      ```bash
      $ cd films-api-services
      ```
  2. Create a python virtual environment
      ```bash
      $ python -m venv env
      ```
  3. Activate venv
     * Linux
     ```bash
     $ source env/bin/activate
     ```

     * Windows (run the file)
     ```bash
     $ env\Scripts\activate.bat
     ```
  4. Install dependencies
      ```bash
      $ pip install -r films/requirements.txt
      ```
* Run the application
  * Makefile
  ```bash
  $ make run
  ```
  or
  * Docker compose
  ```bash
  $ docker compose up -d
  ```
## Usage

To see full documentation of the project [import](https://youtu.be/M-qHvBhULes) films-api-docs.json to your Postman workspace.

