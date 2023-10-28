import os
from django.core.management.base import BaseCommand
from blog.models import Country

class Command(BaseCommand):
    """
    Custom management command to populate the list of countries from a text file into
    the database.

    This command reads data from a text file named 'countries.txt' and populates the
    'Country' model in the database with the provided information. The text file is
    assumed to contain tab-separated values for each country's attributes, with at
    least 18 fields present.

    The script handles the data parsing, validation, and creation of Country objects
    in the database.

    Usage:
    python manage.py populate_countries

    Example:
    python manage.py populate_countries
    """
    help = 'Populate the list of countries from a text file'

    def handle(self, *args, **kwargs):
        # Constructs the file path to the countries.txt file using the current file's directory.
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'countries.txt')
        # Opens the countries.txt file and iterates over each line. Each line is split based on
        # the tab character, assuming that there are at least 18 fields separated by tabs.
        with open(file_path, 'r') as file:
            for line in file:
                columns = line.split('\t')
                if len(columns) >= 18:  # number of fields in countries.txt file
                    (
                        iso, iso3, iso_numeric, fips, country, capital, area_sq_km, population,
                        continent, tld, currency_code, currency_name, phone, postal_code_format,
                        postal_code_regex, languages, geo_name_id, neighbours, *_
                    ) = columns
                    # get_or_create method either retrieves an existing Country object based on
                    # the provided parameters or create a new one if it doesn't exist.
                    country_obj, created = Country.objects.get_or_create(
                        iso=iso.strip(),
                        iso3=iso3.strip(),
                        iso_numeric=iso_numeric.strip(),
                        fips=fips.strip(),
                        country_name=country.strip(),
                        capital=capital.strip(),
                        area_sq_km=float(area_sq_km.strip()) if area_sq_km.strip() else 0.0,
                        population=int(population.strip()) if population.strip() else 0,
                        continent=continent.strip(),
                        tld=tld.strip() if tld.strip() else '',
                        currency_code=currency_code.strip(),
                        currency_name=currency_name.strip(),
                        phone=phone.strip()[:100],
                        postal_code_format=postal_code_format.strip()[:100],
                        postal_code_regex=postal_code_regex.strip()[:100],
                        languages=languages.strip(),
                        geo_name_id=geo_name_id.strip() if geo_name_id.strip() else 0,
                        neighbours=neighbours.strip(),
                    )

            self.stdout.write(self.style.SUCCESS('Successfully populated countries data'))
