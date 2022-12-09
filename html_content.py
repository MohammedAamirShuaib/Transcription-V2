import webbrowser


def html_english_webpage(select_box_html, dir_name, use_id, username):
    html_english_webpage_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/uploadpage.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><br><br><div align='right'><a href='{username}/Non_English/' class='other_lang'>Non English Transcription</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='content_box' align ='center'><br/><br><img src='/static/images/logo_trans.png' height='60'><br/><h1>Transcription Tool</h1><form action='/{use_id}/{username}/English/{dir_name}' enctype='multipart/form-data' method='post' align='center'><select name='project_name' id='project_name' required><option disabled selected value> Select Project </option>{select_box_html}</select>&nbsp;&nbsp;<a href='/{username}/create_new_project/' class='new_project'>New Project</a>&nbsp;&nbsp;<br/><br>&nbsp;<input name='files' id='files' class='upload-box' type='file'  multiple required>&nbsp;&nbsp;<button class='btn'><span class='btn_text'>Transcribe</span></button>&nbsp;&nbsp;<a href='/{username}/projects/{use_id}' class='new_project'>Previous Records</a>&nbsp;&nbsp;</form><script src='/static/uploadpage.js'></script></div></body></html>"
    return html_english_webpage_content


def html_non_english_webpage(project_select_box, lang_select_box, dir_name, use_id, username):
    html_non_english_webpage_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/uploadpage_ML.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><br><div align='right'><button class='backbtn' onclick='window.history.back()'>English Transcription</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class='content_box' align ='center'><br/><br><img src='/static/images/logo_trans.png' height='60'><br/><h1>Transcription Tool</h1><form action='/{use_id}/{username}/Other/{dir_name}' enctype='multipart/form-data' method='post' align='center'><select name='project_name' id='project_name' class='project_box' required><option disabled selected value> Project </option>{project_select_box}</select>&nbsp;&nbsp;<select name='language' id='language' class='language_box' required><option disabled selected value> Language </option>{lang_select_box}</select><br/><br><input name='files' class='upload-box' type='file' multiple required>&nbsp;&nbsp;<button class='btn'><span class='btn_text'>Transcribe and Translate</span></button><br/><br><br><a href='/{use_id}/{username}/Non_English/projects/' class='new_project'>Previous Records</a>&nbsp;&nbsp;<a href='/{use_id}/{username}/Non_English/create_new_project/' class='new_project'>New Project</a>&nbsp;&nbsp;</form><script src='/static/uploadpage.js'></script><br><br><br><br><br><div class='note_box'>Note: <br>Other Language Transcriptions does not have Speaker Detection<br>Output is a transcription of audio in plain text file<br>Output has both plain transcription and translated text to English<br></div></div></body></html>"
    return html_non_english_webpage_content


def html_english_completed(html, exception, username, use_id):
    html_english_completed_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/download.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><button class='backbtn' onclick='window.history.back()'>Back</button><div class='center'><h2 align='center'>Download Transcriptions</h2></div><table><tr><th height='40'>User</th><th height='40'>Project Name</th><th height='40'>File Name</th><th height='40'>Word</th><th height='40'>CSV</th><th height='40'>Time</th><th height='40'>Status</th></tr>{html}</table><P>{exception}</P><br><br></body></html>"
    return html_english_completed_content


def html_non_english_completed(html, exception, username, use_id):
    html_completed_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/download.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><button class='backbtn' onclick='window.history.back()'>Back</button><div class='center'><h2 align='center'>Download Transcriptions</h2></div><table><tr><th height='40'>User</th><th height='40'>Project Name</th><th height='40'>File Name</th><th height='40'>Original Transcript</th><th height='40'>Translated (English)</th><th height='40'>Time</th><th height='40'>Status</th></tr>{html}</table><P>{exception}</P><br><br></body></html>"
    return html_completed_content


def html_get_projects(table, use_id, username):
    html_get_project_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/project_records.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><button onclick='window.history.back()'>Back</button><div class='center'><h2 align='center'>Transcription Records</h2><h3 align='center'>Select Project</h3></div><table><tr><th height='40'>Project</th><th height='40'>Files</th></tr>{table}</table><br><br></body></html>"
    return html_get_project_content


def html_get_english_records(table, use_id, username, project_name):
    html_get_english_records_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/file_records.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><button onclick='window.history.back()'>Back</button><div class='center'><h2 align='center'>Transcription Records</h2><h3 align='center'>Project - {project_name}</h3></div><table><tr><th height='40'>Date Time</th><th height='40'>User</th><th height='40'>File Name</th><th height='40'>Word</th><th height='40'>Excel</th></tr>{table}</table><br><br></body></html>"
    return html_get_english_records_content


def html_get_non_english_records(table, use_id, username, project_name):
    html_get_non_english_records_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/file_records.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><button class='backbtn' onclick='window.history.back()'>Back</button><div class='center'><h2 align='center'>Transcription Records</h2><h3 align='center'>Project - {project_name}</h3></div><table><tr><th height='40'>Date Time</th><th height='40'>User</th><th height='40'>File Name</th><th height='40'>Original Transcript</th><th height='40'>Translated (English)</th></tr>{table}</table><br><br></body></html>"
    return html_get_non_english_records_content


def html_logs(logs):
    html_logs_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/logs.css'><head><title>Transcription Tool</title><link rel='icon' href='/static/images/osg_icon.png'></head><meta charset='utf-8'><body><div class='center'><br/><h1>Transcription Logs</h1><br/><p>{logs}</p></div></body></html>"
    return html_logs_content
