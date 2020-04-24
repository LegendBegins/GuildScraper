# GuildScraper
A multi-threaded web scraper for roleplayerguild.com threads

To use, just replace the URL with the URL of the thread you want to scrape and the PAGECOUNT with the number of pages you'd like to save.

The data is saved in an object with the format of data[page][postOnPage][(text, poster, post ID)] and written to a file

e.g. data[1][4][0] gets the text of the fifth post on page 2 (0-indexed) 
