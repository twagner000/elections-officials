import json
import glob
import os

from common import dir_path


files = glob.glob(dir_path(__file__) + '/cache/*.json')
data = []
print(f'Found {len(files)} files')
for file in files:
  with open(file) as fh:
    datum = json.load(fh)
    county = datum['title'].split('Supervisor')[0].strip()
    data += [{
      'locale': county,
      'official': datum['name'].replace(u'\xa0', ' ').split(',')[0].strip(),
      'emails': [datum['email'].split(':')[1].strip()],  # ignore leading 'mailto:'
      'url': datum['url'],
      'county': county,
    }]

with open('public/florida.json', 'w') as fh:
  json.dump(data, fh)
