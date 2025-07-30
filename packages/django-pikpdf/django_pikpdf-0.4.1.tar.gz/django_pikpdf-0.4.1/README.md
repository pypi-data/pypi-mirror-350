
# django-pikpdf - propper html to pdf generator

django-pikpdf is a Django app to generate pdfs from html templates.
This app will capture the html from a template and convert it to a pdf file 
with all styles in tact - just like you see it in the browser

Produced by ISO/SEC27001 certified software development company - MB Pikutis

Generator method returns htp responce which you can directly return to screen and file bytes, if you want to attach file to email, or return different response

This generator **does not rely on xhtml2pdf**

Generator uses api on www.pikutis.lt site. No information sent to api is stored longer than required for processing. 

To obtain API key, use contact form in the site.

## Quick start


1. Add "django-pikpdf" to your INSTALLED_APPS setting like this::

    ```
    INSTALLED_APPS = [
        ...,
        "django_pikpdf",
    ]

2. Add the following settings to your settings.py:
    
    ```
    PIKUTIS_API_KEY=os.environ.get("PIKUTIS_API_KEY", None) # can be obtained from https://www.pikutis.lt for free
    SITE_URL = os.environ.get("SITE_URL", "https://www.pikutis.lt") # your website url
    PIKPDF_SHORT_URLS = ["/uploaded_images/"] # urls that you use to serve content from your site.
    Static and Media urls are parsed from STATIC_URL and MEDIA_URL settings.
    
2. Include conversion method get_document_pdf_response and django render to string as so:

    ```
    from django_pikpdf.converter import get_document_pdf_response
    from django.template.loader import render_to_string

3. Include class to set params for your pdf printing
    ```
    from django_pikpdf.controllers.api import PdfApiParams

4. Use the parameters and method to convert your html to pdf and return a response:

    ```
    pdf_api_params:PdfApiParams = PdfApiParams()
    pdf_api_params.display_header_footer = True
    pdf_api_params.print_background = False
    pdf_api_params.auth_token_name="TokenName" <-- Used to authenticate all requests for protected resources
    pdf_api_params.auth_token_value="TokenValue" <-- Used to authenticate all requests for protected resources
    http_response, file_bytes = get_document_pdf_response(html, "test.pdf", pdf_api_params)
    # HTTP response is a response object which will display pdf in browser screen
    # file_bytes is the pdf file buffer, which you can i.e. attach to email
    return http_response

Possible parameters for PdfApiParams class:
    
    ```
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
    auth_token_name:str = None
    auth_token_value:str = None
    wait_timeout:int = 10
    file_name:str = "generated.pdf"

That's it! You can now convert your html to pdf and return it as a response.
