"""Main file to start crawling process"""

from Crawler.controller import Controller


class Config:
    num_threads = 5
    seeds = ['https://www.wikipedia.org/',
              'https://www.quora.com']


def crawl():
    crawler = Controller(Config.num_threads, Config.seeds)
    crawler.run()


if __name__ == "__main__":
    crawl()
