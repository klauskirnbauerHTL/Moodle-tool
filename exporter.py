import xml.etree.ElementTree as ET
import sqlite3

def export_to_moodle_xml(db_path, question_ids, filename):
    """Exportiert ausgewählte Fragen als Moodle XML"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    quiz = ET.Element('quiz')

    for qid in question_ids:
        c.execute('SELECT title, questiontext, single, tags, points FROM questions WHERE id=?', (qid,))
        row = c.fetchone()
        if not row:
            continue
        title, questiontext, single, tags, points = row

        question = ET.SubElement(quiz, 'question', type='multichoice')

        name = ET.SubElement(question, 'name')
        ET.SubElement(name, 'text').text = title

        questiontext_node = ET.SubElement(question, 'questiontext', format='html')
        ET.SubElement(questiontext_node, 'text').text = questiontext

        ET.SubElement(question, 'generalfeedback', format='html').text = ''
        ET.SubElement(question, 'defaultgrade').text = f'{points:.1f}'
        ET.SubElement(question, 'single').text = 'true' if single == 1 else 'false'
        ET.SubElement(question, 'shuffleanswers').text = 'true'
        ET.SubElement(question, 'answernumbering').text = 'abc'

        # Tags
        tags_root = ET.SubElement(question, 'tags')
        for t in tags.split(','):
            tag_text = t.strip()
            if tag_text:
                tag = ET.SubElement(tags_root, 'tag')
                ET.SubElement(tag, 'text').text = tag_text

        # Antworten
        c.execute('SELECT answertext, is_correct FROM answers WHERE question_id=?', (qid,))
        answers = c.fetchall()
        for answertext, is_correct in answers:
            fraction = '100' if is_correct == 1 else '0'
            answer = ET.SubElement(question, 'answer', fraction=fraction, format='html')
            ET.SubElement(answer, 'text').text = answertext
            ET.SubElement(answer, 'feedback', format='html').text = ''

    tree = ET.ElementTree(quiz)
    
    # ✅ KORRIGIERTE XML-SCHREIBUNG (ohne short_empty_tags)
    with open(filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    conn.close()
