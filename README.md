# ![auto-scrape-logo](https://raw.githubusercontent.com/chrispalmo/auto-scrape/master/autoscrape/static/android-icon-36x36.png) auto-scrape - Docker

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
- basic user authenticalion for remote deployments

# Initial Project Setup

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker-Compose](https://docs.docker.com/compose/install/).
2. Create autoscrape.env file in project root directory and populate with environment variables.
Admin username and password should be set here. 
    ```
    AUTOSCRAPE_ADMIN_USERNAME=<username>
    AUTOSCRAPE_ADMIN_PASSWORD=<password>
    ```
3. To start development environment (Elevated privileges may be required depending on your Docker setup)
    ```
    docker-compose -f docker-compose-dev.yml up
    ```
4. To start production environment (Elevated privileges may be required depending on your Docker setup)
    ```
    docker-compose -f docker-compose.yml up
    ```
Both development and production environments are reachable on port 5000