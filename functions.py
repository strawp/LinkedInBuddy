import re, html, json

# Parse a blob of data found on a page
def parseData( data, emailstyle=None ):
  rtn = []
  for row in data:
    # if 'occupation' in list(row.keys()) and row['occupation'] is not None: title = sanitise(row['occupation'])
    # elif 'headline' in list(row.keys()) and row['headline'] is not None: title = sanitise(row['headline'])
    # else: title = ''
    # if 'locationName' in list(row.keys()):
    #   location = row['locationName']
    # else:
    #   location = ''
    # if location is None: location = ''
    person = {
      'firstname': sanitise( row.get('name').split(' ')[0] ).strip(),
      'lastname': sanitise( ' '.join(row.get('name').split(' ')[1:]) ).strip(),
      'title': row.get('description','').strip(),
      'location': row.get('location',''),
      'employer': '; '.join(list(set([x.get('name') for x in row.get('worksFor')])))
    }
    if person['firstname'] == '' or person['lastname'] == '': continue
    if emailstyle:
      fi = person['firstname'][0].lower()
      li = person['lastname'][0].lower()
      email = ( emailstyle
      .replace('<fn>', person['firstname'].lower())
      .replace('<ln>', person['lastname'].lower())
      .replace('<fi>', fi)
      .replace('<li>', li) )
      person['email'] = email
    rtn.append(person)
  return rtn
    
def sanitise( txt ):
  if txt is None: return txt
  rtn = ''
  for c in txt:
    if ord(c) not in list(range(31,128)): continue
    rtn += c
  return rtn

def searchResponseForProfileInfo( resp, url, emailstyle=None ):
  m = re.findall(r'<script type="application/ld\+json">([^<]+)</script>', resp.replace('\r','') )
  rtn = []
  for code in m:
    code = html.unescape(code).replace(r'\n','\n').strip()
    code = re.sub(r'\\x[0-9a-f]{2}','',code)
    code = sanitise( code )
    try:
      data = json.loads(code)
    except Exception as e:
      # print(e)
      # print('Error parsing:',code)
      continue
    data = [x for x in data.get('@graph') if x.get('@type') == 'Person']
    rtn = rtn + parseData( data, emailstyle )
  return rtn
