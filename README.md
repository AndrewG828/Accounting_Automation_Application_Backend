# Accounting_Automation_Application_Backend

## Setup

1. **Clone the repo:**

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>

   ```

2. **Install Dependencies:**

   ```bash
   npm install express sequelize pg pg-hstore
   npm install --save-dev nodemon

   ```

3. **Configure PostgeSQL Database**
   Make sure PostgreSQL is installed and running.

   Create a database.

   Update your database connection string in the code or environment variables.

4. **Run the app:**

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
