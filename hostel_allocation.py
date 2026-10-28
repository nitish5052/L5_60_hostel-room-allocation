
"""Hostel room allocation system with basic safety and quality fixes."""

import html
import math
import secrets

import yaml
from flask import Flask, request

rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load hostel configuration and create rooms."""
    config = yaml.safe_load(text)

    if not isinstance(config, dict) or "blocks" not in config:
        raise ValueError("Invalid hostel configuration")

    rooms.clear()
    allocations.clear()
    waitlist.clear()

    for block, info in config["blocks"].items():
        for number in range(1, info["rooms"] + 1):
            room_no = f"{block}{number}"
            rooms[room_no] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }

    return config


def allocate_room(student_id, name, gender, year, preferred=None):
    """Allocate a suitable room to a student."""
    if not isinstance(year, int) or isinstance(year, bool):
        return None

    if student_id in allocations:
        return allocations[student_id]["room"]

    if preferred is None:
        preferred = []

    candidates = list(dict.fromkeys(preferred + list(rooms.keys())))

    for room_no in candidates:
        if room_no not in rooms:
            continue

        room = rooms[room_no]

        if room["gender"] != gender:
            continue

        if len(room["occupants"]) >= room["capacity"]:
            continue

        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name,
            "room": room_no,
            "year": year,
        }

        if student_id in waitlist:
            waitlist.remove(student_id)

        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)

    return None


def vacate_room(student_id):
    """Remove a student from their room and allocation record."""
    allocation = allocations.pop(student_id, None)

    if allocation is None:
        return False

    room_no = allocation["room"]
    occupants = rooms[room_no]["occupants"]

    if student_id in occupants:
        occupants.remove(student_id)

    return True


def monthly_fee(student_id, days_stayed):
    """Calculate fees for each started 30-day period."""
    if student_id not in allocations:
        raise ValueError("Student has no room allocation")

    if not isinstance(days_stayed, int) or days_stayed < 0:
        raise ValueError("Days stayed must be a non-negative integer")

    room_no = allocations[student_id]["room"]
    fee = rooms[room_no]["fee"]
    months = math.ceil(days_stayed / 30)

    return months * fee


def priority_order(students):
    """Order students from most senior to least senior."""
    return sorted(
        students,
        key=lambda student: student["year"],
        reverse=True,
    )


def room_lottery(student_ids):
    """Return a secure random ordering of student IDs."""
    shuffled_ids = list(student_ids)

    for index in range(len(shuffled_ids) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        shuffled_ids[index], shuffled_ids[swap_index] = (
            shuffled_ids[swap_index],
            shuffled_ids[index],
        )

    return shuffled_ids


def vacant_beds():
    """Count every unoccupied bed, including partially empty rooms."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db():
    """Return a placeholder warden database status."""
    return sqlite_connect(host="localhost", user="warden")


def sqlite_connect(host, user):
    """Simulate a database status without claiming a real connection."""
    return {
        "host": host,
        "user": user,
        "connected": False,
    }


@app.route("/room")
def room_lookup():
    """Look up a student's room using a query parameter."""
    student_id = request.args.get("id", "")
    safe_student_id = html.escape(student_id)
    allocation = allocations.get(student_id)

    if allocation is None:
        room_info = "No room allocated"
    else:
        room_info = f"Room: {html.escape(allocation['room'])}"

    return (
        f"<h1>Room lookup for {safe_student_id}: "
        f"{room_info}</h1>"
    )


def run_portal():
    """Start the Flask portal without debug mode."""
    app.run(debug=False)


def main():
    """Demonstrate hostel allocation operations."""
    load_config()

    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))

    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])

    print("Fee for S1, 45 days:", monthly_fee("S1", 45))

    students = [{"year": 1}, {"year": 4}, {"year": 2}]
    print(
        "Priority (seniors first?):",
        [student["year"] for student in priority_order(students)],
    )

    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
