# Fiestabulous
A webpage to party and have fun!

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technologies](#technologies)
- [Backend](#backend)
- [Frontend](#frontend)
- [How to use it](#how-to-use-it)
- [Authors](#authors)

## Description
Fiestabulous is a project that allows people to find upcoming events. Users can enroll for an event as long as there are available spots. The users can also create and manage their own party and modify some aspects about it.

## Features
- Create an account
- Login
- Create an event
- Edit an event
- Delete an event
- Enroll for an event
- Explore events
- See the details of an event
- See the details of an event as an organizer

## Technologies
The project is developed using the following technologies:
- Backend:
    - Python
    - Flask
    - MySQL
    - Azure Database for MySQL
- Frontend:
    - HTML
    - CSS
    - JavaScript
    - Bootstrap
    - JQuery

## Backend
The backend is developed using Python and Flask. The database is hosted in Azure Database for MySQL. The backend works as a REST API, the endpoints are the following:
- `/user`
    - **POST**: Create a user
    - **GET**: Get all the users
- `/user/<user_id>`
    - **GET**: Get a specific user
    - **PUT**: Update a specific user
    - **DELETE**: Delete a specific user
- `/event`
    - **GET**: Get all the events
    - **POST**: Create an event
- `/event/<event_id>`
    - **GET**: Get a specific event
    - **PUT**: Update a specific event
    - **DELETE**: Delete a specific event
- `/guest/<event_id>/guest?type=<type>`
    - **GET**: Get all the guests of an event
    - **POST**: Add a guest to an event
- `/guest/<guest_id>`
    - **PUT**: Update a specific guest
    - **DELETE**: Delete a specific guest
- `/options?table=<table>&field=<field>&value=<value>`
    - **GET**: Get the options that the URL provides

## Frontend
The frontend is developed using HTML, CSS, JavaScript, Bootstrap and JQuery. The frontend uses fetch to communicate with the backend. The frontend is divided in the following pages:
- `/`: Home page
- `/auth/login`: Login page
- `/auth/register`: Register page
- `/parties`: Parties page
- `/party/<party_id>`: Party page
- `/party_admin/<party_id>`: Party admin page

## How to use it
To use it you need to access the following link: [https://fiestabulous.azurewebsites.net/](https://fiestabulous.azurewebsites.net/) and create an account. Once you have an account you can create your own parties or enroll for other parties you find interesting.

## Authors
- [Johan Cabrera](https://github.com/PAPIPHOX)
- [Omar Macias](https://github.com/OmarMacMa)
