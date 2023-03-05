import uuid

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EMail(object):
    def __init__(self, to, subject, cc=[], bcc=[]):
        self.to = to
        self.subject = subject
        self.cc = cc
        self.bcc = bcc
        self._html = None
        self._text = None
        self._random_string = str(uuid.uuid4())

    def _render(self, template, context):
        return render_to_string(template, context)

    def html(self, template, context):
        self._html = self._render(template, context)

    def text(self, template, context):
        self._text = self._render(template, context)

    def send(self, from_addr=None, fail_silently=False):
        if isinstance(self.to, str):
            self.to = [self.to]
        if not from_addr:
            from_addr = getattr(settings, "EMAIL_FROM_ADDR")
            prefix_title = getattr(settings, "EMAIL_PREFIX_TITLE", "Easystart")
            # generate random address
            address_string = from_addr.split("@")
            from_addr = "{0} <{1}-{2}@{3}>".format(
                prefix_title, address_string[0], self._random_string, address_string[1]
            )

        msg = EmailMultiAlternatives(
            self.subject, self._text, from_addr, self.to, bcc=self.bcc, cc=self.cc
        )

        if self._html:
            msg.attach_alternative(self._html, "text/html")

        msg.send(fail_silently)
