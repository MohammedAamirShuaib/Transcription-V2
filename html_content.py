import webbrowser


def html_completed(html, exception, username, use_id):
    html_completed_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/download.css'><head><title>OSG - Video Transcription Tool</title></head><meta charset='utf-8'><body><a href='/home/{username}/{use_id}/' class='home_btn'>Home</a><div class='center'><h2 align='center'>Download Transcriptions</h2></div><table><tr><th height='40'>User</th><th height='40'>Project Name</th><th height='40'>File Name</th><th height='40'>Word</th><th height='40'>CSV</th><th height='40'>Time</th><th height='40'>Status</th></tr>{html}</table><P>{exception}</P><br><br></body></html>"
    return html_completed_content


def html_webpage(select_box_html, dir_name, use_id, username):
    html_webpage_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/uploadpage.css'><head><title>OSG - Video Transcription Tool</title></head><meta charset='utf-8'><body><div class='logo' align='center'></div><div class='content_box' align ='center'><br/><br><img src='/static/images/logo_trans.png' height='60'><br/><h1>Video Transcription Tool</h1><form action='/{use_id}/{username}/{dir_name}' enctype='multipart/form-data' method='post' align='center'><select name='project_name' id='project_name' required><option disabled selected value> Select Project </option>{select_box_html}</select>&nbsp;&nbsp;<a href='/{username}/create_new_project/' class='new_project'>New Project</a>&nbsp;&nbsp;<br/><br>&nbsp;<input name='files' id='files' class='upload-box' type='file'  multiple required>&nbsp;&nbsp;<button class='btn'><span class='btn_text'>Transcribe</span></button>&nbsp;&nbsp;<a href='/{username}/records/{use_id}' class='new_project'>Previous Records</a>&nbsp;&nbsp;</form><script src='/static/uploadpage.js'></script></div></body></html>"
    return html_webpage_content


def html_logs(logs):
    html_logs_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/logs.css'><head><title>OSG - Video Transcription Tool</title></head><meta charset='utf-8'><body><div class='center'><br/><h1>Transcription Logs</h1><br/><p>{logs}</p></div></body></html>"
    return html_logs_content


def html_get_records(table, use_id, username):
    html_get_records_content = f"<!DOCTYPE html><html lang='en'><link rel='stylesheet' href='/static/showrecords.css'><head><title>OSG - Video Transcription Tool</title></head><meta charset='utf-8'><body><a href='/home/{username}/{use_id}/' class='home_btn'>Home</a><div class='center'><h2 align='center'>Transcription Records</h2></div><table><tr><th height='40'>Date Time</th><th height='40'>User</th><th height='40'>Project Name</th><th height='40'>File Name</th><th height='40'>Word</th><th height='40'>CSV</th></tr>{table}</table><br><br></body></html>"
    return html_get_records_content
