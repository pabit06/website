"""
WSGI entry point for cPanel / Babal Host (Passenger).
Keep this file in the project root (same folder as manage.py).
"""
import sys
import os

# Project root = directory containing this file
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
os.chdir(project_root)  # so relative paths (static, db) work under Passenger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
