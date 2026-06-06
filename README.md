# Assetra : Enterprise Asset & Operations Management Platform

**Assetra** is a scalable enterprise-grade asset and operations management platform designed to centralize organizational infrastructure workflows including asset tracking, ticket management, user administration, role-based access control, and operational governance.

Modern organizations often struggle with fragmented systems for managing IT assets, employee access, operational requests, and internal issue resolution.
These disconnected workflows lead to poor visibility, operational inefficiencies, inconsistent access control, and difficulties in maintaining scalable infrastructure processes.

Assetra solves this by introducing a **modular backend-driven management ecosystem** that consolidates asset lifecycle management, permission systems, operational ticketing, and administrative workflows into a unified architecture.

This is not just an inventory tracker or CRUD dashboard —
it is a **system-oriented enterprise operations platform** engineered using scalable backend architecture principles, domain-driven modularity, layered separation, and real-world RBAC workflows.

---

# Core Highlights

* **Enterprise Asset Management**
  Track and manage organizational assets throughout their lifecycle.

* **Role-Based Access Control (RBAC)**
  Granular permission handling for admins, managers, employees, and operational teams.

* **Operational Ticketing System**
  Manage issue reporting, task assignments, and operational workflows.

* **Organization & User Management**
  Supports multi-user enterprise structures with scalable user administration.

* **Authentication & Authorization**
  Secure access workflows using JWT authentication architecture.

* **Feature-Based Modular Architecture**
  Clean separation of business domains for scalability and maintainability.

* **Scalable Backend Infrastructure**
  Designed using production-oriented backend engineering practices.

* **Audit-Friendly System Design**
  Structured workflows for operational traceability and accountability.

---

# System Design Philosophy

Assetra is designed around how real enterprise systems operate internally.

Typical management systems only focus on:

* Storing asset data
* Managing users
* Basic CRUD operations

Assetra goes beyond that by implementing:

* **Permission-driven workflows**
* **Scalable organization management**
* **Operational ticket routing**
* **Structured RBAC architecture**
* **Business-rule enforcement**
* **Feature modularization**
* **Enterprise-grade backend layering**
* **Maintainable service-oriented architecture**

The platform is structured to simulate how enterprise IT operations and infrastructure management systems function in production environments.

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
| Caching / Sessions | Redis        |
| API Testing        | Postman      |
| Package Management | Poetry / pip |
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
│   ├── core/                    # Configuration & constants
│   ├── database/                # Database connection & session handling
│   ├── dependencies/            # Dependency injection utilities
│   ├── exceptions/              # Custom exception handlers
│   ├── middleware/              # Custom middleware components
│   ├── models/                  # SQLAlchemy ORM models
│   ├── modules/                 # Feature-based modules
│   │   ├── auth/
│   │   ├── users/
│   │   ├── organizations/
│   │   ├── roles/
│   │   ├── permissions/
│   │   ├── assets/
│   │   └── tickets/
│   │
│   ├── repositories/            # Database access layer
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic layer
│   ├── utilities/               # Utility/helper functions
│   └── websocket/               # Real-time communication layer
│
├── .env
├── alembic.ini
├── main.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

# Core Modules

| Module                   | Description                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| Authentication Module    | Handles JWT authentication, login workflows, and session management |
| User Management          | Manages employee accounts and user operations                       |
| Organization Management  | Supports organization-level structuring and administration          |
| Role & Permission System | Implements scalable RBAC workflows                                  |
| Asset Management         | Tracks and manages enterprise assets                                |
| Ticketing System         | Handles operational requests, issues, and workflow tracking         |
| Notification System      | Planned support for alerts and event-driven notifications           |
| Audit & Logging          | Maintains operational traceability and logs                         |

---

# Business Rules Enforced

* Users can only access features allowed by assigned roles
* Assets are mapped and managed under organizational structures
* Permission inheritance is enforced consistently across modules
* Operational tickets follow structured workflow states
* Soft deletion preserves audit integrity
* Authentication-protected routes enforce authorization validation
* Organizational boundaries isolate data access securely

---

# Asset Lifecycle Workflow (Conceptual)

The asset management workflow follows:

1. Admin creates organizational assets
2. Assets are categorized and assigned
3. Authorized users access asset records
4. Operational tickets can be raised against assets
5. Ticket workflows move through defined states
6. System maintains audit visibility for operations
7. Asset status updates dynamically based on workflow activity

---

# Features

* JWT-based authentication
* Role-based access control
* Multi-role permission handling
* Enterprise asset tracking
* Operational ticket management
* Organization management
* Feature-based architecture
* RESTful API design
* Structured exception handling
* PostgreSQL integration
* Scalable service layer
* Soft delete support
* Audit-ready workflows
* Redis integration support
* WebSocket-ready architecture

---

# API Architecture

Assetra follows a **layered feature-oriented backend architecture**:

```text
Client Request
      ↓
FastAPI Router Layer
      ↓
Service Layer (Business Logic)
      ↓
Repository Layer (Database Access)
      ↓
PostgreSQL Database
```

Each module maintains separation between:

* Routers
* Services
* Schemas
* Repositories
* Models
* Business rules

This architecture ensures:

* Scalability
* Cleaner maintenance
* Easier testing
* Better modularity
* Independent feature expansion
* Production-oriented engineering standards

---

# Authentication Architecture

Assetra uses JWT-based authentication workflows:

```text
User Login
    ↓
JWT Access Token Generation
    ↓
Protected API Access
    ↓
Role & Permission Validation
    ↓
Authorized Resource Access
```

Planned enhancements include:

* Refresh tokens
* OTP-based authentication
* Redis-backed token blacklisting
* Session tracking
* Multi-device login handling

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
REDIS_URL=redis://localhost:6379
```

---

## 5. Run Database Migrations

```bash
alembic upgrade head
```

---

## 6. Run the Application

```bash
uvicorn main:app --reload
```

---

# Example Operational Workflow

1. Super Admin creates organization
2. Admin configures roles & permissions
3. Employees are onboarded
4. Assets are registered into the system
5. Users interact with assigned assets
6. Operational issues generate tickets
7. Tickets move through workflow states
8. Admins monitor operational activities

---

# Future Enhancements

* OTP-based passwordless authentication
* Real-time updates using WebSockets
* Redis-based session invalidation
* Asset analytics dashboard
* AI-powered ticket categorization
* Email notification workflows
* Event-driven architecture integration
* Activity timeline tracking
* Multi-tenant organization isolation
* File attachment support
* Elasticsearch-based search system
* Kubernetes deployment support
* CI/CD pipeline integration

---

# Why Assetra?

Assetra is not just an asset management API.

It is an attempt to engineer a scalable backend system that reflects how real enterprise operational ecosystems function internally.

The project demonstrates:

* Backend system design
* RBAC implementation
* Enterprise architecture patterns
* Modular backend engineering
* Database modeling
* Operational workflow handling
* Scalable FastAPI architecture
* Clean service-repository separation

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

Assetra is built to simulate how modern enterprise infrastructure systems manage assets, permissions, operational workflows, and organizational processes at scale.

From RBAC implementation and modular backend architecture to scalable service layers and operational workflow management, the project is designed to reflect real-world backend engineering practices used in enterprise platforms.
