-- PostgreSQL Script
-- Create schemas and set up permissions for Kol Torah application
-- Run this script as a PostgreSQL superuser after creating roles

-- Create schemas
CREATE SCHEMA IF NOT EXISTS sources;
CREATE SCHEMA IF NOT EXISTS main;
CREATE SCHEMA IF NOT EXISTS webapp;

-- Schema: sources
-- ingestion: read/write, webapp: no access

-- Grant usage and create privileges to ingestion
GRANT USAGE, CREATE ON SCHEMA sources TO ingestion;

-- Grant privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA sources TO ingestion;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA sources TO ingestion;

-- Set default privileges for future tables created by ingestion
ALTER DEFAULT PRIVILEGES IN SCHEMA sources
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ingestion;
ALTER DEFAULT PRIVILEGES IN SCHEMA sources
    GRANT USAGE, SELECT ON SEQUENCES TO ingestion;

-- Revoke all from webapp (explicit denial)
REVOKE ALL ON SCHEMA sources FROM webapp;


-- Schema: main
-- ingestion: read/write, webapp: read-only

-- Grant usage and create privileges to ingestion
GRANT USAGE, CREATE ON SCHEMA main TO ingestion;

-- Grant privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA main TO ingestion;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA main TO ingestion;

-- Grant read-only access to webapp
GRANT USAGE ON SCHEMA main TO webapp;
GRANT SELECT ON ALL TABLES IN SCHEMA main TO webapp;

-- Set default privileges for future tables created by ingestion
ALTER DEFAULT PRIVILEGES IN SCHEMA main
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ingestion;
ALTER DEFAULT PRIVILEGES IN SCHEMA main
    GRANT USAGE, SELECT ON SEQUENCES TO ingestion;

-- Set default privileges for webapp (read-only on future tables)
ALTER DEFAULT PRIVILEGES IN SCHEMA main
    GRANT SELECT ON TABLES TO webapp;


-- Schema: webapp
-- ingestion: no access, webapp: read/write

-- Grant usage and create privileges to webapp
GRANT USAGE, CREATE ON SCHEMA webapp TO webapp;

-- Grant privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA webapp TO webapp;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA webapp TO webapp;

-- Set default privileges for future tables created by webapp
ALTER DEFAULT PRIVILEGES IN SCHEMA webapp
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO webapp;
ALTER DEFAULT PRIVILEGES IN SCHEMA webapp
    GRANT USAGE, SELECT ON SEQUENCES TO webapp;

-- Revoke all from ingestion (explicit denial)
REVOKE ALL ON SCHEMA webapp FROM ingestion;


-- Add comments for documentation
COMMENT ON SCHEMA sources IS 'Schema for source data (ingestion: read/write, webapp: no access)';
COMMENT ON SCHEMA main IS 'Schema for main application data (ingestion: read/write, webapp: read-only)';
COMMENT ON SCHEMA webapp IS 'Schema for web application data (ingestion: no access, webapp: read/write)';
