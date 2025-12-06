# 🎓 University Management System

A full-stack web application for managing university data including Students, Instructors, and Courses. Built with **Flask/MongoDB** backend and **Vue.js/Vuetify** frontend.

![University Management System](https://img.shields.io/badge/Vue.js-3.5-brightgreen) ![Flask](https://img.shields.io/badge/Flask-3.0-blue) ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green) ![License](https://img.shields.io/badge/license-MIT-orange)

---


---

## ✨ Features

### Backend (Flask REST API)
- ✅ **RESTful API** with full CRUD operations
- ✅ **MongoDB** integration with PyMongo
- ✅ **Advanced Search & Filtering** (regex-based, case-insensitive)
- ✅ **Pagination & Sorting** support
- ✅ **Data Validation** (email, GPA, course codes)
- ✅ **Auto-cleanup** on delete (referential integrity)
- ✅ **CORS** enabled for cross-origin requests

### Frontend (Vue.js + Vuetify)
- ✅ **Modern UI** with Vuetify Material Design
- ✅ **Responsive Design** (mobile-friendly)
- ✅ **Real-time Search** with debouncing
- ✅ **State Management** using Pinia
- ✅ **Form Validation** with error handling
- ✅ **Confirmation Dialogs** for destructive actions
- ✅ **Error Notifications** with snackbars
- ✅ **Beautiful Gradient Background** with animations

### Entities Managed
- 👨‍🎓 **Students** - ID, name, email, GPA, enrollment status
- 👨‍🏫 **Instructors** - Employee ID, name, department, salary, courses taught
- 📚 **Courses** - Course code, title, credits, instructor assignment

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vuetify 3** - Material Design component library
- **Pinia** - State management
- **Vue Router** - Navigation
- **Axios** - HTTP client
- **Vite** - Build tool

---

## 📦 Installation & Setup

### Prerequisites
- **Node.js** (v20.19.0 or higher)
- **Python** (v3.10 or higher)
- **MongoDB** (local or MongoDB Atlas)

---

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install flask flask-cors pymongo python-dotenv
   ```

4. **Create `.env` file:**
   ```bash
   MONGO_URI=mongodb://localhost:27017/
   # OR for MongoDB Atlas:
   # MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

5. **Run the server:**
   ```bash
   python app.py
   ```
   
   Backend will run on: `http://localhost:5000`

---

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd university-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will run on: `http://localhost:3000`

---

## 🚀 Usage

1. **Start MongoDB** (if using local):
   ```bash
   mongod
   ```

2. **Start Backend**:
   ```bash
   cd backend
   python app.py
   ```

3. **Start Frontend**:
   ```bash
   cd university-frontend
   npm run dev
   ```

4. **Open browser** and navigate to:
   ```
   http://localhost:3000
   ```

---

## 📁 Project Structure

```
university-management-system/
│
├── backend/
│   ├── app.py                 # Flask application & API endpoints
│   ├── .env                   # Environment variables (MongoDB URI)
│   └── requirements.txt       # Python dependencies
│
├── university-frontend/
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   │   ├── layout/        # NavBar, SideBar
│   │   │   ├── ConfirmModal.vue
│   │   │   ├── Pagination.vue
│   │   │   ├── SearchFilters.vue
│   │   │   ├── StatCard.vue
│   │   │   ├── StudentFormModal.vue
│   │   │   ├── InstructorFormModal.vue
│   │   │   └── CourseFormModal.vue
│   │   │
│   │   ├── views/             # Page components
│   │   │   ├── Dashboard.vue
│   │   │   ├── StudentsView.vue
│   │   │   ├── InstructorsView.vue
│   │   │   └── CoursesView.vue
│   │   │
│   │   ├── stores/            # Pinia state management
│   │   │   ├── students.js
│   │   │   ├── instructors.js
│   │   │   ├── courses.js
│   │   │   └── sidebar.js
│   │   │
│   │   ├── services/          # API communication
│   │   │   └── api.js
│   │   │
│   │   ├── router/            # Vue Router configuration
│   │   │   └── index.js
│   │   │
│   │   ├── App.vue            # Root component
│   │   ├── main.js            # Application entry point
│   │   └── index.css          # Global styles
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
│
└── README.md
```

---

## 🔌 API Endpoints

### Students
- `GET    /api/students` - Get all students (with filters)
- `POST   /api/students` - Create new student
- `PUT    /api/students/:id` - Update student
- `DELETE /api/students/:id` - Delete student

### Instructors
- `GET    /api/instructors` - Get all instructors
- `POST   /api/instructors` - Create new instructor
- `PUT    /api/instructors/:id` - Update instructor
- `DELETE /api/instructors/:id` - Delete instructor

### Courses
- `GET    /api/courses` - Get all courses
- `POST   /api/courses` - Create new course
- `PUT    /api/courses/:id` - Update course
- `DELETE /api/courses/:id` - Delete course

---

## 🎨 Key Features Showcase

### 1. **Dashboard Overview**
- Real-time statistics
- Recent students list
- Quick action buttons
- Top courses display

### 2. **Advanced Search & Filters**
- Quick search across all fields
- GPA filtering
- Status filtering (Active/Inactive)
- Department filtering

### 3. **Data Tables**
- Sortable columns
- Pagination support
- Loading states
- Empty states
- Color-coded chips (GPA, Status)

### 4. **Form Validation**
- Real-time validation
- Email format checking
- GPA range validation (0.0-4.0)
- Course code format validation
- Unique ID checking

### 5. **Confirmation Dialogs**
- Delete confirmations
- Warning messages
- Auto-cleanup notifications

---

## 🧪 Testing

### Test Data
Sample students, instructors, and courses are automatically seeded on first run.

### Manual Testing
1. Create a new student
2. Search for students by name
3. Filter students by GPA
4. Edit student information
5. Delete a student (observe confirmation)
6. Check Dashboard updates

---

## 🚧 Future Enhancements

- [ ] User authentication (JWT)
- [ ] Role-based access control
- [ ] File upload for student photos
- [ ] Export data to CSV/PDF
- [ ] Email notifications
- [ ] Course enrollment system
- [ ] Grade management
- [ ] Attendance tracking
- [ ] Dark/Light theme toggle
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@AhmedElkadeem0](https://github.com/AhmedElkadeem0)
- Email: ahmed.320230052@ejust.edu.eg

---

## 🙏 Acknowledgments

- Vue.js team for the amazing framework
- Vuetify team for the beautiful UI components
- MongoDB team for the flexible database
- Flask team for the lightweight web framework

---

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

**⭐ If you found this project helpful, please give it a star!**