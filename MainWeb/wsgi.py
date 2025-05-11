"""
WSGI config for MainWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MainWeb.settings')

application = get_wsgi_application()

import os
if os.environ.get("RUN_SUPERUSER", "false") == "true":
    import subprocess
    subprocess.call(["python", "create_superuser.py"])
