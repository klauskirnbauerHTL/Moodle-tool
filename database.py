import sqlite3
import os
import xml.etree.ElementTree as ET

def init_database_schema(db_path):
    """Erstellt die Tabellen falls nicht vorhanden"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Prüfen ob question_type Spalte existiert
    c.execute("PRAGMA table_info(questions)")
    columns = [column[1] for column in c.fetchall()]
    
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        questiontext TEXT NOT NULL,
        single INTEGER DEFAULT 1,
        tags TEXT DEFAULT '',
        points REAL DEFAULT 1.0,
        question_type TEXT DEFAULT 'multichoice'
    )''')
    
    # Wenn Spalte nicht existiert, hinzufügen (Migration)
    if 'question_type' not in columns and len(columns) > 0:
        c.execute("ALTER TABLE questions ADD COLUMN question_type TEXT DEFAULT 'multichoice'")
    
    c.execute('''CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        answertext TEXT NOT NULL,
        is_correct INTEGER DEFAULT 0,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )''')
    conn.commit()
    conn.close()

def get_questions_overview(db_path):
    """Liefert Übersicht: ID, Titel, Punkte, Tags, Anzahl Antworten"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT q.id, q.title, q.points, q.tags, COUNT(a.id) FROM questions q LEFT JOIN answers a ON q.id=a.question_id GROUP BY q.id")
    rows = c.fetchall()
    conn.close()
    return rows

def save_question(db_path, title, questiontext, single, tags, points, answers):
    """Speichert Frage + Antworten"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("INSERT INTO questions (title, questiontext, single, tags, points) VALUES (?, ?, ?, ?, ?)",
             (title, questiontext, single, tags, points))
    qid = c.lastrowid
    
    for answer_text, is_correct in answers:
        if answer_text.strip():
            c.execute("INSERT INTO answers (question_id, answertext, is_correct) VALUES (?, ?, ?)",
                     (qid, answer_text.strip(), is_correct))
    
    conn.commit()
    conn.close()
    return qid

def duplicate_question(db_path, question_id):
    """Dupliziert eine Frage inkl. aller Antworten"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Original-Frage laden
    c.execute("SELECT title, questiontext, single, tags, points, question_type FROM questions WHERE id=?", (question_id,))
    result = c.fetchone()
    if not result:
        conn.close()
        return None
    
    title, questiontext, single, tags, points, question_type = result
    # Titel mit "(Kopie)" markieren
    new_title = f"{title} (Kopie)"
    
    # Neue Frage einfügen
    c.execute("""INSERT INTO questions (title, questiontext, single, tags, points, question_type) 
                VALUES (?, ?, ?, ?, ?, ?)""",
             (new_title, questiontext, single, tags, points, question_type))
    new_qid = c.lastrowid
    
    # Antworten kopieren
    c.execute("SELECT answertext, is_correct FROM answers WHERE question_id=?", (question_id,))
    answers = c.fetchall()
    for answer_text, is_correct in answers:
        c.execute("INSERT INTO answers (question_id, answertext, is_correct) VALUES (?, ?, ?)",
                 (new_qid, answer_text, is_correct))
    
    conn.commit()
    conn.close()
    return new_qid

def import_moodle_xml(db_path, xml_filename):
    """Importiert Moodle XML Fragen in die lokale DB"""
    try:
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        
        if root.tag != 'quiz':
            return 0, "Fehler: Ungültiges Moodle XML (kein <quiz> Root)"
        
        imported_count = 0
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        for question_elem in root.findall('question'):
            if question_elem.get('type') != 'multichoice':
                continue  # Nur MC-Fragen importieren
            
            # Frage-Daten extrahieren
            name_elem = question_elem.find('.//name/text')
            title = name_elem.text.strip() if name_elem is not None else "Unbenannte Frage"
            
            qtext_elem = question_elem.find('.//questiontext/text')
            questiontext = qtext_elem.text.strip() if qtext_elem is not None else ""
            
            single_elem = question_elem.find('single')
            single = 1 if single_elem is not None and single_elem.text == 'true' else 0
            
            defaultgrade_elem = question_elem.find('defaultgrade')
            points = float(defaultgrade_elem.text) if defaultgrade_elem is not None else 1.0
            
            # Tags extrahieren
            tags = ""
            tags_root = question_elem.find('tags')
            if tags_root is not None:
                for tag_elem in tags_root.findall('tag/text'):
                    if tag_elem is not None and tag_elem.text:
                        tags += tag_elem.text.strip() + ","
                tags = tags.rstrip(',')
            
            # Frage einfügen
            c.execute("""INSERT INTO questions (title, questiontext, single, tags, points) 
                        VALUES (?, ?, ?, ?, ?)""",
                     (title, questiontext, single, tags, points))
            qid = c.lastrowid
            
            # Antworten einfügen
            for answer_elem in question_elem.findall('answer'):
                answertext_elem = answer_elem.find('text')
                fraction = answer_elem.get('fraction', '0')
                is_correct = 1 if fraction == '100' else 0
                
                if answertext_elem is not None and answertext_elem.text:
                    c.execute("INSERT INTO answers (question_id, answertext, is_correct) VALUES (?, ?, ?)",
                             (qid, answertext_elem.text.strip(), is_correct))
            
            imported_count += 1
        
        conn.commit()
        conn.close()
        return imported_count, f"✓ {imported_count} MC-Fragen importiert!"
        
    except ET.ParseError as e:
        return 0, f"XML Parse Fehler: {str(e)}"
    except Exception as e:
        return 0, f"Import Fehler: {str(e)}"
