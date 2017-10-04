# Full path and name to your csv file
#csv_filepathname="/home/mitch/projects/wantbox.com/wantbox/zips/data/zipcodes.csv"
# Full path to your django project directory
#your_djangoproject_home="/home/mitch/projects/wantbox.com/wantbox/"

from django.core.management import setup_environ
import settings
setup_environ(settings)
from tracksheet.models import ZipCode
import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
for row in dataReader:
    if row[0] != 'ZIPCODE':
# Ignore the header row, import everything else
    zipcode = ZipCode()
    zipcode.zipcode = row[0]
    zipcode.city = row[1]
    zipcode.statecode = row[2]
    zipcode.statename = row[3]
    zipcode.save()