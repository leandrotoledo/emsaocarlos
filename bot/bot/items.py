# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LinhaItem(Item):
	linha 	 = Field()
	link     = Field()
	nome 	 = Field()
	origem   = Field()
	destino  = Field()
	via      = Field()
	ida      = Field()
	volta    = Field()