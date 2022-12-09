from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uuid
from typing import List
from functions import *
from html_content import *


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
Connect.initiate_db()

# ------------------------------view login page------------------------------


@app.get('/', response_class=HTMLResponse)
async def get_sign_in(request: Request):
    use_id = str(uuid.uuid4())[0:8]
    return templates.TemplateResponse("login.html", {'request': request, 'use_id': use_id})

# ------------------------------authenticate and view transcription page------------------------------


@app.post('/{use_id}/', response_class=HTMLResponse)
async def landingpage(request: Request, use_id, username: str = Form(...), password: str = Form(...)):
    valid = authenticate(username, password)
    if valid:
        select_box_html, dir_name = get_english_projects()
        return HTMLResponse(content=html_english_webpage(select_box_html, dir_name, use_id, username), status_code=200)


@app.get('/{use_id}/{username}/Non_English/', response_class=HTMLResponse)
async def other_transcription(request: Request, use_id, username):
    select_box_html, language_box_html, dir_name = get_other_projects()
    return HTMLResponse(content=html_non_english_webpage(select_box_html, language_box_html, dir_name, use_id, username), status_code=200)

# ------------------------------start transcriptions------------------------------


@app.post("/{use_id}/{username}/English/{dir_name}/", response_class=HTMLResponse)
async def transcribe_english(*, project_name: str = Form(...), files: List[UploadFile] = File(...), dir_name, use_id, username):
    html, exception_html, username, use_id = start_transcribe(
        project_name, files, dir_name, use_id, username, "en")
    return HTMLResponse(content=html_english_completed(html, exception_html, username, use_id), status_code=200)


@app.post("/{use_id}/{username}/Other/{dir_name}/", response_class=HTMLResponse)
async def transcribe_other(*, project_name: str = Form(...), language: str = Form(...), files: List[UploadFile] = File(...), dir_name, use_id, username):
    config = Connect.config()
    languages = eval(config['Languages']['languages'])
    lang = languages['language_code'][languages['language'].index(language)]
    html, exception_html, username, use_id = start_transcribe(
        project_name, files, dir_name, use_id, username, lang)
    return HTMLResponse(content=html_non_english_completed(html, exception_html, username, use_id), status_code=200)

# ------------------------------download transcribed file------------------------------


@app.get('/download/{project_name}/{file_path}/', response_class=RedirectResponse)
async def download(project_name, file_path):
    config = Connect.config()
    s3 = Connect.s3()
    zip_url = s3.generate_presigned_url(ClientMethod='get_object',
                                        Params={
                                            'Bucket': config['S3SETTINGS']['bucket'],
                                            'Key': config['S3SETTINGS']['folder']+project_name+"/"+file_path
                                        },
                                        ExpiresIn=120)
    return RedirectResponse(zip_url)

# ------------------------------create new user------------------------------


@app.post('/create_new_users')
async def create_user(request: Request, email_id: str = Form(...), username: str = Form(...), password: str = Form(...)):
    mydb = Connect.db()
    new_user_cursor = mydb.cursor()
    query = "INSERT into Users(email_id,username,password) values(%s,%s,%s)"
    hash_password = bcrypt.hash(password)
    new_user = [(email_id, username, hash_password),]
    new_user_cursor.executemany(query, new_user)
    mydb.commit()
    return {'status': "Created New User", 'username': username, 'password': password}

# ------------------------------create new project page display------------------------------


@app.get('/{username}/create_new_project')
async def create_project(request: Request, username):
    return templates.TemplateResponse("new_project.html", {'request': request, 'username': username})


@app.get('/{use_id}/{username}/Non_English/create_new_project')
async def create_project(request: Request, username, use_id):
    return templates.TemplateResponse("new_project_NE.html", {'request': request, 'use_id': use_id, 'username': username})

# ------------------------------add new project------------------------------


@app.post('/{username}/add_new_project/')
async def new_project(request: Request, username, project_name: str = Form(...)):
    try:
        mydb = Connect.db()
        add_project_cursor = mydb.cursor()
        query = "INSERT into Projects(project_name,username, language) values(%s,%s,%s)"
        add_project = [(project_name, username, "English"),]
        add_project_cursor.executemany(query, add_project)
        mydb.commit()
        use_id = str(uuid.uuid4())[0:8]
        dir_name = str(uuid.uuid4())
        project_cursor = mydb.cursor()
        project_cursor.execute("select project_name from Projects;")
        select_box_html = ""
        for i in project_cursor:
            select_box_html += "<option value='"+i[0]+"'>"+i[0]+"</option>"
        return templates.TemplateResponse("added_new_project.html", {'request': request, 'username': username})
    except:
        return {'Error': 'Project already exists'}


@app.post('/{use_id}/{username}/Non_English/add_new_project/')
async def new_project(request: Request, username, project_name: str = Form(...)):
    try:
        mydb = Connect.db()
        add_project_cursor = mydb.cursor()
        query = "INSERT into Projects(project_name,username,language) values(%s,%s,%s)"
        add_project = [(project_name, username, "Non English"),]
        add_project_cursor.executemany(query, add_project)
        mydb.commit()
        use_id = str(uuid.uuid4())[0:8]
        dir_name = str(uuid.uuid4())
        project_cursor = mydb.cursor()
        project_cursor.execute("select project_name from Projects;")
        select_box_html = ""
        for i in project_cursor:
            select_box_html += "<option value='"+i[0]+"'>"+i[0]+"</option>"
        return templates.TemplateResponse("added_new_project.html", {'request': request, 'username': username})
    except:
        return {'Error': 'Project already exists'}

# ------------------------------view previous records------------------------------


@app.get('/{username}/projects/{use_id}', response_class=HTMLResponse)
async def get_projects(request: Request):
    mydb = Connect.db()
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    mydb = Connect.db()
    record_cursor = mydb.cursor()
    record_cursor.execute(
        "SELECT project_name FROM Projects WHERE language = 'English' ORDER BY id DESC;")
    table_rows = record_cursor.fetchall()
    project_dict = {'project_name': [], "count": []}
    for proj in table_rows:
        record_cursor.execute(
            "SELECT count(id) from Records WHERE project_name='"+proj[0]+"';")
        count_files = record_cursor.fetchall()
        project_dict['count'].append(count_files[0][0])
        project_dict['project_name'].append(proj[0])
    table = ""
    for i in range(len(project_dict['project_name'])):
        project_name = project_dict['project_name'][i]
        if project_dict['count'][i] > 0:
            no_count = str(project_dict['count'][i])+" Files"
        else:
            no_count = "No Files Yet"
        link = use_id+"/"+project_name
        table += "<tr><td>"+project_name+"</td><td><a href='" + \
            link+"' class='project-link'>"+no_count+"</td></tr>"
    return HTMLResponse(content=html_get_projects(table, use_id, username), status_code=200)


@app.get('/{username}/projects/{use_id}/{project_name}', response_class=HTMLResponse)
async def get_files(request: Request):
    mydb = Connect.db()
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    project_name = request.path_params['project_name']
    record_cursor = mydb.cursor()
    record_cursor.execute("SELECT * FROM Records WHERE project_name='" +
                          project_name+"' AND language = 'English' ORDER BY date_time DESC;")
    table_rows = record_cursor.fetchall()
    table = ""
    for re in table_rows:
        table += "<tr><td>"+re[1].strftime("%d-%m-%Y %I:%M %p") + \
            "</td><td>"+re[2]+"</td><td>"+re[4]+"</td>"
        table += "<td><a href='"+re[5]+"' class='dwn-link'>Download</a></td>"
        table += "<td><a href='"+re[6] + \
            "' class='dwn-link'>Download</a></td></tr>"
    return HTMLResponse(content=html_get_english_records(table, use_id, username, project_name), status_code=200)


@app.get('/{use_id}/{username}/Non_English/projects/', response_class=HTMLResponse)
async def get_projects(request: Request):
    mydb = Connect.db()
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    mydb = Connect.db()
    record_cursor = mydb.cursor()
    record_cursor.execute(
        "SELECT project_name FROM Projects WHERE language = 'Non English' ORDER BY id DESC;")
    table_rows = record_cursor.fetchall()
    project_dict = {'project_name': [], "count": []}
    for proj in table_rows:
        record_cursor.execute(
            "SELECT count(id) from Records WHERE project_name='"+proj[0]+"';")
        count_files = record_cursor.fetchall()
        project_dict['count'].append(count_files[0][0])
        project_dict['project_name'].append(proj[0])
    table = ""
    for i in range(len(project_dict['project_name'])):
        project_name = project_dict['project_name'][i]
        if project_dict['count'][i] > 0:
            no_count = str(project_dict['count'][i])+" Files"
        else:
            no_count = "No Files Yet"
        link = use_id+"/"+project_name
        table += "<tr><td>"+project_name+"</td><td><a href='" + \
            link+"' class='project-link'>"+no_count+"</td></tr>"
    return HTMLResponse(content=html_get_projects(table, use_id, username), status_code=200)


@app.get('/{use_id}/{username}/Non_English/projects/{use_id1}/{project_name}', response_class=HTMLResponse)
async def get_files(request: Request):
    mydb = Connect.db()
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    project_name = request.path_params['project_name']
    record_cursor = mydb.cursor()
    record_cursor.execute("SELECT * FROM Records WHERE project_name='" +
                          project_name+"' AND language != 'English' ORDER BY date_time DESC;")
    table_rows = record_cursor.fetchall()
    table = ""
    for re in table_rows:
        table += "<tr><td>"+re[1].strftime("%d-%m-%Y %I:%M %p") + \
            "</td><td>"+re[2]+"</td><td>"+re[4]+"</td>"
        table += "<td><a href='"+re[5]+"' class='dwn-link'>Download</a></td>"
        table += "<td><a href='"+re[6] + \
            "' class='dwn-link'>Download</a></td></tr>"
    return HTMLResponse(content=html_get_non_english_records(table, use_id, username, project_name), status_code=200)


# ------------------------------view errors from the API------------------------------


@app.get('/error/{lines}', response_class=HTMLResponse)
async def get_error(request: Request):
    try:
        error_file = open('logs/errors.log', 'r')
        error_lines = error_file.readlines()
        n = int(request.path_params['lines'])
        if len(error_lines) > n:
            error_lines = error_lines[-n:]
        count = 0
        logs = ""
        for log in error_lines:
            count += 1
            logs += "Line"+str(count)+": "+log+"<br/>"
        error_file.close()
    except:
        logs = "No Errors Logged Yet"
    return HTMLResponse(content=html_logs(logs), status_code=200)

# ------------------------------view logs from the API------------------------------


@app.get('/logs/{lines}', response_class=HTMLResponse)
async def get_logs(request: Request):
    log_file = open('logs/logs.log', 'r')
    log_lines = log_file.readlines()
    n = int(request.path_params['lines'])
    if len(log_lines) > n:
        log_lines = log_lines[-n:]
    count = 0
    logs = ""
    for log in log_lines:
        count += 1
        logs += "Line"+str(count)+": "+log+"<br/>"
    log_file.close()
    return HTMLResponse(content=html_logs(logs), status_code=200)
