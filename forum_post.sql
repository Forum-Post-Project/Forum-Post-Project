-- User Table
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255)
);

-- Category Table
CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Topic Table
CREATE TABLE Topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category_id INT,
    user_id INT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Reply Table
CREATE TABLE Reply (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    topic_id INT,
    user_id INT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Message Table
CREATE TABLE Message (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    sender_id INT,
    receiver_id INT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES User(user_id),
    FOREIGN KEY (receiver_id) REFERENCES User(user_id)
);

-- User_Category_Access Table
CREATE TABLE User_Category_Access (
    user_id INT,
    category_id INT,
    access_level ENUM('Read', 'Write'),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    PRIMARY KEY (user_id, category_id)
);

-- Vote Table
CREATE TABLE Vote (
    vote_id INT AUTO_INCREMENT PRIMARY KEY,
    reply_id INT,
    user_id INT,
    vote_type ENUM('Upvote', 'Downvote'),
    FOREIGN KEY (reply_id) REFERENCES Reply(reply_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    UNIQUE KEY (reply_id, user_id)
);

-- Best_Reply Table
CREATE TABLE Best_Reply (
    topic_id INT,
    reply_id INT,
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id),
    FOREIGN KEY (reply_id) REFERENCES Reply(reply_id),
    PRIMARY KEY (topic_id)
);

-- Topic_Lock Table
CREATE TABLE Topic_Lock (
    topic_id INT,
    locked_by INT,
    lock_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id),
    FOREIGN KEY (locked_by) REFERENCES User(user_id),
    PRIMARY KEY (topic_id)
);

-- Category_Lock Table
CREATE TABLE Category_Lock (
    category_id INT,
    locked_by INT,
    lock_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (locked_by) REFERENCES User(user_id),
    PRIMARY KEY (category_id)
);
