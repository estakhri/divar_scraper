
# Divar Real Estate Web Scraper

This Python project is a web scraper that extracts real estate listings (such as apartments for sale) from the website [Divar](https://divar.ir). It uses `Selenium` and `BeautifulSoup` to automate the extraction of data like title, price, area, and additional details of apartments for sale in various neighborhoods of Shiraz (or any other city of your choice).

## Features
- Uses `Selenium` with a Firefox WebDriver to dynamically load pages.
- Prevents loading of images to improve scraping speed.
- Extracts and saves property details, including title, subtitle, area (in meters), year of construction, number of rooms, total price, price per meter, floor, and a description.
- Saves the extracted data to a CSV file.
- Easily adjustable to target different cities or areas by changing the URLs.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- `selenium`
- `beautifulsoup4`
- `geckodriver` (for Firefox WebDriver)
- `csv` (part of Python's standard library)

You can install the necessary Python packages using pip:

```bash
pip install selenium beautifulsoup4
```

Make sure to have Firefox installed along with `geckodriver`. You can download `geckodriver` from [here](https://github.com/mozilla/geckodriver/releases) and add it to your PATH.

## How It Works

The script works in the following steps:
1. **Initialize Selenium WebDriver**: The `UrlScraper` class initializes a Firefox WebDriver instance with options to prevent image loading for better performance.
2. **Load Pages**: It loads pages dynamically from the real estate section of Divar and scrolls down to fetch more listings.
3. **Scrape Data**: Extracts details of properties like title, subtitle, price, area, number of rooms, and other relevant details using `BeautifulSoup`.
4. **Save to CSV**: The data is saved to a CSV file (`DivarScraper.csv`) in a structured format with appropriate headers.
5. **Tear Down**: Once all the data has been fetched and saved, the WebDriver and file resources are closed.

## Usage

1. Clone the repository or download the script.
2. Ensure that the necessary dependencies are installed.
3. Modify the list of neighborhoods or city areas (found in the `urls` list) if needed, to match your preferred search regions.
4. Run the script:

```bash
python divar_scraper.py
```

The script will fetch apartment data from Divar and save it to `DivarScraper.csv` in the working directory.

## Customization

- **Change the City**: To scrape data from other cities, modify the base URL in the `scrap_page` method. For example, replace `shiraz` with another city.
- **Change Scraping Parameters**: The query string parameters in the URLs, such as `building-age` and `sort`, can be adjusted to modify search results.

## CSV File Format

The scraped data is saved in a CSV file with the following columns:

- `Mahale`: Neighborhood
- `Title`: Property title
- `Subtitle`: Subtitle (if available)
- `Meter`: Area of the apartment
- `Year`: Year of construction
- `Room`: Number of rooms
- `TotalPrice`: Total price of the apartment
- `MeterPrice`: Price per square meter
- `Floor`: Floor number
- `Description`: Additional description about the property

## Notes

- The scraper includes a delay of a few seconds to ensure that the data is fully loaded on the page before scraping.
- The current script is designed to scrape apartments in the city of Shiraz, but can easily be adapted for other cities or property types by modifying the base URLs.
- Be cautious when scraping websites and ensure that you comply with their terms of service.

## Future Enhancements

- Add multi-threading to speed up the scraping process.
- Implement error handling for missing data fields.
- Support for other property types (e.g., rentals, commercial properties).

## License

This project is licensed under the MIT License.
