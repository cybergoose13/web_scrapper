from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

url = 'https://www.google.com'

req= Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
webpage= urlopen(req).read()

page_soup= soup(webpage, "html.parser")

print(page_soup)

