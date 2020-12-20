# API for YaMDb

[![YourActionName Actions Status](https://github.com/kabanovanika/yamdb_final/workflows/Yamdb-final%20workflow/badge.svg)](https://github.com/kabanovanika/yamdb_final/actions)

REST Api for YaMDB service - database of movie, books and music reviews. 
The available endpoints are reflected in documentation, which will be available after running the project, 
via link [http://localhost:80/redoc/](http://0.0.0.0:80/redoc/)

## Getting Started

To start this project you need to clone this repository to your local machine. 

### Prerequisites

After cloning the repo you need to install all the requirements with the command below. 

```
pip install -r requirements.txt
```
You also need Docker to be installed and started. Please check [docker.com](https://www.docker.com) for further instructions. 

### How to use

To start the app you need only one simple command. Check if you are in the root directory of the project.

```
docker-compose up
```

It will start the containers and project will be available on http://0.0.0.0:80/admin/

You need to collect static with the command 

```
docker-compose exec web python manage.py collectstatic
```

To create superuser use command below

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser 
```

To fill database with test data use the command 

```
docker-compose exec web python manage.py loaddata fixtures.json
```

## Built With

* [DRF](https://www.django-rest-framework.org/) - The web framework used

## Authors

* **Nika Kabanova** - *Initial work* - [kabanovanika](https://github.com/kabanovanika) - Yandex.Praktikum student 🤓 
