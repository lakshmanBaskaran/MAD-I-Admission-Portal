from flask import Blueprint, render_template, request, redirect
from extensions import db
from models import User, Student, Company, PlacementDrive, Application
from routes.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    return render_template(
        "admin_dashboard.html",
        total_students=Student.query.count(),
        total_companies=Company.query.count(),
        total_drives=PlacementDrive.query.count(),
        total_applications=Application.query.count()
    )


@admin_bp.route("/companies")
@role_required("admin")
def view_companies():
    companies = Company.query.all()
    return render_template("admin_companies.html", companies=companies)


@admin_bp.route("/approve_company/<int:id>")
@role_required("admin")
def approve_company(id):
    company = Company.query.get_or_404(id)
    company.approved = True
    db.session.commit()
    return redirect("/admin/companies")


@admin_bp.route("/drives")
@role_required("admin")
def view_drives():
    drives = PlacementDrive.query.all()
    return render_template("admin_drives.html", drives=drives)


@admin_bp.route("/approve_drive/<int:id>")
@role_required("admin")
def approve_drive(id):
    drive = PlacementDrive.query.get_or_404(id)
    drive.status = "Approved"
    db.session.commit()
    return redirect("/admin/drives")


@admin_bp.route("/blacklist_user/<int:user_id>")
@role_required("admin")
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return redirect("/admin/dashboard")


@admin_bp.route("/search_student")
@role_required("admin")
def search_student():
    query = request.args.get("q")
    students = Student.query.join(User).filter(User.name.contains(query)).all()
    return render_template("admin_search_students.html", students=students)


@admin_bp.route("/search_company")
@role_required("admin")
def search_company():
    query = request.args.get("q")
    companies = Company.query.filter(Company.company_name.contains(query)).all()
    return render_template("admin_search_companies.html", companies=companies)


@admin_bp.route("/applications")
@role_required("admin")
def all_applications():
    applications = Application.query.all()
    return render_template("admin_applications.html", applications=applications)