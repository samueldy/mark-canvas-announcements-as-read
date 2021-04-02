# Using Canvas v1 API to access an Announcement and mark it as read
import json
import requests
import os
import datetime
import time

# Initialize some important variables:

HOME_DIR = os.path.expanduser("~")
API_FILE = os.path.join(HOME_DIR, ".instructure", ".instructure.json")

with open(API_FILE, "r") as f:
    api_info = json.load(f)
TOKEN = api_info["token"]
auth = {"Authorization": "Bearer " + TOKEN}
MY_DOMAIN = "https://umich.instructure.com"
start_date = datetime.datetime(1000, 1, 1).isoformat()

# Necessary to list all announcements
# Work through Canvas' pagination model if the relevant links exist
def get_paginated_list(result: requests.models.Response) -> list:
    """
    Easily handle pagination with Canvas API requests
    """

    items_list = result.json()

    while True:
        try:
            result.headers["Link"]

            # Handle pagination links
            pagination_links = result.headers["Link"].split(",")

            pagination_urls = {}
            for link in pagination_links:
                url, label = link.split(";")
                label = label.split("=")[-1].replace('"', "")
                url = url.replace("<", "").replace(">", "")
                pagination_urls.update({label: url})

            # Now try to get the next page
            print(f"""\tGetting next page of announcements...""")
            result = requests.get(pagination_urls["next"], headers=auth)
            items_list.extend(result.json())

        except KeyError:
            print("Reached end of paginated list")
            break

    return items_list

# Get all courses

courses = requests.get(
    MY_DOMAIN + "/api/v1/courses", headers=auth, params={"per_page": 10000}
)


def mark_announcement_read(course_id, disc_id):
    conn_str = (
        MY_DOMAIN
        + "/api/v1/courses/"
        + str(course_id)
        + "/discussion_topics/"
        + str(disc_id)
        + "/read.json"
    )
    requests.put(conn_str, headers={**auth, **{"Content-Length": "0"}})


def mark_announcement_unread(course_id, disc_id):
    conn_str = (
        MY_DOMAIN
        + "/api/v1/courses/"
        + str(course_id)
        + "/discussion_topics/"
        + str(disc_id)
        + "/read.json"
    )
    requests.delete(conn_str, headers=auth)


for course in courses.json():
    try:
        course_id = course["id"]
    except TypeError:
        # Potentially malformed JSON response; skip this one.
        print(f"Couldn't get info for course {course}. Skipping.")
        continue

    nowtime = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Retrieve all announcements that have been published in the course

    params = {
        "context_codes[]": "course_" + str(course_id),
        "start_date": start_date,
        "end_date": nowtime,
        "per_page": 50,
    }

    # Try to get announcements. If we get a non-200 response, we're probably
    # not authorized to view the course and thus can't alter the read state of
    # any announcements, so skip the course.
    announcements_response = requests.get(
        MY_DOMAIN + "/api/v1/announcements", headers=auth, params=params
    )

    if announcements_response.status_code != 200:
        print(
            f"Cannot access course {course_id} -- "
            f"are you authorized to view this course? (No announcements changed.)"
        )
        continue
    else:
        print(f"""Marking announcements for course {course_id} ({course["name"]})""")

    # Get all announcements from paginated list
    announcements_list = get_paginated_list(announcements_response)

    for announcement in announcements_list:

        # Delete the offending announcements
        if announcement["read_state"] == "unread":
            disc_id = announcement["id"]
            # print(announcement["title"])
            # Mark the offending announcement as read
            mark_announcement_read(course_id, disc_id)
            print("    Marked " + announcement["title"] + " as read.")
            time.sleep(1)

print("Done.")
