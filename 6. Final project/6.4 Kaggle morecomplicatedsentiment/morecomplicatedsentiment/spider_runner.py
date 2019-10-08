from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process, Queue


def crawler(q, spider, urls, settings):
    try:
        runner = CrawlerRunner(settings)
        deferred = runner.crawl(spider, start_urls=urls)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)

def run_spider(spider, urls, settings):
    q = Queue()
    p = Process(target=crawler, args=(q, spider, urls, settings,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
