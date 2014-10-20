#!usr/bin/python
from lxml import html

#Use lxml to fetch the html at the url given and return a list
#  using xpath
def scrape(url,xpath):
    parsedObj = html.parse(url)
    wod=parsedObj.xpath(xpath)
    print wod


## Example
def main():
    scrape(url="http://berkeley-crossfit.com/2013/12/03/wod-12-03-2013/"
        ,xpath='//*[@class="entry-content"]/p/text()')


if __name__ == '__main__':
    main()