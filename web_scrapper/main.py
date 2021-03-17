import argparse
import logging
logging.basicConfig(level=logging.INFO)

import research_page_objects as research
from common import config

logger = logging.getLogger(__name__)

def _research_scraper(research_site_uid):
    host=config()['research_sites'][research_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    homepage = research.HomePage(research_site_uid, host)

    for link in homepage.article_links:
        print(link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    research_site_choices = list(config()['research_sites'].keys())
    parser.add_argument('research_site',
            help='Site that you want to scrape',
            type =str,
            choices=research_site_choices)
    
    args = parser.parse_args()
    _research_scraper(args.research_site)
