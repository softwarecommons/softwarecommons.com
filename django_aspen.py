from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
import os

from aspen.request_processor import RequestProcessor as AspenRequestProcessor
from aspen.http.request import Path as AspenPath
from aspen.simplates.renderers import Renderer, Factory
from aspen.simplates.simplate import Simplate
from django.conf import settings
from django.http import HttpResponse as DjangoResponse
from django.template import Template
from django.template.context import Context as DjangoContext


class NoProjectRoot(Exception):
    pass


def install(*a, **kw):
    """Install Aspen into a Django app.
    """
    arp = kw.pop('_aspen_request_processor', None)
    if arp is None:

        # Infer project and www roots.
        default_project_root = None
        parent = inspect.stack()[1]
        if parent:
            default_project_root = os.path.dirname(parent[1])
        kw['project_root'] = kw.get('project_root', default_project_root)
        if kw['project_root'] is None:
            raise NoProjectRoot()
        kw['www_root'] = kw.get('www_root', os.path.join(kw['project_root'], 'www'))
        if 'changes_reload' not in kw:
            kw['changes_reload'] = settings.DEBUG
        if 'renderer_default' not in kw:
            kw['renderer_default'] = 'django'

        # Instantiate and configure.
        arp = AspenRequestProcessor(*a, **kw)
        Simplate.renderer_factories['django'] = AspenDjangoRendererFactory(arp)
    return arp


class AspenDjangoRenderer(Renderer):

    def compile(self, fspath, raw):
        return Template(raw)

    def render_content(self, aspen_context):
        django_context = DjangoContext(aspen_context)
        return self.compiled.render(django_context)


class AspenDjangoRendererFactory(Factory):
    Renderer = AspenDjangoRenderer


def view(django_request):
    arp = settings.ASPEN_REQUEST_PROCESSOR
    state = arp.process( AspenPath(django_request.path)
                       , django_request.GET
                       , django_request.META.get('HTTP_ACCEPT', None)
                       , {'request': django_request}
                        )
    _, _, output = state
    body = output.body
    if type(body) is not type(b''):
        assert output.charset
        body = body.encode(output.charset)
    return DjangoResponse(content=body, content_type=output.media_type)
