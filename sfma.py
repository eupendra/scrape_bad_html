import scrapy
import scraper_helper as sh


class SfmaSpider(scrapy.Spider):
    name = 'sfma'
    start_urls = ['https://www.sfma.org.sg/member/members-directory']

    def parse(self, response):
        for link in response.css('#myList a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(link),
                                 callback=self.parse_details)

    def parse_details(self, response):
        address_parts = response.xpath('//div[@class="min-vh-100 container-fluid bg-white pb-3"]/p[1]//text()').getall()
        address_parts = [sh.cleanup(x) for x in address_parts]

        Name = response.css('.text-sfma ::text').get()
        Address = ', '.join(address_parts)
        Phone = sh.cleanup(response.xpath('//strong[text()="Tel:"]/../text()').get())
        Fax = sh.cleanup(response.xpath('//strong[text()="Fax:"]/../text()').get())
        Email = sh.cleanup(response.xpath('//strong[text()="Email:"]/../text()').get())
        Website = sh.cleanup(response.xpath('//strong[text()="Website:"]/../text()').get())
        yield {
            'Name': Name,
            'Address': Address,
            'Phone': Phone,
            'Fax': Fax,
            'Email': Email,
            'Website': Website,
            'Link': response.url
        }
