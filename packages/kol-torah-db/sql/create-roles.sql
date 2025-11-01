-- PostgreSQL Script
-- Create database roles for Kol Torah application
-- Run this script as a PostgreSQL superuser

-- Create ingestion role for data ingestion pipelines
CREATE ROLE ingestion WITH LOGIN PASSWORD '*********';

-- Create webapp role for the admin web application
CREATE ROLE webapp WITH LOGIN PASSWORD '*********';

-- Grant connection privileges
GRANT CONNECT ON DATABASE kol_torah TO ingestion;
GRANT CONNECT ON DATABASE kol_torah TO webapp;

-- Comment for documentation
COMMENT ON ROLE ingestion IS 'Role for data ingestion pipelines';
COMMENT ON ROLE webapp IS 'Role for web application';
