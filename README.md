# ResolveDesk — IT Helpdesk & Incident Management System

A Flask-based academic project for centralized IT issue reporting, ticket assignment, progress tracking, comments, audit history and dashboard analytics.

## Included features

- Employee registration and secure password hashing
- Role-aware accounts: employee, technician and admin
- Ticket creation with category and priority
- Ticket lists, status filtering and ticket detail pages
- Technician/admin status updates; admin assignment and priority management
- Ticket comments and activity history
- Role-filtered dashboard metrics and Chart.js status chart
- Admin user directory
- CSRF protection on forms
- SQLite for immediate local startup; PostgreSQL through `DATABASE_URL`

## Requirements

- Python 3.10+
- PostgreSQL 14+ (optional for first local run; SQLite is configured by default)

## Run on Windows

Open PowerShell or the VS Code terminal in this folder:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Open http://127.0.0.1:5000. The database tables are created automatically on first start.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again. You can also use Command Prompt with `.venv\Scripts\activate.bat`.

## Create the first administrator

After installing dependencies, run:

```bash
flask --app run.py create-admin
```

The command prompts for name, email and password. Use this administrator account to promote registered users to technician/admin roles in the database. For this starter release, role promotion is performed directly in PostgreSQL/SQLite; a full admin role-management screen is a planned extension.

## PostgreSQL configuration

Create a database and user in PostgreSQL, then set `DATABASE_URL` in `.env`:

```env
DATABASE_URL=postgresql+psycopg://helpdesk_user:your_password@localhost:5432/it_helpdesk
SECRET_KEY=use-a-long-random-secret
```

Restart the application. SQLAlchemy will create tables automatically. Do not commit `.env` or real credentials.

## Promote an employee to technician/admin

Use pgAdmin Query Tool (replace email and role):

```sql
UPDATE "user" SET role = 'technician' WHERE email = 'tech@example.com';
UPDATE "user" SET role = 'admin' WHERE email = 'admin@example.com';
```

Allowed roles: `employee`, `technician`, `admin`.

## Project structure

```text
app/
  __init__.py        Flask application factory
  auth.py            Login, registration and logout
  forms.py           Validated WTForms
  main.py            Dashboard and user directory
  models.py          SQLAlchemy models
  tickets.py         Ticket workflows
  templates/         Jinja2 pages
  static/            CSS and JavaScript
config.py
run.py
requirements.txt
```

## Important notes / next development increments

This is a functional MVP foundation, not a production-certified service desk. Before production use, add email notifications, attachment scanning/storage, pagination, stronger account lifecycle controls, database migrations, rate limiting, audit retention policy, automated backups, SLA policy configuration and deployment-specific persistent PostgreSQL. Vercel serverless deployments require an external PostgreSQL database and production secret; do not use local SQLite for serverless persistence.

## Academic project testing ideas

1. Register an employee and sign in.
2. Submit tickets with each priority and category.
3. Confirm an employee only sees their own tickets.
4. Promote a second account to technician and assign a ticket.
5. Confirm the technician can update only assigned tickets.
6. Confirm the administrator can assign tickets and change priority.
7. Add comments and verify activity history.
8. Confirm dashboard counts change with ticket status.

## License

Created as an educational project starter. Adapt the content and add your own evaluation evidence before academic submission.
