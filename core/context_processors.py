from django.conf import settings

from .models import SiteSettings

ASSET_FILES = ('css/style.css', 'js/main.js')


def site_settings(request):
    """Makes logo / company name available on every page (navbar, favicon, footer)."""
    return {'site': SiteSettings.load(), 'asset_v': _asset_version()}


def _asset_version():
    """Local only: last-edit time of the CSS/JS, added as ?v= so browsers never keep an
    old copy. In production the file names are already hashed by collectstatic."""
    if not settings.DEBUG:
        return ''
    folder = settings.STATICFILES_DIRS[0]
    try:
        return str(int(max((folder / f).stat().st_mtime for f in ASSET_FILES)))
    except OSError:
        return ''
