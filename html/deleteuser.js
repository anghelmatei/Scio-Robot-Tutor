// PostgreSQL connection information
const DB_HOST = "ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech";
const DB_PORT = "5432";
const DB_NAME = "BucharestHackathon2024";
const DB_USER = "admin";
const DB_PASSWORD = "D0OG5cvldrMg";
const DB_SSL_MODE = "require";
const ENDPOINT_ID = "ep-sweet-moon-a4zutfgf"; // Add the Endpoint ID here

// Get the username from POST data
const username = req.body.username; // Assuming req is available and contains the POST data

// Construct SQL query to delete user
const query = `DELETE FROM users WHERE username = '${username}'`;

// Establish database connection
const { Client } = require('pg');

const client = new Client({
  user: DB_USER,
  host: DB_HOST,
  database: DB_NAME,
  password: DB_PASSWORD,
  port: DB_PORT,
  ssl: {
    rejectUnauthorized: false,
    ca: fs.readFileSync('./rds-combined-ca-bundle.pem').toString(),
  },
});

client.connect();

// Execute query
client.query(query, (err, res) => {
  if (err) {
    console.error('Error executing query', err.stack);
    return;
  }
  console.log(`Deleted entry with username '${username}' from the 'users' table`);
});

// Close database connection
client.end();
