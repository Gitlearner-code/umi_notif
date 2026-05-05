"""Print 500 response body with DEBUG=True to capture tracebacks."""
import os
import re
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "umi_notif.settings")

import django

django.setup()

from django.conf import settings  # noqa: E402

settings.DEBUG = False  # match production / typical local when DEBUG env unset

from django.test import Client  # noqa: E402


def main():
    c = Client()
    r = c.get("/", HTTP_HOST="127.0.0.1")
    m = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', r.content)
    if not m:
        print("GET failed", r.status_code, r.content[:500])
        return
    csrf = m.group(1).decode()
    r2 = c.post(
        "/",
        {
            "csrfmiddlewaretoken": csrf,
            "departement": "G.I",
            "level": "L2",
            "message_type": "SUG",
            "content": "x",
            "attestation": "on",
            "preview": "x",
        },
        HTTP_HOST="127.0.0.1",
    )
    m2 = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', r2.content)
    csrf2 = m2.group(1).decode() if m2 else csrf
    r3 = c.post(
        "/",
        {
            "csrfmiddlewaretoken": csrf2,
            "departement": "G.I",
            "level": "L2",
            "message_type": "SUG",
            "content": "x",
            "post": "x",
        },
        HTTP_HOST="127.0.0.1",
    )
    print("status", r3.status_code)
    if r3.status_code >= 400:
        print(r3.content.decode("utf-8", errors="replace")[:8000])


if __name__ == "__main__":
    main()
