# Register new scrapers below

from autoscrape.scrapers.hacker_news_1 import HackerNews1
from autoscrape.scrapers.hacker_news_2 import HackerNews2
from autoscrape.scrapers.intelligent_investor import IntelligentInvestor

scrapers = {
	"HackerNews1": HackerNews1,
	"HackerNews2": HackerNews2,
	"IntelligentInvestor": IntelligentInvestor
}