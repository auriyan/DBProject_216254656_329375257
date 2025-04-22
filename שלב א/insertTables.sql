-- insertTables.sql

-- Customers
INSERT INTO customer (customer_id, name, phone) VALUES (1, 'דנה כהן', '0521234567');
INSERT INTO customer (customer_id, name, phone) VALUES (2, 'יואב לוי', '0547654321');
INSERT INTO customer (customer_id, name, phone) VALUES (3, 'נועה ישראלי', '0532223344');
INSERT INTO customer (customer_id, name, phone) VALUES (4, 'עידן שלמה', '0509998888');

-- Employees
INSERT INTO employee (employee_id, name, hire_date) VALUES (100, 'תמר אוחיון', TO_DATE('2020-05-10', 'YYYY-MM-DD'));
INSERT INTO employee (employee_id, name, hire_date) VALUES (101, 'רן רפאלי', TO_DATE('2021-11-20', 'YYYY-MM-DD'));
INSERT INTO employee (employee_id, name, hire_date) VALUES (102, 'עדי ברק', TO_DATE('2022-07-01', 'YYYY-MM-DD'));

-- Instructors
INSERT INTO instructor (instructor_id, license_number) VALUES (100, 'IN123');
INSERT INTO instructor (instructor_id, license_number) VALUES (102, 'IN456');

-- Cashiers
INSERT INTO cashier (cashier_id, register_number) VALUES (101, 4);

-- Equipment
INSERT INTO equipment (equipment_id, type, size) VALUES (1, 'סקי', 'M');
INSERT INTO equipment (equipment_id, type, size) VALUES (2, 'מקלות', 'L');
INSERT INTO equipment (equipment_id, type, size) VALUES (3, 'קסדה', 'S');
INSERT INTO equipment (equipment_id, type, size) VALUES (4, 'נעליים', 'M');

-- Lessons
INSERT INTO lesson (lesson_id, lesson_date, duration, instructor_id) 
VALUES (10, TO_DATE('2025-01-10', 'YYYY-MM-DD'), 60, 100);
INSERT INTO lesson (lesson_id, lesson_date, duration, instructor_id) 
VALUES (11, TO_DATE('2025-01-12', 'YYYY-MM-DD'), 90, 102);

-- Rentals
INSERT INTO rental (rental_id, rental_date, return_date, customer_id, cashier_id) 
VALUES (200, TO_DATE('2025-01-09', 'YYYY-MM-DD'), TO_DATE('2025-01-11', 'YYYY-MM-DD'), 1, 101);
INSERT INTO rental (rental_id, rental_date, return_date, customer_id, cashier_id) 
VALUES (201, TO_DATE('2025-01-10', 'YYYY-MM-DD'), TO_DATE('2025-01-12', 'YYYY-MM-DD'), 2, 101);

-- Payments
INSERT INTO payment (payment_id, amount, payment_date, rental_id) 
VALUES (300, 250.00, TO_DATE('2025-01-09', 'YYYY-MM-DD'), 200);
INSERT INTO payment (payment_id, amount, payment_date, rental_id) 
VALUES (301, 180.00, TO_DATE('2025-01-10', 'YYYY-MM-DD'), 201);

-- Lesson Participants
INSERT INTO lesson_participants (customer_id, lesson_id) VALUES (1, 10);
INSERT INTO lesson_participants (customer_id, lesson_id) VALUES (2, 10);
INSERT INTO lesson_participants (customer_id, lesson_id) VALUES (3, 11);

-- Rental Equipment
INSERT INTO rental_equipment (rental_id, equipment_id) VALUES (200, 1);
INSERT INTO rental_equipment (rental_id, equipment_id) VALUES (200, 2);
INSERT INTO rental_equipment (rental_id, equipment_id) VALUES (201, 3);
INSERT INTO rental_equipment (rental_id, equipment_id) VALUES (201, 4);
