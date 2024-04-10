CREATE TABLE IF NOT EXISTS key_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    key VARCHAR(255) NOT NULL,
    CONSTRAINT unique_email_key UNIQUE (email, key)
);