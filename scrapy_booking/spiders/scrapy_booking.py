from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy_booking.items import ScrapyBookingItem

class BookingSpider(Spider):
    name = 'scrapy_booking'
    start_urls = ["https://www.booking.com/searchresults.html?region=4127;ss=Goa"]

    def parse_reviews(self, response):
        nextpage = True
        hotelitem = response.meta['hotelitem']
        for item in response.css('.review_list'):
            for i in item.css('.review_item'):
                reviewer = i.css('.review_item_reviewer>h4>span::text').extract_first()
                country = i.css('.reviewer_country>span>span::text').extract_first()
                review_score = i.css('.review_item_review_score::text').extract_first()
                review_word = [x.strip('\r\n') for x in i.css('.review_info_tag::text').extract() if x.strip('\r\n')!='']
                hotelitem['reviews'].append({'reviewer':reviewer, 'country':country,
                                             'review_word':review_word, 'review_score':review_score})
        
        NEXT_PAGE_SELECTOR = '#review_next_page_link'
        next_page = response.css(NEXT_PAGE_SELECTOR).xpath('@href').extract_first()
        if next_page:
            request = Request(
                response.urljoin(next_page),
                callback=self.parse_reviews
                )
            request.meta['hotelitem'] = hotelitem
            yield request
        yield hotelitem

    def parse_hotel(self, response):
        hotelitem = response.meta['hotelitem']
        hotelitem['location_bbox'] = response.css('.show_map').xpath('@data-bbox').extract_first()
        hotelitem['location_coords'] = response.css('.show_map').xpath('@data-coords').extract_first()
        hotelitem['location_address'] = response.css('.hp_address_subtitle::text').extract_first()
        hotelitem['star_rating'] = response.css('.invisible_spoken::text').extract_first()
        reviews_url = response.css('.show_all_reviews_btn').xpath('@href').extract_first()
        request = Request(response.urljoin(reviews_url), callback=self.parse_reviews)
        request.meta['hotelitem'] = hotelitem
        yield request


    def parse(self, response):
        page = 0	
        hotelcount = 0
        while hotelcount < 1600:
            hotelitem = ScrapyBookingItem()
            hotelitem['reviews'] = []
            HOTEL_SELECTOR = '.sr_item'
            for hotel in response.css(HOTEL_SELECTOR):
                hotelcount += 1
                hotelitem['hotel_id'] = str(hotel.xpath('@data-hotelid').extract_first())
                hotelitem['name'] = hotel.css('.sr-hotel__name::text').extract_first()
                hotelitem['rating_word'] = hotel.css('.js--hp-scorecard-scoreword::text').extract_first()
                hotelitem['rating_score'] = hotel.css('.js--hp-scorecard-scoreval::text').extract_first()
                hotel_url = hotel.css('.hotel_name_link').xpath('@href').extract_first() 
                request = Request(
                    response.urljoin(hotel_url),
                    callback=self.parse_hotel
            	    )
                request.meta['hotelitem'] = hotelitem
                yield request

            page += 1
            url_suffix = '&rows=15&offset=' + str(page * 15)
            print ("##############################################################################################################################")
            print ("Final count :", hotelcount, page)
            print ("##############################################################################################################################")
            yield Request(
                'https://www.booking.com/searchresults.html?region=4127;ss=Goa' + url_suffix,
                callback=self.parse
                )

