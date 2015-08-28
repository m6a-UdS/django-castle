========
Usage
========

To use django-castleio in a django project::

1. Add the package ``djcastleio`` to ``settings.INSTALLED_APPS``

2. Set the following setting variables::

    CASTLEIO_API_KEY = "your key"
    CASTLEIO_API_SECRET = "your secret"

3. Add the ``{% load castleio %}`` template tag on the top of your templates where you want to track users

4. Add the following tags to the templates in the bottom of the head::

    {% castleio_load %}
    {% castleio_register_user request.user %}
    {% castleio_secure %}
