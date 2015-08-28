========
Usage
========

To use django-castle in a django project::

1. Add the package ``djcastle`` to ``settings.INSTALLED_APPS``

2. Set the following setting variables::

    CASTLE_API_KEY = "your key"
    CASTLE_API_SECRET = "your secret"

3. Add the ``{% load castle %}`` template tag on the top of your templates where you want to track users

4. Add the following tags to the templates in the bottom of the head::

    {% castle_load %}
    {% castle_register_user request.user %}
    {% castle_secure %}
