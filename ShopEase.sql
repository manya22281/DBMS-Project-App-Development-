

CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Address VARCHAR(100),
    Phone_No INT,
    Order_History INT DEFAULT 0,
    Account_Status VARCHAR(100),
    Password VARCHAR(100) NOT NULL
);
CREATE TABLE Vendor (
    Vendor_ID INT PRIMARY KEY,
    Description VARCHAR(100) NOT NULL,
    Phone_No INT,
    Supply_Items VARCHAR(100) NOT NULL
);
CREATE TABLE Admin (
    Admin_ID INT PRIMARY KEY,
    User_ID INT NOT NULL,
    Vendor_ID INT NOT NULL ,
    Password VARCHAR(100) NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Vendor_ID) REFERENCES Vendor(Vendor_ID)
);

CREATE TABLE Category (
    Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(30) NOT NULL
);

-- Drop the existing Items table
DROP TABLE IF EXISTS Items;

-- Recreate the Items table with the correct schema
CREATE TABLE Items (
    Item_Name VARCHAR(30) PRIMARY KEY,
    Item_Price FLOAT NOT NULL,
    Quantity INT NOT NULL,
    Description VARCHAR(1000),
    Category_ID INT,
    FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID)
);
CREATE TABLE Cart (
    Cart_ID INT PRIMARY KEY,
    Total_Amount FLOAT,
    Discount FLOAT,
    Quantity INT NOT NULL ,
    User_ID INT,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);
CREATE TABLE Tracking_Details (
    Tracking_ID INT PRIMARY KEY,
    Delivery_Partner_Phone_No INT,
    Delivery_Partner_Name VARCHAR(30),
    User_Address VARCHAR(100),
    Delivery_Time INT
);

CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Date_And_Time DATETIME NOT NULL,
    Cart_ID INT,
    Tracking_ID INT,
    FOREIGN KEY (Cart_ID) REFERENCES Cart(Cart_ID),
    FOREIGN KEY (Tracking_ID) REFERENCES Tracking_Details(Tracking_ID)
    
);


CREATE TABLE Manages (
    Help_And_Support VARCHAR(30) NOT NULL,
    Feedback VARCHAR(30) NOT NULL,
    User_ID INT, 
    FOREIGN KEY (User_ID) REFERENCES USERS(User_ID)
);

CREATE TABLE LoginAttempts (
    Attempt_ID INTEGER PRIMARY KEY,
    User_ID INTEGER NOT NULL,
    Success INTEGER NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

-- Create trigger to block account after 3 login failures
-- Create trigger to block account after 3 login failures

CREATE INDEX idx_User_ID ON Cart(User_ID);
CREATE INDEX idx_Category_ID ON Items(Category_ID);
CREATE INDEX idx_Tracking_ID ON Payment(Tracking_ID);



INSERT INTO Users (User_ID, Name, Phone_No, Address, Order_History,Account_Status,Password) 
VALUES 
    (1, 'Manya', 123456789, 'Noida', 0,'Unblocked','manya'),
    (2, 'Arun', 123456789, 'Dwarka', 0,'Unblocked','arun'),
    (3, 'Sneha', 123456789, 'Saket', 0,'Unblocked','sneha'),
    (4, 'Yatin', 123456789, 'Bareli', 0,'Unblocked','yatin'),
    (5, 'Rayma', 123456789, 'Noida', 0,'Unblocked','rayma'),
    (6, 'Ritu', 123456789, 'Noida', 0,'Unblocked','ritu'),
    (7, 'Vansh', 123456789, 'Dwarka',0,'Unblocked','vansh'),
    (8, 'Mohit', 123456789, 'Saket', 0,'Unblocked','mohit'),
    (9, 'Rohit', 123456789, 'Bareli', 0,'Unblocked','rohit'),
    (10, 'Chintu', 123456789, 'Noida', 0,'Unblocked','chintu');

INSERT INTO Vendor (Vendor_ID, Description, Phone_No, Supply_Items) 
VALUES 
    (101, 'Vendor A', 1122334459, 'Item1'),
    (102, 'Vendor B', 1112223339, 'Item2'),
    (103, 'Vendor C', 1112223338, 'Item3'),
    (104, 'Vendor D', 1112223337, 'Item4'),
    (105, 'Vendor E', 1112223336, 'Item5'),
    (106, 'Vendor A', 1122334454, 'Item6'),
    (107, 'Vendor B', 1112223398, 'Item7'),
    (108, 'Vendor C', 1112223334, 'Item8'),
    (109, 'Vendor D', 1112223323, 'Item9'),
    (110, 'Vendor E', 1112223321, 'Item10');
INSERT INTO Admin (Admin_ID, User_ID, Vendor_ID, Password) 
VALUES 
    (2021, 1, 101, '2021'),
    (2022, 2, 102 , '2022'),
    (2023, 3, 103 , '2023'),
    (2024, 4, 104 , '2024'),
    (2025, 5, 105 , '2025'),
    (2026, 6, 106 , '2026'),
    (2027, 7, 107 , '2027'),
    (2028, 8, 108 , '2028'),
    (2029, 9, 109 , '2029'),
    (2030, 10, 110 , '2030');



INSERT INTO Category (Category_ID, Category_Name) 
VALUES 
    (1000, 'Dairy Products'),
    (1001, 'Pharmacy'),
    (1002, 'Bakery and Biscuits'),
    (1003, 'Vegetables and Fruits'),
    (1004, 'Home and Office'),
    (1005, 'Sweets and Chocolates'),
    (1006, 'Drinks and Juices'),
    (1007, 'Chips and Namkeen'),
    (1008, 'Dry Fruits and Cereals'),
    (1009, 'Bath and Body');


INSERT INTO Items (Item_Name, Item_Price, Quantity, Description, Category_ID) 
VALUES 
    ('Milk', 59.00, 100,'Full Cream Milk (Polypack) Milk is homogenized toned pasteurized milk.', 1000),
    ('Crocin', 20.00,100, 'Crocin Advance tablet is a pain-relieving medicine', 1001),
    ('Hide And Seek', 45.00,100, 'Sprinkled with the goodness of chocolate, the Parle Hide & Seek Chocolate Chip Cookie', 1002),
    ('Onion', 34.00,100, 'Onion is a staple in India and is commonly chopped .', 1003),
    ('Fevicol', 100.00, 100,'Universal craft glue ideal for pasting a variety of materials from papers, candy sticks', 1004),
    ('Cadbury Silk', 190.00,100, 'Cadbury Dairy Milk Silk chocolate is creamier, smoother, and more indulgent.', 1005),
    ('Pepsi', 40.00,100, 'Live your life to the fullest with a passion to do something crazy each day.', 1006),
    ('American Lays', 20.00,100, 'Add some hearty flavor to your day with Lay’s American Style Cream and Onion!', 1007),
    ('Ashirwaad Atta', 220.00, 100,'Aashirvaad Shudh Chakki Atta uses the 4-step advantage process of sourcing, cleaning, grinding & contactless packaging.', 1008),
    ('Soap', 60.00, 100,'Patanjali Haldi Chandan Kanti Soap for skincare', 1009);


INSERT INTO Cart (Cart_ID, Total_Amount, Discount, Quantity, User_ID) 
VALUES 
    (1, 79.00, 0, 2, 1),
    (2, 190.00, 0, 1, 2),
    (3, 59.00, 0, 1, 3),
    (4, 60.00, 0, 3, 4),
    (5, 59.00, 0, 1, 5),
    (6, 60.00, 0, 3, 6),
    (7, 59.00, 0, 1, 7),
    (8, 60.00, 0, 3, 8),
    (9, 59.00, 0, 1, 9),
    (10, 60.00, 0, 3, 10);


INSERT INTO Tracking_Details (Tracking_ID, Delivery_Partner_Phone_No, Delivery_Partner_Name, User_Address, Delivery_Time) 
VALUES 
    (4001, '123456789', 'Urmila', 'Noida', 15),
    (4002, '123456789', 'Meena', 'Noida', 30),
    (4003, '123456789', 'Dev', 'Noida', 20),
    (4004, '123456789', 'Rahul', 'Noida', 40),
    (4005, '123456789', 'Teena', 'Noida', 60),
    (4006, '123456789', 'Ankita', 'Noida', 45),
    (4007, '123456789', 'Anica', 'Noida', 30),
    (4008, '123456789', 'Devashi', 'Noida', 20),
    (4009, '123456789', 'Mehul', 'Noida', 25),
    (4010, '123456789', 'Yash', 'Noida', 15);


INSERT INTO Payment (Payment_ID, Date_And_Time, Cart_ID, Tracking_ID) 
VALUES 
    (3001, '2024-01-26 16:00:00', 1, 4001),
    (3002, '2024-02-06 06:00:00', 2, 4002),
    (3003, '2024-02-26 15:00:00', 3, 4003),
    (3004, '2024-03-06 05:00:00', 4, 4004),
    (3005, '2024-03-26 14:00:00', 5, 4005),
    (3006, '2024-04-06 09:00:00', 6, 4006),
    (3007, '2024-04-26 13:00:00', 7, 4007),
    (3008, '2024-05-06 08:00:00', 8, 4008),
    (3009, '2024-05-26 12:00:00', 9, 4009),
    (3010, '2024-06-06 07:00:00', 10, 4010);

INSERT INTO Manages ( Help_And_Support, Feedback, User_ID) 
VALUES 
    ( 'Customer Service', '3 stars' , 1 ),
    ( 'Technical Support', '4 stars' , 2),
    ( 'User Assistance', '5 stars' , 3),
    ( 'Product Inquiry', '2 stars' , 4),
    ( 'Complaint Resolution', '4 stars' , 5);




-- DROP TABLE IF EXISTS Users;
-- DROP TABLE IF EXISTS Vendor;
-- DROP TABLE IF EXISTS Admin;
-- DROP TABLE IF EXISTS Category;
-- DROP TABLE IF EXISTS Items;
-- DROP TABLE IF EXISTS Cart;
-- DROP TABLE IF EXISTS Tracking_Details;
-- DROP TABLE IF EXISTS Payment;
-- DROP TABLE IF EXISTS Manages;
-- DROP TABLE IF EXISTS LoginAttempts;