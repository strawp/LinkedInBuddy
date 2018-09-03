# LinkedInBuddy
A Burp passive scanner extension which helpfully takes a note of any names and job titles you encounter whilst browsing LinkedIn

There are currently two ways of using this:

## linkedinbuddy.py

This is ultra basic at the moment and outputs the STDOUT only, so to set up you will want to go to the "Output" tab in Extender -> Extensions and select "Save to file". It registers as a passive scan and will be outputting names directly to your file as you browse.

## cli.py

This allows you to scan a saved set of responses from Burp offline, via the command line. After exploring LinkedIn, select all the responses in Burp (target or proxy log, right-click, save selected items). This will then dump out a list of unique records that were in any of the responses.

You can filter on job title by regex and also supply an email address scheme for the company to generate email addresses for each staff member.


