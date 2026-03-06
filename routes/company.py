from flask import Blueprint, render_template, request, redirect
from extensions import db
from models import Company, PlacementDrive, Application
from routes.decorators import role_required
from flask_login import current_user
from datetime import datetime

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/dashboard")
@role_required("company")
def dashboard():
    company = Company.query.filter_by(user_id=current_user.id).first()
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    return render_template("company_dashboard.html", drives=drives)


@company_bp.route("/create_drive", methods=["POST"])
@role_required("company")
def create_drive():
    company = Company.query.filter_by(user_id=current_user.id).first()
    if not company.approved:
        return "Company Not Approved"

    drive = PlacementDrive(
        company_id=company.id,
        job_title=request.form["job_title"],
        job_description=request.form["job_description"],
        eligibility_criteria=request.form.get("eligibility"),
        application_deadline=datetime.strptime(request.form["deadline"], "%Y-%m-%d")
    )
    db.session.add(drive)
    db.session.commit()

    return redirect("/company/dashboard")


@company_bp.route("/applications/<int:drive_id>")
@role_required("company")
def view_applications(drive_id):
    apps = Application.query.filter_by(drive_id=drive_id).all()
    return render_template("company_applications.html", applications=apps)


@company_bp.route("/update_status/<int:app_id>", methods=["POST"])
@role_required("company")
def update_status(app_id):
    app = Application.query.get_or_404(app_id)
    app.status = request.form["status"]
    db.session.commit()
    return redirect("/company/dashboard")