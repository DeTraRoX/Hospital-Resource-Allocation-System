<p align="center">
  <img src="https://placehold.co/800x250/3498db/ffffff?text=Hospital+Resource+Allocation+System" alt="Project Banner" />
</p>

<h1 align="center">🏥 Hospital Resource Allocation System</h1>

<p align="center">
  <em>A real-time, full-stack web application for dynamic monitoring and management of critical hospital resources.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLModel-0.0.18-orange?style=for-the-badge&logo=sqlmodel&logoColor=white" alt="SQLModel" />
  <img src="https://img.shields.io/badge/Alembic-1.13.1-blueviolet?style=for-the-badge&logo=alembic&logoColor=white" alt="Alembic" />
  <img src="https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/DeTraRoX/Hospital-Resource-Allocation-System/ci.yml?branch=main&style=for-the-badge&logo=github" alt="CI/CD Status" />
  <img src="https://img.shields.io/github/actions/workflow/status/DeTraRoX/Hospital-Resource-Allocation-System/tests.yml?label=tests&style=for-the-badge&logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/github/license/DeTraRoX/Hospital-Resource-Allocation-System?style=for-the-badge" alt="License" />
</p>

---

## 🌟 Overview
In today’s fast-paced healthcare environment, **efficient resource management** is a life-saving necessity.  
The **Hospital Resource Allocation System** is a robust full-stack solution that enables hospitals to:

- 📊 **Monitor** critical resources in real-time (beds, ICU units, ventilators, oxygen cylinders).  
- 🏥 **Manage** patient queues automatically and fairly.  
- 🔄 **Allocate** resources instantly using WebSockets for live updates.  
- 📜 **Track** every activity with transparent logging.  

This application empowers hospital administrators to make **data-driven, real-time decisions**, ensuring resources reach the patients who need them most.  

---

## ✨ Key Features
✅ **Real-time Resource Dashboard** – Live updates without refreshing, powered by WebSockets.  
✅ **Automated Patient Queue** – Intelligent resource allocation with fairness and transparency.  
✅ **Live Activity & Allocation Logs** – Continuous feed of events (registrations, allocations, releases).  
✅ **Scalable Backend** – Built with asynchronous FastAPI + SQLModel + Alembic.  
✅ **Responsive Frontend** – Clean, mobile-friendly interface with HTML, CSS, and JavaScript.  
✅ **Database Migrations** – Smooth schema evolution with Alembic.  
✅ **PostgreSQL Database** – Reliable, production-ready relational database.  

---

## 📸 Demo & Screenshots
- **Dashboard Overview** – Real-time hospital resources at a glance.  
- **Patient Registration** – Add new patients with resource requirements.  
- **Activity Log** – Live stream of hospital events.  

> *(Insert screenshots here once available)*  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DeTraRoX/Hospital-Resource-Allocation-System.git
cd Hospital-Resource-Allocation-System
2️⃣ Create a Virtual Environment
python -m venv .venv
# Activate the virtual environment
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r backend/requirements.txt

4️⃣ Run Database Migrations
alembic upgrade head

5️⃣ Start the Application
uvicorn backend.main:app --reload


➡ Open http://127.0.0.1:8000
 in your browser to access the live dashboard.

📂 Project Structure
.
├── backend/
│   ├── app/
│   │   ├── routers/       # API endpoints (patients, allocations, resources)
│   │   ├── services/      # Business logic and helpers
│   │   ├── db/            # Database connection & session management
│   │   ├── models.py      # SQLModel data models
│   │   ├── schemas.py     # Pydantic request/response validation
│   │   └── ws/            # WebSocket event handlers
│   ├── alembic/           # Database migration scripts
│   ├── .env.example       # Environment variable template
│   ├── main.py            # FastAPI app entry point
│   └── requirements.txt   # Dependencies
├── .venv/                 # Virtual environment
├── .gitignore             # Ignored files
└── README.md              # Project documentation

🤝 Contributing

We welcome contributions of all kinds!
Here’s how you can help:

🐛 Report Bugs – Open an issue.

💡 Suggest Features – Share your ideas.

🔧 Submit Pull Requests – Contribute directly to the codebase.

📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and distribute it.

<p align="center">🚑 Built with ❤️ to make hospital resource management faster, fairer, and more efficient.</p> ```
