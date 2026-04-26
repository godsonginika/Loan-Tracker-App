# 💰 Loan Tracker Application

A full-featured personal loan and debt tracking web application built with Django. Keep track of money you've lent out or borrowed, record repayments, and monitor outstanding balances — all in one place.

---

## 📸 Features

- **Authentication** — Register, login and logout securely
- **Contacts** — Manage people you lend to or borrow from
- **Loans** — Record loans with direction (lent/borrowed), interest rate, loan date and due date
- **Payments** — Track repayments against each loan
- **Auto Status** — Loans automatically update to overdue or paid based on due date and balance
- **Dashboard** — Summary of total lent, borrowed, active loans and overdue alerts
- **Loan History** — Paid off loans are separated from active ones
- **Overpayment Protection** — Prevents recording a payment greater than the remaining balance
- **Security** — Every user can only access their own data

---

## 🛠️ Tech Stack

- **Backend** — Python, Django
- **Database** — PostgreSQL
- **Frontend** — Bootstrap 5, custom CSS
- **Authentication** — Django built-in auth system
- **Environment** — python-decouple for managing secrets

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/loan-tracker.git
   cd loan-tracker
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with the following:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. Visit `http://127.0.0.1:8000` in your browser

---

## 📁 Project Structure

```
loan_tracker/
├── loan_tracker/        ← Project settings and URLs
├── loans/               ← Main app
│   ├── models.py        ← Contact, Loan, Payment models
│   ├── views.py         ← Class-based views
│   ├── forms.py         ← ModelForms with validation
│   └── urls.py          ← App URL patterns
├── templates/
│   ├── base.html        ← Base layout with sidebar
│   ├── registration/    ← Login template
│   └── loans/           ← All app templates
├── static/
│   └── css/
│       └── style.css    ← Custom styles
├── .env                 ← Environment variables (not committed)
├── .gitignore
└── manage.py
```

---

## 📊 Models

### Contact
Represents a person you lend to or borrow from. Linked to the logged in user.

### Loan
Records a loan with the following key fields:
- `direction` — whether you lent or borrowed the money
- `principal` — the original loan amount
- `interest_rate` — annual interest rate (%)
- `loan_date` — the actual date the loan was made
- `duration` and `duration_type` — used to auto-calculate the due date
- `due_date` — auto-calculated from duration or set manually
- `status` — active, overdue, or paid (auto-managed)

### Payment
Records a repayment against a loan. Automatically marks the loan as paid when the balance reaches zero.

---

## 🔒 Security

- All views are protected with `LoginRequiredMixin`
- Users can only access their own data through `owner=request.user` filtering
- CSRF protection enabled on all forms
- Sensitive settings managed through environment variables

---

## 🧠 What I Learned

This project was built to reinforce Django fundamentals including:

- Django project and app structure
- Model design and relationships with ForeignKey
- Django ORM for querying and aggregating data
- Class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- ModelForms with custom validation
- Django authentication system
- Template inheritance with `{% extends %}` and `{% block %}`
- URL routing with named URLs
- Business logic in models using custom methods
- Environment variable management with python-decouple
- PostgreSQL integration with Django

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
