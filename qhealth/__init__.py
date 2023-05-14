


from __future__ import absolute_import, unicode_literals

import os

if "QHEALTH_CLOUD" not in os.environ:
    from .celery import app as celery_app

    __all__ = ("celery_app",)
