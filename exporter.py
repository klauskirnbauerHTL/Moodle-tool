import xml.etree.ElementTree as ET
import sqlite3

def export_to_moodle_xml(db_path, question_ids, filename):
    """Exportiert ausgewählte Fragen als Moodle XML"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    quiz = ET.Element('quiz')

    for qid in question_ids:
        c.execute('SELECT title, questiontext, single, tags, points, question_type FROM questions WHERE id=?', (qid,))
        row = c.fetchone()
        if not row:
            continue
        title, questiontext, single, tags, points = row[:5]
        question_type = row[5] if len(row) > 5 else 'multichoice'

        # Fragetyp bestimmen
        if question_type == 'essay':
            question = ET.SubElement(quiz, 'question', type='essay')
        elif question_type == 'shortanswer':
            question = ET.SubElement(quiz, 'question', type='shortanswer')
        else:
            question = ET.SubElement(quiz, 'question', type='multichoice')

        name = ET.SubElement(question, 'name')
        ET.SubElement(name, 'text').text = title

        questiontext_node = ET.SubElement(question, 'questiontext', format='html')
        ET.SubElement(questiontext_node, 'text').text = questiontext

        ET.SubElement(question, 'generalfeedback', format='html').text = ''
        ET.SubElement(question, 'defaultgrade').text = f'{points:.1f}'
        
        # Nur bei Multichoice
        if question_type == 'multichoice':
            ET.SubElement(question, 'single').text = 'true' if single == 1 else 'false'
            ET.SubElement(question, 'shuffleanswers').text = 'true'
            ET.SubElement(question, 'answernumbering').text = 'abc'
        
        # Essay-spezifische Felder
        if question_type == 'essay':
            ET.SubElement(question, 'responseformat').text = 'editor'
            ET.SubElement(question, 'responserequired').text = '1'
            ET.SubElement(question, 'responsefieldlines').text = '15'
            ET.SubElement(question, 'attachments').text = '0'
            ET.SubElement(question, 'attachmentsrequired').text = '0'
            ET.SubElement(question, 'graderinfo', format='html').text = ''
            ET.SubElement(question, 'responsetemplate', format='html').text = ''
        
        # Shortanswer-spezifische Felder
        if question_type == 'shortanswer':
            ET.SubElement(question, 'usecase').text = '0'

        # Tags
        tags_root = ET.SubElement(question, 'tags')
        for t in tags.split(','):
            tag_text = t.strip()
            if tag_text:
                tag = ET.SubElement(tags_root, 'tag')
                ET.SubElement(tag, 'text').text = tag_text

        # Antworten (nur bei Multichoice und Shortanswer)
        if question_type in ['multichoice', 'shortanswer']:
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
