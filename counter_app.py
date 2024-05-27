import streamlit as st
from sqlalchemy import create_engine, text

# Initialize connection.
conn = st.connection('my_sql_connection', type='sql')

# Create table if it does not exist.
with conn.engine.connect() as connection:
    connection.execute(text('''
    CREATE TABLE IF NOT EXISTS counter (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        count INTEGER NOT NULL
    )
    '''))

    # Initialize the counter if it is empty.
    result = connection.execute(text('SELECT COUNT(*) FROM counter')).fetchone()
    if result[0] == 0:
        connection.execute(text('INSERT INTO counter (count) VALUES (0)'))

# Function to get the current count.
def get_count():
    with conn.engine.connect() as connection:
        result = connection.execute(text('SELECT count FROM counter WHERE id = 1')).fetchone()
        return result[0] if result else 0

# Function to increment the count.
def increment_count():
    current_count = get_count()
    new_count = current_count + 1
    with conn.engine.connect() as connection:
        connection.execute(text('UPDATE counter SET count = :count WHERE id = 1'), {'count': new_count})
    return new_count

# Streamlit app layout.
st.title('Számláló alkalmazás')
st.write('Az aktuális érték: ', get_count())

if st.button('Növel'):
    new_count = increment_count()
    st.write('Az új érték: ', new_count)

# Display saved values
st.write("Mentett értékek:")
with conn.engine.connect() as connection:
    rows = connection.execute(text('SELECT * FROM counter')).fetchall()
    for row in rows:
        st.write(row)
