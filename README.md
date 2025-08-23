<p align="center">
<img src="https://placehold.co/800x250/3498db/ffffff?text=Hospital+Resource+Allocation+System" alt="Project Banner" />
</p>

<h1 align="center">Hospital Resource Allocation System 🏥</h1>

<p align="center">
A real-time, full-stack web application for the dynamic monitoring and management of critical hospital resources.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/SQLModel-0.0.18-orange?style=for-the-badge&logo=sqlmodel&logoColor=white" alt="SQLModel" />
<img src="https://img.shields.io/badge/Alembic-1.13.1-blueviolet?style=for-the-badge&logo=alembic&logoColor=white" alt="Alembic" />
<img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white" alt="JavaScript" />
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
</p>

🌟 Project Overview
In a fast-paced healthcare environment, efficient resource management is a life-saving necessity. The Hospital Resource Allocation System is a powerful full-stack solution designed to streamline hospital operations. It provides a real-time, dynamic dashboard for administrators to monitor resource availability, manage patient waiting lists, and track system activities with unparalleled ease. This application helps optimize decision-making and ensures that critical resources are allocated to patients who need them most.

✨ Key Features
Real-time Resource Dashboard: A clean and intuitive dashboard that provides a live view of vital resource availability, including beds, ICU units, ventilators, and oxygen cylinders. The data updates instantly via WebSockets, eliminating the need for manual refreshes.

Automated Patient Queue: Patients are automatically registered and placed on a waiting list. The system intelligently allocates resources to the next available patient, ensuring a fair and streamlined process.

Live Activity & Allocation Logs: A dynamic log feed provides a continuous stream of events as they occur, such as new patient registrations and resource allocations. This transparent logging ensures that administrators can track every action within the system.

Robust & Scalable Backend: Built on FastAPI, a high-performance Python web framework, the backend is asynchronous and robust, capable of handling multiple concurrent requests. It includes a WebSocket server for real-time communication.

Intuitive & Responsive Frontend: Developed using modern HTML, CSS, and vanilla JavaScript, the user interface is simple to navigate and responsive on all devices, providing a seamless user experience.

Dynamic Database Management: Utilizes SQLModel for a smooth, type-safe interaction with the database and Alembic for managing database migrations, ensuring the schema remains consistent as the project evolves.

📸 Demo & Screenshots
Dashboard Overview
Get a live look at all available resources and active patient allocations.
<img src="https://raw.githubusercontent.com/DeTraRoX/Hospital-Resource-Allocation-System/main/images/dashboard.png" alt="Dashboard Screenshot" />

Patient Registration
Register new patients with their details and resource requirements.
<img src="https://raw.githubusercontent.com/DeTraRoX/Hospital-Resource-Allocation-System/main/images/registration.png" alt="Patient Registration Form" />

Real-time Activity Log
Watch as events unfold with a live feed of patient registrations and resource allocations.
<img src="https://raw.githubusercontent.com/DeTraRoX/Hospital-Resource-Allocation-System/main/images/chart%26logs.png" alt="Real-time Activity Log" />

⚙️ Installation and Setup
Follow these steps to get the project up and running on your local machine.

1. Project Structure
Our project is organized for clarity and maintainability with a clean, logical file structure:

.
├── backend/
│   ├── app/
│   │   ├── routers/       # API endpoints (e.g., patients, allocations, resources)
│   │   ├── services/      # Business logic and helper functions
│   │   ├── db/            # Database connection, engine, and session management
│   │   ├── models.py      # SQLModel data models
│   │   ├── schemas.py     # Pydantic models for request/response validation
│   │   └── ws/            # WebSocket handlers for real-time communication
│   ├── alembic/           # Database migration scripts
│   ├── .env.example       # Template for environment variables
│   ├── main.py            # Main entry point for the FastAPI application
│   └── requirements.txt   # Project dependencies
├── .venv/                 # Python virtual environment
├── .gitignore             # Files ignored by Git
└── README.md              # Project information
2. Clone the Repository
Open your terminal and clone the project to your local machine:

Bash

git clone https://github.com/DeTraRoX/Hospital-Resource-Allocation-System.git
cd Hospital-Resource-Allocation-System
3. Set up the Python Virtual Environment
A virtual environment keeps project dependencies isolated.

Bash

python -m venv .venv
# Activate the virtual environment
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
4. Install Dependencies
Install all required packages from the requirements.txt file:

Bash

pip install -r backend/requirements.txt
5. Run the Application
Launch the FastAPI application using Uvicorn. The --reload flag enables live updates as you make changes to the code.

Bash

uvicorn main:app --reload
Open your web browser and navigate to http://127.0.0.1:8000 to view the live dashboard.

❤️ Contributing
We welcome contributions of all kinds! If you'd like to help improve this project, please feel free to:

Open an issue to report a bug or suggest a new feature.

Submit a pull request with your proposed changes.
