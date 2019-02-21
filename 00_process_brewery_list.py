"""
I've already downloaded the HTML listing out the 8,993 breweries in the US from The Brewers Association site.

You can use the same file I use here or get an updated list by visiting
    https://www.brewersassociation.org/directories/breweries/
and searching for all US-based breweries.
"""

from bs4 import BeautifulSoup

with open("us-breweries.xml", "r") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, "html.parser")

"""
An example:
<div class="brewery">
 <ul class="vcard simple brewery-info">
  <li class="name">Zymurgy Brewing Co</li>
  <li class="address">624 Main St East</li>
  <li>Menomonie, WI 54751 | <a ...>Map</a></li>
  <li class="telephone">Phone: (715) 578-9026</li>
  <li class="brewery_type">Type:<a ...>Micro</a></li>
  <li class="url"><a ...>www.zymurgybrew.com</a></li>
 </ul>
 <ul class="vcard simple col2 logos">
  <a ...><img .../></a>
 </ul>
</div>

We only care about addresses, which are broken over two list items.
  <li class="address">624 Main St East</li>
  <li>Menomonie, WI 54751 | <a ...>Map</a></li>
"""

breweries = soup.findAll("div", {"class": "brewery"})

def get_address(brewery):
    line1 = brewery.select_one("li.address")
    line2 = brewery.select_one("li.address + li")
    if len(line1.text) < 2:
        return ""
    return line1.text + line2.text.replace(" | Map", "")

addresses = list(map(get_address, breweries))

print(addresses)