import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

HIGHLIGHT_RE = re.compile(r'\*(.+?)\*', re.S)
ITALIC_RE = re.compile(r'(?<!\w)_(.+?)_(?!\w)', re.S)


def _inline(text):
    text = HIGHLIGHT_RE.sub(r'<span class="text-highlight">\1</span>', text)
    return ITALIC_RE.sub(r'<em>\1</em>', text)


@register.filter
def highlight(value):
    """*word* -> gold highlight, _word_ -> italic. Single line, no <p> wrapping."""
    if not value:
        return ''
    return mark_safe(_inline(escape(value)).replace('\n', '<br>'))


@register.filter
def rich_text(value):
    """Like `highlight`, but blank lines become separate <p> paragraphs."""
    if not value:
        return ''
    paragraphs = re.split(r'\n\s*\n', escape(value).replace('\r\n', '\n').strip())
    return mark_safe(''.join(f'<p>{_inline(p).replace(chr(10), "<br>")}</p>' for p in paragraphs))
