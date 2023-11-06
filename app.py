import logging
import os

from dotenv import load_dotenv
from flask import Flask, render_template

from external_apis.alfa_requests.fetchers import FetchGroup
from services.balance import get_balance_info_for_last_week
from services.recordings import get_recordings_for_last_week
from services.reports import get_reports_for_last_week

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s')

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s')

load_dotenv()
app = Flask(__name__)


@app.route('/get_reports', methods=['GET'])
def view_reports():
    data = get_reports_for_last_week()
    unique_list = unique(data)
    return render_template('reports.html', data=data, unique_list=unique_list)

def unique(input_list):
    unique_groups = set()
    result_list = []
    for item in input_list:
        # Проверяем, был ли уже добавлен "group_name" в множество
        if item["group_name"] not in unique_groups:
            # Добавляем "group_name" в множество
            unique_groups.add(item["group_name"])
            # Добавляем соответствующий элемент в результирующий список
            result_list.append({"group_name": item["group_name"], "date": item["date"]})
    return result_list

@app.route('/get_balance', methods=['GET'])
def view_balance():
    data = get_balance_info_for_last_week()
    return render_template('balance.html', data=data)\

@app.route('/get_recordings', methods=['GET'])
def view_recordings():
    data = get_recordings_for_last_week()
    return render_template('recordings.html', data=data)


@app.route('/', methods=['GET'])
def main():
    if os.getenv("DEV_MODE") == "1":
        groups = FetchGroup.all()
        return render_template('index.html', data = groups)
    else:
        return render_template('index.html', data=None)

if os.getenv("DEV_MODE") == "1":
    if __name__ == '__main__':
        app.run()
