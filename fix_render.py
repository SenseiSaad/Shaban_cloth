import re
import os

with open('noorani_backend/settings.py', 'r', encoding='utf-8') as f:
    settings = f.read()

# 1. Imports
if "import os" not in settings:
    settings = "import os\n" + settings
if "import dj_database_url" not in settings:
    settings = "import dj_database_url\nfrom dotenv import load_dotenv\nload_dotenv()\n" + settings

# 2. ALLOWED_HOSTS
settings = re.sub(
    r"ALLOWED_HOSTS\s*=\s*\[.*?\]", 
    "ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') + ['.onrender.com']", 
    settings
)

# 3. DEBUG and SECRET_KEY
settings = re.sub(r"DEBUG\s*=\s*(True|False)", "DEBUG = os.environ.get('DEBUG', 'False') == 'True'", settings)
settings = re.sub(r"SECRET_KEY\s*=\s*'.*?'", "SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-render-key')", settings)

# 4. Middleware
if "whitenoise.middleware.WhiteNoiseMiddleware" not in settings:
    settings = settings.replace(
        "'django.middleware.security.SecurityMiddleware',", 
        "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
    )

# 5. Database Setup
db_match = re.search(r"DATABASES\s*=\s*\{.*?\n\}", settings, re.DOTALL)
if db_match:
    render_db = """DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}"""
    settings = settings.replace(db_match.group(0), render_db)

# 6. Static files
if "STATIC_ROOT" not in settings:
    settings += "\n# Static Files Configuration for Render\n"
    settings += "STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')\n"
    settings += "STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n"

# 7. CORS
if "CORS_ALLOW_ALL_ORIGINS" not in settings:
    settings += "\nCORS_ALLOW_ALL_ORIGINS = True\n"

with open('noorani_backend/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings)

# Build.sh
build_sh = """#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
"""
with open('build.sh', 'w') as f:
    f.write(build_sh)

os.chmod('build.sh', 0o755)

