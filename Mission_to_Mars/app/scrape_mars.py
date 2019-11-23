def scrape():
    from splinter import Browser
    import pandas as pd
    from bs4 import BeautifulSoup

    executable_path ={'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    soup = BeautifulSoup(browser.html)
    list = soup.find_all('div', class_='slide')
    list_contents = []
    for li in list:
        news_p = li.find('div', class_='rollover_description_inner').contents[0].replace('\n','')
        news_title = li.find('div', class_='content_title').find('a').contents[0].replace('\n','')
        list_contents.append({'headline':news_title, 'paragraph':news_p})

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    soup = BeautifulSoup(browser.html)
    foot = soup.find('footer')

    link = foot.find('a')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + link

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    soup = BeautifulSoup(browser.html)

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').contents[0]

    url4 = 'https://space-facts.com/mars/'
    mars_facts_df = pd.read_html(url4)[0]

    table_html = mars_facts_df.to_html()

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    soup = BeautifulSoup(browser.html)

    descriptions = soup.find_all('div', class_='description')

    images_list = []

    for desc in descriptions:
        browser.visit(url5)
        soup = BeautifulSoup(browser.html)
        text = desc.find('h3').contents[0]
        browser.click_link_by_partial_text(text)
        soup = BeautifulSoup(browser.html)
        img_url = soup.find('li').find('a')['href']
        images_list.append({'title':text, 'img_url':img_url})
        
    dict = {
        'nasa_news': list_contents,
        'featured_image_url': featured_image_url,
        'weather': mars_weather,
        'mars_facts': table_html,
        'images': images_list
        }

    return dict