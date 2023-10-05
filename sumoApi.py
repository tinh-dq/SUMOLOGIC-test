import csv
import json
import logging
import sys
import time
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
import delorean
import mss
import mss.tools
import pyperclip
import requests
from dateutil import parser

import data

# To get all logs change level='DEBUG'
logging.basicConfig(filename='output/sumo_search_job.log', level='DEBUG',
                    format='%(asctime)s %(levelname)s: %(message)s')
logging.info('*************STARTING REQUEST*************')

# The API is going to send back cookies after you make the first request.  Those cookies are required to further
# interact, so we use a session to save those cookies.
session = requests.Session()


# Takes a search job, creates it and returns the ID.
def executeSearchJob(search_job):
    logging.info('executing search job: ' + json.dumps(search_job))
    r = session.post(data.SUMO_API_URL + '/api/v1/search/jobs', data=json.dumps(search_job), headers=data.headers)
    if r.status_code != 202:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to execute search job! ' + r.text)
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response ' + json.dumps(response))
        return response['id']


# Polls the search job id until it completes.  Check's the status every 5 seconds.
def pollSearchJob(job_id):
    logging.info('checking status of search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id)
    while True:
        if r.status_code != 200:
            logging.error('Got back status code ' + str(r.status_code))
            logging.error('Unable to check status of searchJob ' + job_id + '!')
            sys.exit(1)
        else:
            response = json.loads(r.text)
            # logging.info('Got back response for search job id ' + job_id + ' ' + json.dumps(response))
            status = response['state']
            if status == 'DONE GATHERING RESULTS':
                logging.info('DONE GATHERING RESULTS')
                break
            else:
                logging.info('GATHERING RESULTS wait 5s')
            time.sleep(5)
            r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id)


# Gets the record count of the job
def getRecordCount(job_id):
    logging.info('Getting record count for search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id)
    if r.status_code != 200:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to get record count of searchJob ' + job_id + '!')
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response for search job id ' + job_id + ' ' + json.dumps(response))
        return response['recordCount']


# Gets the message count
def getMessageCount(job_id):
    logging.info('Getting message count for search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id)
    if r.status_code != 200:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to get record count of searchJob ' + job_id + '!')
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response for search job id ' + job_id + ' ' + json.dumps(response))
        return response['messageCount']


# Get the first message
def getFirstMessage(job_id):
    logging.info('Getting first message for search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id + '/messages?offset=0&limit=1')
    if r.status_code != 200:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to get record count of searchJob ' + job_id + '!')
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response for search job id ' + job_id + ' ' + json.dumps(response))
        return response['messages']


# Get the all messages
# AppVersion API
def getAppVersionCsv(
        job_id,
        file_name='output/AppVersionApi_v' + data.inp['sqe']['client'][0] + '.csv'
):
    logging.info('Getting messages for search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id + '/messages?offset=0&limit=100')
    if r.status_code != 200:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to get record count of searchJob ' + job_id + '!')
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response for search job id ' + job_id + ' \n' + json.dumps(response))
        csv_doc = [['_messagetimems', '_messagetime', '_raw']]
        for x in response['messages']:
            tms = int(x['map']["_messagetime"])
            dt = datetime.fromtimestamp(tms / 1000)
            t = dt.strftime("%m/%d/%Y %I:%M:%S.%f")[:-3] + dt.strftime(" %p +0700")
            csv_doc.append([tms, t, x['map']["_raw"]])
        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_doc)
        return csv_doc


# Get all records
def getApiCallCountCsv(job_id, file_name):
    logging.info('Getting records for search job: ' + job_id)
    r = session.get(data.SUMO_API_URL + '/api/v1/search/jobs/' + job_id + '/records?offset=0&limit=100')
    if r.status_code != 200:
        logging.error('Got back status code ' + str(r.status_code))
        logging.error('Unable to get record count of searchJob ' + job_id + '!')
        sys.exit(1)
    else:
        response = json.loads(r.text)
        logging.debug('Got back response for search job id ' + job_id + ' \n' + json.dumps(response))
        csv_doc = [['version', 'url', 'code_type', '_count']]
        for x in response['records']:
            csv_doc.append([x['map']['version'], x['map']['url'], x['map']['code_type'], x['map']['_count']])
        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_doc)
        return csv_doc


# AppVersion API
def appVersionApiSearch():
    print("Getting CSV AppVersionAPI")
    # We create the search job and are given back the ID
    search_job_id = executeSearchJob(data.app_version_search)
    # We poll the search job every 5 seconds until it is complete, or fails.
    pollSearchJob(search_job_id)
    # This will print the number of messages that were found that matched.
    # count = getMessageCount(search_job_id)
    # logging.info('Found %s messages ', count)
    logging.debug('Messages:\n%s' % json.dumps(getAppVersionCsv(search_job_id)))
    tk.messagebox.showinfo('Done!', 'Get CSV AppVersionAPI done!')


# SQE Search
def sqeSearch():
    print("Getting CSV API call count SQE")
    search_job_id = executeSearchJob(data.sqeSearch)
    pollSearchJob(search_job_id)
    file_name = 'output/ApiCallCount_v%s.csv' % data.inp['sqe']['client'][0]
    logging.info('Messages:\n%s' % json.dumps(getApiCallCountCsv(search_job_id, file_name)))
    tk.messagebox.showinfo('Done!', 'Get CSV API call count SQE done!')


# Market Search
def marketSearch():
    print("Getting CSV API call count Market")
    search_job_id = executeSearchJob(data.marketSearch)
    pollSearchJob(search_job_id)
    file_name = 'output/ApiCallCount_v%s.csv' % data.inp['market']['client'][0]
    logging.info('Messages:\n%s' % json.dumps(getApiCallCountCsv(search_job_id, file_name)))
    tk.messagebox.showinfo('Done!', 'Get CSV API call count Market done!')


def timestamp(dt):
    return delorean.Delorean(dt, timezone='Asia/Ho_Chi_Minh').epoch * 1000


def getApiCallCountLink(service_id, version):
    query = data.call_count_query
    start_time = timestamp(parser.parse(data.inp['test_time'][0]))
    end_time = timestamp(parser.parse(data.inp['test_time'][1]))
    parameters = 'serviceId1:%s,version1:%s' % (service_id, version)
    link = '%squery=%s&startTime=%s&endTime=%s&parameters=%s' % (
        data.web_end_point, query, start_time, end_time, parameters)
    return link


def getAppVersionLink():
    query = data.version_query
    start_time = timestamp(parser.parse(data.inp['install_time'][0]))
    end_time = timestamp(parser.parse(data.inp['install_time'][1]))
    parameters = 'userId:%s' % data.inp['user_id']
    link = '%squery=%s&startTime=%s&endTime=%s&parameters=%s' % (
        data.web_end_point, query, start_time, end_time, parameters)
    return link


edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))


def goAppVersionLink():
    url = getAppVersionLink()
    logging.info("AppVersionLink:\n" + url)
    msg_box = tk.messagebox.askyesnocancel('AppVersion url', 'Open url on browser?'
                                                             '\nYes: Open, No: Add in clipboard')
    if msg_box:
        webbrowser.get('edge').open(url)
    elif msg_box is not None:
        pyperclip.copy(url)


def goApiCallCountSQELink():
    url = getApiCallCountLink(data.inp['sqe']['service_id'], data.inp['sqe']['client'][0])
    logging.info("sqeLink:\n" + url)
    msg_box = tk.messagebox.askyesnocancel('API call count SQE url', 'Open url on browser?'
                                                                     '\nYes: Open, No: Add in clipboard')
    if msg_box:
        webbrowser.get('edge').open(url)
    elif msg_box is not None:
        pyperclip.copy(url)


def goApiCallCountMarketLink():
    url = getApiCallCountLink(data.inp['market']['service_id'], data.inp['market']['client'][0])
    logging.info("marketLink:\n" + url)
    msg_box = tk.messagebox.askyesnocancel('API call count market url', 'Open url on browser?'
                                                                        '\nYes: Open, No: Add in clipboard')
    if msg_box:
        webbrowser.get('edge').open(url)
    elif msg_box is not None:
        pyperclip.copy(url)


def captureScreen(file_name):
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }

        # Grab the data
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_name)


def captureAppVersion():
    captureScreen('output/AppVersionApi_v%s.png' % data.inp['sqe']['client'][0])


def captureSQE():
    captureScreen('output/ApiCallCount_v%s.png' % data.inp['sqe']['client'][0])


def captureMarket():
    captureScreen('output/ApiCallCount_v%s.png' % data.inp['market']['client'][0])


class MainScreen:

    def __init__(self, master):
        self.frame_content = ctk.CTkFrame(master)
        self.frame_content.grid(row=0, column=0, sticky='nswe')

        self.frame_content.grid_columnconfigure(0, weight=1)
        self.frame_content.grid_columnconfigure(1, weight=1)
        for _ in range(7):
            self.frame_content.grid_rowconfigure(_, minsize=60)
        self.frame_content.configure(padx=10, pady=10)
        ctk.CTkButton(self.frame_content, text='AppVersion CSV', command=appVersionApiSearch, width=180, height=40) \
            .grid(row=0, column=0, columnspan=2)
        ctk.CTkButton(self.frame_content, text='ApiCallCount SQE CSV', command=sqeSearch, width=180, height=40) \
            .grid(row=1, column=0, columnspan=2)
        ctk.CTkButton(self.frame_content, text='ApiCallCount Market CSV', command=marketSearch, width=180, height=40) \
            .grid(row=2, column=0, columnspan=2)

        ctk.CTkButton(self.frame_content, text='AppVersion POST call Link', command=goAppVersionLink, width=180,
                      height=40).grid(row=3, column=0)
        ctk.CTkButton(self.frame_content, text='ApiCallCount SQE Link', command=goApiCallCountSQELink, width=180,
                      height=40).grid(row=4, column=0)
        ctk.CTkButton(self.frame_content, text='ApiCallCount Market Link', command=goApiCallCountMarketLink, width=180,
                      height=40).grid(row=5, column=0)

        ctk.CTkButton(self.frame_content, text='Capture 2nd screen', command=captureAppVersion, width=180, height=40) \
            .grid(row=3, column=1)
        ctk.CTkButton(self.frame_content, text='Capture 2nd screen', command=captureSQE, width=180, height=40) \
            .grid(row=4, column=1)
        ctk.CTkButton(self.frame_content, text='Capture 2nd screen', command=captureMarket, width=180, height=40) \
            .grid(row=5, column=1)


if __name__ == "__main__":
    window = ctk.CTk()
    window.title('Bixby SUMOLOGIC')
    window.geometry('390x320')
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    content = MainScreen(window)
    window.mainloop()
