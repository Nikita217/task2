import os, json
from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_data = json.loads(os.environ["CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xtKKUV4879T79pb4tytj1BhsSALAP_X4vHdQVAbLXAc").sheet1

@app.route('/')
def index():
    tasks = sheet.get_all_records()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.json.get("task")
    if task:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records = sheet.get_all_records()
        new_id = len(records) + 1
        sheet.append_row([new_id, task, "", now])
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})

@app.route('/done', methods=['POST'])
def done():
    task_id = int(request.json.get("id"))
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row["ID"] == task_id and not row["Done"]:
            sheet.update_cell(i, 3, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return jsonify({"status": "done"})
    return jsonify({"status": "not_found"})

@app.route('/delete', methods=['POST'])
def delete():
    task_id = int(request.json.get("id"))
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row["ID"] == task_id:
            sheet.delete_row(i)
            return jsonify({"status": "deleted"})
    return jsonify({"status": "not_found"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
