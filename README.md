# Observability in Software Development (2026)

# Overview
This repository contains all files related to my Bachelor's Thesis, including WIP notes, word docs and the final LaTeX result. All work done on the thesis can be found somewhere in this repository or within it's git history. 

# AI Use
No AI was used in the creation of this bachelor's thesis, it'd probably be wrong anyway. 

# reportMancer
reportMancer is a Flask application that runs a server, offering a POST API, to which
reports are sent in the following formats:

- ReportingAPI - JSON with at least the following values:
    - body
    - userAgent
    - destination
    - type
    - timestamp
    - attempts 

- DMARC - txt file:
    - "v=DMARC1;p=none;sp=quarantine;pct=100;rua=mailto:dmarcreports@example.com;"

The Flask application parses these requests and sends it on in a single unified format,
filling in the details if not clear (adding current timestamp, userAgent)

Optional whitelist for incoming IPs, as well as outgoing IPs is available.


# Obsidian
This repository contains .obsidian files, which are used with the Obsidian app. The app has been set up for recurring commits every hour, which showcase the ongoing work being done on the thesis. Along manual commits, these commits can be seen in the git history as:

`Hourly snapshot: hh:mm YY/MM/DD`