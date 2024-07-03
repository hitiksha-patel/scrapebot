import falcon
import requests
from bs4 import BeautifulSoup, Tag
import urllib.parse
import logging
import html
from typing import Any, Dict
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
LOG_FILE = os.getenv('LOG_FILE', 'Scrapebot.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)

class AppInfoResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        raw_body: str = req.bounded_stream.read().decode('utf-8')
        form_data: Dict[str, Any] = urllib.parse.parse_qs(raw_body)

        url: str = form_data.get('url', [None])[0]

        if not url:
            logging.error("Missing 'url' parameter in the request")
            raise falcon.HTTPBadRequest(title="Missing parameter", description="The 'url' parameter is required.")

        # Validate URL format
        parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logging.error(f"Invalid URL provided: {url}")
            raise falcon.HTTPBadRequest(title="Invalid URL", description="Please provide a valid URL.")

        # Check if the domain is from en.aptoide.com
        if 'en.aptoide.com' not in parsed_url.netloc:
            logging.error(f"Invalid domain: {parsed_url.netloc}")
            raise falcon.HTTPBadRequest(title="Invalid URL", description="Only URLs from en.aptoide.com are accepted.")

        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()  # Raise an error for non-200 status codes

            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            app_info_div = soup.find('div', class_='info__DetailsCol-sc-hpbddq-11 kvOojZ')

            if not app_info_div or not isinstance(app_info_div, Tag):
                logging.error(f"App information not found on Aptoide platform for URL: {url}")
                raise falcon.HTTPNotFound(description="App information not found on the Aptoide platform")

            details: Dict[str, Any] = {
                'Name': None,
                'Downloads': None,
                'Version': None,
                'Release Date': None,
                'Description': None
            }

            for span in app_info_div.find_all('span', class_='info__APKDetail-sc-hpbddq-8 buGwFg'):
                text: str = span.get_text(strip=True)
                if 'Name' in text:
                    details['Name'] = text.replace('Name:', '').strip()
                elif 'Downloads' in text:
                    details['Downloads'] = text.replace('Downloads:', '').strip()
                elif 'Version' in text:
                    details['Version'] = text.replace('Version:', '').strip()
                elif 'Release Date' in text:
                    details['Release Date'] = text.replace('Release Date:', '').strip()

            description_elements = soup.find_all('p', class_='details__Paragraph-sc-rnz8ql-2 emzOuH')

            # Remove bullet points and join all description elements into a single paragraph
            description: str = ' '.join([p.get_text(strip=True) for p in description_elements if p.get_text(strip=True)])

            # Remove any bullet points and extra white spaces
            cleaned_description = re.sub(r'[\u2022•*-]', '', description)
            cleaned_description = re.sub(r'\s+', ' ', cleaned_description).strip()

            details['Description'] = cleaned_description

            logging.info(f"Successful request processed for URL: {url}")

            # Prepare JSON response
            resp.media = details
            resp.content_type = falcon.MEDIA_JSON

        except requests.exceptions.RequestException as e:
            logging.error(f"Request to Aptoide failed for URL: {url}, Error: {str(e)}")
            raise falcon.HTTPNotFound(description="App information not found on the Aptoide platform")

        except Exception as e:
            logging.error(f"Unexpected error occurred: {str(e)}")
            raise falcon.HTTPInternalServerError(description="Internal server error")

class IndexResource:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.content_type = 'text/html'
        try:
            with open('templates/index.html', 'r') as f:
                resp.body = f.read()
        except FileNotFoundError:
            resp.status = falcon.HTTP_404
            resp.body = "index.html not found"


app = falcon.App()
app.add_route('/', IndexResource())
app.add_route('/get-app-info', AppInfoResource())
