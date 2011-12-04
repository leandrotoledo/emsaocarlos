from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from bot.items import LinhaItem

import pdb


class AthenasLinhas(CrawlSpider):
	name = 'linhasdiurnas'
	base_url = 'http://www.athenaspaulista.com.br/LINHAS/'
	start_urls = ['http://www.athenaspaulista.com.br/LINHAS/Linhas.htm']

	USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html )"

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		trs = hxs.select('.//table[2]/tr[position()>=2 and not(position()>=52)]')
	
		for tr in trs:  
			linha = LinhaItem()

			linha['linha'] = tr.select('./td[1]//text()').extract()[1]
			linha['link']  = self.base_url + tr.select('./td[3]//a/@href').extract()[0]
			linha['nome']  = tr.select('./td[3]//text()').extract()[1]
			linha['nome']  = linha['nome'].replace('\t', '')
			linha['nome']  = linha['nome'].replace('\n', '')
			linha['nome']  = linha['nome'].replace('\r', '')

			try:
				linha['origem']  = linha['nome'].split(' X ')[0].strip()
				linha['destino'] = linha['nome'].split(' X ')[1].split(' - ')[0].strip()
				linha['via']     = linha['nome'].split(' X ')[1].split(' - ')[1].strip()
			except IndexError:
				linha['origem']  = ''
				linha['destino'] = ''
				linha['via']     = ''

			request = Request(linha['link'], callback=self.parse_item)
			request.meta['linha'] = linha

			yield request


	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)

		linha = response.meta['linha']
		
		linha['ida'] = hxs.select('.//div[3]/table/tr//text()').extract()
		linha['ida'] = [ l.replace('\t', '') for l in linha['ida'] ]
		linha['ida'] = [ l.replace('\n', '') for l in linha['ida'] ]
		linha['ida'] = [ l.replace('\r', '') for l in linha['ida'] ]
		linha['ida'] = [ l.strip() for l in ' '.join(linha['ida']).split(';') ]

		linha['volta'] = hxs.select('.//div[5]/table/tr//text()').extract()
		linha['volta'] = [ l.replace('\t', '') for l in linha['volta'] ]
		linha['volta'] = [ l.replace('\n', '') for l in linha['volta'] ]
		linha['volta'] = [ l.replace('\r', '') for l in linha['volta'] ]
		linha['volta'] = [ l.strip() for l in ' '.join(linha['volta']).split(';') ]

		return linha
