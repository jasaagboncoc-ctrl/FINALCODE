# =========================================================
# DATA AND SYSTEM SETTINGS
# =========================================================
from datetime import datetime

students = []
sections = []
attendance_dates = []

subjects = {
    "1": "ITE-260 - Computer Programming 1",
    "2": "ITE-366 - Introduction to Computing"
}

periods = ["P3"]
MAX_ATTENDANCE_DAYS = 10
ATTENDANCE_POINTS_PER_DAY = 5
GRADE_MAXIMUMS = {"attendance": 10, "practice": 3, "reflection": 3, "quiz": 7, "checkin": 100}
GRADE_WEIGHTS = {"attendance": 5, "practice": 35, "reflection": 15, "quiz": 15, "checkin": 30}

USERNAME = "teacher"
PASSWORD = "teacher123"

# =========================================================
# SECTION FUNCTIONS
# =========================================================
def select_section():
    if len(sections) == 0:
        print("\nNo sections available.")
        return None

    print("\nSELECT SECTION")
    print("----------------------------------------")

    for number, section in enumerate(sections, start=1):
        print("[{}]. {}".format(number, section))

    print("[0]. Back")

    while True:
        choice = input("\nSelect Section: ")

        if choice == "0":
            return None

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(sections):
                return sections[number - 1]

        print("Invalid selection.")


def add_sections():
    print("\nADD SECTIONS")
    print("----------------------------------------")
    print("[0]. Back")

    number = 1

    while True:
        section = input("\nSection {}: ".format(number)).strip()

        if section == "0":
            return

        if section == "":
            print("Please enter a section.")
            continue

        if section in sections:
            print("Section already exists!")
        else:
            sections.append(section)
            sections.sort(key=lambda section: section.upper())
            print("Section added successfully!")
            number += 1


def change_section():
    old_section = select_section()

    if old_section is None:
        return

    print("\nCHANGE SECTION NAME")
    print("----------------------------------------")
    print("Current Section:", old_section)

    new_section = input("New Section Name: ").strip()

    if new_section == "":
        print("\nSection name cannot be empty.")
        return

    if new_section in sections:
        print("\nThat section already exists.")
        return

    sections[sections.index(old_section)] = new_section

    for student in students:
        if student["section"] == old_section:
            student["section"] = new_section

    sections.sort(key=lambda section: section.upper())
    print("\nSection name changed successfully!")


# =========================================================
# STUDENT REGISTRATION
# =========================================================
def register_students():
    section = select_section()

    if section is None:
        return

    print("\nREGISTER STUDENTS")
    print("----------------------------------------")
    print("Section:", section)
    print("Paste one student name per line.")
    print("Press ENTER on an empty line when finished.")
    print("[0]. Back")

    while True:
        name = input("\nStudent Name: ").strip()

        if name == "0":
            return

        if name == "":
            break

        exists = False

        for student in students:
            if student["name"].upper() == name.upper():
                exists = True
                break

        if exists:
            print("Student already exists!")
            continue

        students.append({
            "name": name,
            "section": section,
            "grades": {},
            "attendance": {}
        })

        print("Student added successfully!")

    students.sort(key=lambda student: student["name"].upper())
    print("\nStudents registered successfully!")


# =========================================================
# STUDENT SELECTION
# =========================================================
def select_student(section=None):
    if section is None:
        selected_students = students
    else:
        selected_students = []
        for student in students:
            if student["section"] == section:
                selected_students.append(student)

    if len(selected_students) == 0:
        print("\nNo students available.")
        return None

    selected_students.sort(key=lambda student: student["name"].upper())

    print("\nSELECT STUDENT")
    print("----------------------------------------")

    for number, student in enumerate(selected_students, start=1):
        print("[{}]. {}".format(number, student["name"]))

    print("[0]. Back")

    while True:
        choice = input("\nSelect Student: ")

        if choice == "0":
            return None

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(selected_students):
                return selected_students[number - 1]

        print("Invalid selection.")


# =========================================================
# STUDENT LIST / MANAGEMENT
# =========================================================
def view_student_list():
    section = select_section()

    if section is None:
        return

    while True:
        print("\nSTUDENT LIST")
        print("-" * 80)
        print("Section:", section)
        print()
        print("{:<6}{}".format("No.", "Student Name"))
        print("-" * 80)

        section_students = []

        for student in students:
            if student["section"] == section:
                section_students.append(student)

        section_students.sort(key=lambda student: student["name"].upper())

        for number, student in enumerate(section_students, start=1):
            print("{:<6}{}".format(number, student["name"]))

        print("-" * 80)
        print("Total Students:", len(section_students))
        print("-" * 80)

        print("\nSTUDENT MANAGEMENT")
        print("[1]. Delete Student")
        print("[2]. Transfer Student")
        print("[3]. Change Section Name")
        print("[0]. Back")
        print("-" * 80)

        choice = input("Select: ")

        if choice == "1":
            delete_student(section)
        elif choice == "2":
            transfer_student(section)
        elif choice == "3":
            change_section()
            return
        elif choice == "0":
            return
        else:
            print("Invalid selection.")


def delete_student(section):
    student = select_student(section)

    if student is None:
        return

    confirm = input(
        "\nDelete {}? (Y/N): ".format(student["name"])
    ).upper()

    if confirm == "Y":
        students.remove(student)
        print("\nStudent deleted successfully!")
    else:
        print("\nDelete cancelled.")


def transfer_student(section):
    student = select_student(section)

    if student is None:
        return

    new_section = select_section()

    if new_section is None:
        return

    student["section"] = new_section
    print("\nStudent transferred successfully!")
    print("New Section:", new_section)


# =========================================================
# SUBJECT AND PERIOD
# =========================================================
def select_subject():
    print("\nSELECT SUBJECT")
    print("----------------------------------------")

    for number, subject in subjects.items():
        print("[{}]. {}".format(number, subject))

    print("[0]. Back")

    while True:
        choice = input("\nSelect Subject: ")

        if choice == "0":
            return None

        if choice in subjects:
            return subjects[choice]

        print("Invalid selection.")


def select_period():
    # This system is configured to use P3 only.
    print("\nSELECT PERIOD")
    print("----------------------------------------")
    print("[1]. P3 - Period 3")
    print("[0]. Back")

    while True:
        choice = input("\nSelect Period: ").strip()
        if choice == "0":
            return None
        if choice == "1":
            return "P3"
        print("Invalid selection.")


# =========================================================
# ATTENDANCE
# =========================================================
def add_attendance_date():
    print("\nADD ATTENDANCE DATE")
    print("----------------------------------------")
    print("[1]. Automatic Date (today)")
    print("[2]. Manual Date (MM/DD/YYYY)")
    print("[0]. Back")

    while True:
        choice = input("Select date option: ").strip()

        if choice == "0":
            return

        if choice == "1":
            # Automatically use the computer's current local date.
            date = datetime.now().strftime("%m/%d/%Y")
            print("\nToday's date:", date)
            break

        if choice == "2":
            while True:
                date_input = input("Enter date (MM/DD/YYYY): ").strip()

                if date_input == "0":
                    return

                try:
                    # Validate the date and enforce the requested format.
                    parsed_date = datetime.strptime(date_input, "%m/%d/%Y")
                    if parsed_date.strftime("%m/%d/%Y") != date_input:
                        raise ValueError
                    date = date_input
                    break
                except ValueError:
                    print("Invalid date. Use MM/DD/YYYY, for example 10/14/2026.")
            break

        print("Invalid selection. Please choose 1, 2, or 0.")

    if len(attendance_dates) >= MAX_ATTENDANCE_DAYS:
        print("You can record a maximum of {} attendance dates.".format(MAX_ATTENDANCE_DAYS))
        return

    if date in attendance_dates:
        print("Attendance date {} already exists!".format(date))
        return

    attendance_dates.append(date)
    print("Attendance date {} added successfully!".format(date))
    print("Attendance dates recorded: {}/{}".format(len(attendance_dates), MAX_ATTENDANCE_DAYS))


def select_attendance_date():
    if len(attendance_dates) == 0:
        print("\nNo attendance dates available.")
        return None

    print("\nSELECT ATTENDANCE DATE")
    print("----------------------------------------")

    for number, date in enumerate(attendance_dates, start=1):
        print("[{}]. {}".format(number, date))

    print("[0]. Back")

    while True:
        choice = input("\nSelect Date: ")

        if choice == "0":
            return None

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(attendance_dates):
                return attendance_dates[number - 1]

        print("Invalid selection.")


def enter_attendance_date():
    section = select_section()
    if section is None:
        return

    section_students = sorted(
        [student for student in students if student["section"] == section],
        key=lambda student: student["name"].upper()
    )
    if not section_students:
        print("\nNo students are registered in this section.")
        return

    print("\nATTENDANCE TYPE")
    print("----------------------------------------")
    print("[1]. Face-to-Face")
    print("[2]. Online")
    print("[0]. Back")
    while True:
        choice = input("Select: ").strip()
        if choice == "0":
            return
        if choice == "1":
            attendance_type = "Face-to-Face"
            break
        if choice == "2":
            attendance_type = "Online"
            break
        print("Invalid selection.")

    while True:
        date = select_attendance_date()
        if date is None:
            return

        # A record counts as recorded even when its value is 0 (Absent).
        missing_students = [
            student for student in section_students
            if attendance_type not in student.get("attendance", {}).get(date, {})
        ]

        if not missing_students:
            print("\nATTENDANCE ALREADY RECORDED!")
            print("Section:", section)
            print("Date   :", date)
            print("Type   :", attendance_type)
            print("Every student in this section already has a record for this date and type.")
            print("[1]. Select Another Date")
            print("[0]. Back")
            next_choice = input("Select: ").strip()
            if next_choice == "1":
                continue
            if next_choice == "0":
                return
            print("Invalid selection. Returning to date selection.")
            continue

        already_count = len(section_students) - len(missing_students)
        if already_count:
            print("\nSome students already have a record for this date/type.")
            print("Their records will be skipped; only missing students will be recorded.")

        print("\nENTER ATTENDANCE")
        print("-" * 80)
        print("Section :", section)
        print("Date    :", date)
        print("Type    :", attendance_type)
        print("P = Present ({} points)".format(ATTENDANCE_POINTS_PER_DAY))
        print("A = Absent (0 points)")
        print("[0] = Stop and return")
        print("-" * 80)

        for student in missing_students:
            while True:
                status = input("{}: ".format(student["name"])).strip().upper()
                if status == "0":
                    print("\nEntry stopped. All completed records have been recorded for this session.")
                    return
                if status not in ("P", "A"):
                    print("Please enter P, A, or 0.")
                    continue

                student.setdefault("attendance", {})
                student["attendance"].setdefault(date, {})
                student["attendance"][date][attendance_type] = (
                    ATTENDANCE_POINTS_PER_DAY if status == "P" else 0
                )
                break

        print("\nAttendance recorded successfully!")
        print("All students now have a record for {} on {}.".format(attendance_type, date))
        return


def calculate_attendance(student):
    # Each date can contribute only once, even if both attendance types exist.
    # A present day is worth 5 raw points; 10 days maximum = 50 raw points.
    present_days = 0
    for date, records in student["attendance"].items():
        if any(points > 0 for points in records.values()):
            present_days += 1
    present_days = min(present_days, MAX_ATTENDANCE_DAYS)
    return present_days * ATTENDANCE_POINTS_PER_DAY


def view_attendance():
    section = select_section()

    if section is None:
        return

    while True:
        section_students = [
            student for student in students
            if student["section"] == section
        ]
        section_students.sort(key=lambda student: student["name"].upper())

        print("\n" + "=" * 100)
        print("                 ATTENDANCE CLASS RECORD")
        print("=" * 100)
        print("Section:", section)
        print("Legend: P = Present | A = Absent | - = Not recorded")
        print("-" * 100)

        if not attendance_dates:
            print("No attendance dates have been added yet.")
        else:
            print("{:<30}".format("Student Name"), end="")
            for date in attendance_dates:
                print("{:<12}".format(date), end="")
            print("{:<10}".format("Total"))
            print("-" * 100)

            for student in section_students:
                print("{:<30}".format(student["name"][:29]), end="")
                total = 0

                for date in attendance_dates:
                    value = 0
                    letter = "-"
                    records = student["attendance"].get(date, {})

                    if records:
                        value = max(records.values(), default=0)
                        letter = "P" if any(points > 0 for points in records.values()) else "A"
                        # Count a calendar date only once, even if both types were entered.
                        total += ATTENDANCE_POINTS_PER_DAY if value > 0 else 0

                    print("{:<12}".format(letter), end="")

                total = min(total, MAX_ATTENDANCE_DAYS * ATTENDANCE_POINTS_PER_DAY)
                print("{:<10}".format("{}/50".format(total)))

            print("-" * 100)
            print("Students in section:", len(section_students))
            print("Attendance dates recorded:", len(attendance_dates))

        print("\n[1]. Delete Attendance Date")
        print("[0]. Back")
        choice = input("Select: ").strip()

        if choice == "0":
            return

        if choice != "1":
            print("Invalid selection. Please choose 1 or 0.")
            continue

        if not attendance_dates:
            print("\nThere are no attendance dates to delete.")
            continue

        print("\nSAVED ATTENDANCE DATES")
        print("-" * 40)
        for number, date in enumerate(attendance_dates, start=1):
            print("[{}]. {}".format(number, date))
        print("[0]. Cancel")

        date_choice = input("Select the date to delete: ").strip()
        if date_choice == "0":
            print("Deletion cancelled.")
            continue

        if not date_choice.isdigit():
            print("Invalid selection. Enter a listed number.")
            continue

        date_index = int(date_choice) - 1
        if date_index < 0 or date_index >= len(attendance_dates):
            print("Invalid selection. Enter a listed number.")
            continue

        date_to_delete = attendance_dates[date_index]
        confirm = input(
            "Delete {} and its attendance records for ALL students? (Y/N): ".format(
                date_to_delete
            )
        ).strip().upper()

        if confirm == "Y":
            attendance_dates.pop(date_index)
            for student in students:
                student.setdefault("attendance", {}).pop(date_to_delete, None)
            print("Attendance date {} and its records were deleted.".format(date_to_delete))
            print("Attendance totals and grade calculations will use the remaining records.")
        elif confirm == "N":
            print("Deletion cancelled.")
        else:
            print("Please enter Y or N. No records were deleted.")


def attendance_menu():
    while True:
        print("\nATTENDANCE")
        print("----------------------------------------")
        print("[1]. Add Attendance Date")
        print("[2]. Enter Attendance")
        print("[3]. View Attendance")
        print("[0]. Back")
        print("----------------------------------------")

        choice = input("Select: ")

        if choice == "1":
            add_attendance_date()
        elif choice == "2":
            enter_attendance_date()
        elif choice == "3":
            view_attendance()
        elif choice == "0":
            return
        else:
            print("Invalid selection.")


# =========================================================
# GRADE DATA
# =========================================================
def get_grade_data(student, subject, period):
    if subject not in student["grades"]:
        student["grades"][subject] = {}

    if period not in student["grades"][subject]:
        student["grades"][subject][period] = {
            "attendance": 0,
            "practice": 0,
            "reflection": 0,
            "quiz": 0,
            "checkin": 0,
            "period_grade": None
        }

    return student["grades"][subject][period]


# =========================================================
# FINAL GRADE CALCULATION
# =========================================================
def calculate_grade(student, subject, period):
    data = get_grade_data(student, subject, period)
    data["attendance"] = calculate_attendance(student)  # raw attendance points, max 50

    # Convert attendance's 50 raw points to the table's 10-point maximum, then apply 5%.
    attendance_score = data["attendance"] / ATTENDANCE_POINTS_PER_DAY
    attendance_grade = (attendance_score / GRADE_MAXIMUMS["attendance"]) * GRADE_WEIGHTS["attendance"]
    practice_grade = (data["practice"] / GRADE_MAXIMUMS["practice"]) * GRADE_WEIGHTS["practice"]
    reflection_grade = (data["reflection"] / GRADE_MAXIMUMS["reflection"]) * GRADE_WEIGHTS["reflection"]
    quiz_grade = (data["quiz"] / GRADE_MAXIMUMS["quiz"]) * GRADE_WEIGHTS["quiz"]
    checkin_grade = (data["checkin"] / GRADE_MAXIMUMS["checkin"]) * GRADE_WEIGHTS["checkin"]

    final_grade = attendance_grade + practice_grade + reflection_grade + quiz_grade + checkin_grade
    data["period_grade"] = final_grade
    return final_grade


# =========================================================
# ENTER GRADE COMPONENT
# =========================================================
def enter_grade_component(section, subject, period, component, maximum):
    section_students = []

    for student in students:
        if student["section"] == section:
            section_students.append(student)

    section_students.sort(key=lambda student: student["name"].upper())

    print("\n{}".format(component.upper()))
    print("-" * 100)
    print("Section :", section)
    print("Subject :", subject)
    print("Period  :", period)
    print("Maximum :", maximum, "points")
    print("-" * 100)
    print("{:<35}{:<10}".format("Student Name", "Grade"))
    print("-" * 100)

    for student in section_students:
        data = get_grade_data(student, subject, period)

        if component == "Let's Practice":
            current = data["practice"]
        elif component == "Reflection":
            current = data["reflection"]
        elif component == "Wrap-up Quiz":
            current = data["quiz"]
        else:
            current = data["checkin"]

        print("{:<35}{}/{}".format(student["name"], current, maximum))

    print("-" * 100)
    print("[0]. Back")

    for student in section_students:
        data = get_grade_data(student, subject, period)

        while True:
            grade_input = input("\n{}: ".format(student["name"]))

            if grade_input == "0":
                return

            try:
                grade = float(grade_input)

                if grade < 0 or grade > maximum:
                    print("Invalid grade. Enter 0 to {} only.".format(maximum))
                    continue

                if component == "Let's Practice":
                    data["practice"] = grade
                elif component == "Reflection":
                    data["reflection"] = grade
                elif component == "Wrap-up Quiz":
                    data["quiz"] = grade
                elif component == "Check-in":
                    data["checkin"] = grade

                calculate_grade(student, subject, period)
                break

            except ValueError:
                print("Please enter a valid number.")

    print("\nGrades recorded successfully!")


# =========================================================
# ENTER GRADES
# =========================================================
def enter_grades():
    section = select_section()

    if section is None:
        return

    subject = select_subject()

    if subject is None:
        return

    period = select_period()

    if period is None:
        return

    while True:
        print("\nENTER GRADES")
        print("----------------------------------------")
        print("Section :", section)
        print("Subject :", subject)
        print("Period  :", period)
        print("----------------------------------------")
        print("[1]. Let's Practice       - 3 points (35%)")
        print("[2]. Reflection           - 3 points (15%)")
        print("[3]. Wrap-up Quiz         - 7 points (15%)")
        print("[4]. Check-in             - 100 points (30%)")
        print("[5]. Regrade / Change Grade")
        print("[0]. Back")
        print("----------------------------------------")

        choice = input("Select: ")

        if choice == "1":
            enter_grade_component(section, subject, period, "Let's Practice", 3)
        elif choice == "2":
            enter_grade_component(section, subject, period, "Reflection", 3)
        elif choice == "3":
            enter_grade_component(section, subject, period, "Wrap-up Quiz", 7)
        elif choice == "4":
            enter_grade_component(section, subject, period, "Check-in", 100)
        elif choice == "5":
            regrade(section, subject, period)
        elif choice == "0":
            return
        else:
            print("Invalid selection.")


# =========================================================
# REGRADE / CHANGE GRADE
# =========================================================
def regrade(section, subject, period):
    section_students = []

    for student in students:
        if student["section"] == section:
            section_students.append(student)

    section_students.sort(key=lambda student: student["name"].upper())

    if len(section_students) == 0:
        print("\nNo students available.")
        return

    print("\nRE-GRADE / CHANGE GRADE")
    print("-" * 100)
    print("Section :", section)
    print("Subject :", subject)
    print("Period  :", period)
    print("-" * 100)

    for number, student in enumerate(section_students, start=1):
        data = get_grade_data(student, subject, period)
        print(
            "[{}]. {} Practice: {}/3 Reflection: {}/3 Quiz: {}/7 Check-in: {}/100".format(
                number,
                student["name"],
                data["practice"],
                data["reflection"],
                data["quiz"],
                data["checkin"]
            )
        )

    print("\n[0]. Back")

    while True:
        choice = input("\nSelect Student: ")

        if choice == "0":
            return

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(section_students):
                student = section_students[number - 1]
                break

        print("Invalid selection.")

    while True:
        print("\nSELECT GRADE TO CHANGE")
        print("----------------------------------------")
        print("[1]. Let's Practice")
        print("[2]. Reflection")
        print("[3]. Wrap-up Quiz")
        print("[4]. Check-in")
        print("[0]. Back")
        print("----------------------------------------")

        choice = input("Select: ")

        if choice == "0":
            return

        if choice == "1":
            component = "Let's Practice"
            maximum = 3
        elif choice == "2":
            component = "Reflection"
            maximum = 3
        elif choice == "3":
            component = "Wrap-up Quiz"
            maximum = 7
        elif choice == "4":
            component = "Check-in"
            maximum = 100
        else:
            print("Invalid selection.")
            continue

        data = get_grade_data(student, subject, period)

        if component == "Let's Practice":
            current = data["practice"]
        elif component == "Reflection":
            current = data["reflection"]
        elif component == "Wrap-up Quiz":
            current = data["quiz"]
        else:
            current = data["checkin"]

        print("\nCURRENT GRADE: {}/{}".format(current, maximum))

        while True:
            new_grade_input = input("Enter New Grade: ")

            try:
                new_grade = float(new_grade_input)

                if new_grade < 0 or new_grade > maximum:
                    print("Invalid grade. Enter 0 to {} only.".format(maximum))
                    continue

                break

            except ValueError:
                print("Please enter a valid number.")

        if component == "Let's Practice":
            data["practice"] = new_grade
        elif component == "Reflection":
            data["reflection"] = new_grade
        elif component == "Wrap-up Quiz":
            data["quiz"] = new_grade
        elif component == "Check-in":
            data["checkin"] = new_grade

        calculate_grade(student, subject, period)
        print("\nGrade changed successfully!")
        return


# =========================================================
# VIEW CLASS GRADES
# =========================================================
def view_grades():
    section = select_section()

    if section is None:
        return

    subject = select_subject()

    if subject is None:
        return

    period = select_period()

    if period is None:
        return

    print("\nCLASS GRADE RECORD")
    print("-" * 130)
    print("Section:", section)
    print("Subject:", subject)
    print("Period :", period)
    print("-" * 130)

    print(
        "{:<28}{:<12}{:<12}{:<12}{:<12}{:<14}{:<12}{}".format(
            "Student Name",
            "Attend",
            "Practice",
            "Reflection",
            "Quiz",
            "Check-in",
            "Final Grade",
            "Status"
        )
    )
    print("-" * 130)

    section_students = []

    for student in students:
        if student["section"] == section:
            section_students.append(student)

    section_students.sort(key=lambda student: student["name"].upper())

    for student in section_students:
        data = get_grade_data(student, subject, period)
        final_grade = calculate_grade(student, subject, period)

        if final_grade >= 80:
            status = "PASSED"
        else:
            status = "FAILED"

        print(
            "{:<28}{:<12}{:<12}{:<12}{:<12}{:<14}{:<12.2f}% {}".format(
                student["name"],
                "{}/10".format(data["attendance"] / ATTENDANCE_POINTS_PER_DAY),
                "{}/3".format(data["practice"]),
                "{}/3".format(data["reflection"]),
                "{}/7".format(data["quiz"]),
                "{}/100".format(data["checkin"]),
                final_grade,
                status
            )
        )

    print("-" * 130)
    print("[0]. Back")
    input("\nPress ENTER to return...")


# =========================================================
# GRADE CARD
# =========================================================
def show_grade_card(student, subject, period):
    data = get_grade_data(student, subject, period)
    final_grade = calculate_grade(student, subject, period)

    if final_grade >= 80:
        status = "PASSED"
    else:
        status = "FAILED"

    print("\nGRADE CARD")
    print("-" * 65)
    print("Student :", student["name"])
    print("Section :", student["section"])
    print("Subject :", subject)
    print("Period  :", period)
    print("-" * 65)

    print("\nATTENDANCE")
    print("-" * 65)
    print("{:<25}{:<20}{}".format("Date", "Face-to-Face", "Online"))
    print("-" * 65)

    for date in attendance_dates:
        face = "-"
        online = "-"

        if date in student["attendance"]:
            if "Face-to-Face" in student["attendance"][date]:
                if student["attendance"][date]["Face-to-Face"] == 5:
                    face = "P"
                else:
                    face = "A"

            if "Online" in student["attendance"][date]:
                if student["attendance"][date]["Online"] == 5:
                    online = "P"
                else:
                    online = "A"

        print("{:<25}{:<20}{}".format(date, face, online))

    print("-" * 65)
    print("Attendance      : {}/10 (5%) [5 raw points per present day]".format(data["attendance"] / ATTENDANCE_POINTS_PER_DAY))

    print("\nGRADES")
    print("-" * 65)
    print("Let's Practice  : {}/3 (35%)".format(data["practice"]))
    print("Reflection      : {}/3 (15%)".format(data["reflection"]))
    print("Wrap-up Quiz    : {}/7 (15%)".format(data["quiz"]))
    print("Check-in        : {}/100 (30%)".format(data["checkin"]))
    print("-" * 65)
    print("Final Grade: {:.2f}%".format(final_grade))
    print("Status: {}".format(status))
    print("-" * 65)
    print("[0]. Back")
    input("\nPress ENTER to return...")


def view_grade_card():
    section = select_section()

    if section is None:
        return

    student = select_student(section)

    if student is None:
        return

    subject = select_subject()

    if subject is None:
        return

    period = select_period()

    if period is None:
        return

    show_grade_card(student, subject, period)


# =========================================================
# GRADE STATUS
# =========================================================
def view_grade_status():
    section = select_section()

    if section is None:
        return

    subject = select_subject()

    if subject is None:
        return

    period = select_period()

    if period is None:
        return

    print("\nGRADE STATUS")
    print("-" * 80)
    print("Section:", section)
    print("Subject:", subject)
    print("Period :", period)
    print("-" * 80)

    section_students = []

    for student in students:
        if student["section"] == section:
            section_students.append(student)

    section_students.sort(key=lambda student: student["name"].upper())

    for student in section_students:
        final_grade = calculate_grade(student, subject, period)

        if final_grade >= 80:
            status = "PASSED"
        else:
            status = "FAILED"

        print("{:<35} {:.2f}% {}".format(student["name"], final_grade, status))

    print("-" * 80)
    print("[0]. Back")
    input("\nPress ENTER to return...")


# =========================================================
# CHANGE PASSWORD
# =========================================================
def change_password():
    global PASSWORD

    print("\nCHANGE PASSWORD")
    print("----------------------------------------")

    current = input("Current Password: ")

    if current != PASSWORD:
        print("\nIncorrect password.")
        return

    new_password = input("New Password: ")

    if new_password == "":
        print("\nPassword cannot be empty.")
        return

    PASSWORD = new_password
    print("\nPassword changed successfully!")


# =========================================================
# STUDENT MENU
# SECTION FIRST
# =========================================================
def student_menu():
    while True:
        section = select_section()

        if section is None:
            return

        student = select_student(section)

        if student is None:
            continue

        subject = select_subject()

        if subject is None:
            continue

        period = select_period()

        if period is None:
            continue

        show_grade_card(student, subject, period)


# =========================================================
# TEACHER / ADMIN LOGIN
# =========================================================
def teacher_login():
    print("\nTEACHER / ADMIN LOGIN")
    print("----------------------------------------")
    username = input("Username: ")
    password = input("Password: ")

    if username == USERNAME and password == PASSWORD:
        print("\nLogin successful!")
        teacher_menu()
    else:
        print("\nInvalid username or password.")


# =========================================================
# TEACHER / ADMIN MENU
# =========================================================
def teacher_menu():
    while True:
        print("\nTEACHER / ADMIN MENU")
        print("----------------------------------------")
        print("[1]. Add Sections")
        print("[2]. Register Students")
        print("[3]. View Student List")
        print("[4]. Attendance")
        print("[5]. Enter Grades")
        print("[6]. View Grades")
        print("[7]. View Grade Card")
        print("[8]. View Grade Status")
        print("[9]. Change Password")
        print("[0]. Logout")
        print("----------------------------------------")

        choice = input("Select: ")

        if choice == "1":
            add_sections()
        elif choice == "2":
            register_students()
        elif choice == "3":
            view_student_list()
        elif choice == "4":
            attendance_menu()
        elif choice == "5":
            enter_grades()
        elif choice == "6":
            view_grades()
        elif choice == "7":
            view_grade_card()
        elif choice == "8":
            view_grade_status()
        elif choice == "9":
            change_password()
        elif choice == "0":
            print("\nLogged out successfully!")
            return
        else:
            print("Invalid selection.")


# =========================================================
# MAIN PROGRAM
# =========================================================
while True:
    print("\nSTUDENT GRADE MONITORING SYSTEM")
    print("----------------------------------------")
    print("[1]. Teacher / Admin")
    print("[2]. Student")
    print("[0]. Exit")
    print("----------------------------------------")

    choice = input("Select: ")

    if choice == "1":
        teacher_login()
    elif choice == "2":
        student_menu()
    elif choice == "0":
        print("\nThank you for using the Student Grade Monitoring System!")
        break
    else:
        print("Invalid selection.")