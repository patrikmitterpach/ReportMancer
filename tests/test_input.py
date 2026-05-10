#
# Setup example from
# https://flask.palletsprojects.com/en/stable/testing/
#

import pytest
import json

from main import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


#
# Variables used in tests
#
empty_json = json.dumps({})
valid_jsons = [
    {
        "type": "security-violation",
        "age": 10,
        "url": "https://example.com/vulnerable-page/",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "body": {
            "blocked": "https://evil.com/evil.js",
            "policy": "bad-behavior 'none'",
            "status": 200,
            "referrer": "https://evil.com/",
        },
    },
   
        {
            "type": "certificate-issue",
            "age": 32,
            "url": "https://www.example.com/",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "body": {
                "date-time": "2014-04-06T13:00:50Z",
                "hostname": "www.example.com",
                "port": 443,
                "effective-expiration-date": "2014-05-01T12:40:50Z",
                "served-certificate-chain": [
"""-----BEGIN CERTIFICATE-----\
MIIEBDCCAuygAwIBAgIDAjppMA0GCSqGSIb3DQEBBQUAMEIxCzAJBgNVBAYTAlVT\
HFa9llF7b1cq26KqltyMdMKVvvBulRP/F/A8rLIQjcxz++iPAsbw+zOzlTvjwstz\
WHPbqCRiOwY1nQ2pM714A5AuTHhdUDqB1O6gyHA43LL5Z/qHQF1hwFGPa4NrzQU6\
yuGnBXj8ytqU0CwIPX4WecigUCAkVDNx\
-----END CERTIFICATE-----"""],
            },
        }
    ,
   
        {
            "type": "cpu-on-fire",
            "age": 29,
            "url": "https://example.com/thing.js",
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "body": {"temperature": 614.0},
        }
    ,
]

empty_xml = ""

valid_xml = """
    <feedback> 
      <version>1.0</version> 
      <report_metadata> 
        <org_name>reporting_org_name</org_name> 
        <email>reporter@domain.com</email> 
        <extra_contact_info></extra_contact_info> 
        <report_id>0000123456</report_id> 
        <date_range> 
          <begin>1234123489</begin> 
          <end>1234123499</end> 
        </date_range> 
      </report_metadata> 
      <policy_published> 
        <domain>domain.com</domain> 
        <adkim>r</adkim> 
        <aspf>r</aspf> 
        <p>reject</p> 
        <sp>reject</sp> 
        <pct>100</pct> 
      </policy_published> 
      <record> 
        <row> 
          <source_ip>191.XX.XX.XXX</source_ip> 
          <count>1</count> 
          <policy_evaluated> 
            <disposition>none</disposition> 
            <dkim>pass</dkim> 
            <spf>fail</spf> 
          </policy_evaluated> 
        </row> 
        <identifiers> 
          <header_from>domain.com</header_from> 
          <envelope_from>sender.domain.com</envelope_from> 
        </identifiers> 
        <auth_results> 
          <dkim> 
            <domain>domain.com</domain> 
            <selector>12345</selector> 
            <result>pass</result> 
          </dkim> 
          <spf>
            <domain>sender.domain.com</domain> 
            <scope>xxxxx</scope> 
            <result>pass</result> 
          </spf> 
        </auth_results> 
      </record> 
    </feedback>"""

#
# Tests down from here
#

## JSON Tests

def test_post_empty_json(client):
    response = client.post("/", data=empty_json)
    assert response.status == "400 BAD REQUEST"

def test_post_valid_json_no_content_type(client):
    response = client.post("/", data=valid_jsons[0])
    assert response.status == "400 BAD REQUEST"

def test_post_valid_json_wrong_content_type(client):
    response = client.post("/", data=valid_jsons[0], content_type="text/xml")
    assert response.status == "400 BAD REQUEST"

# Loop over all valid tests
@pytest.mark.parametrize("dictionary", valid_jsons)
def test_post_full_jsons_valid(client, dictionary):
    response = client.post("/", data=json.dumps(dictionary), content_type="text/json")
    assert response.status == "200 OK"

## XML Tests
def test_post_empty_xml(client):
    response = client.post("/", data=empty_xml)
    assert response.status == "400 BAD REQUEST"


def test_post_valid_xml_no_content_type(client):
    response = client.post("/", data=valid_xml)
    assert response.status == "400 BAD REQUEST"

def test_post_valid_xml_wrong_content_type(client):
    response = client.post("/", data=valid_xml, content_type="text/json")
    assert response.status == "400 BAD REQUEST"


def test_post_valid_xml(client):
    response = client.post("/", data=valid_xml, content_type="text/xml")
    assert response.status == "200 OK"