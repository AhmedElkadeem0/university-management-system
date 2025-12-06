import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps # Helper to convert MongoDB BSON to JSON
from datetime import datetime
from bson.objectid import ObjectId
import re # For regular expressions

def merge_queries(existing_query, new_query):
    """Helper function to merge MongoDB queries using $and operator."""
    if not existing_query:
        return new_query
    return {"$and": [existing_query, new_query]}

def try_parse_int(value):
    """Try to parse value as integer, return None if not possible."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

load_dotenv()
app = Flask(__name__)
CORS(app)
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = "UniversityDB"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print(f"Successfully connected to MongoDB Atlas/local. Database collections: {db.list_collection_names()}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # You might want to exit or handle this error more gracefully in a production app
    exit(1)

# MOVE THESE ROUTES OUTSIDE THE EXCEPT BLOCK - FIX THE INDENTATION!

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "UniversityDB API is running successfully!"})
#=======================================================================================================================
#students#
@app.route('/api/students', methods=['GET'])
def get_students():
    """Fetches a list of students with filtering, sorting, pagination, and search capabilities."""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        # Filter parameters
        gpa_filter = request.args.get('gpaFilter')
        course_filter = request.args.get('course')
        status_filter = request.args.get('status')
        
        # Sorting
        sort_by = request.args.get('sortBy', 'student_id')
        sort_order = int(request.args.get('sortOrder', 1))
        
        # --- ENHANCED SEARCH PARAMETERS ---
        search_name = request.args.get('searchName')
        student_id_search = request.args.get('studentId')
        email_search = request.args.get('email')
        search_term = request.args.get('search')
        # ----------------------------------

        query = {}
        
        # Existing filters
        if gpa_filter:
            try:
                query['gpa'] = {'$gte': float(gpa_filter)}
            except ValueError:
                return jsonify({"message": "Invalid GPA filter value"}), 400
        
        if course_filter:
            query['courses_enrolled'] = course_filter
        
        if status_filter:
            if status_filter.lower() == 'active':
                query['is_active'] = True
            elif status_filter.lower() == 'inactive':
                query['is_active'] = False

        # --- ADD SEARCH CAPABILITIES ---
        
        # Exact Student ID Search
        if student_id_search:
            try:
                query['student_id'] = int(student_id_search)
            except ValueError:
                return jsonify({
                    "data": [], 
                    "page": page, 
                    "limit": limit, 
                    "totalResults": 0, 
                    "totalPages": 0
                }), 200

        # Email Search
        if email_search:
            email_query = {"email": {"$regex": email_search, "$options": "i"}}
            query = merge_queries(query, email_query)

        # Name Search (First name OR Last name)
        if search_name:
            search_regex = {"$regex": search_name, "$options": "i"} 
            name_query = {
                "$or": [
                    {"first_name": search_regex},
                    {"last_name": search_regex}
                ]
            }
            query = merge_queries(query, name_query)

        # General Search (across name, email, and student_id)
        if search_term:
            search_regex = {"$regex": search_term, "$options": "i"}
            general_search_query = {
                "$or": [
                    {"first_name": search_regex},
                    {"last_name": search_regex},
                    {"email": search_regex},
                    {"student_id": try_parse_int(search_term)},
                ]
            }
            general_search_query["$or"] = [item for item in general_search_query["$or"] if item is not None]
            query = merge_queries(query, general_search_query)

        # --- Execute Query ---
        total_students = db.students.count_documents(query)
        students_cursor = db.students.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        
        students_list = []
        for student in students_cursor:
            student['_id'] = str(student['_id'])
            students_list.append(student)
        
        return jsonify({
            "success": True,
            "data": students_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "totalResults": total_students,
                "totalPages": (total_students + limit - 1) // limit
            }
        }), 200

    except Exception as e:
        print(f"Error fetching students: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve students", 
            "error": str(e)
        }), 500
    

# POST route to create a new student
@app.route('/api/students', methods=['POST'])
def create_student():
    """Inserts a new student record into the database."""
    try:
        # Get the JSON data sent from the client
        student_data = request.json
        
        if not student_data:
            return jsonify({"message": "No data provided"}), 400

        # --- Required Field Validation ---
        required_fields = ['student_id', 'first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in student_data:
                return jsonify({"message": f"Missing required field: {field}"}), 400

        # --- Data Validation and Preprocessing ---
        # Ensure student_id is an integer and check for uniqueness
        if 'student_id' in student_data:
            try:
                student_data['student_id'] = int(student_data['student_id'])
            except ValueError:
                return jsonify({"message": "student_id must be a valid integer"}), 400
            
            # Check if student_id already exists
            existing_student = db.students.find_one({"student_id": student_data['student_id']})
            if existing_student:
                return jsonify({"message": "Student with this ID already exists"}), 409

        # Check if email already exists
        if 'email' in student_data:
            existing_email = db.students.find_one({"email": student_data['email']})
            if existing_email:
                return jsonify({"message": "Student with this email already exists"}), 409

        # Ensure enrollment_date is converted to a datetime object
        if 'enrollment_date' in student_data:
            if isinstance(student_data['enrollment_date'], str):
                try:
                    student_data['enrollment_date'] = datetime.strptime(student_data['enrollment_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            # Set default enrollment date to today
            student_data['enrollment_date'] = datetime.now()

        # Validate GPA range
        if 'gpa' in student_data:
            try:
                gpa = float(student_data['gpa'])
                if not (0.0 <= gpa <= 4.0):
                    return jsonify({"message": "GPA must be between 0.0 and 4.0"}), 400
                student_data['gpa'] = gpa
            except ValueError:
                return jsonify({"message": "GPA must be a valid number"}), 400
        else:
            student_data['gpa'] = 0.0

        # Ensure courses_enrolled is a list
        if 'courses_enrolled' not in student_data:
            student_data['courses_enrolled'] = []
        elif not isinstance(student_data['courses_enrolled'], list):
            return jsonify({"message": "courses_enrolled must be a list"}), 400

        # Set default is_active if not provided
        if 'is_active' not in student_data:
            student_data['is_active'] = True

        # --- MongoDB Insert ---
        result = db.students.insert_one(student_data)
        
        # Retrieve the newly inserted document to return it with the MongoDB _id
        new_student = db.students.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string for JSON serialization
        new_student['_id'] = str(new_student['_id'])
        
        return jsonify({
            "success": True,
            "message": "Student created successfully",
            "data": new_student
        }), 201  # 201 Created status code

    except Exception as e:
        print(f"Error creating student: {e}")
        return jsonify({"message": "Failed to create student record", "error": str(e)}), 500

# PUT route to update an existing student by ID
@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Updates a student record using flexible MongoDB operators."""
    try:
        # Check if the ID provided is a valid MongoDB ObjectId
        if not ObjectId.is_valid(student_id):
            return jsonify({"message": "Invalid student ID format"}), 400

        # Get the JSON data sent from the client
        update_data = request.json
        
        if not update_data:
            return jsonify({"message": "No update data provided"}), 400

        # Check if student exists first
        existing_student = db.students.find_one({"_id": ObjectId(student_id)})
        if not existing_student:
            return jsonify({"message": "Student not found"}), 404

        # --- Dynamic Update Query Construction ---
        mongo_update_query = {}

        # 1. Simple $set operations (for basic field changes)
        set_fields = {}
        for key, value in update_data.items():
            if key in ['first_name', 'last_name', 'email', 'gpa', 'is_active', 'enrollment_date']:
                # Perform validation and type conversion
                if key == 'gpa':
                    try:
                        gpa_value = float(value)
                        if not (0.0 <= gpa_value <= 4.0):
                            return jsonify({"message": "GPA must be between 0.0 and 4.0"}), 400
                        set_fields[key] = gpa_value
                    except ValueError:
                        return jsonify({"message": "GPA must be a valid number"}), 400
                
                elif key == 'email':
                    # Check for email uniqueness (excluding current student)
                    existing_email = db.students.find_one({
                        "email": value,
                        "_id": {"$ne": ObjectId(student_id)}
                    })
                    if existing_email:
                        return jsonify({"message": "Email already exists"}), 409
                    set_fields[key] = value
                
                elif key == 'is_active':
                    set_fields[key] = bool(value)
                
                elif key == 'enrollment_date':
                    if isinstance(value, str):
                        try:
                            set_fields[key] = datetime.strptime(value, '%Y-%m-%d')
                        except ValueError:
                            return jsonify({"message": "Invalid date format for enrollment_date. Use YYYY-MM-DD"}), 400
                    else:
                        set_fields[key] = value
                
                else:
                    set_fields[key] = value

        if set_fields:
            mongo_update_query['$set'] = set_fields

        # 2. Handle array operations more safely
        array_operations = {}
        
        # $push operations
        if '$push' in update_data:
            array_operations['$push'] = {}
            for field, value in update_data['$push'].items():
                if field == 'courses_enrolled':
                    # Ensure we're pushing to an array field
                    if not isinstance(value, list):
                        value = [value]
                    array_operations['$push'][field] = {"$each": value} # each for add multiple items
                else:
                    array_operations['$push'][field] = value

        # $pull operations
        if '$pull' in update_data:
            array_operations['$pull'] = {}
            for field, value in update_data['$pull'].items():
                if field == 'courses_enrolled':
                    if isinstance(value, list):
                        array_operations['$pull'][field] = {"$in": value}
                    else:
                        array_operations['$pull'][field] = value
                else:
                    array_operations['$pull'][field] = value

        # $addToSet operations (avoid duplicates)
        if '$addToSet' in update_data:
            array_operations['$addToSet'] = {}
            for field, value in update_data['$addToSet'].items():
                if field == 'courses_enrolled':
                    if not isinstance(value, list):
                        value = [value]
                    array_operations['$addToSet'][field] = {"$each": value}
                else:
                    array_operations['$addToSet'][field] = value

        # Merge array operations into main query
        for op, values in array_operations.items():
            if op not in mongo_update_query:
                mongo_update_query[op] = {}
            mongo_update_query[op].update(values)
    
        # 3. Numerical operations ($inc, $mul)
        for op in ['$inc', '$mul']:
            if op in update_data:
                numerical_ops = {}
                for key, value in update_data[op].items():
                    try:
                        numerical_ops[key] = float(value)
                    except ValueError:
                        return jsonify({"message": f"{op} values must be numerical"}), 400
                
                if op not in mongo_update_query:
                    mongo_update_query[op] = {}
                mongo_update_query[op].update(numerical_ops)

        # 4. Other MongoDB operators
        for op in ['$rename', '$unset', '$min', '$max', '$currentDate']:
            if op in update_data:
                mongo_update_query[op] = update_data[op]

        # --- Execute the Update ---
        if not mongo_update_query:
            return jsonify({"message": "No valid update operations provided"}), 400

        result = db.students.update_one(
            {"_id": ObjectId(student_id)},
            mongo_update_query
        )

        if result.matched_count == 0:
            return jsonify({"message": "Student not found"}), 404

        # Retrieve and return the updated document
        updated_student = db.students.find_one({"_id": ObjectId(student_id)})
        updated_student['_id'] = str(updated_student['_id'])

        return jsonify({
            "status": "success",
            "message": "Student updated successfully",
            "data": updated_student,
            "modifiedCount": result.modified_count
        }), 200

    except Exception as e:
        print(f"Error updating student: {e}")
        return jsonify({"message": "Failed to update student record", "error": str(e)}), 500


# DELETE route to remove a student by ID
@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Deletes a student record based on the MongoDB _id."""
    try:
        # 1. Validate the format of the student_id
        if not ObjectId.is_valid(student_id):
            return jsonify({
                "success": False,
                "message": "Invalid student ID format"
            }), 400

        # 2. Check if student exists first and get their info
        student = db.students.find_one({"_id": ObjectId(student_id)})
        if not student:
            return jsonify({
                "success": False,
                "message": "Student not found"
            }), 404

        # 3. Check for dependencies and log warning if enrolled in courses
        warning_message = None
        if student.get('courses_enrolled') and len(student['courses_enrolled']) > 0:
            warning_message = f"Student was enrolled in {len(student['courses_enrolled'])} courses"
            print(f"Warning: Deleting student {student_id} who is enrolled in courses: {student['courses_enrolled']}")

        # 4. Execute the delete operation
        result = db.students.delete_one({"_id": ObjectId(student_id)})

        # 5. Check the result
        if result.deleted_count == 0:
            return jsonify({
                "success": False,
                "message": "Student not found"
            }), 404

        # 6. Return success response with optional warning
        response_data = {
            "success": True,
            "message": "Student deleted successfully",
            "data": {
                "deleted_student": {
                    "student_id": student.get('student_id'),
                    "name": f"{student.get('first_name', '')} {student.get('last_name', '')}".strip(),
                    "email": student.get('email')
                }
            }
        }
        
        # Add warning to response if student was enrolled in courses
        if warning_message:
            response_data["warning"] = warning_message

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error deleting student: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to delete student record", 
            "error": str(e)
        }), 500  


#=======================================================================================================================

#instructors#
# GET route to fetch all instructors (basic Read)
@app.route('/api/instructors', methods=['GET'])
def get_instructors():
    """Fetches a list of all instructors with search, filtering, and pagination."""
    try:
        # --- 1. Get Query Parameters ---
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        # Filter parameters
        department_filter = request.args.get('department')
        min_salary = request.args.get('min_salary')
        max_salary = request.args.get('max_salary')
        course_taught = request.args.get('course_taught')
        
        # Sorting
        sort_by = request.args.get('sort_by', 'employee_id')
        sort_order = int(request.args.get('sort_order', 1))  # 1 = asc, -1 = desc
        
        # --- SEARCH PARAMETERS ---
        search_name = request.args.get('searchName')
        employee_id_search = request.args.get('employeeId')
        department_search = request.args.get('departmentSearch')
        search_term = request.args.get('search')
        # -------------------------

        # --- 2. Build the Filter/Query Dictionary ---
        query = {}
        
        # Department Filter (exact match)
        if department_filter:
            query['department'] = department_filter
        
        # Salary Range Filter
        if min_salary or max_salary:
            query['salary'] = {}
            if min_salary:
                try:
                    query['salary']['$gte'] = float(min_salary)
                except ValueError:
                    return jsonify({
                        "success": False,
                        "message": "Invalid min_salary value"
                    }), 400
            if max_salary:
                try:
                    query['salary']['$lte'] = float(max_salary)
                except ValueError:
                    return jsonify({
                        "success": False,
                        "message": "Invalid max_salary value"
                    }), 400
        
        # Course Taught Filter
        if course_taught:
            query['courses_taught'] = course_taught

        # --- SEARCH IMPLEMENTATIONS ---
        
        # Exact Employee ID Search
        if employee_id_search:
            try:
                query['employee_id'] = int(employee_id_search)
            except ValueError:
                # Return empty results for invalid ID
                return jsonify({
                    "success": True,
                    "data": [], 
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "totalResults": 0,
                        "totalPages": 0
                    }
                }), 200

        # Department Search (partial match)
        if department_search:
            department_query = {"department": {"$regex": department_search, "$options": "i"}}
            query = merge_queries(query, department_query)

        # Name Search (First name OR Last name)
        if search_name:
            search_regex = {"$regex": search_name, "$options": "i"} 
            name_query = {
                "$or": [
                    {"first_name": search_regex},
                    {"last_name": search_regex}
                ]
            }
            query = merge_queries(query, name_query)

        # General Search (across name, department, and employee_id)
        if search_term:
            search_regex = {"$regex": search_term, "$options": "i"}
            general_search_query = {
                "$or": [
                    {"first_name": search_regex},
                    {"last_name": search_regex},
                    {"department": search_regex},
                    {"employee_id": try_parse_int(search_term)},
                ]
            }
            general_search_query["$or"] = [item for item in general_search_query["$or"] if item is not None]
            query = merge_queries(query, general_search_query)

        # --- 3. Execute the Query ---
        total_instructors = db.instructors.count_documents(query)
        
        instructors_cursor = db.instructors.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        
        # Convert to proper JSON format
        instructors_list = []
        for instructor in instructors_cursor:
            instructor['_id'] = str(instructor['_id'])
            instructors_list.append(instructor)
        
        # --- 4. Return the Response ---
        return jsonify({
            "success": True,
            "data": instructors_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "totalResults": total_instructors,
                "totalPages": (total_instructors + limit - 1) // limit
            }
        }), 200

    except Exception as e:
        print(f"Error fetching instructors: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve instructors", 
            "error": str(e)
        }), 500

# POST route to create a new instructor
@app.route('/api/instructors', methods=['POST'])
def create_instructor():
    """Inserts a new instructor record with comprehensive validation."""
    try:
        instructor_data = request.json
        
        # Basic validation
        if not instructor_data:
            return jsonify({"message": "No data provided"}), 400

        # Required fields validation
        required_fields = ['employee_id', 'first_name', 'last_name', 'department']
        missing_fields = [field for field in required_fields if field not in instructor_data]
        if missing_fields:
            return jsonify({
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Employee ID validation and uniqueness check
        try:
            employee_id = int(instructor_data['employee_id'])
            instructor_data['employee_id'] = employee_id
        except (ValueError, TypeError):
            return jsonify({"message": "employee_id must be a valid integer"}), 400

        existing_employee = db.instructors.find_one({"employee_id": employee_id})
        if existing_employee:
            return jsonify({"message": "Instructor with this employee ID already exists"}), 409

        # Salary validation (optional field)
        if 'salary' in instructor_data:
            try:
                salary = float(instructor_data['salary'])
                if salary < 0:
                    return jsonify({"message": "Salary cannot be negative"}), 400
                instructor_data['salary'] = salary
            except (ValueError, TypeError):
                return jsonify({"message": "Salary must be a valid number"}), 400

        # Department validation (ensure it's a string)
        if not isinstance(instructor_data['department'], str):
            return jsonify({"message": "Department must be a string"}), 400

        # First name and last name validation
        if not isinstance(instructor_data['first_name'], str) or not instructor_data['first_name'].strip():
            return jsonify({"message": "First name must be a non-empty string"}), 400

        if not isinstance(instructor_data['last_name'], str) or not instructor_data['last_name'].strip():
            return jsonify({"message": "Last name must be a non-empty string"}), 400

        # Courses taught validation and initialization
        if 'courses_taught' in instructor_data:
            if not isinstance(instructor_data['courses_taught'], list):
                return jsonify({"message": "courses_taught must be a list"}), 400
            # Validate that all courses are strings
            for course in instructor_data['courses_taught']:
                if not isinstance(course, str):
                    return jsonify({"message": "All courses in courses_taught must be strings"}), 400
            # Remove any empty strings from the list
            instructor_data['courses_taught'] = [course for course in instructor_data['courses_taught'] if course.strip()]
        else:
            instructor_data['courses_taught'] = []

        # Insert into database
        result = db.instructors.insert_one(instructor_data)
        
        # Retrieve the newly created instructor
        new_instructor = db.instructors.find_one({"_id": result.inserted_id})
        new_instructor['_id'] = str(new_instructor['_id'])

        return jsonify({
            "success": True,
            "message": "Instructor created successfully",
            "data": new_instructor
        }), 201

    except Exception as e:
        print(f"Error creating instructor: {e}")
        return jsonify({
            "message": "Failed to create instructor record", 
            "error": str(e)
        }), 500

# PUT route to update an existing instructor by ID
@app.route('/api/instructors/<instructor_id>', methods=['PUT'])
def update_instructor(instructor_id):
    """Updates an instructor record, supporting salary change, course assignment, and field rename."""
    try:
        if not ObjectId.is_valid(instructor_id):
            return jsonify({"message": "Invalid instructor ID format"}), 400

        # Check if instructor exists first
        existing_instructor = db.instructors.find_one({"_id": ObjectId(instructor_id)})
        if not existing_instructor:
            return jsonify({"message": "Instructor not found"}), 404

        update_data = request.json
        if not update_data:
            return jsonify({"message": "No update data provided"}), 400

        mongo_update_query = {}

        # 1. Simple $set operations with validation
        set_fields = {}
        for key, value in update_data.items():
            if key in ['first_name', 'last_name', 'department', 'salary']:
                # Add validation for each field
                if key in ['first_name', 'last_name']:
                    if not isinstance(value, str) or not value.strip():
                        return jsonify({"message": f"{key} must be a non-empty string"}), 400
                    set_fields[key] = value.strip()
                
                elif key == 'department':
                    if not isinstance(value, str) or not value.strip():
                        return jsonify({"message": "Department must be a non-empty string"}), 400
                    set_fields[key] = value.strip()
                
                elif key == 'salary':
                    try:
                        salary_value = float(value)
                        if salary_value < 0:
                            return jsonify({"message": "Salary cannot be negative"}), 400
                        set_fields[key] = salary_value
                    except (ValueError, TypeError):
                        return jsonify({"message": "Salary must be a valid number"}), 400
        
        if set_fields:
            mongo_update_query['$set'] = set_fields

        # 2. Specific Instructor Operator Handling
        
        # Update Salary using $mul (for percentage raises)
        if 'salary_multiplier' in update_data:
            try:
                multiplier = float(update_data['salary_multiplier'])
                if multiplier <= 0:
                    return jsonify({"message": "Salary multiplier must be positive"}), 400
                mongo_update_query.setdefault('$mul', {})['salary'] = multiplier
            except ValueError:
                return jsonify({"message": "Salary multiplier must be a number"}), 400

        # Increment/Decrement Salary using $inc
        if 'salary_increment' in update_data:
            try:
                increment = float(update_data['salary_increment'])
                mongo_update_query.setdefault('$inc', {})['salary'] = increment
            except ValueError:
                return jsonify({"message": "Salary increment must be a number"}), 400

        # Assign Course using $addToSet (avoids duplicates)
        if 'assign_course' in update_data:
            course = update_data['assign_course']
            if not isinstance(course, str) or not course.strip():
                return jsonify({"message": "Course to assign must be a non-empty string"}), 400
            mongo_update_query.setdefault('$addToSet', {})['courses_taught'] = course.strip()

        # Assign Multiple Courses
        if 'assign_courses' in update_data:
            courses = update_data['assign_courses']
            if not isinstance(courses, list):
                return jsonify({"message": "assign_courses must be a list"}), 400
            
            valid_courses = [course.strip() for course in courses if isinstance(course, str) and course.strip()]
            if valid_courses:
                mongo_update_query.setdefault('$addToSet', {})['courses_taught'] = {'$each': valid_courses}

        # Remove Course using $pull
        if 'remove_course' in update_data:
            course = update_data['remove_course']
            if not isinstance(course, str) or not course.strip():
                return jsonify({"message": "Course to remove must be a non-empty string"}), 400
            mongo_update_query.setdefault('$pull', {})['courses_taught'] = course.strip()

        # Remove Multiple Courses
        if 'remove_courses' in update_data:
            courses = update_data['remove_courses']
            if not isinstance(courses, list):
                return jsonify({"message": "remove_courses must be a list"}), 400
            
            valid_courses = [course.strip() for course in courses if isinstance(course, str) and course.strip()]
            if valid_courses:
                mongo_update_query.setdefault('$pull', {})['courses_taught'] = {'$in': valid_courses}
            
        # Rename Field (e.g., department -> dept)
        if 'rename_field' in update_data and isinstance(update_data['rename_field'], dict):
            mongo_update_query.setdefault('$rename', {}).update(update_data['rename_field'])

        # Clear all courses
        if update_data.get('clear_courses') == True:
            mongo_update_query.setdefault('$set', {})['courses_taught'] = []

        # Direct MongoDB operators (for advanced users)
        for op in ['$inc', '$mul', '$rename', '$unset', '$push', '$pull', '$addToSet']:
            if op in update_data and op not in ['$set']:  # Avoid conflict with our $set logic
                if op in ['$inc', '$mul']:
                    # Validate numerical operations
                    for field, value in update_data[op].items():
                        try:
                            float(value)
                        except (ValueError, TypeError):
                            return jsonify({"message": f"{op} values must be numerical"}), 400
                
                if op not in mongo_update_query:
                    mongo_update_query[op] = {}
                mongo_update_query[op].update(update_data[op])

        if not mongo_update_query:
            return jsonify({"message": "No valid update operations provided"}), 400

        # Execute the Update
        result = db.instructors.update_one(
            {"_id": ObjectId(instructor_id)},
            mongo_update_query
        )

        if result.matched_count == 0:
            return jsonify({"message": "Instructor not found"}), 404

        # Return the updated document
        updated_instructor = db.instructors.find_one({"_id": ObjectId(instructor_id)})
        updated_instructor['_id'] = str(updated_instructor['_id'])

        return jsonify({
            "success": True,
            "message": "Instructor updated successfully", 
            "data": updated_instructor,
            "modifiedCount": result.modified_count
        }), 200

    except Exception as e:
        print(f"Error updating instructor: {e}")
        return jsonify({"message": "Failed to update instructor record", "error": str(e)}), 500
    
# DELETE route to remove an instructor by ID
@app.route('/api/instructors/<instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    """Deletes an instructor record based on the MongoDB _id."""
    try:
        if not ObjectId.is_valid(instructor_id):
            return jsonify({"message": "Invalid instructor ID format"}), 400

        result = db.instructors.delete_one({"_id": ObjectId(instructor_id)})

        if result.deleted_count == 0:
            return jsonify({"message": "Instructor not found"}), 404

        return ('', 204)

    except Exception as e:
        print(f"Error deleting instructor: {e}")
        return jsonify({"message": "Failed to delete instructor record", "error": str(e)}), 500
    

#=======================================================================================================================

#courses#

# GET route to fetch all courses with pagination and filtering
@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Fetches a list of all courses with optional pagination and filtering."""
    try:
        # Get query parameters with defaults
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        # Filter parameters
        instructor_filter = request.args.get('instructor_id')
        min_credits = request.args.get('min_credits')
        max_credits = request.args.get('max_credits')
        course_code_filter = request.args.get('course_code')
        department_filter = request.args.get('department')

        # Sorting
        sort_by = request.args.get('sort_by', 'course_code')
        sort_order = int(request.args.get('sort_order', 1))  # 1 = asc, -1 = desc

        # Build query
        query = {}
        
        if instructor_filter and ObjectId.is_valid(instructor_filter):
            query['instructor_id'] = ObjectId(instructor_filter)
        
        if course_code_filter:
            query['course_code'] = {"$regex": course_code_filter, "$options": "i"}  # case-insensitive
        
        if department_filter:
            query['course_code'] = {"$regex": f"^{department_filter}", "$options": "i"}  # courses starting with dept code
        
        # Credit hours range filter
        if min_credits or max_credits:
            query['credit_hours'] = {}
            if min_credits:
                query['credit_hours']['$gte'] = int(min_credits)
            if max_credits:
                query['credit_hours']['$lte'] = int(max_credits)

        # Get total count for pagination
        total_courses = db.courses.count_documents(query)

        # Execute query with pagination and sorting
        courses_cursor = db.courses.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)

        # Convert to list and handle ObjectId serialization
        courses_list = []
        for course in courses_cursor:
            course['_id'] = str(course['_id'])
            # Convert instructor_id to string if it exists
            if course.get('instructor_id'):
                course['instructor_id'] = str(course['instructor_id'])
            courses_list.append(course)

        return jsonify({
            "success": True,
            "data": courses_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_courses,
                "pages": (total_courses + limit - 1) // limit
            }
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": "Invalid parameter format",
            "error": str(e)
        }), 400
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve courses",
            "error": str(e)
        }), 500

# POST route to create a new course
@app.route('/api/courses', methods=['POST'])
def create_course():
    """Inserts a new course record with comprehensive validation."""
    try:
        course_data = request.json
        
        # Basic validation
        if not course_data:
            return jsonify({"message": "No data provided"}), 400

        # Required fields validation
        required_fields = ['course_code', 'title', 'credit_hours']
        missing_fields = [field for field in required_fields if field not in course_data]
        if missing_fields:
            return jsonify({
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Course code validation and uniqueness check
        course_code = course_data['course_code'].strip().upper()  # Normalize to uppercase
        if not course_code:
            return jsonify({"message": "Course code cannot be empty"}), 400
        
        # Check format (e.g., "CS101", "MA201")
        if not re.match(r'^[A-Z]{2,4}\d{3}$', course_code):
            return jsonify({
                "message": "Invalid course code format. Use format like: CS101, MA201"
            }), 400

        existing_course = db.courses.find_one({"course_code": course_code})
        if existing_course:
            return jsonify({"message": "Course with this code already exists"}), 409
        
        course_data['course_code'] = course_code

        # Title validation
        title = course_data['title'].strip()
        if not title:
            return jsonify({"message": "Course title cannot be empty"}), 400
        course_data['title'] = title

        # Description validation (optional field)
        if 'description' in course_data:
            description = course_data['description'].strip()
            if not description:
                return jsonify({"message": "Description cannot be empty if provided"}), 400
            course_data['description'] = description
        else:
            course_data['description'] = ""  # Default empty description

        # Credit hours validation
        try:
            credit_hours = int(course_data['credit_hours'])
            if credit_hours < 1 or credit_hours > 6:  # Reasonable range for credit hours
                return jsonify({"message": "Credit hours must be between 1 and 6"}), 400
            course_data['credit_hours'] = credit_hours
        except (ValueError, TypeError):
            return jsonify({"message": "credit_hours must be a valid integer"}), 400

        # Instructor validation (optional field)
        if 'instructor_id' in course_data:
            instructor_id = course_data['instructor_id']
            if not ObjectId.is_valid(instructor_id):
                return jsonify({"message": "Invalid instructor ID format"}), 400
            
            # Verify instructor exists
            instructor = db.instructors.find_one({"_id": ObjectId(instructor_id)})
            if not instructor:
                return jsonify({"message": "Instructor not found"}), 404
            
            course_data['instructor_id'] = ObjectId(instructor_id)

        # Insert into database
        result = db.courses.insert_one(course_data)
        
        # Retrieve the newly created course
        new_course = db.courses.find_one({"_id": result.inserted_id})
        new_course['_id'] = str(new_course['_id'])
        if new_course.get('instructor_id'):
            new_course['instructor_id'] = str(new_course['instructor_id'])

        return jsonify({
            "success": True,
            "message": "Course created successfully",
            "data": new_course
        }), 201

    except Exception as e:
        print(f"Error creating course: {e}")
        return jsonify({
            "message": "Failed to create course record", 
            "error": str(e)
        }), 500
    
# PUT route to update an existing course by ID
@app.route('/api/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    """Updates a course record with comprehensive validation."""
    try:
        if not ObjectId.is_valid(course_id):
            return jsonify({"message": "Invalid course ID format"}), 400

        # Check if course exists first
        existing_course = db.courses.find_one({"_id": ObjectId(course_id)})
        if not existing_course:
            return jsonify({"message": "Course not found"}), 404

        update_data = request.json
        if not update_data:
            return jsonify({"message": "No update data provided"}), 400

        mongo_update_query = {}

        # 1. Handle credit_hours update with validation
        if 'credit_hours' in update_data:
            try:
                new_hours = int(update_data['credit_hours'])
                if new_hours < 1 or new_hours > 6:
                    return jsonify({"message": "Credit hours must be between 1 and 6"}), 400
                mongo_update_query.setdefault('$set', {})['credit_hours'] = new_hours
            except ValueError:
                return jsonify({"message": "credit_hours must be a valid integer"}), 400

        # 2. Handle title update with validation
        if 'title' in update_data:
            title = update_data['title'].strip()
            if not title:
                return jsonify({"message": "Title cannot be empty"}), 400
            mongo_update_query.setdefault('$set', {})['title'] = title

        # 3. Handle description update
        if 'description' in update_data:
            description = update_data['description'].strip()
            mongo_update_query.setdefault('$set', {})['description'] = description

        # 4. Handle course_code update with validation
        if 'course_code' in update_data:
            course_code = update_data['course_code'].strip().upper()
            if not course_code:
                return jsonify({"message": "Course code cannot be empty"}), 400
            
            # Validate course code format
            if not re.match(r'^[A-Z]{2,4}\d{3}$', course_code):
                return jsonify({
                    "message": "Invalid course code format. Use format like: CS101, MA201"
                }), 400
            
            # Check for uniqueness (excluding current course)
            existing_code = db.courses.find_one({
                "course_code": course_code,
                "_id": {"$ne": ObjectId(course_id)}
            })
            if existing_code:
                return jsonify({"message": "Course code already exists"}), 409
            
            mongo_update_query.setdefault('$set', {})['course_code'] = course_code

        # 5. Handle instructor assignment/change
        if 'instructor_id' in update_data:
            instructor_id = update_data['instructor_id']
            
            if instructor_id is None:
                # Remove instructor assignment
                mongo_update_query.setdefault('$unset', {})['instructor_id'] = ""
            elif ObjectId.is_valid(instructor_id):
                # Verify instructor exists
                instructor = db.instructors.find_one({"_id": ObjectId(instructor_id)})
                if not instructor:
                    return jsonify({"message": "Instructor not found"}), 404
                
                mongo_update_query.setdefault('$set', {})['instructor_id'] = ObjectId(instructor_id)
            else:
                return jsonify({"message": "Invalid instructor ID format"}), 400

        # 6. Handle instructor removal specifically
        if update_data.get('remove_instructor') == True:
            mongo_update_query.setdefault('$unset', {})['instructor_id'] = ""

        # 7. Direct MongoDB operators support
        for op in ['$inc', '$mul', '$rename', '$unset']:
            if op in update_data:
                if op in ['$inc', '$mul']:
                    # Validate numerical operations
                    for field, value in update_data[op].items():
                        try:
                            float(value)
                        except (ValueError, TypeError):
                            return jsonify({"message": f"{op} values must be numerical"}), 400
                
                if op not in mongo_update_query:
                    mongo_update_query[op] = {}
                mongo_update_query[op].update(update_data[op])

        if not mongo_update_query:
            return jsonify({"message": "No valid update operations provided"}), 400

        # Execute the Update
        result = db.courses.update_one(
            {"_id": ObjectId(course_id)},
            mongo_update_query
        )

        if result.matched_count == 0:
            return jsonify({"message": "Course not found"}), 404

        # Return the updated document
        updated_course = db.courses.find_one({"_id": ObjectId(course_id)})
        updated_course['_id'] = str(updated_course['_id'])
        if updated_course.get('instructor_id'):
            updated_course['instructor_id'] = str(updated_course['instructor_id'])

        return jsonify({
            "success": True,
            "message": "Course updated successfully", 
            "data": updated_course,
            "modifiedCount": result.modified_count
        }), 200

    except Exception as e:
        print(f"Error updating course: {e}")
        return jsonify({"message": "Failed to update course record", "error": str(e)}), 500
    
# DELETE route to remove a course by ID
@app.route('/api/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Deletes a course record based on the MongoDB _id."""
    try:
        if not ObjectId.is_valid(course_id):
            return jsonify({"message": "Invalid course ID format"}), 400

        # Check if course exists first and get its info
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            return jsonify({"message": "Course not found"}), 404

        course_code = course.get('course_code')
        
        # Auto-remove course from students' enrolled courses
        db.students.update_many(
            {"courses_enrolled": course_code},
            {"$pull": {"courses_enrolled": course_code}}
        )

        # Auto-remove course from instructors' courses_taught
        db.instructors.update_many(
            {"courses_taught": course_code},
            {"$pull": {"courses_taught": course_code}}
        )

        # Execute the delete operation
        result = db.courses.delete_one({"_id": ObjectId(course_id)})

        if result.deleted_count == 0:
            return jsonify({"message": "Course not found"}), 404

        # Return success response with message
        return jsonify({
            "success": True,
            "message": "Course deleted successfully with automatic cleanup",
            "deleted_course": {
                "course_code": course_code,
                "title": course.get('title'),
                "credit_hours": course.get('credit_hours')
            }
        }), 200

    except Exception as e:
        print(f"Error deleting course: {e}")
        return jsonify({"message": "Failed to delete course record", "error": str(e)}), 500


# --- Run Application ---
if __name__ == '__main__':
    # Flask runs on port 3000 by default
    app.run(debug=True)