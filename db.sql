-- Create Database
CREATE DATABASE CulinaryAI;
USE CulinaryAI;

-- Users Table (Admins & Workers)
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Worker') NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu Table (Food Items)
CREATE TABLE Menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    availability BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255)
);

-- Orders Table
CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('Pending', 'In Progress', 'Completed', 'Canceled') DEFAULT 'Pending',
    total_price DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash', 'Card', 'Online') DEFAULT 'Cash',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Order Items Table (Each order contains multiple menu items)
CREATE TABLE OrderItems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_id INT NOT NULL,
    quantity INT NOT NULL,
    special_request TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES Menu(id) ON DELETE CASCADE
);

-- Reservations Table
CREATE TABLE Reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    reservation_time DATETIME NOT NULL,
    guests INT NOT NULL,
    table_number INT NOT NULL,
    status ENUM('Upcoming', 'Completed', 'Canceled') DEFAULT 'Upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- General Info Table
CREATE TABLE GeneralInfo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL
);



-- Insert Users (Admins & Workers)
INSERT INTO Users (name, email, password, role, phone) VALUES
('Ahmed Khan', 'ahmed@restaurant.com', 'hashedpassword1', 'Admin', '03001234567'),
('Sara Ali', 'sara@restaurant.com', 'hashedpassword2', 'Worker', '03009876543'),
('Bilal Raza', 'bilal@restaurant.com', 'hashedpassword3', 'Worker', '03211234567');

-- Insert Menu Items
INSERT INTO Menu (name, description, price, category, availability, image_url) VALUES
('Chicken Biryani', 'Spicy chicken biryani with raita and salad', 450, 'Rice', TRUE, 'images/biryani.jpg'),
('Seekh Kabab', 'Delicious beef seekh kababs served with naan', 350, 'BBQ', TRUE, 'images/seekh_kabab.jpg'),
('Karahi Gosht', 'Mutton karahi with rich spices and tomatoes', 1200, 'Curry', TRUE, 'images/karahi.jpg'),
('Daal Chawal', 'Traditional lentils with steamed rice', 250, 'Vegetarian', TRUE, 'images/daal_chawal.jpg'),
('Peshawari Chapli Kabab', 'Juicy chapli kabab with chutney', 400, 'BBQ', TRUE, 'images/chapli_kabab.jpg');

-- Insert Orders
INSERT INTO Orders (user_id, status, total_price, payment_method) VALUES
(2, 'Pending', 800, 'Cash'),
(3, 'In Progress', 1200, 'Card'),
(2, 'Completed', 350, 'Online');

-- Insert Order Items
INSERT INTO OrderItems (order_id, menu_id, quantity, special_request) VALUES
(1, 1, 2, 'Extra spicy'),
(1, 2, 1, ''),
(2, 3, 1, 'Less oil'),
(3, 5, 2, 'With extra chutney');

-- Insert Reservations
INSERT INTO Reservations (user_id, reservation_time, guests, table_number, status) VALUES
(2, '2025-03-18 19:30:00', 4, 12, 'Upcoming'),
(3, '2025-03-19 20:00:00', 2, 7, 'Upcoming'),
(1, '2025-03-20 21:00:00', 6, 5, 'Upcoming');

-- Insert General Info (FAQs)
INSERT INTO GeneralInfo (question, answer) VALUES
('What are your restaurant timings?', 'We are open from 12:00 PM to 11:00 PM daily.'),
('Do you offer home delivery?', 'Yes, we provide home delivery within a 10km radius.'),
('What payment methods do you accept?', 'We accept cash, card, and online payments.'),
('Do you have a vegetarian menu?', 'Yes, we offer a variety of vegetarian dishes.'),
('How can I make a reservation?', 'You can book a table online or call us at 03001234567.');
select * from Users;


-- Add Customers Table
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    PhoneNumber VARCHAR(15) UNIQUE NOT NULL,
    Name VARCHAR(255) DEFAULT 'Unknown',
    DietaryConstraints TEXT NULL,
    Allergy TEXT NULL
);

-- Add OrderTracking Table
CREATE TABLE IF NOT EXISTS OrderTracking (
    OrderID INT PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    Status ENUM('Pending', 'Preparing', 'Ready', 'Delivered') DEFAULT 'Pending',
    FOREIGN KEY (OrderID) REFERENCES Orders(id) ON DELETE CASCADE
);

-- Populate Customers Table
INSERT INTO Customers (PhoneNumber, Name, DietaryConstraints, Allergy) VALUES
('923001112233', 'Ali Khan', 'Vegetarian', 'Peanuts'),
('923004445566', 'Sarah Ahmed', 'Gluten-Free', NULL),
('923008889900', 'Unknown', NULL, 'Lactose'),
('923009990011', 'Hamza Sheikh', NULL, NULL);

-- Populate OrderTracking Table
INSERT INTO OrderTracking (OrderID, CustomerName, Status) VALUES
(2, 'Ali Khan', 'Pending'),
(3, 'Sarah Ahmed', 'Preparing')


