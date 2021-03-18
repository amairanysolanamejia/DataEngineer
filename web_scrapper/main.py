import argparse
import logging
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import research_page_objects as research
from common import config

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _research_scraper(research_site_uid):
    host=config()['research_sites'][research_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    homepage = research.HomePage(research_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(research_site_uid, host, link)

        if article:
            logger.info('Article fetched!!! yeih')
            articles.append(article)
            print(article.title)
        print(len(articles))

def _fetch_article(research_site_uid, host, link):
    logger.info('Start fetching article at {}'.format(link))

    article = None
    try:
            article = research.ArticlePage(research_site_uid, _build_link(host,link))
    except(HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info = False)

    if article and not article.body:
        logger.warning('Invalid article, there is no body')
        return None
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else: 
        return '{host}({uri}'.format(host=host,uri=link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    research_site_choices = list(config()['research_sites'].keys())
    parser.add_argument('research_site',
            help='Site that you want to scrape',
            type =str,
            choices=research_site_choices)
    
    args = parser.parse_args()
    _research_scraper(args.research_site)
