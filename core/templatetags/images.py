from django import template

register = template.Library()


@register.filter
def cld(image, transform='w_1200'):
    """Cloudinary URL with auto format/quality and the given transformation.

    Usage: {{ hero.background_image|cld:"w_1920" }}  — returns '' when no image is set.
    """
    if not image:
        return ''
    try:
        url = image.url
    except ValueError:
        return ''
    marker = '/image/upload/'
    if marker in url:
        return url.replace(marker, f'{marker}f_auto,q_auto,{transform}/', 1)
    return url


@register.filter
def cld_icon(image, size=64):
    """Round, edge-to-edge PNG icon (favicon / touch icon) from a Cloudinary image."""
    if not image:
        return ''
    try:
        url = image.url
    except ValueError:
        return ''
    marker = '/image/upload/'
    if marker in url:
        return url.replace(marker, f'{marker}w_{size},h_{size},c_fill,g_center,r_max,f_png/', 1)
    return url
