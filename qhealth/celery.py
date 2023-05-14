


from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime
from django.conf import settings

if "QHEALTH_CLOUD" not in os.environ:
    from celery import Celery
    from celery.schedules import crontab

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qhealth.settings")

    if "CI" in os.environ:
        app = Celery(
            "qhealth",
            backend="redis://localhost:6379/1",
            broker="redis://localhost:6379/0",
        )
    else:
        app = Celery(
            "qhealth", backend="redis://redis:6379/1", broker="redis://redis:6379/0"
        )

    app.autodiscover_tasks()

    @app.task(bind=True)
    def debug_task(self):
        print(f"Request: {self.request!r}")

    if not settings.IS_TEST:
        app.conf.beat_schedule = {
            "backup-db": {
                "task": "frontend.tasks.backup_db",
                "schedule": crontab(hour=16, minute=30),
                "options": {
                    "expires": int(settings.DBBACKUP_INTERVAL * 24 * 3600),
                },
            },
        }

        if settings.PING_SATELLITE.lower() == "true":
            app.conf.beat_schedule = {
                "ping-satellite": {
                    "task": "frontend.tasks.ping_satellite",
                    "schedule": crontab(minute=(datetime.now().minute + 1) % 60),
                    "options": {
                        "expires": 3600,
                    },
                },
            }
