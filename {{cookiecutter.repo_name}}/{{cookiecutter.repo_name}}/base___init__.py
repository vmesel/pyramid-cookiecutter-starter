from pyramid.config import Configurator
{%- if cookiecutter.backend == 'zodb' %}
from pyramid_zodbconn import get_connection

from .models import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())
{%- endif %}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_{{ cookiecutter.template_language }}')
    {%- if cookiecutter.backend == 'zodb' %}
        config.include('pyramid_tm')
        config.include('pyramid_retry')
        config.include('pyramid_zodbconn')
    {%- endif %}
    {%- if cookiecutter.rest_framework == 'cornice' %}
        config.include('cornice')
    {%- endif %}
    {%- if cookiecutter.backend == 'sqlalchemy' %}
        config.include('.models')
    {%- endif %}
    {%- if cookiecutter.backend == 'zodb' %}
        config.set_root_factory(root_factory)
    {%- endif %}
    {%- if cookiecutter.authentication == 'jwt' %}
        config.include('pyramid_jwt')
    {%- endif %}
    {%- if cookiecutter.pyramid_services == 'pyramid-services' %}
        config.include('pyramid_services')
        config.include('.services')
    {%- endif %}
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
