ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;
CREATE USER ferremas_db IDENTIFIED BY ferremas_db ACCOUNT UNLOCK;
GRANT CONNECT, RESOURCE, DBA TO ferremas_db;