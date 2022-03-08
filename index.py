import requests
from bs4 import BeautifulSoup
import json

with open('./mapping.json') as f:
  mapping = json.load(f)

def get_text_by_selectors(url, selectors):
  data = [get_text_by_selector(url, selector) for selector in selectors]
  return data

def get_text_by_selector(url, selector):
  root = requests.get(url)
  soup = BeautifulSoup(root.text, 'html.parser')
  data = soup.select(selector)
  
  return [item.text for item in data if item.text ]

def get_widgets_data(template, widgets):
  selectors = template["selectors"]
  base_url = template["url"]
  urls = [(widget, base_url.replace('${widget-name}', widget)) for widget in widgets]
  data = [{"name": widget, "data": get_text_by_selector(url, selectors[0])} for (widget, url) in urls]
  return data


project_url = mapping["url"]
project_selectors = mapping["selectors"]

project_data = get_text_by_selectors(project_url, project_selectors)



widget_template = mapping["widget"]["template"]
widget_names = mapping["widget"]["widgets"]
widget_data = get_widgets_data(widget_template, widget_names)

with open('data/project_raw.json', 'w') as file:
     file.write(json.dumps(widget_data))