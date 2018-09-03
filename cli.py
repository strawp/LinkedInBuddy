from functions import *

# Run in CLI mode against a saved items XML file
def main():
  # Load file in as XML
  # 
  import argparse, os, base64, re, json
  parser = argparse.ArgumentParser(description="A CLI interface for running an engagement") # ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-t',"--title", default='.*', help="Filter results by job titles which match this regex (e.g. \"at Microsoft\")")
  parser.add_argument('-e',"--emailstyle", default=None, help="The email address style, e.g. <fi>.<ln>@microsoft.com")
  parser.add_argument("infile", help="Burp XML file containing saved items from LinkedIn")
  args = parser.parse_args()
 
  if not args.infile:
    parser.print_usage()
    sys.exit(2)
    
  if not os.path.isfile( args.infile ):
    print args.infile + ' doesn\'t exist'
    sys.exit(2)

  from lxml import etree
  xml = etree.parse( args.infile )
  items = xml.xpath('/items/item' )
  people = []
  for item in items:
    url = item.find('url').text
    r = item.find('response')
    if 'base64' in r.attrib.keys() and r.attrib['base64'] == 'true':
      try:
        response = base64.b64decode( r.text )
      except:
        print 'Error converting response from base64'
        continue
    else:
      response = r.text
    if not response: continue
    response = str(response)
    headers = response.replace('\r','').split("\n\n")[0]
    response = response.replace('\r','').split("\n\n")[1]
    if re.search('Content-Type: text\/html', response ):
      searchResponseForProfileInfo( response, url, args.emailstyle )
    else:
      try:
        data = json.loads(response)
      except:
        continue
      people += parseData( data, args.emailstyle )
  uniq = {}
  for p in people:
    if p['firstname'] == '' or p['lastname'] == '': continue
    if not re.search(args.title, p['title'], re.I): continue
    key = p['firstname'].lower() + '_' + p['lastname'].lower() + '_' + p['title'].lower()
    uniq[key] = p

  for k in sorted(uniq.keys()):
    p = uniq[k]
    print p['firstname'] + ' ' + p['lastname'] + ': ' + p['title'],
    if 'email' in p.keys():
      print ' : ' + p['email'],
    print '\n',



if __name__ == "__main__":
  main()

