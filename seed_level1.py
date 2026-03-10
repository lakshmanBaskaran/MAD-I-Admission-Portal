from app import app
from extensions import db
from models import User, Student, Company, PlacementDrive, Application
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import random

with app.app_context():

    print("Clearing old data...")

    Application.query.delete()
    PlacementDrive.query.delete()
    Student.query.delete()
    Company.query.delete()
    User.query.delete()

    db.session.commit()

    # ------------------------
    # CREATE USERS
    # ------------------------

    students_users = []
    companies_users = []

    print("Creating student users...")

    for i in range(1, 11):
        user = User(
            name=f"Student {i}",
            email=f"student{i}@portal.com",
            password_hash=generate_password_hash("password"),
            role="student"
        )
        db.session.add(user)
        students_users.append(user)

    print("Creating company users...")

    for i in range(1, 6):
        user = User(
            name=f"HR {i}",
            email=f"company{i}@portal.com",
            password_hash=generate_password_hash("password"),
            role="company"
        )
        db.session.add(user)
        companies_users.append(user)

    admin = User(
        name="Admin",
        email="admin@portal.com",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )

    db.session.add(admin)

    db.session.commit()

    # ------------------------
    # CREATE STUDENTS
    # ------------------------

    print("Creating student profiles...")

    students = []

    for user in students_users:

        student = Student(
            user_id=user.id,
            phone="9876543210",
            course="B.Tech CSE",
            graduation_year=2025
        )

        db.session.add(student)
        students.append(student)

    db.session.commit()

    # ------------------------
    # CREATE COMPANIES
    # ------------------------

    print("Creating companies...")

    companies = []

    for i, user in enumerate(companies_users):

        company = Company(
            user_id=user.id,
            company_name=f"TechCorp {i+1}",
            hr_contact="9876543210",
            website="https://company.com",
            approved=True
        )

        db.session.add(company)
        companies.append(company)

    db.session.commit()

    # ------------------------
    # CREATE DRIVES (CGPA)
    # ------------------------

    print("Creating placement drives...")

    drives = []

    jobs = [
        "Software Engineer",
        "Backend Developer",
        "Data Analyst",
        "AI Engineer",
        "Frontend Developer"
    ]

    cgpa_requirements = [6.0, 6.5, 7.0, 7.5, 8.0]

    for i in range(10):

        company = random.choice(companies)

        drive = PlacementDrive(
            company_id=company.id,
            job_title=random.choice(jobs),
            job_description="Exciting opportunity for fresh graduates",
            eligibility_criteria=str(random.choice(cgpa_requirements)),
            application_deadline=date(2025, 12, 31),
            status="Approved"
        )

        db.session.add(drive)
        drives.append(drive)

    db.session.commit()

    # ------------------------
    # CREATE APPLICATIONS
    # ------------------------

    print("Creating applications...")

    for student in students:

        applied_drives = random.sample(drives, k=3)

        for drive in applied_drives:

            application = Application(
                student_id=student.id,
                drive_id=drive.id,
                status=random.choice(
                    ["Applied", "Shortlisted", "Selected", "Rejected"]
                ),
                applied_on=datetime.utcnow()
            )

            db.session.add(application)

    db.session.commit()

    print("Database seeded successfully!")