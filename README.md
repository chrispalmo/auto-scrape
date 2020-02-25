# ![auto-scrape-logo](https://raw.githubusercontent.com/chrispalmo/auto-scrape/master/autoscrape/static/android-icon-36x36.png) auto-scrape

Auto-scrape is a platform for building, managing and remotely deploying web scrapers. It provides the "essential infrastructure" for web scraping while allowing developers to focus on writng Selenium web scraping scripts in a simple and familiar way.

It is built using the [Flask](https://palletsprojects.com/p/flask/) framework and uses [SQLAlchemy](https://www.sqlalchemy.org/) to interface with the SQL database of your choice.

# Demo
GIF screenshots demonstrating the user interface in action <a href="https://palmo.xyz/post/20200224-manage-selenium-web-scrapers-with-auto-scrape/#user-interface-overview">here</a>.

# Features: 
- live progress logging
- database for saving scraped data - no database experience required!
- CSV export
- multiple simultaneous scrapers
- basic resource management
- basic user authenticalion for remote deployments (see [fea-simple-auth](https://github.com/chrispalmo/auto-scrape/tree/fea-simple-auth) branch

# Initial Project Setup

1. [Download chromedriver](https://chromedriver.chromium.org/downloads) and place it in `/autoscrape`. 
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables (for [fea-simple-auth](https://github.com/chrispalmo/auto-scrape/tree/fea-simple-auth) branch only):

Windows:
```
$env:AUTOSCRAPE_ADMIN_USERNAME="your_admin_username"
$env:AUTOSCRAPE_ADMIN_PASSWORD="your_admin_password"
```
MacOS / Linux:
```
export AUTOSCRAPE_ADMIN_USERNAME="your_admin_username"
export AUTOSCRAPE_ADMIN_PASSWORD="your_admin_password"
```
You could also store authentication details this way for scrapers run behind a paywall.
4. Start scraping: `flask run`


