# File Format

All files should be names in the following format and placed in db_migrations folder

`[number in sequence]_[description].sql`

Example:

`001_CREATE_USER_TABLE.sql`

**Contents in file should include sql commands only**

Once a file is migrated, it will show as an error in future migrations. Only 
new SQL files will show as successful