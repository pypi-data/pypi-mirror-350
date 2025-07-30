import base64
from dataclasses import dataclass
import json
from typing import Optional
import requests
from django.conf import settings

FORMAT_CHOICES = {
    "A4": "A4",
    "A5": "A5",
    "A6": "A6",
    "Letter": "Letter",
}

@dataclass
class PdfApiParams:
    '''
        Class for api params
    '''
    display_header_footer:bool = False
    format:str = FORMAT_CHOICES["A4"]
    landscape:bool = False
    print_background:bool = False
    prefer_css_page_size:bool = True
    scale:float = 1.0
    margin_top:float = 0
    margin_bottom:float = 0
    margin_left:float = 0
    margin_right:float = 0
    auth_token_name:Optional[str] = None
    auth_token_value:Optional[str] = None
    wait_timeout:int = 10
    file_name:str = "generated.pdf"

    def to_json(self) -> str:
        '''
            Returns json string of the class
            excluding auth_token_name and auth_token_value
        '''
        return json.dumps({
            "display_header_footer": self.display_header_footer,
            "format": self.format,
            "landscape": self.landscape,
            "print_background": self.print_background,
            "prefer_css_page_size": self.prefer_css_page_size,
            "scale": self.scale,
            "margin_top": self.margin_top,
            "margin_bottom": self.margin_bottom,
            "margin_left": self.margin_left,
            "margin_right": self.margin_right,
            "wait_timeout": self.wait_timeout,
            "file_name": self.file_name
        })


def get_api_token() -> str:
    '''
        Returns pikutis api token
    '''
    return settings.PIKUTIS_API_KEY

def call_pdf_api(file_string:str, api_params:Optional[PdfApiParams]) -> dict:
    '''
        Calls pikutis api and returns response
    '''
    if hasattr(settings, 'PIKPDF_API_URL'):
        api_url = settings.PIKPDF_API_URL
    else:
        api_url:str = "https://www.pikutis.lt/api/generate-pdf/"
    pdf_request:requests.Request = requests.Request('POST', url=api_url)
    pdf_request.headers = {"Token": get_api_token()}
    payload:dict = {
        "document": base64.b64encode(file_string.encode('utf-8')).decode('utf-8'),
        "auth": {
            "auth_token_name": api_params.auth_token_name,
            "auth_token_value": api_params.auth_token_value
        }
    }
    pdf_request.data = json.dumps(payload).encode('utf-8')
    if api_params:
        pdf_request.params = api_params.to_json()

    pdf_response:requests.Response = requests.Session().send(pdf_request.prepare())
    return json.loads(pdf_response.content)

def get_pdf_file(pdf_response:dict) -> bytes:
    '''
        Returns pdf file bytes
    '''
    return base64.b64decode(pdf_response['file_bytes_base_64'])