from django.apps import AppConfig
import threading
import subprocess
import os


class RestFrameworkConfig(AppConfig):
    name = 'ardhi_framework'
    verbose_name = "Ardhi Lands framework"

    def ready(self):
        """
        This function runs when Django starts.
        We can use it to trigger migrations *once* on server startup.
        """
        if os.environ.get('RUN_MAIN') != 'true':  # avoid double run during autoreload
            return

        # def migrate_once():
        #     try:
        #         subprocess.call(['python', 'manage.py', 'makemigrations', 'ardhi_framework'])
        #         subprocess.call(['python', 'manage.py', 'migrate', 'ardhi_framework'])
        #     except Exception as e:
        #         print(f"[Ardhi Init] Migration error: {e}")
        #
        # threading.Thread(target=migrate_once).start()

