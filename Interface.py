import streamlit as st
import mysql.connector
from mysql.connector import Error

# MySQL Database Connection Function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Update with your MySQL host
            user="root",       # Update with your MySQL username
            password="Rahul@2002",  # Update with your MySQL password
            database="final_project"  # Update with your database name
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Insert Data into Recruiter Table
def insert_recruiter(contact_person, contact, company, company_profile):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Recruiter (ContactPerson, Contact, Company, CompanyProfile)
                VALUES (%s, %s, %s, %s)
            """, (contact_person, contact, company, company_profile))
            connection.commit()
            st.success("Recruiter added successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Insert Data into Job Table
def insert_job(location, date, experience, skills, title, contact_person, salary_range):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Job (Location, Date, Experience, Skills, Title, ContactPerson, SalaryRange)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (location, date, experience, skills, title, contact_person, salary_range))
            connection.commit()
            st.success("Job added successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Insert Data into Candidate Table
def insert_candidate(ed_level, gender, years_coded, country, previous_salary, skills):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Candidate (EdLevel, Gender, YearsCoded, Country, PreviousSalary, Skills)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ed_level, gender, years_coded, country, previous_salary, skills))
            connection.commit()
            st.success("Candidate added successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Streamlit App
st.title("Talent Acquisition Dashboard")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Add Recruiter", "Add Job", "Add Candidate", "View Data", "Complex Queries"])

if menu == "Add Recruiter":
    st.header("Add a New Recruiter")
    contact_person = st.text_input("Contact Person")
    contact = st.text_input("Contact")
    company = st.text_input("Company")
    company_profile = st.text_area("Company Profile")
    if st.button("Add Recruiter"):
        if contact_person and contact and company:
            insert_recruiter(contact_person, contact, company, company_profile)
        else:
            st.error("Please fill all required fields!")

elif menu == "Add Job":
    st.header("Add a New Job")
    location = st.text_input("Location")
    date = st.text_input("Date")
    experience = st.text_input("Experience")
    skills = st.text_area("Skills")
    title = st.text_input("Job Title")
    contact_person = st.text_input("Contact Person")
    salary_range = st.text_input("Salary Range")
    if st.button("Add Job"):
        if location and date and experience and title and contact_person:
            insert_job(location, date, experience, skills, title, contact_person, salary_range)
        else:
            st.error("Please fill all required fields!")

elif menu == "Add Candidate":
    st.header("Add a New Candidate")
    ed_level = st.text_input("Education Level")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    years_coded = st.number_input("Years Coded", min_value=0)
    country = st.text_input("Country")
    previous_salary = st.number_input("Previous Salary", min_value=0)
    skills = st.text_area("Skills")
    if st.button("Add Candidate"):
        if ed_level and gender and country:
            insert_candidate(ed_level, gender, years_coded, country, previous_salary, skills)
        else:
            st.error("Please fill all required fields!")

elif menu == "View Data":
    st.header("Data")
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            st.subheader("Recruiters")
            cursor.execute("SELECT * FROM Recruiter")
            recruiters = cursor.fetchall()
            st.write(recruiters)

            st.subheader("Jobs")
            cursor.execute("SELECT * FROM Job")
            jobs = cursor.fetchall()
            st.write(jobs)

            st.subheader("Candidates")
            cursor.execute("SELECT * FROM Candidate")
            candidates = cursor.fetchall()
            st.write(candidates)
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

elif menu == "Complex Queries":
    st.header("Run Complex Queries")
    query_option = st.selectbox(
        "Select a Query",
        [
            "Top 3 Most In-Demand Skills Across All Jobs",
            "Find Recruiters Posting Jobs in a Specific Location",
            "Find Jobs Offering Salary for a Specific Skill",
            "Jobs Available by Recruiter with a Minimum Experience Requirement",
            "Compute Mean Salary by Education Level"
        ]
    )

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)

        if query_option == "Top 3 Most In-Demand Skills Across All Jobs":
            st.subheader("Top 3 Most In-Demand Skills")
            try:
                cursor.execute("""
                    SELECT Skill, COUNT(*) AS SkillCount
                    FROM (
                        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(Skills, ',', n.n), ',', -1)) AS Skill
                        FROM Job
                        CROSS JOIN (
                            SELECT a.N + b.N * 10 + 1 AS n
                            FROM (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) a,
                                 (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) b
                            ORDER BY n
                        ) n
                        WHERE n.n <= 1 + (LENGTH(Skills) - LENGTH(REPLACE(Skills, ',', '')))
                    ) AS SkillList
                    GROUP BY Skill
                    ORDER BY SkillCount DESC
                    LIMIT 3;
                """)
                results = cursor.fetchall()
                st.write(results)
            except Exception as e:
                st.error(f"Error: {e}")
        
        elif query_option == "Find Recruiters Posting Jobs in a Specific Location":
            st.subheader("Recruiters Posting Jobs in a Specific Location")
            location = st.text_input("Enter Location (e.g., Amsterdam)")
            
            if location and st.button("Run Query"):
                connection = create_connection()
                if connection:
                    cursor = connection.cursor(dictionary=True)
                    try:
                        query = """
                            SELECT r.ContactPerson, r.Company, j.Title, j.Location
                            FROM Recruiter r
                            JOIN Job j ON r.ContactPerson = j.ContactPerson
                            WHERE j.Location = %s;
                        """
                        cursor.execute(query, (location,))
                        results = cursor.fetchall()
                        if results:
                            st.write(results)
                        else:
                            st.info(f"No jobs found in {location}.")
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif query_option == "Find Jobs Offering Salary for a Specific Skill":
            st.subheader("Jobs with Salary for a Skill")
            skill = st.text_input("Enter Skill (e.g., Python)")
            if st.button("Run Query"):
                try:
                    cursor.execute("""
                        SELECT Title, Location, SalaryRange, Skills
                        FROM Job
                        WHERE Skills LIKE %s
                        ORDER BY CAST(SUBSTRING_INDEX(SalaryRange, '-', -1) AS UNSIGNED) DESC
                        LIMIT 5;
                    """, (f"%{skill}%",))
                    results = cursor.fetchall()
                    st.write(results)
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif query_option == "Compute Mean Salary by Education Level":
            st.subheader("Mean Salary of Candidates by Education Level")
            
            # Dropdown for selecting the education level
            ed_level = st.selectbox("Select Education Level", ["Undergraduate", "Master", "PhD"])
            
            if st.button("Run Query"):
                connection = create_connection()
                if connection:
                    cursor = connection.cursor(dictionary=True)
                    try:
                        query = """
                            SELECT AVG(PreviousSalary) AS MeanSalary
                            FROM Candidate
                            WHERE EdLevel = %s;
                        """
                        cursor.execute(query, (ed_level,))
                        result = cursor.fetchone()
                        mean_salary = result["MeanSalary"]
                        
                        if mean_salary:
                            st.success(f"The mean salary for {ed_level} candidates is: ${mean_salary:.2f}")
                        else:
                            st.info(f"No {ed_level} candidates found in the database.")
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif query_option == "Jobs Available by Recruiter with a Minimum Experience Requirement":
            st.subheader("Jobs by Recruiter with Minimum Experience")
            min_experience = st.number_input("Enter Minimum Experience (in years)", min_value=0, step=1)
            if st.button("Run Query"):
                try:
                    cursor.execute("""
                        SELECT r.ContactPerson, r.Company, j.Title, j.Experience
                        FROM Recruiter r
                        JOIN Job j ON r.ContactPerson = j.ContactPerson
                        WHERE CAST(SUBSTRING_INDEX(Experience, ' ', 1) AS UNSIGNED) >= %s;
                    """, (min_experience,))
                    results = cursor.fetchall()
                    st.write(results)
                except Exception as e:
                    st.error(f"Error: {e}")

        cursor.close()
        connection.close()