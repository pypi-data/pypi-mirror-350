from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def fix_static_urls(html:str) -> str:
    """
    Fixes the static urls in the html file
    """
    return html.replace(settings.STATIC_URL, settings.SITE_URL + settings.STATIC_URL)

def fix_media_urls(html:str) -> str:
    """
    Fixes the media urls in the html file
    """
    return html.replace(settings.MEDIA_URL, settings.SITE_URL + settings.MEDIA_URL)

def fix_other_urls(html:str) -> str:
    """
    Fixes other urls in the html file
    """
    if hasattr(settings, 'PIKPDF_SHORT_URLS') and settings.PIKPDF_SHORT_URLS:
        if isinstance(settings.PIKPDF_SHORT_URLS, list):
            for url in settings.PIKPDF_SHORT_URLS:
                html = html.replace(url, settings.SITE_URL + url)
        else:
            logger.error("PIKPDF_SHORT_URLS urls should be a list")
    return html
