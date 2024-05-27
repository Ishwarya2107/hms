#use this file for creating the following:
#1.creating connection
#2.creating database
#3.creating table
#4.describe table

from mysql.connector import connect, Error
insert_into_user = """
INSERT INTO details_of_users (name, age, address, occupation, city, contact, password, gender)
VALUES ('John Doe', 30, '123 Main St', 'Engineer', 'New York', 1234567890, 'password123', 'Male');

"""
show_data = """
        select * from details_of_users
"""
show_table_query = """
        describe user_details
"""
create_table_query = """
    create table details_of_users(
    
    name varchar(100),
    age int, 
    address varchar(500),
    occupation varchar(100),
    city varchar(100),
    contact bigint,
    password varchar(100) primary key,
    gender varchar(100)
    )

"""
create_doctors = """
create table doctors(
doc_name varchar(100),
body_part varchar(100),
hospital varchar(100)
)
"""
create_appointment_request_table = """
CREATE TABLE appointments_requests (
    id int auto_increment primary key,
    user_id varchar(100),
    doc_name varchar(100),
    name varchar(100),
    age int, 
    gender varchar(100),
    description varchar(500),
    bodypart varchar(100),
    location varchar(100),
    timings time,
    dates date,
    hos_name varchar(100)
);
"""
create_hospital_table = """
create table hospitals(
name varchar(100) primary key,
location varchar(100)
)
"""
insert_hospitals = """
INSERT INTO hospitals (name, location)
VALUES 
    ('PSG hospital', 'cbe'),
    ('HEM hospital', 'chennai'),
    ('GKNMH', 'salem');
"""
insert_doctors = """
insert into doctors(doc_name,body_part,hospital)
values
('Peter','stomach','PSG Hospital'),
('Adam','leg','HEM hospital'),
('William','head','GKNMH');
"""

try:
    with connect(
        host="localhost",
        user="root",
        password="ish21072004#",
        database = "hms"
    ) as connection:
         
         with connection.cursor() as cursor:
            
            cursor.execute(create_appointment_request_table
                           )
            connection.commit()
            # cursor.execute('select name,age,gender,description from appointments_requests where doc_name = William')
                    
          
            
            result = cursor.fetchall()
            
            for row in result:
                print(row)

 

  
   
   
       
        
except Error as e:
    print(e)