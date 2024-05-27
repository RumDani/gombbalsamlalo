import streamlit as st
import sqlite3

# Adatbázis kapcsolat létrehozása a secrets.toml fájl alapján
conn = st.experimental_connection('sql')

# Táblázat létrehozása, ha még nem létezik
conn.execute('''
CREATE TABLE IF NOT EXISTS counter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count INTEGER NOT NULL
)
''')

# Alapértelmezett érték beállítása, ha a tábla üres
result = conn.execute('SELECT COUNT(*) FROM counter').fetchone()
if result[0] == 0:
    conn.execute('INSERT INTO counter (count) VALUES (0)')

# Aktuális érték beolvasása az adatbázisból
def get_count():
    result = conn.execute('SELECT count FROM counter WHERE id = 1').fetchone()
    return result[0]

# Számláló érték növelése
def increment_count():
    current_count = get_count()
    new_count = current_count + 1
    conn.execute('UPDATE counter SET count = ? WHERE id = 1', (new_count,))
    return new_count

# Streamlit felület
st.title('Számláló alkalmazás')
st.write('Az aktuális érték: ', get_count())

if st.button('Növel'):
    new_count = increment_count()
    st.write('Az új érték: ', new_count)
