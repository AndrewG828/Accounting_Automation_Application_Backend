# Accounting_Automation_Application_Backend

## Setup

1. **Clone the repo:**

   ```bash
   git clone git@github.com:AndrewG828/Accounting_Automation_Application_Backend.git
   cd Accounting_Automation_Application_Backend

   ```

2. **Install Dependencies:**

   ```bash
   npm install express sequelize pg pg-hstore cors dotenv bcrypt multer csv-parser
   npm install --save-dev nodemon

   ```

3. **Configure PostgeSQL Database**

   Make sure PostgreSQL is installed and running.

   Create a database.

   Update your database connection string in the code or environment variables.

5. **Run the app:**

   For development (auto-restart on changes):

   ```bash
   npm run dev
   ```

## Dependencies

- express
- sequelize
- pg
- pg-hstore
- nodemon

## Notes

- Remember to add your .env file (for secrets like DB credentials) and add it to .gitignore.
