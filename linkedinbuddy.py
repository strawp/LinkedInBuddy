from burp import IBurpExtender
from burp import ITab
from burp import IScannerCheck
from burp import IMessageEditorController
from burp import IBurpExtenderCallbacks
from java.awt import Component;
from java.io import PrintWriter;
from java.util import ArrayList;
from java.util import List;
from javax.swing import JScrollPane;
from javax.swing import JSplitPane;
from javax.swing import JPanel;
from javax.swing import JTabbedPane;
from javax.swing import JTable;
from javax.swing import SwingUtilities;
from javax.swing.table import AbstractTableModel;
from org.apache.commons.lang3 import StringEscapeUtils
from threading import Lock
from functions import *
import re, json

class BurpExtender(IBurpExtender, ITab, IMessageEditorController, AbstractTableModel, IScannerCheck):
    
    #
    # implement IBurpExtender
    #
    columns = [
      # bytearray("#"),
      "First Name",
      "Last Name",
      "Occupation",
      "Company",
      "Location"
    ]
    
    def	registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()
        
        # set our extension name
        callbacks.setExtensionName("LinkedIn Buddy")
        
        # # create the log and a lock on which to synchronize when adding log entries
        # self._log = ArrayList()
        # self._lock = Lock()
        # 
        # # main split pane
        # self._splitpane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        # 
        # # table of log entries
        # logTable = Table(self)
        # scrollPane = JScrollPane(logTable)
        # self._splitpane.setLeftComponent(scrollPane)

        # # tabs with request/response viewers
        # tabs = JTabbedPane()
        # self._requestViewer = callbacks.createMessageEditor(self, False)
        # self._responseViewer = callbacks.createMessageEditor(self, False)
        # tabs.addTab("Request", self._requestViewer.getComponent())
        # tabs.addTab("Response", self._responseViewer.getComponent())
        # self._splitpane.setRightComponent(tabs)
        # 
        # # customize our UI components
        # callbacks.customizeUiComponent(self._splitpane)
        # callbacks.customizeUiComponent(logTable)
        # callbacks.customizeUiComponent(scrollPane)
        # callbacks.customizeUiComponent(tabs)
        # 
        # # add the custom tab to Burp's UI
        # callbacks.addSuiteTab(self)
        
        # register ourselves as an HTTP listener
        # callbacks.registerHttpListener(self)
        callbacks.registerScannerCheck(self)
        
        return
        
    #
    # implement ITab
    #
    
    def getTabCaption(self):
        return "LinkedIn Buddy"
    
    # def getUiComponent(self):
    #     return self._splitpane
        
    def doPassiveScan(self, baseRequestResponse):
        
        # Check if linkedin
        srv = baseRequestResponse.getHttpService()
        # print srv
        if 'linkedin.com' not in srv.getHost():
          print(srv.getHost() + ' is not linkedin')
          return

        url = self._helpers.analyzeRequest(baseRequestResponse).getUrl()
        m = re.search( r'^https:\/\/www\.linkedin\.com(:443)?\/(voyager|in)\/', url.toString() ) 
        if not m: 
          print(url.toString() + ' is not a relevant page')
          return

        # print url

        respinfo = self._helpers.analyzeResponse(baseRequestResponse.getResponse())
        mimetype = respinfo.getStatedMimeType()
        if mimetype == 'HTML':

          # Get all <code> blocks
          print('Finding code blocks in ' + url)
          resp = str(bytearray(baseRequestResponse.getResponse()))
          
          self.searchResponseForProfileInfo( resp, url )
        
        elif mimetype == 'JSON':
          print(url + ' is raw JSON')
          resp = str(bytearray(baseRequestResponse.getResponse())[respinfo.getBodyOffset():])
          data = json.loads(resp)
          self.parseData(data)

        # Check if it has blob of user data in it

        # Turn all user data into structure

        # Check user not already seen

        # Add each item to log

        # only process requests
        # if messageIsRequest:
        #     return
        # print baseRequestResponse.getResponse()

        # create a new log entry with the message details
        # self._lock.acquire()
        # row = self._log.size()
        # self._log.add(LogEntry(bytearray('Bob'),bytearray('Bobblington'),bytearray('Chief Bobber'),bytearray( 'Bobsco'),bytearray('Bobbville'),bytearray('Aaaaa'),bytearray('bbbbb')))
        # self.fireTableRowsInserted(row, row)
        # self._lock.release()
   

    def searchResponseForProfileInfo( rep, url ):
      m = re.findall(r'<code[^>]*>([^<]+)<\/code>', resp )
      for code in m:
        code = StringEscapeUtils.unescapeHtml4(code)
        # print code
        try:
          data = json.loads(code)
        except:
          print('Failed to parse json from ' + url)
          continue
        # print data
        self.parseData( data )
    
    # Parse a blob of data found on a page
    def parseData( self, data ):
      if 'included' not in list(data.keys()): return
      for row in data['included']:
        if 'firstName' in list(row.keys()) and 'lastName' in list(row.keys()):
          if 'occupation' in list(row.keys()): title = self.sanitise(row['occupation'])
          elif 'headline' in list(row.keys()): title = self.sanitise(row['headline'])
          else: title = ''
          if 'locationName' in list(row.keys()):
            location = row['locationName']
          else:
            location = ''
          print(self.sanitise(row['firstName'])+'\t'+self.sanitise(row['lastName'])+'\t'+title+'\t'+location)

    def sanitise( self, txt ):
      rtn = ''
      for c in txt:
        if ord(c) not in list(range(128)): continue
        rtn += c
      return rtn



    #
    # extend AbstractTableModel
    #
    
    # def getRowCount(self):
    #     try:
    #         return self._log.size()
    #     except:
    #         return 0

    # def getColumnCount(self):
    #     return len(self.columns)

    # def getColumnName(self, columnIndex):
    #     return self.columns[columnIndex]

    # def getValueAt(self, rowIndex, columnIndex):
    #     logEntry = self._log.get(rowIndex)
    #     if columnIndex == 1:
    #         return logEntry._firstname.toString()
    #     if columnIndex == 2:
    #         return logEntry._lastname.toString()
    #     if columnIndex == 3:
    #         return logEntry._occupation.toString()
    #     if columnIndex == 4:
    #         return logEntry._company.toString()
    #     if columnIndex == 5:
    #         return logEntry._location.toString()
    #     return ""

    #
    # implement IMessageEditorController
    # this allows our request/response viewers to obtain details about the messages being displayed
    #
    

#
# extend JTable to handle cell selection
#
    
# class Table(JTable):
#     def __init__(self, extender):
#         self._extender = extender
#         self.setModel(extender)
#     
#     def changeSelection(self, row, col, toggle, extend):
#     
#         # show the log entry for the selected row
#         logEntry = self._extender._log.get(row)
#         self._extender._requestViewer.setMessage(logEntry._requestResponse.getRequest(), True)
#         self._extender._responseViewer.setMessage(logEntry._requestResponse.getResponse(), False)
#         self._extender._currentlyDisplayedItem = logEntry._requestResponse
#         
#         JTable.changeSelection(self, row, col, toggle, extend)
    
#
# class to hold details of each log entry
#

class LogEntry:
    def __init__( self, firstname, lastname, occupation, companyname, locationname, publicidentifier, profilepic ):
        self._firstname = firstname
        self._lastname = lastname
        self._occupation = occupation
        self._companyName = companyname
        self._locationName = locationname
        self._publicIdentifier = publicidentifier
        self._profilepic = profilepic


