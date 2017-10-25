import requests
import json
from datetime import datetime, timedelta

api_token = "WTS8E_CuvcyrnLHEy_JR"


def get_since(hours):
    """Given number of hours as an integer, return the UTC date and time."""

    now = datetime.utcnow()
    since = now - timedelta(hours=hours)

    return since


def do_get_request(endpoint, resource, payload={}):
    """Handle all GET requests."""

    url = "https://api.pagerduty.com/{0}".format(endpoint)

    headers = {
        "Authorization": "Token token={0}".format(api_token),
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    payload["limit"] = 100    

    r = requests.get(url, headers=headers, data=json.dumps(payload))

    if r.status_code == 200:
        r = r.json()

        # Pagination handling if there are over 100 resources returned
        try:
            if r["more"] == True:
                output = r 
                payload["offset"] = 100

                while r["more"]:
                    r = requests.get(url, headers=headers, data=json.dumps(payload)).json()

                    for i in r[resource]:
                        output[resource].append(i)

                    payload["offset"] += 100
                
                r = output
            
            return r

        except:
            return r

    else:
        raise Exception("There was an issue with the GET request: \nStatus code: {code} \nError: {error}"\
            .format(code=r.status_code, error=r.text))


def get_incidents_since():
    """Given a UTC date and time, return all incidents triggered in a PD account since that time."""

    incidents = do_get_request("incidents", "incidents", {"since": str(get_since(16))})

    incident_ids = []

    for incident in incidents["incidents"]:
        incident_ids.append(str(incident["id"]))

    return incident_ids


def get_incident_log_entries(incident_id):
    """Given an incident ID, return log entry details."""

    log_entries = do_get_request("incidents/{0}/log_entries".format(incident_id), "log_entries")

    print("Incident ID: {0} \n".format(incident_id))

    for ile in log_entries["log_entries"]:
        print(ile["created_at"])
        print(ile["summary"] + "\n")
        
        if ile["type"] == "annotate_log_entry":
            print("Worknote: " + ile["channel"]["summary"] + "\n")


if __name__ == "__main__":
    # get_incident_log_entries("PGGHZ4B")
    do_get_request("incidents", "incidents")




