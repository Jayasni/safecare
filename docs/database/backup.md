# PostgreSQL Backup and Restore

## pgAdmin 4
1. Connect to the local PostgreSQL server.
2. Right-click `Sagecare_db`.
3. Select Backup.
4. Choose a filename such as `sagecare_db_backup.sql`.
5. Select format Plain or Custom as appropriate.
6. Save.

To restore:
1. Right-click Databases.
2. Select Restore.
3. Choose the backup file.
4. Restore into `Sagecare_db` or a new database.

## Command Line
```powershell
pg_dump -U postgres -h localhost -p 5432 -d Sagecare_db > sagecare_db_backup.sql
psql -U postgres -h localhost -p 5432 -d Sagecare_db < sagecare_db_backup.sql
```

The PostgreSQL client binaries must be installed and available in your system PATH.