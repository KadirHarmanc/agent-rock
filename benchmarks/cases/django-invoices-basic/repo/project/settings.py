DEBUG = True

ALLOWED_HOSTS = ["billing.local"]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

REST_FRAMEWORK = {
  "DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.IsAuthenticated"
  ]
}
