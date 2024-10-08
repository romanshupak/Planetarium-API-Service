# Planetarium-API-Service


## Overview
Planetarium-API-Service is a web application designed to manage a planetarium, 
including the creation and administration of shows, sessions, reservations, 
and tickets. This service provides a REST API for handling information about 
planetarium domes, astronomy shows, sessions, and ticket reservations. 
The system is built with a focus on ease of use for both users and administrators, 
as well as robust data validation.

# Features
### Planetarium Dome Management

* Allows the creation and editing of planetarium dome details, including the number of rows and seats per row.
  
### Astronomy Show Management

* Add, edit, and delete astronomy shows with options to upload images and assign themes to each show.

### Session Scheduling

* Organize and manage show sessions linked to specific planetariums, including selecting the date and time for each session.

### Ticket Reservations

*  Users can book tickets for selected sessions, with the system ensuring seat availability and validating ticket information.

### Dynamic Seat Availability Display

*  For each session, the occupied seats are displayed, helping users choose available seats.

### Authentication and Authorization

* Supports JWT-based authentication for secure access to the API. Administrators have extended privileges to manage the entire system.

### API Documentation

* Built-in API documentation generated with drf_spectacular provides convenient access to descriptions of available endpoints.

### Powerful admin panel for advanced managing

## Usage
### User Authentication

* Secure login system to ensure only authorized personnel can create, update, or delete maintenance tasks.

#### The possibility to make registration and obtain your personal JWT Token:
* http://127.0.0.1:8000/api/user/register/
* http://127.0.0.1:8000/api/user/token/

## Installation
Python3 must be already installed
* git clone https://github.com/romanshupak/Planetarium-API-Service.git
* cd Planetarium-API-Service
* python -m venv venv
* venv\Scripts\activate (on Windows)
* source venv/bin/activate (on macOS)
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver

### Environment Variables
To configure the application, you need to set up the following environment variables in your .env file:

* POSTGRES_PASSWORD: The password for your PostgreSQL database.
* POSTGRES_USER: The username for your PostgreSQL database.
* POSTGRES_DB: The name of your PostgreSQL database.
* POSTGRES_HOST: The host address for your PostgreSQL database (e.g., localhost or the address of your PostgreSQL server).
* POSTGRES_PORT: The port number on which your PostgreSQL database is running.
* PGDATA: The directory where PostgreSQL will store its data files (e.g., root).
* DJANGO_SECRET_KEY: The secret key used by Django for security purposes. This should be a long, random string.

Make sure to replace the placeholder values with your actual configuration settings before running the application.


## Run with docker
Docker should be installed
* docker-compose build
* docker-compose up

## Getting access
* create user via /api/uer/register/
* get access token via /api/user/token/

## Getting Started
To get started with Maintenance Manager, follow these steps:

1. Clone the repository from GitHub.
2. Install the necessary dependencies.
3. Set up the database with the required schemas.
4. Run the application and log in to access the full range of features.


## Additional Info
For demonstration purposes, you can use the following token credentials:

* Email: test_admin@admin.com
* Password: test12345

In Docker
* Email: docker_admin@admin.com
* Password: docker12345


#### These credentials provide access, allowing you to explore the application's features.