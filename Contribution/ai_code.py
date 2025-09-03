# Simple Flask Backend Demo for Students
# This shows how to receive and process user data from a web form

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store user data in memory (in real apps, you'd use a database)
users = []

# HTML form page - what students will see
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Registration Demo</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        form { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        input, select { width: 100%; padding: 8px; margin: 8px 0; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; }
        .users { margin-top: 20px; }
        .user-card { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🎓 Student Registration System</h1>
    
    <form id="studentForm">
        <h3>Register a New Student</h3>
        
        <label>Full Name:</label>
        <input type="text" id="name" placeholder="Enter student name" required>
        
        <label>Email:</label>
        <input type="email" id="email" placeholder="student@example.com" required>
        
        <label>Grade Level:</label>
        <select id="grade" required>
            <option value="">Select Grade</option>
            <option value="9">Grade 9</option>
            <option value="10">Grade 10</option>
            <option value="11">Grade 11</option>
            <option value="12">Grade 12</option>
        </select>
        
        <button type="submit">Register Student</button>
    </form>
    
    <div class="users" id="userList">
        <h3>📋 Registered Students</h3>
        <p>No students registered yet...</p>
    </div>

    <script>
        // Handle form submission
        document.getElementById('studentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Get form data
            const studentData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                grade: document.getElementById('grade').value
            };
            
            try {
                // Send data to our Python backend
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(studentData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('✅ Student registered successfully!');
                    document.getElementById('studentForm').reset();
                    loadStudents(); // Refresh the list
                } else {
                    alert('❌ Error: ' + result.error);
                }
            } catch (error) {
                alert('❌ Connection error: ' + error.message);
            }
        });
        
        // Load and display all registered students
        async function loadStudents() {
            try {
                const response = await fetch('/api/students');
                const students = await response.json();
                
                const userList = document.getElementById('userList');
                
                if (students.length === 0) {
                    userList.innerHTML = '<h3>📋 Registered Students</h3><p>No students registered yet...</p>';
                } else {
                    userList.innerHTML = '<h3>📋 Registered Students</h3>' +
                        students.map(student => `
                            <div class="user-card">
                                <strong>${student.name}</strong><br>
                                📧 ${student.email}<br>
                                📚 Grade ${student.grade}<br>
                                <small>ID: ${student.id}</small>
                            </div>
                        `).join('');
                }
            } catch (error) {
                console.error('Error loading students:', error);
            }
        }
        
        // Load students when page first loads
        loadStudents();
    </script>
</body>
</html>
"""

# Route 1: Serve the HTML form
@app.route('/')
def home():
    """Show the registration form to users"""
    return render_template_string(HTML_FORM)

# Route 2: API endpoint to receive student registration data
@app.route('/api/register', methods=['POST'])
def register_student():
    """
    This is where the magic happens! 🎯
    This endpoint receives JSON data from the frontend form
    """
    try:
        # Get the JSON data sent from the form
        student_data = request.get_json()
        
        # Validate that we have all required fields
        required_fields = ['name', 'email', 'grade']
        for field in required_fields:
            if not student_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if email is already registered
        for existing_student in users:
            if existing_student['email'] == student_data['email']:
                return jsonify({'error': 'Email already registered!'}), 400
        
        # Create a new student record
        new_student = {
            'id': len(users) + 1,  # Simple ID generation
            'name': student_data['name'],
            'email': student_data['email'],
            'grade': int(student_data['grade'])
        }
        
        # Add to our "database" (just a list in memory)
        users.append(new_student)
        
        print(f"✅ NEW STUDENT REGISTERED: {new_student}")  # Teacher can see this in terminal
        
        # Send success response back to frontend
        return jsonify({
            'message': 'Student registered successfully!',
            'student': new_student
        }), 201
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  # Debug info for teacher
        return jsonify({'error': 'Server error occurred'}), 500

# Route 3: API endpoint to get all registered students
@app.route('/api/students', methods=['GET'])
def get_students():
    """Return all registered students"""
    return jsonify(users)

# Route 4: API endpoint to get a specific student
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get one specific student by their ID"""
    student = next((s for s in users if s['id'] == student_id), None)
    
    if student:
        return jsonify(student)
    else:
        return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Student Registration System...")
    print("📖 Teaching Points for Students:")
    print("   • Form data → JSON → Python backend")
    print("   • POST request = sending data TO server")
    print("   • GET request = getting data FROM server")
    print("   • JSON = universal data format")
    print("   • Status codes: 200=OK, 400=Bad Request, 404=Not Found")
    print("\n🌐 Open http://localhost:5000 in your browser")
    
    app.run(debug=True, host='0.0.0.0', port=5000)