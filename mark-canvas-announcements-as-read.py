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
MY_DOMAIN = "https://MYINSTITUTION.instructure.com"
start_date = datetime.datetime(1000, 1, 1).isoformat()

# Necessary to list all announcements

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
    course_id = course["id"]
    nowtime = datetime.datetime.now().isoformat()

    # Retrieve all announcements that have been published in the course

    params = {
        "context_codes[]": "course_" + str(course_id),
        "start_date": start_date,
        "end_date": nowtime,
        "per_page": 10000,
    }

    # Try to get announcements. If we get a non-200 response, we're probably
    # not authorized to view the course and thus can't alter the read state of
    # any announcements, so skip the course.
    announcements = requests.get(
        MY_DOMAIN + "/api/v1/announcements", headers=auth, params=params
    )

    if announcements.status_code != 200:
        print(
            f"Cannot access course {course_id} -- are you authorized to view this course? (No announcements changed.)"
        )
        continue
    else:
        print(f"""Marking announcements for course {course_id} ({course["name"]})""")

    for announcement in announcements.json():

        # Delete the offending announcements
        if announcement["read_state"] == "unread":
            disc_id = announcement["id"]
            # print(announcement["title"])
            # Mark the offending announcement as read
            mark_announcement_read(course_id, disc_id)
            print("    Marked " + announcement["title"] + " as read.")
            time.sleep(1)

print("Done.")