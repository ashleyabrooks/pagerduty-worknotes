import json
import requests
import sys

from datetime import datetime, timedelta


api_token = ""


def do_get_request(endpoint, resource, payload={}):
    """Handle all GET requests."""

    url = "https://api.pagerduty.com/{0}".format(endpoint)
    #url = "https://requestb.in/th5li5th"

    headers = {
        "Authorization": "Token token={0}".format(api_token),
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    payload["limit"] = 100 
    payload["time_zone"] = 'UTC'   

    r = requests.get(url, headers=headers, params=payload)

    return r.json()

    if r.status_code == 200:
        r = r.json()

        # Pagination handling if there are over 100 resources returned
        try:
            if r["more"] == True:
                output = r 
                payload["offset"] = 100

                while r["more"]:
                    r = requests.get(url, headers=headers, params=payload).json()

                    for i in r[resource]:
                        output[resource].append(i)

                    payload["offset"] += 100
                r = output
            return r
        except:
            print(sys.exc_type, sys.exc_info)
            return r

    else:
        raise Exception("There was an issue with the GET request: \nStatus code: {code} \nError: {error}"\
            .format(code=r.status_code, error=r.text))


def get_incidents_since(hours):
    """Given a UTC date and time, return all incidents triggered in a PD account since that time."""

    def get_since(hours):

        now = datetime.utcnow()
        since = now - timedelta(hours=hours)

        return since

    incidents = do_get_request("incidents", "incidents", {"since": str(get_since(hours))})

    incident_ids = []

    for incident in incidents["incidents"]:
        incident_ids.append(str(incident["id"]))

    return incident_ids


def get_incident_log_entries(incident_id):
    """Given an incident ID, return log entry details."""

    log_entries = do_get_request("incidents/{0}/log_entries".format(incident_id), "log_entries")

    print("--------------- Incident ID: {0} ---------------\n".format(incident_id))

    for ile in log_entries["log_entries"]:
        print(ile["created_at"])
        print(ile["summary"] + "\n")
        
        if ile["type"] == "annotate_log_entry":
            print("Worknote: " + ile["channel"]["summary"] + "\n")


def display_worknotes(hours):
    """Prints out worknotes for given number of hours."""

    recent_incidents = get_incidents_since(hours)

    for incident_id in recent_incidents:
        get_incident_log_entries(incident_id)


def check_inputs():
    """Check sys arguments before running rest of script."""

    if len(sys.argv) != 2:
        print("Usage: This script is intended to print the latest worknotes on an account given a number of hours as a single integer.")
        print("Enter `worknotes.py <number of hours>` to run this program.")
        sys.exit()


if __name__ == "__main__":
    check_inputs()

    hours = int(sys.argv[1])

    display_worknotes(hours)

