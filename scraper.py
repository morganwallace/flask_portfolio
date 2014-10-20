#!usr/bin/python
from lxml import html

#Use lxml to fetch the html at the url given and return a list
#  using xpath
def scrape(url,xpath):
    parsedObj = html.parse(url)
    return parsedObj.xpath(xpath)


## Example
def main():
    print scrape(url="http://www.google.com"
        ,xpath='//*[@class="ProfileTweet-text"]/text()')


if __name__ == '__main__':
    main()