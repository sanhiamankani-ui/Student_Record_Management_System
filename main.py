import csv
import json
import os

CSV_FILE = "students.csv"
JSON_FILE = "students.json"
FIELDS = ["ID", "Name", "Age", "Course", "Marks"]


def load_students():
    students = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["Age"] = int(row["Age"])
                    row["Marks"] = float(row["Marks"])
                    students.append(row)
        except (OSError, ValueError, KeyError) as error:
            print("Could not load CSV records:", error)
    return students


def save_students(students):
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
    except OSError as error:
        print("Could not save records:", error)


def add_student(students):
    student_id = input("Enter student ID: ").strip()
    if any(student["ID"] == student_id for student in students):
        print("That student ID already exists.")
        return

    name = input("Enter student name: ").strip()
    course = input("Enter course: ").strip()

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks (0-100): "))
        if age <= 0 or not 0 <= marks <= 100:
            print("Age must be positive and marks must be from 0 to 100.")
            return
    except ValueError:
        print("Please enter valid numbers for age and marks.")
        return

    student = {
        "ID": student_id,
        "Name": name,
        "Age": age,
        "Course": course,
        "Marks": marks
    }
    students.append(student)
    save_students(students)
    print("Student added successfully!")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n--- All Student Records ---")
    for student in students:
        print(
            f"ID: {student['ID']} | Name: {student['Name']} | "
            f"Age: {student['Age']} | Course: {student['Course']} | "
            f"Marks: {student['Marks']}"
        )


def search_student(students):
    student_id = input("Enter student ID to search: ").strip()
    for student in students:
        if student["ID"] == student_id:
            print("Student found:", student)
            return
    print("Student not found.")


def update_student(students):
    student_id = input("Enter student ID to update: ").strip()
    for student in students:
        if student["ID"] == student_id:
            name = input("Enter new name: ").strip()
            course = input("Enter new course: ").strip()
            try:
                age = int(input("Enter new age: "))
                marks = float(input("Enter new marks (0-100): "))
                if age <= 0 or not 0 <= marks <= 100:
                    print("Invalid age or marks.")
                    return
            except ValueError:
                print("Please enter valid numbers.")
                return

            student["Name"] = name
            student["Course"] = course
            student["Age"] = age
            student["Marks"] = marks
            save_students(students)
            print("Student updated successfully!")
            return
    print("Student not found.")


def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()
    for student in students:
        if student["ID"] == student_id:
            students.remove(student)
            save_students(students)
            print("Student deleted successfully!")
            return
    print("Student not found.")


def show_top_students(students):
    # List comprehension selects students with marks above 80.
    top_students = [student for student in students if student["Marks"] > 80]

    # Lambda function sorts students by marks, highest first.
    top_students.sort(key=lambda student: student["Marks"], reverse=True)

    if not top_students:
        print("No students have marks above 80.")
        return

    print("\n--- Students with Marks Above 80 ---")
    for student in top_students:
        print(student)


def main():
    students = load_students()
    while True:
        print("\n===== Student Record Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Show Top Students")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice (1-7): "))
            if choice == 1:
                add_student(students)
            elif choice == 2:
                view_students(students)
            elif choice == 3:
                search_student(students)
            elif choice == 4:
                update_student(students)
            elif choice == 5:
                delete_student(students)
            elif choice == 6:
                show_top_students(students)
            elif choice == 7:
                print("Thank you for using the system!")
                break
            else:
                print("Please choose a number from 1 to 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
