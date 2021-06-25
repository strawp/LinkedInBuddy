import re, html, json

# Parse a blob of data found on a page
def parseData( data, emailstyle=None ):
  if 'included' not in list(data.keys()): return []
  rtn = []
  for row in data['included']:
    if 'firstName' in list(row.keys()) and 'lastName' in list(row.keys()):
      if row['firstName'] is None or row['lastName'] is None: continue
      if 'occupation' in list(row.keys()) and row['occupation'] is not None: title = sanitise(row['occupation'])
      elif 'headline' in list(row.keys()) and row['headline'] is not None: title = sanitise(row['headline'])
      else: title = ''
      if 'locationName' in list(row.keys()):
        location = row['locationName']
      else:
        location = ''
      if location is None: location = ''
      person = {
        'firstname': sanitise( row['firstName'] ).strip(),
        'lastname': sanitise( row['lastName'] ).strip(),
        'title': title.strip(),
        'location': location.strip()
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
  m = re.findall(r'<code[^>]*>([^<]+)<\/code>', resp )
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
    # print( data )
    rtn = rtn + parseData( data, emailstyle )
  return rtn
