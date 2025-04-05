import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import re

__all__ = ["get_logos_from_websites"]

def validate_and_fix_url(url):
  """
  Check if an URL is valid. If not, try to correct it.
        
  Args:
    url (string): The url to be checked.
    
  Returns:
    string: The corrected url, or None if the url is invalid.
  """
  if not url or not isinstance(url, str):
      return None

  url = url.strip()

  if not re.match(r'^(http|https)://', url, re.IGNORECASE):
      url = 'http://' + url

  parsed_url = urlparse(url)

  if parsed_url.scheme not in ['http', 'https']:
      url = 'http://' + url.split('://')[-1]
      parsed_url = urlparse(url)

  fixed_path = re.sub(r'/+', '/', parsed_url.path)

  netloc = parsed_url.netloc.lower()
  if not netloc.startswith('www.') and '.' in netloc:
      netloc = 'www.' + netloc

  fixed_url = urlunparse((parsed_url.scheme, netloc, fixed_path, '', '', ''))

  return fixed_url

def get_website_logo(url):
  """
  Get the logo of a website.
      
  Args:
    url (string): The url of the website.
  
  Returns:
    string: The url of the logo, or None if no logo was found.
  """
  try:
      headers = {"User-Agent": "Mozilla/5.0"}
      response = requests.get(url, headers=headers, timeout=10)
      response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")

      icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
      if icon_link and "href" in icon_link.attrs:
          return urljoin(url, icon_link["href"])

      og_image = soup.find("meta", property="og:image")
      if og_image and "content" in og_image.attrs:
          return urljoin(url, og_image["content"])

      logo_img = soup.find("img", {"class": lambda x: x and "logo" in x.lower()})
      if not logo_img:
          logo_img = soup.find("img", {"id": lambda x: x and "logo" in x.lower()})

      if logo_img and "src" in logo_img.attrs:
          return urljoin(url, logo_img["src"])

  except requests.exceptions.RequestException as e:
      print(f"Error accessing website: {e}")

  return None  

def get_logos_from_websites(websites_file_path):
  """
  Get the logos of the websites in the file.
        
  Args:
    websites_file_path (string): The path to the file containing the websites.
  
  Returns:
    list: A list of tuples of form (website url, logo url).
  """
  df = pd.read_parquet(websites_file_path)

  logos = []
  found_logos = found_logo_rate = 0

  for index, row in df.iterrows():
      if index == 20:
        break
      website_url = row[0]
      print(f"Initial URL: {website_url}")

      validated_url = validate_and_fix_url(website_url)

      if not validated_url:
          print("Invalid URL. Moving on.")
          continue

      print(f"Validated URL: {validated_url}")

      logo_url = get_website_logo(validated_url)
      if logo_url:
          print(f"Possible logo: {logo_url}")
          logos.append((website_url, logo_url))
          found_logos += 1
      else:
          print("No logo found.")
      found_logo_rate = found_logos / (index + 1)

      print("=" * 30)
  
  return logos, found_logo_rate