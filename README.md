# VoterFinder

VoterFinder is a tool designed to help users easily locate voter information, analyze data, and manage election-related datasets. This project aims to simplify the process of exploring voter demographics and organizing related data for campaigns, studies, and civic engagement.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vivertido/voterfinder.git
   ```

2. Obtain your voter data. Usually your county will provide a list for purchase.
3. Clean your data. You should remove unecessary columns to reduce size of dataset. This app uses just basic info for search, but feel free to allow for all the columns of iterest:
     - First name
     - Last name
     - Phone
     - City
     - Mail address
4. Create a db at /instance (create this directory)
   ```bash
   sqlite3 my_database.db
5. Enable CSV Mode Tell SQLite to read data in CSV format:
   ```sql
   .mode csv
6. Import the CSV File Use the `.import` command to load your `.csv` file into a new table:
   ```sql
   .import your_file.csv table_name
7. Verify the Import Check if the data has been imported:
   ```sql
   SELECT * FROM table_name;
8. Exit sql:
   ```sql
   .exit

