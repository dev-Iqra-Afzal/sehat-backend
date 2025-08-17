
-- auth-service
CREATE DATABASE auth_db;
CREATE USER auth_user WITH ENCRYPTED PASSWORD 'auth_db_password';
GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;

-- resource-service
CREATE DATABASE resource_db;
CREATE USER resource_user WITH ENCRYPTED PASSWORD 'resource_db_password';
GRANT ALL PRIVILEGES ON DATABASE resource_db TO resource_user;

-- notification-service
CREATE DATABASE notification_db;
CREATE USER notification_user WITH ENCRYPTED PASSWORD 'notification_db_password';
GRANT ALL PRIVILEGES ON DATABASE notification_db TO notification_user;

