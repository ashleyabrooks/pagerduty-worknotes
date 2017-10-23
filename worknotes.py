import requests
import json
from datetime import datetime, timedelta

api_token = "WTS8E_CuvcyrnLHEy_JR"


def get_since(hours):
    """Given number of hours as an integer, return the UTC date and time."""

    now = datetime.utcnow()
    since = now - timedelta(hours=hours)

    return since


def do_get_request(endpoint, payload={}):
    """Handle all GET requests."""

    url = "https://api.pagerduty.com/{0}".format(endpoint)

    headers = {
        "Authorization": "Token token={0}".format(api_token),
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    r = requests.get(url, headers=headers, data=json.dumps(payload))

    return r.json()


def get_incidents_since():
    """Given a UTC date and time, return all incidents triggered in a PD account since that time."""

    endpoint = "incidents"

    payload = {"since": str(get_since(16))}

    incidents = do_get_request(endpoint, payload)

    incident_ids = []

    for incident in incidents["incidents"]:
        incident_ids.append(str(incident["id"]))

    print incident_ids


def get_incident_log_entries(incident_id):
    """Given an incident ID, return log entry details."""

    endpoint = "incidents/{0}/log_entries".format(incident_id)

    ile = do_get_request(endpoint)

    return ile

if __name__ == "__main__":
    get_incident_log_entries()




