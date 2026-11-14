from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from .extensions import db
from .models import Ticket, User

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    base = Ticket.query
    if current_user.role == 'employee':
        base = base.filter_by(requester_id=current_user.id)
    elif current_user.role == 'technician':
        base = base.filter_by(assignee_id=current_user.id)
    total = base.count()
    open_count = base.filter(Ticket.status.in_(['Open','In Progress'])).count()
    resolved_count = base.filter_by(status='Resolved').count()
    critical_count = base.filter_by(priority='Critical').count()
    recent = base.order_by(Ticket.updated_at.desc()).limit(8).all()
    status_rows = db.session.query(Ticket.status, func.count(Ticket.id)).filter(Ticket.id.in_([t.id for t in base.all()])).group_by(Ticket.status).all() if total else []
    return render_template('dashboard.html', total=total, open_count=open_count, resolved_count=resolved_count, critical_count=critical_count, recent=recent, status_labels=[r[0] for r in status_rows], status_values=[r[1] for r in status_rows])

@bp.route('/admin/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('Administrator access is required.', 'danger')
        return redirect(url_for('main.dashboard'))
    people = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', people=people)
