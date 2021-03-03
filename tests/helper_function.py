from contextlib import contextmanager

from flask import template_rendered


@contextmanager
def captured_templates(app):
    """
    Helper context manager function taken from Flask docs for unit testing.
    Determines the template rendered and the variables passed to it.
    """

    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
