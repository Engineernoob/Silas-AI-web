import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
con = sqlite3.connect("silas.db")
cursor = con.cursor()

# Create the table if it doesn't exist
query = """
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    path VARCHAR(1000)
)
"""
cursor.execute(query)

# Define the applications to insert
commands = [
    ('notes', '/Applications/Notes.app'),
    ('safari', '/Applications/Safari.app'),
    ('terminal', '/Applications/Utilities/Terminal.app'),
    ('calendar', '/Applications/Calendar.app'),
    ('Arc', '/Applications/Arc.app'),
    ('vscode', '/Applications/Visual Studio Code.app')
]

# Insert the commands into the sys_command table using parameterized queries
insert_query = "INSERT INTO sys_command (name, path) VALUES (?, ?)"
cursor.executemany(insert_query, commands)

# Drop the existing web_command table if it exists (to avoid column issues)
cursor.execute("DROP TABLE IF EXISTS web_command")

# Create the web_command table with the correct structure
web_command_query = """
CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    url VARCHAR(1000)
)
"""
cursor.execute(web_command_query)

# Insert some common web commands
web_commands = [
    ('youtube', 'https://www.youtube.com'),
    ('google', 'https://www.google.com'),
    ('github', 'https://www.github.com'),
    ('chatgpt', 'https://chatgpt.com/'),
    ("slack", "https://slack.com/"),
    ("amazon", "https://www.amazon.com/"),
    ('reddit', 'https://www.reddit.com')
]
web_insert_query = "INSERT INTO web_command (name, url) VALUES (?, ?)"
cursor.executemany(web_insert_query, web_commands)


# Commit changes to the database
con.commit()

# Close the connection
con.close()
