from glob import glob
import json
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString


from common import dir_path

_dir = dir_path(__file__)

files = glob(f'{_dir}/cache/*.html')

def parse_addr_line(key, line):
  if not isinstance(line, NavigableString):
    return {}
  else:
    return {key: line.strip().title().replace(' Ga ', ' GA ')}

def parse_contact_line(line):
  if not isinstance(line, NavigableString):
    return {}
  parsed = line.split(':')
  if len(parsed) == 2:
    k, v = parsed
    return {k.strip(): v.strip()}
  return {}

def parse_contact(h4):
  title = h4.text
  line1 = h4.next_element.next_element
  line2 = line1.next_element.next_element
  if title.endswith('Address:'):
    return {
      'kind': title.split(':')[0],
      **parse_addr_line('addr1', line1),
      **parse_addr_line('addr2', line2),
    }
  elif title == 'Contact Information:':
    return {
      'kind': title.split(':')[0],
      **parse_contact_line(line1),
      **parse_contact_line(line2),
    }
  else:
    raise ValueError('Encountered unrecognized contact')

def parse_html(file):
  with open(file) as fh:
    soup = BeautifulSoup(fh.read(), "lxml")

  registrar_str = soup.find('hr').next_element
  name = registrar_str.next_element.next_element
  county = re.search('(.* County) Chief Registrar', registrar_str).group(1).title()

  contact_els = soup.find_all('h4')
  contacts = [parse_contact(contact) for contact in contact_els]
  contacts_dict = {
    contact['kind']: contact
    for contact in contacts
  }

  email_el = soup.find('a')
  email = email_el.text.strip() if email_el else None
  fax = contacts_dict.get('Contact Information', {}).get('Fax')

  return {
    'locale': county.strip(),
    'county': county.strip(),
    'official': name.title().strip(),
    'emails': [email] if email else [],
    'faxes': [fax] if fax else [],
    'contacts': contacts_dict,
  }

def main():
  js = [parse_html(file) for file in files]
  print(F'Found {len(js)} records')

  with open('public/georgia.json', 'w') as fh:
    json.dump(js, fh)


if __name__ == '__main__':
  main()
