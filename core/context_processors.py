from .models import SiteSettings


def site_settings(request):
    """Makes logo / company name available on every page (navbar, favicon, footer)."""
    return {'site': SiteSettings.load()}
