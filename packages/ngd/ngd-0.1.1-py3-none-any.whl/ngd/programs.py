# Dictionary to store all program texts
program_texts = {
    1: """PROGRAM1
-- Create the database
CREATE DATABASE HospitalDB;

-- Connect to the database
\c HospitalDB;

-- Create Patients table
CREATE TABLE Patients (
    PatientID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    AdmissionDate DATE
);

-- Create Doctors table
CREATE TABLE Doctors (
    DoctorID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Specialization VARCHAR(100),
    Experience INT
);

-- Insert into Patients
INSERT INTO Patients (Name, Age, Gender, AdmissionDate) VALUES
('John Doe', 25, 'Male', '2024-06-15'),
('Jane Smith', 40, 'Female', '2024-05-12'),
('Tom Hanks', 60, 'Male', '2024-06-15'),
('Alice Brown', 15, 'Female', '2024-04-10'),
('Bob Lee', 35, 'Male', '2024-06-13');

-- Insert into Doctors
INSERT INTO Doctors (Name, Specialization, Experience) VALUES
('Dr. Adam White', 'Cardiology', 12),
('Dr. Susan Clark', 'Neurology', 9),
('Dr. Max Payne', 'Orthopedics', 7),
('Dr. Emma Green', 'Cardiology', 5);

a) Fetch All Patient Details
SELECT * FROM Patients;
b) List Patients Admitted on a Specific Date ('2024-06-15')
SELECT * 
FROM Patients 
WHERE AdmissionDate = '2024-06-15';
c) List Patients by Age Group (Example: 0–18, 19–40, 41–60, 60+)
SELECT
    CASE
        WHEN Age <= 18 THEN '0-18'
        WHEN Age BETWEEN 19 AND 40 THEN '19-40'
        WHEN Age BETWEEN 41 AND 60 THEN '41-60'
        ELSE '60+'
    END AS AgeGroup,
    COUNT(*) AS PatientCount
FROM Patients
GROUP BY AgeGroup
ORDER BY AgeGroup;
d) Update Patient Details (Change Name for PatientID = 1)
UPDATE Patients
SET Name = 'Updated Name'
WHERE PatientID = 1;
e) List Doctors by Specialization ('Cardiology')
SELECT * 
FROM Doctors 
WHERE Specialization = 'Cardiology';
f) -- Create junction table
CREATE TABLE PatientDoctor (
    PatientID INT REFERENCES Patients(PatientID),
    DoctorID INT REFERENCES Doctors(DoctorID)
);

-- Sample assignments
INSERT INTO PatientDoctor (PatientID, DoctorID) VALUES
(1, 1), (2, 2), (3, 1), (4, 3), (5, 4);

-- Query for count
SELECT d.Name AS DoctorName, COUNT(pd.PatientID) AS PatientCount
FROM Doctors d
LEFT JOIN PatientDoctor pd ON d.DoctorID = pd.DoctorID
GROUP BY d.Name;
g)SELECT AVG(Experience) AS AverageExperience
FROM Doctors;

""",

    2: """program2

Use Fauxton or command line to insert sample documents. For command line:

bash
Copy
Edit
curl -X PUT http://localhost:5984/studentdb
Add a sample student:

bash
Copy
Edit
curl -X POST http://localhost:5984/studentdb \
-H "Content-Type: application/json" \
-d '{
  "_id": "5",
  "SRN": 5,
  "Sname": "Rahul",
  "Degree": "BCA",
  "Sem": 4,
  "CGPA": 7.0
}'
Add documents for students 6, 7, etc. similarly.

a) Display all the documents
CMD:
bash
Copy
Edit
curl -X GET "http://user:pass@localhost:5984/studentdb/_all_docs?include_docs=true"
Fauxton:
Open studentdb

Click "All Documents"

Enable Include Docs

b) Display all the students in BCA
This requires a view since Mango is not allowed.

1. Create a Design Document (_design/studentViews) in Fauxton
In Fauxton:

Go to studentdb → Design Documents → + New View

Name: studentViews

View name: by_degree

Map function:

javascript
Copy
Edit
function (doc) {
  if (doc.Degree === "BCA") {
    emit(doc.Sname, doc);
  }
}
Save the view.

CMD:
bash
Copy
Edit
curl "http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/by_degree?include_docs=true"
c) Display all the students in ascending order (e.g., by name)
Use a view sorted by name.

Fauxton Design Doc (studentViews) → View name: by_name
javascript
Copy
Edit
function (doc) {
  emit(doc.Sname, doc);
}
CMD:
bash
Copy
Edit
curl "http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/by_name?include_docs=true"

d) Display first 5 students
Use the view from (c) and limit the output.

CMD:
bash
Copy
Edit
curl "http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/by_name?include_docs=true&limit=5"

e) Display students 5, 6, 7 (by ID)
CMD:
bash
Copy
Edit
curl -X POST http://user:pass@localhost:5984/studentdb/_all_docs?include_docs=true \
-H "Content-Type: application/json" \
-d '{
  "keys": ["5", "6", "7"]
}'
Fauxton:
Go to "All Documents"

Search each document manually by ID 5, 6, 7

f) List the degree of student "Rahul"
Fetch by student name (if _id = name), or filter from a view.

If you stored Rahul under _id: "Rahul":

CMD:
bash
Copy
Edit
curl http://user:pass@localhost:5984/studentdb/Rahul
Otherwise, create a view:

javascript
Copy
Edit
function (doc) {
  if (doc.Sname === "Rahul") {
    emit(doc.Sname, doc.Degree);
  }
}
Then:

bash
Copy
Edit
curl http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/by_rahul

g) Display students 5, 6, 7 in descending order of percentage
Assuming percentage ≈ CGPA × 10.

In CouchDB, sort must be done in the view. Create a view:

javascript
Copy
Edit
function (doc) {
  if ([5,6,7].includes(doc.SRN)) {
    emit(doc.CGPA, doc);
  }
}
Then reverse sort:

CMD:
bash
Copy
Edit
curl "http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/by_cgpa?descending=true&include_docs=true"

h) Display all BCA students with CGPA > 6 but < 7.5
In view:

javascript
Copy
Edit
function (doc) {
  if (doc.Degree === "BCA" && doc.CGPA > 6 && doc.CGPA < 7.5) {
    emit(doc.Sname, doc);
  }
}
CMD:
bash
Copy
Edit
curl http://user:pass@localhost:5984/studentdb/_design/studentViews/_view/bca_cgpa_range?include_docs=true""",

    3: """PROGRAM 3:
1. Create Database
curl -X PUT http://localhost:5984/librarydb
2. Insert Book Documents
Example for inserting one document:
curl -X POST http://localhost:5984/librarydb -H "Content-Type: application/json" -d '{
  "ISBN": "9780141182636",
  "Title": "The Great Gatsby",
  "Author": "F. Scott Fitzgerald",
  "Genre": "Fiction",
  "PublicationYear": 1925,
  "CopiesAvailable": 5,
  "Rating": 4.3
}'

👉 Repeat for other books using their respective details (as in the PDF).
9780141182636 | The Great Gatsby | F. Scott Fitzgerald | Fiction | 1925 | Copies: 5 | Rating: 4.3 9780439139595 | Harry Potter and the Goblet of Fire | J.K. Rowling | Fantasy | 2000 | Copies: 8 | Rating: 4.8 9780451524935 | 1984 | George Orwell | Fiction | 1949 | Copies: 3 | Rating: 4.6 9780143127741 | Sapiens | Yuval Noah Harari | History | 2011 | Copies: 6 | Rating: 4.7 9780061120084 | To Kill a Mockingbird | Harper Lee | Fiction | 1960 | Copies: 7 | Rating: 4.9 9780307278449 | The Road | Cormac McCarthy | Fiction | 2006 | Copies: 4 | Rating: 4.1
a) Display all the documents
curl -X GET http://localhost:5984/librarydb/_all_docs?include_docs=true

b) Display all books in genre "Fiction"
curl -X PUT http://localhost:5984/librarydb/_design/genre -H "Content-Type: application/json" -d '{
  "views": {
    "fiction_books": {
      "map": "function(doc) { if(doc.Genre === 'Fiction') emit(doc.Title, doc); }"
    }
  }
}'

📄 Query it:
curl -X GET http://localhost:5984/librarydb/_design/genre/_view/fiction_books

c) Display books sorted by Title

curl -X PUT http://localhost:5984/librarydb/_design/sorted -H "Content-Type: application/json" -d '{
  "views": {
    "by_title": {
      "map": "function(doc) { emit(doc.Title, doc); }"
    }
  }
}'

📄 Query it:
curl -X GET http://localhost:5984/librarydb/_design/sorted/_view/by_title

d) Display first 3 books
curl -X GET "http://localhost:5984/librarydb/_design/sorted/_view/by_title?limit=3"
e) Display books 4, 5, and 6
curl -X GET "http://localhost:5984/librarydb/_design/sorted/_view/by_title?skip=3&limit=3"

f) List the author of the book titled "The Great Gatsby"
curl -X GET "http://localhost:5984/librarydb/_design/sorted/_view/by_title?key=\"The Great Gatsby\"&include_docs=true""",

    4: """PROGRAM4:
a. Create User Nodes

CREATE (:User {UserID: 1, Username: 'Alice'}),
       (:User {UserID: 2, Username: 'Bob'}),
       (:User {UserID: 3, Username: 'Jane'}),
       (:User {UserID: 4, Username: 'Tom'}),
       (:User {UserID: 5, Username: 'Mike'}),
       (:User {UserID: 6, Username: 'Sara'});

b. Create FOLLOWS Relationships

MATCH (a:User {Username: 'Jane'}), (b:User {Username: 'Alice'}) CREATE (a)-[:FOLLOWS]->(b);
MATCH (a:User {Username: 'Jane'}), (b:User {Username: 'Bob'}) CREATE (a)-[:FOLLOWS]->(b);
MATCH (a:User {Username: 'Mike'}), (b:User {Username: 'Alice'}) CREATE (a)-[:FOLLOWS]->(b);
MATCH (a:User {Username: 'Tom'}), (b:User {Username: 'Bob'}) CREATE (a)-[:FOLLOWS]->(b);
MATCH (a:User {Username: 'Sara'}), (b:User {Username: 'Alice'}) CREATE (a)-[:FOLLOWS]->(b);

a) Display All Users
MATCH (u:User)
RETURN u.UserID, u.Username;

b) Display Users Followed by "Jane"
MATCH (:User {Username: 'Jane'})-[:FOLLOWS]->(followed:User)
RETURN followed.Username;
c) Display All Users in Ascending Order by Username
MATCH (u:User)
RETURN u.Username
ORDER BY u.Username ASC;

d) Users Who Follow Both "Alice" and "Bob"
MATCH (u:User)-[:FOLLOWS]->(:User {Username: 'Alice'}),
      (u)-[:FOLLOWS]->(:User {Username: 'Bob'})
RETURN u.Username;

e) Users With the Most Number of Followers
MATCH (follower:User)-[:FOLLOWS]->(followed:User)
RETURN followed.Username, COUNT(follower) AS FollowerCount
ORDER BY FollowerCount DESC
LIMIT 1;

f) Display First 5 Users
MATCH (u:User)
RETURN u.Username
ORDER BY u.Username
LIMIT 5;""",

    5: """PROGRAM 5:

// Users
CREATE (:User {UserID: 1, Username: 'John'}),
       (:User {UserID: 2, Username: 'Alice'}),
       (:User {UserID: 3, Username: 'Bob'}),
       (:User {UserID: 4, Username: 'Jane'}),
       (:User {UserID: 5, Username: 'Mike'});

// Movies
CREATE (:Movie {MovieID: 101, Title: 'Inception'}),
       (:Movie {MovieID: 102, Title: 'The Matrix'}),
       (:Movie {MovieID: 103, Title: 'Interstellar'}),
       (:Movie {MovieID: 104, Title: 'The Dark Knight'}),
       (:Movie {MovieID: 105, Title: 'Titanic'});

// Likes
MATCH (u:User {Username: 'John'}), (m:Movie {Title: 'Inception'}) CREATE (u)-[:LIKES]->(m);
MATCH (u:User {Username: 'John'}), (m:Movie {Title: 'The Matrix'}) CREATE (u)-[:LIKES]->(m);
MATCH (u:User {Username: 'Alice'}), (m:Movie {Title: 'Inception'}) CREATE (u)-[:LIKES]->(m);
MATCH (u:User {Username: 'Bob'}), (m:Movie {Title: 'The Matrix'}) CREATE (u)-[:LIKES]->(m);
MATCH (u:User {Username: 'Jane'}), (m:Movie {Title: 'Titanic'}) CREATE (u)-[:LIKES]->(m);
MATCH (u:User {Username: 'Mike'}), (m:Movie {Title: 'Inception'}) CREATE (u)-[:LIKES]->(m);

a) Display All Movies Liked by User "John"

MATCH (:User {Username: 'John'})-[:LIKES]->(m:Movie)
RETURN m.Title;

b) Find All Users Who Like the Movie "Inception"

MATCH (u:User)-[:LIKES]->(:Movie {Title: 'Inception'})
RETURN u.Username;

c) Display All Movies in Ascending Order by Title

MATCH (m:Movie)
RETURN m.Title
ORDER BY m.Title ASC;

d) Users Who Like Both "The Matrix" and "Inception"

MATCH (u:User)-[:LIKES]->(:Movie {Title: 'The Matrix'}),
      (u)-[:LIKES]->(:Movie {Title: 'Inception'})
RETURN u.Username;

e) Most Liked Movie

MATCH (u:User)-[:LIKES]->(m:Movie)
RETURN m.Title, COUNT(u) AS Likes
ORDER BY Likes DESC
LIMIT 1;

f) Top 5 Users Who Like the Most Movies

MATCH (u:User)-[:LIKES]->(m:Movie)
RETURN u.Username, COUNT(m) AS TotalLikes
ORDER BY TotalLikes DESC
LIMIT 5;""",

    6: """Program 6:
      a) Insert Products using HSET

HSET product:101 Name "iPhone" Category "Electronics" Price 900
HSET product:102 Name "Refrigerator" Category "Appliances" Price 1200
HSET product:103 Name "Headphones" Category "Electronics" Price 600
🔹 b) Retrieve details of a specific product by ProductID

HGETALL product:101
🔹 c) Fetch all products belonging to a specific category (e.g., Electronics)
Redis doesn't support filtering inside hashes, so we need to maintain a manual index:

Add ProductIDs to a Set by Category:
1)

SADD category:Electronics 101 103
Retrieve members and then fetch product details:
2)

SMEMBERS category:Electronics
# Then:
HGETALL product:101
HGETALL product:103
🔹 d) List Products in a Price Range (500 - 1000)
Add ProductIDs to a Sorted Set, score = Price:

1)
ZADD priceIndex 900 101
ZADD priceIndex 1200 102
ZADD priceIndex 600 103
Query:
2)
ZRANGEBYSCORE priceIndex 500 1000
# Output: 101 103
Then:

3)
HGETALL product:101
HGETALL product:103
🔹 e) Update Product Price
Update the Price field in the hash:

HSET product:101 Price 950
Update the sorted set:

ZADD priceIndex 950 101
🔹 f) Delete a Product
Remove hash:


DEL product:101
Remove from category and price index:

SREM category:Electronics 101
ZREM priceIndex 101
""",

    7: """Program 7: a) Insert Employee Details into Redis

HSET employee:201 Name "Alice" Department "HR" Position "Manager" Salary 60000
HSET employee:202 Name "Bob" Department "Engineering" Position "Developer" Salary 80000
HSET employee:203 Name "Charlie" Department "HR" Position "Recruiter" Salary 45000
🔹 b) Retrieve All Employees in a Specific Department (e.g., "HR")
Redis can't filter hash fields directly, so you need to maintain a Set for each department:


SADD department:HR 201 203
SADD department:Engineering 202
Then to get all "HR" employees:


SMEMBERS department:HR
# Output: 201, 203

HGETALL employee:201
HGETALL employee:203
🔹 c) List Employees with Salary Above a Certain Amount (e.g., $50,000)
Use a Sorted Set where score = salary:


ZADD salaryIndex 60000 201
ZADD salaryIndex 80000 202
ZADD salaryIndex 45000 203
Then query:


ZRANGEBYSCORE salaryIndex 50001 +inf
# Output: 201, 202

HGETALL employee:201
HGETALL employee:202
🔹 d) Update an Employee's Position (e.g., change employee 202's position)

HSET employee:202 Position "Senior Developer" """
}

def print_program(program_number):
    """
    Print the text of a specific program.
    
    Args:
        program_number (int): The number of the program to print (1-7)
    """
    if program_number not in program_texts:
        print(f"Error: Program {program_number} not found. Available programs are 1-7.")
        return
    
    print(program_texts[program_number]) 