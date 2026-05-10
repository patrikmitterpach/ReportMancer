# Observability in Software Development (2026)

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

- DMARC - aggregate XML

The Flask application parses these requests and sends it on in a single unified format,
filling in the details if not clear (adding current timestamp, userAgent)

Configuration contains the options for adding authentication, as well as enabling export to another server with the syslog format. 
