import inspect
import os

import mistune
from mistune.renderers.html import HTMLRenderer as MistuneRenderer
from mistune_contrib.toc import TocMixin
from aspen.request_processor import RequestProcessor as AspenRequestProcessor, DispatchStatus
from aspen.http.request import Path as AspenPath
from aspen.simplates.renderers import Renderer, Factory
from aspen.simplates.simplate import Simplate
from django.conf import settings
from django.http import \
    HttpResponse as DjangoResponse, \
    HttpResponseNotFound as DjangoNotFound, \
    HttpResponseRedirect as DjangoRedirect
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
            kw['renderer_default'] = 'markdown_then_django'

        # Instantiate and configure.
        arp = AspenRequestProcessor(*a, **kw)
        Simplate.renderer_factories['markdown_then_django'] = MarkdownRendererFactory(arp)
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

class Redirect(Exception):
    def __init__(self, to):
        self.to = to

def redirect(to):
    raise Redirect(to)

def view(django_request):
    aspen_path = AspenPath(django_request.path)
    last_part = aspen_path.parts[-1]
    if last_part and '.' not in last_part:
        # Redirect to trailing slash (I thought this was upstream in Aspen?).
        return DjangoRedirect(aspen_path.decoded + '/')
    arp = settings.ASPEN_REQUEST_PROCESSOR
    try:
        state = arp.process( aspen_path
                           , django_request.GET
                           , django_request.META.get('HTTP_ACCEPT', None)
                           , {'request': django_request, 'path': aspen_path}
                            )
    except Redirect as redirect:
        return DjangoRedirect(redirect.to)
    dispatch_result, _, output = state
    if dispatch_result.status == DispatchStatus.missing:
        return DjangoNotFound()
    body = output.body
    if type(body) is not type(b''):
        assert output.charset
        body = body.encode(output.charset)
    return DjangoResponse(content=body, content_type=output.media_type)


# setup Markdown rendering, with anchors for headers
class TocRenderer(TocMixin, MistuneRenderer):
    pass
toc = TocRenderer(escape=False)
markdown = mistune.Markdown(renderer=toc)

def gfm(md):
    toc.reset_toc()
    html = markdown(md)
    return html

wrapper = """
{{% extends "base.html" %}}
{{% block content %}}
{}
{{% endblock %}}
"""

class MarkdownRenderer(AspenDjangoRenderer):
    def compile(self, filepath, raw):
        raw = wrapper.format(gfm(raw))
        return AspenDjangoRenderer.compile(self, filepath, raw)

class MarkdownRendererFactory(AspenDjangoRendererFactory):
    Renderer = MarkdownRenderer
