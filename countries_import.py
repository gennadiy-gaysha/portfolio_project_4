import os
import django
from blog.models import Country
from django.template.defaultfilters import slugify

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelblog.settings')
django.setup()

# Path to your data file
file_path = 'countries.txt'

# Read data from the file and create the data list
data = []
with open(file_path, 'r') as file:
    for line in file:
        values = line.strip().split('\t')
        if len(values) == 18:  # Assuming there are 18 fields separated by tabs
            country_data = {
                'iso': values[0],
                'iso3': values[1],
                'iso_numeric': values[2],
                'fips': values[3],
                'country_name': values[4],
                'capital': values[5],
                'area_sq_km': float(values[6]),
                'population': int(values[7]),
                'continent': values[8],
                'tld': values[9],
                'currency_code': values[10],
                'currency_name': values[11],
                'phone': values[12],
                'postal_code_format': values[13],
                'postal_code_regex': values[14],
                'languages': values[15],
                'geo_name_id': int(values[16]),
                'neighbours': values[17]
            }
            data.append(country_data)

# Loop through the data and create Country objects
for item in data:
    country = Country(
        iso=item['iso'],
        iso3=item['iso3'],
        iso_numeric=item['iso_numeric'],
        fips=item['fips'],
        country_name=item['country_name'],
        slug=slugify(item['country_name']),
        capital=item['capital'],
        area_sq_km=item['area_sq_km'],
        population=item['population'],
        continent=item['continent'],
        tld=item['tld'],
        currency_code=item['currency_code'],
        currency_name=item['currency_name'],
        phone=item['phone'],
        postal_code_format=item['postal_code_format'],
        postal_code_regex=item['postal_code_regex'],
        languages=item['languages'],
        geo_name_id=item['geo_name_id'],
        neighbours=item['neighbours']
    )
    country.save()
