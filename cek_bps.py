from services.scraper_bps import get_html

soup = get_html()

print(soup.title.text)