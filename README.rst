===============
django-castleio
===============

A django integration for the castle.io service

Documentation
-------------

Using the http://castle.io service this package allows for simple user tracking.

Quickstart
----------

Install django-castleio::

    pip install django-castleio

Then use it in a project::

1. Add the package ``djcastleio`` to ``settings.INSTALLED_APPS``

2. Set the following setting variables::

    CASTLEIO_API_KEY = "your key"
    CASTLEIO_API_SECRET = "your secret"

3. Add the ``{% load castleio %}`` template tag on the top of your templates where you want to track users

4. Add the following tags to the templates in the bottom of the head::

    {% castleio_load %}
    {% castleio_register_user request.user %}
    {% castleio_secure %}

Features
--------

* API wrapper
* Settings for API Key and Secret
* Hook for the login and logout signals
* template tags for user tracking

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
