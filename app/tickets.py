from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from .extensions import db
from .models import Ticket, User, Comment, TicketEvent
from .forms import TicketForm, CommentForm

bp = Blueprint('tickets', __name__)

def can_view(ticket):
    return current_user.role == 'admin' or ticket.requester_id == current_user.id or ticket.assignee_id == current_user.id

def log_event(ticket, message):
    db.session.add(TicketEvent(ticket_id=ticket.id, user_id=current_user.id, message=message))

@bp.route('/new', methods=['GET','POST'])
@login_required
def new():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(ticket_code='TEMP', title=form.title.data.strip(), description=form.description.data.strip(), category=form.category.data, priority=form.priority.data, requester_id=current_user.id)
        db.session.add(ticket)
        db.session.flush()
        ticket.ticket_code = f'HD-{datetime.utcnow():%y%m}-{ticket.id:05d}'
        log_event(ticket, 'Ticket created')
        db.session.commit()
        flash(f'Ticket {ticket.ticket_code} was created.', 'success')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))
    return render_template('tickets/new.html', form=form)

@bp.route('/')
@login_required
def index():
    q = Ticket.query
    if current_user.role == 'employee': q = q.filter_by(requester_id=current_user.id)
    elif current_user.role == 'technician': q = q.filter_by(assignee_id=current_user.id)
    status = request.args.get('status')
    if status: q = q.filter_by(status=status)
    tickets = q.order_by(Ticket.updated_at.desc()).all()
    return render_template('tickets/index.html', tickets=tickets)

@bp.route('/<int:ticket_id>', methods=['GET','POST'])
@login_required
def detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not can_view(ticket): abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(body=form.body.data.strip(), user_id=current_user.id, ticket_id=ticket.id))
        log_event(ticket, 'Comment added')
        db.session.commit()
        flash('Comment added.', 'success')
        return redirect(url_for('tickets.detail', ticket_id=ticket.id))
    technicians = User.query.filter(User.role.in_(['technician','admin']), User.active.is_(True)).order_by(User.name).all()
    events = TicketEvent.query.filter_by(ticket_id=ticket.id).order_by(TicketEvent.created_at.desc()).all()
    return render_template('tickets/detail.html', ticket=ticket, form=form, technicians=technicians, events=events)

@bp.route('/<int:ticket_id>/update', methods=['POST'])
@login_required
def update(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role not in ['admin','technician'] or (current_user.role == 'technician' and ticket.assignee_id != current_user.id): abort(403)
    old_status = ticket.status
    new_status = request.form.get('status')
    if new_status in ['Open','In Progress','On Hold','Resolved','Closed'] and new_status != old_status:
        ticket.status = new_status
        log_event(ticket, f'Status changed from {old_status} to {new_status}')
    if current_user.role == 'admin':
        assignee_id = request.form.get('assignee_id')
        if assignee_id:
            person = User.query.filter(User.id == int(assignee_id), User.role.in_(['technician','admin'])).first()
            if person and ticket.assignee_id != person.id:
                ticket.assignee_id = person.id
                log_event(ticket, f'Assigned to {person.name}')
        priority = request.form.get('priority')
        if priority in ['Low','Medium','High','Critical']:
            ticket.priority = priority
    db.session.commit()
    flash('Ticket updated.', 'success')
    return redirect(url_for('tickets.detail', ticket_id=ticket.id))
