from django.utils.translation import gettext_lazy as _


SECRET_KEY = "tests"

USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    # Required CMS apps
    "cms",
    "menus",
    "treebeard",
    "djangocms_text_ckeditor",
    # Blog requirements
    "aldryn_apphooks_config",
    "parler",
    "taggit",
    "taggit_autosuggest",
    "meta",
    "sortedm2m",
    "easy_thumbnails",
    "filer",
    "djangocms_blog",
    # Agenda app
    "djangocms_blog_agenda",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.static",
                "cms.context_processors.cms_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SITE_ID = 1

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
]

LANGUAGE_CODE = "en"

CMS_TEMPLATES = [
    ("fullwidth.html", "Fullwidth"),
    ("sidebar_left.html", "Sidebar Left"),
    ("sidebar_right.html", "Sidebar Right"),
]

META_SITE_PROTOCOL = "http"
META_USE_SITES = True

TIME_ZONE = "UTC"
USE_TZ = True
STATIC_URL = "/static/"

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)
