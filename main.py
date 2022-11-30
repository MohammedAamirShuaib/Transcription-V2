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
    return templates.TemplateResponse("index.html", {'request': request, 'use_id': use_id})

# ------------------------------authenticate and view transcription page------------------------------


@app.post('/{use_id}/')
async def user(use_id, username: str = Form(...), password: str = Form(...)):
    select_box_html, dir_name = authenticate(username, password)
    return HTMLResponse(content=html_webpage(select_box_html, dir_name, use_id, username), status_code=200)

# ------------------------------start transcriptions------------------------------


@app.post("/{use_id}/{username}/{dir_name}/", response_class=HTMLResponse)
async def transcribe(*, project_name: str = Form(...), files: List[UploadFile] = File(...), dir_name, use_id, username):
    html, exception_html, username, use_id = start_transcribe(
        project_name, files, dir_name, use_id, username)
    return HTMLResponse(content=html_completed(html, exception_html, username, use_id), status_code=200)

# ------------------------------download transcribed file------------------------------


@app.get('/download/{project_name}/{file_path}/')
async def download(project_name, file_path):
    Connect.config()
    s3 = Connect.s3()
    zip_url = s3.generate_presigned_url(ClientMethod='get_object',
                                        Params={'Bucket': config['S3SETTINGS']['bucket'],
                                                'Key': config['S3SETTINGS']['folder']+project_name+"/"+file_path},
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

# ------------------------------add new project------------------------------


@app.post('/{username}/add_new_project')
async def new_project(username, project_name: str = Form(...)):
    mydb = Connect.db()
    add_project_cursor = mydb.cursor()
    query = "INSERT into Projects(project_name,username) values(%s,%s)"
    add_project = [(project_name, username),]
    add_project_cursor.executemany(query, add_project)
    mydb.commit()
    use_id = str(uuid.uuid4())[0:8]
    dir_name = str(uuid.uuid4())
    project_cursor = mydb.cursor()
    project_cursor.execute("select project_name from Projects;")
    select_box_html = ""
    for i in project_cursor:
        select_box_html += "<option value='"+i[0]+"'>"+i[0]+"</option>"
    return HTMLResponse(content=html_webpage(select_box_html, dir_name, use_id, username), status_code=200)

# ------------------------------view previous records------------------------------


@app.get('/{username}/projects/{use_id}', response_class=HTMLResponse)
async def get_projects(request: Request):
    mydb = Connect.db()
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    mydb = Connect.db()
    record_cursor = mydb.cursor()
    record_cursor.execute(
        "SELECT project_name FROM Projects ORDER BY id DESC;")
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
                          project_name+"' ORDER BY date_time DESC;")
    table_rows = record_cursor.fetchall()
    table = ""
    for re in table_rows:
        table += "<tr><td>"+re[1].strftime("%d-%m-%Y %I:%M %p") + \
            "</td><td>"+re[2]+"</td><td>"+re[4]+"</td>"
        table += "<td><a href='"+re[5]+"' class='dwn-link'>Download</a></td>"
        table += "<td><a href='"+re[6] + \
            "' class='dwn-link'>Download</a></td></tr>"
    return HTMLResponse(content=html_get_records(table, use_id, username, project_name), status_code=200)

# ------------------------------back to home page ------------------------------


@app.get('/home/{username}/{use_id}/')
async def user(request: Request):
    mydb = Connect.db()
    dir_name = str(uuid.uuid4())
    use_id = request.path_params['use_id']
    username = request.path_params['username']
    project_cursor = mydb.cursor()
    project_cursor.execute("select project_name from Projects;")
    select_box_html = ""
    for i in project_cursor:
        select_box_html += "<option value='"+i[0]+"'>"+i[0]+"</option>"
    return HTMLResponse(content=html_webpage(select_box_html, dir_name, use_id, username), status_code=200)

# ------------------------------view errors from the API------------------------------


@app.get('/error/{lines}', response_class=HTMLResponse)
async def get_error(request: Request):
    try:
        error_file = open('logs/error_log.txt', 'r')
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
