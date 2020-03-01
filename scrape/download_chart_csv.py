import requests
import datetime
import time
import os


COUNTRY_DICT = {
'global': 'Global',
'us': 'United States',
'gb': 'United Kingdom',
'ad': 'Andorra',
'ar': 'Argentina',
'at': 'Austria',
'au': 'Australia',
'be': 'Belgium',
'bg': 'Bulgaria',
'bo': 'Bolivia',
'br': 'Brazil',
'ca': 'Canada',
'ch': 'Switzerland',
'cl': 'Chile',
'co': 'Colombia',
'cr': 'Costa Rica',
'cy': 'Cyprus',
'cz': 'Czech Republic',
'de': 'Germany',
'dk': 'Denmark',
'do': 'Dominican Republic',
'ec': 'Ecuador',
'ee': 'Estonia',
'es': 'Spain',
'fi': 'Finland',
'fr': 'France',
'gr': 'Greece',
'gt': 'Guatemala',
'hk': 'Hong Kong',
'hn': 'Honduras',
'hu': 'Hungary',
'id': 'Indonesia',
'ie': 'Ireland',
'il': 'Israel',
'in': 'India',
'is': 'Iceland',
'it': 'Italy',
'jp': 'Japan',
'lt': 'Lithuania',
'lu': 'Luxembourg',
'lv': 'Latvia',
'mc': 'Monaco',
'mt': 'Malta',
'mx': 'Mexico',
'my': 'Malaysia',
'ni': 'Nicaragua',
'nl': 'Netherlands',
'no': 'Norway',
'nz': 'New Zealand',
'pa': 'Panama',
'pe': 'Peru',
'ph': 'Philippines',
'pl': 'Poland',
'pt': 'Portugal',
'py': 'Paraguay',
'ro': 'Romania',
'se': 'Sweden',
'sg': 'Singapore',
'sk': 'Slovakia',
'sv': 'El Salvador',
'th': 'Thailand',
'tr': 'Turkey',
'tw': 'Taiwan',
'uy': 'Uruguay',
'vn': 'Viet Nam',
'za': 'South Africa'
}

START_DATE = datetime.date(2020, 1, 31)

OUTPUT_FOLDER = "../"

#loop through every country and date
for currCountry in COUNTRY_DICT.keys():
    print("Starting Country " + currCountry)
    currDate = START_DATE
    while currDate >= datetime.date(2016, 12, 30):

        #build the link and file name based on the country and the dates
        url = "https://spotifycharts.com/regional/" + currCountry + "/weekly/" + (currDate - datetime.timedelta(7)).strftime("%Y-%m-%d") + "--" + currDate.strftime("%Y-%m-%d") + "/download"
        fileName = currCountry.upper() + "_" + currDate.strftime("%Y%m%d") + "_" + "WEEKLY.csv"

        #if the file has not already been downloaded before, download
        if not os.path.exists(OUTPUT_FOLDER + fileName):
            try:
                #the file has not been downloaded.  Download it now
                r = requests.get(url, allow_redirects=True)
                if r.content[:40] != b',,,"Note that these figures are generate':
                    print("Non CSV found " + fileName)
                    time.sleep(2)
                    break
                open(OUTPUT_FOLDER + fileName, 'wb').write(r.content)
                print("Downloaded " + fileName[:-4])
                time.sleep(2)
            except Exception as e:
                #the file does not exist.  I am assuming that is because records do not go back that far. Move on to the next country
                print("error on " + fileName)
                time.sleep(2)
                break
        else:
            print("Skipping File " + fileName)
        currDate = currDate - datetime.timedelta(7)