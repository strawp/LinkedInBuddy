
# Parse a blob of data found on a page
def parseData( data, emailstyle=None ):
  if 'included' not in data.keys(): return []
  rtn = []
  for row in data['included']:
    if 'firstName' in row.keys() and 'lastName' in row.keys():
      if 'occupation' in row.keys(): title = sanitise(row['occupation'])
      elif 'headline' in row.keys(): title = sanitise(row['headline'])
      else: title = ''
      if 'locationName' in row.keys():
        location = row['locationName']
      else:
        location = ''
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
  rtn = ''
  for c in txt:
    if ord(c) not in range(128): continue
    rtn += c
  return rtn

def searchResponseForProfileInfo( rep, url, emailstyle=None ):
  m = re.findall(r'<code[^>]*>([^<]+)<\/code>', resp )
  rtn = []
  for code in m:
    code = StringEscapeUtils.unescapeHtml4(code)
    # print code
    try:
      data = json.loads(code)
    except:
      continue
    # print data
    rtn += parseData( data, emailstyle )
  return rtn
