
import validators
from django.conf import settings

def is_site_url_provided() -> str:
    '''
        Checks if SITE_URL is provided in settings.py
    '''
    if hasattr(settings, 'SITE_URL'):
        if validators.url(settings.SITE_URL):
            if validators.length(settings.SITE_URL, min_val=1, max_val=255):
                return None
            else:
                return "SITE_URL is Token cant be empty or longer than 255 characters"
        else:
            return "SITE_URL is not a valid url"
    else: 
        return "SITE_URL is not provided in settings.py"


def is_static_url_provided() -> str:
    '''
        Checks if STATIC_URL is provided in settings.py
    '''
    if hasattr(settings, 'STATIC_URL'):
        if str(settings.STATIC_URL).startswith('/') and str(settings.STATIC_URL).endswith('/'):
            return None
        else:
            return "STATIC_URL is not a valid url"
    else: 
        return "STATIC_URL is not provided in settings.py"

def is_media_url_provided() -> str:
    '''
        Checks if MEDIA_URL is provided in settings.py
    '''
    if hasattr(settings, 'MEDIA_URL'):
        if str(settings.MEDIA_URL).startswith('/') and str(settings.MEDIA_URL).endswith('/'):
            return None
        else:
            return "MEDIA_URL is not a valid url"
    else: 
        return "MEDIA_URL is not provided in settings.py"

def is_pikutis_api_key_provided() -> str:
    '''
        Checks if PIKUTIS_API_KEY is provided in settings.py
    '''
    if hasattr(settings, 'PIKUTIS_API_KEY'):
        if validators.length(settings.PIKUTIS_API_KEY, min_val=1, max_val=255):
            return None
        else:
            return "PIKUTIS_API_KEY is Token cant be empty or longer than 255 characters"
    else: 
        return "PIKUTIS_API_KEY is not provided in settings.py"
    
def are_settings_valid() -> list:
    '''
        Validates settings.py
    '''
    errors = []
    errors.append(is_site_url_provided())
    errors.append(is_static_url_provided())
    errors.append(is_media_url_provided())
    errors.append(is_pikutis_api_key_provided())
    return list(filter(None, errors))