# Assetra : Enterprise Asset & Operations Management Platform

**Assetra** is a scalable enterprise-grade asset and operations management platform built to centralize organizational workflows including asset tracking, ticket management, user administration, organization control, and role-based access management.

Modern enterprises often rely on disconnected tools for managing assets, operational requests, employee access, and administrative workflows.
This fragmentation creates operational inefficiencies, poor visibility, inconsistent permission handling, and difficulties in scaling internal infrastructure systems.

Assetra solves this problem by introducing a **modular backend-driven operational ecosystem** that unifies enterprise asset management, RBAC workflows, ticket handling, and organizational operations into a single scalable platform.

Rather than functioning as a basic CRUD application, Assetra is designed as a **system-oriented backend infrastructure platform** engineered using layered architecture, modular feature separation, scalable database design, and production-grade backend engineering principles.

---

# Core Highlights

* **Enterprise Asset Management**
  Track, manage, assign, and monitor organizational assets efficiently.

* **Role-Based Access Control (RBAC)**
  Granular permission-driven workflows for administrators, managers, and employees.

* **Operational Ticketing System**
  Manage issue reporting, workflow tracking, and operational requests.

* **Organization Management**
  Supports enterprise organizational structures and user mapping.

* **Authentication & Authorization**
  JWT-based secure authentication workflows.

* **Feature-Based Modular Architecture**
  Scalable project organization with isolated business modules.

* **Audit-Oriented Design**
  Includes audit trail support for enterprise traceability.

* **Scalable Backend Engineering**
  Designed using production-ready FastAPI architecture patterns.

---

# System Design Philosophy

Assetra is engineered around how enterprise operational systems function in real-world environments.

Typical management systems focus only on:

* Managing users
* Storing asset information
* Basic CRUD operations

Assetra extends beyond that by implementing:

* **Permission-based operational workflows**
* **Role hierarchy management**
* **Organization-level isolation**
* **Ticket lifecycle handling**
* **Scalable feature modularization**
* **Service-repository architecture**
* **Audit-friendly backend design**
* **Enterprise-grade maintainability**

The platform is structured to simulate how modern IT operations and enterprise infrastructure systems function at scale.

---

# Tech Stack

| Category           | Technologies |
| ------------------ | ------------ |
| Backend Framework  | FastAPI      |
| Database           | PostgreSQL   |
| ORM                | SQLAlchemy   |
| Database Migration | Alembic      |
| Validation         | Pydantic     |
| Authentication     | JWT          |
| Package Management | Poetry / pip |
| API Testing        | Postman      |
| Language           | Python       |

---

# Project Structure

```bash
Assetra/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── main.py
│   │
│   ├── features/
│   │   ├── assets/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── auth/
│   │   │   ├── controller.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── organizations/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── role/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── permissions/
│   │   │   └── repository.py
│   │   │
│   │   ├── tickets/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── users/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── user_role/
│   │   │   ├── controllers.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   │
│   │   └── user_organization/
│   │       ├── controllers.py
│   │       ├── repository.py
│   │       └── schema.py
│   │
│   ├── models/
│   │   ├── asset.py
│   │   ├── asset_assignment.py
│   │   ├── asset_type.py
│   │   ├── organization.py
│   │   ├── permission.py
│   │   ├── role.py
│   │   ├── ticket.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── seed/
│   │   └── permission.py
│   │
│   └── utilities/
│       ├── audit_trail_mixin.py
│       ├── base.py
│       ├── config.py
│       ├── dependencies.py
│       └── enums.py
│
├── .env
├── alembic.ini
├── poetry.lock
├── pyproject.toml
├── run.py
└── README.md
```

---

# Core Modules

| Module                    | Description                                      |
| ------------------------- | ------------------------------------------------ |
| Authentication Module     | Handles login workflows and JWT token generation |
| User Management           | Manages employee accounts and operational users  |
| Organization Management   | Handles enterprise organizational structures     |
| Role Management           | Implements RBAC workflows and role assignment    |
| Permission Management     | Controls feature-level access permissions        |
| Asset Management          | Handles asset lifecycle and tracking             |
| Ticketing System          | Manages operational issues and workflow tickets  |
| User-Role Mapping         | Maps users with roles dynamically                |
| User-Organization Mapping | Supports organization-level access isolation     |

---

# Business Rules Enforced

* Users can only access features permitted by assigned roles
* Organizational data access is permission restricted
* Assets can be assigned and tracked systematically
* Ticket workflows maintain operational consistency
* Authentication-protected APIs enforce authorization validation
* Audit trail support ensures operational traceability
* Soft deletion patterns preserve enterprise data integrity

---

# Operational Workflow (Conceptual)

The operational workflow follows:

1. Super Admin creates organizations
2. Roles and permissions are configured
3. Users are onboarded into organizations
4. Assets are created and assigned
5. Employees interact with assigned resources
6. Operational issues generate tickets
7. Tickets move through workflow states
8. Admins monitor organizational operations

---

# Features

* JWT Authentication
* Role-Based Access Control (RBAC)
* Organization management
* Enterprise asset tracking
* Operational ticket management
* Permission handling
* Audit trail support
* Layered backend architecture
* Feature-based modular design
* RESTful API development
* PostgreSQL integration
* Structured exception handling
* Scalable repository-service architecture

---

# API Architecture

Assetra follows a **feature-oriented layered architecture**:

```text
Client Request
      ↓
FastAPI Controller Layer
      ↓
Service / Repository Layer
      ↓
SQLAlchemy ORM Layer
      ↓
PostgreSQL Database
```

This architecture ensures:

* Scalability
* Maintainability
* Separation of concerns
* Cleaner testing
* Independent module development
* Easier feature expansion

---

# Authentication Workflow

Assetra uses JWT-based authentication workflows:

```text
User Login
    ↓
JWT Token Generation
    ↓
Protected Route Access
    ↓
Permission Validation
    ↓
Authorized Resource Access
```

---

# Setup & Installation

## 1. Clone the Repository

```bash
git clone https://github.com/AmoghShukla/Assetra.git
cd Assetra
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 3. Install Dependencies

### Using pip

```bash
pip install -r requirements.txt
```

### Using Poetry

```bash
poetry install
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/assetra
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 5. Run Database Migrations

```bash
alembic upgrade head
```

---

## 6. Run the Application

```bash
uvicorn app.main:app --reload
```

---

# Example Enterprise Workflow

1. Super Admin creates an organization
2. Admin defines roles and permissions
3. Employees are onboarded
4. Assets are registered
5. Assets are assigned to users
6. Operational tickets are created
7. Tickets move through workflow stages
8. Admins monitor operational activity

---

# Future Enhancements

* Redis integration
* Refresh token workflows
* OTP/passwordless authentication
* WebSocket-based real-time updates
* Notification engine
* File upload support
* Audit logging dashboard
* Elasticsearch-powered searching
* Multi-tenant support
* Kubernetes deployment support
* CI/CD pipeline integration
* AI-powered ticket categorization

---

# Why Assetra?

Assetra is not just an asset management backend.

It is an attempt to engineer a scalable enterprise operational platform that reflects how modern organizations manage assets, permissions, workflows, and internal operations.

The project demonstrates:

* Backend system design
* RBAC implementation
* Scalable FastAPI architecture
* Enterprise workflow engineering
* Database modeling
* Feature-based architecture
* Service-repository patterns
* Production-oriented backend practices

---

# Contributing

1. Fork the repository
2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Commit your changes:

```bash
git commit -m "Add your feature"
```

4. Push to GitHub:

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

# License

This project is open source and available under the **MIT License**.

---

# Final Note

Assetra is designed to reflect how enterprise infrastructure systems operate internally —
from RBAC implementation and organizational control to asset lifecycle management and operational workflow handling.

The project focuses not only on functionality, but also on scalable backend engineering, modular system design, maintainability, and production-grade architectural practices.
