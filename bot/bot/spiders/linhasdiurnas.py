from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from bot.items import LinhaItem

import pdb


class AthenasLinhas(CrawlSpider):
	name = 'linhasdiurnas'
	base_url = 'http://www.athenaspaulista.com.br/LINHAS/'
	start_urls = ['http://www.athenaspaulista.com.br/LINHAS/Linhas.htm']

	lista_linhas_xpath = './/table[2]/tr[position()>=2 and not(position()>=52)]'


	def parse(self, response):
		hxs = HtmlXPathSelector(response)
	
		for qxs in hxs.select(self.lista_linhas_xpath):  
			loader = XPathItemLoader(LinhaItem(), selector=qxs)
			loader.add_xpath('linha', './td[1]/p//text()')
			loader.add_xpath('nome', './td[3]/p//text()')

			link = self.base_url + qxs.select('./td[3]//a/@href').extract()[0]
			#TODO: Deveria manter o contexto e retornar os dados da proxima pagina
			#      mas o que parece eh que nao esta retornando
			request = Request(link, callback=self.parse_item)
			pdb.set_trace()

			#loader.add_value('ida', request.meta['ida'])
			#loader.add_value('volta', request.meta['volta'])

			yield loader.load_item()


	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)

		linha = {}

		linha['ida']   = hxs.select('.//div[3]/table/tr//text()').extract()
		linha['volta'] = hxs.select('.//div[5]/table/tr//text()').extract()

		return linha