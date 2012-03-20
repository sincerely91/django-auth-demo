# Django Better Auth

A authentication app for Django.

## How is this app better than other auth apps

* class base views
* no dependencies on other packages (unless you wish to add more functionality, like email confirmations)
* allow customizations on every level
	* urls are configured though a class and the location of the class can be provided though settings.py
* email activation and email confirmation are optional, though a related module called django_better_emails
* patch the User model if needed, for example to make the email field unique and not null
* use Django's auth functions as much as possible, i.e. password_reset, logout, etc
* login though username & password, email & password, (username | email) & password
* usable base forms for authentication, user creation, etc

## Installation

* add "better.auth" to INSTALLED_APPS
