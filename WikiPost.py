import csv
import json
from pathlib import Path

import customtkinter as ctk
import pandas as pd
import requests

import data
import sumoApi

base_url = "https://mobilerndhub.sec.samsung.net/wiki/"
url = "https://mobilerndhub.sec.samsung.net/wiki/rest/api/content/"
session = requests.Session()
parent = 1423198376
secret_key = 'NTQxOTcxMjE0NDQ1OivbXJtAMJw/qfSZkEU1FOwQWc6X'
headers = {
    "Authorization": f"Bearer {secret_key}",
    'Accept': 'application/json',
    "Content-Type": "application/json",
    "X-Atlassian-Token": "no-check"
}


def compareCsv():
    file = open(f'output/ApiCallCount_v{data.inp["market"]["client"][0]}.csv', 'r')
    market = list(csv.reader(file))
    file.close()
    file = open(f'output/ApiCallCount_v{data.inp["sqe"]["client"][0]}.csv', 'r')
    sqe = list(csv.reader(file))
    file.close()

    out = []
    for i in range(1, len(market)):
        out.append([market[i][1], market[i][2], market[i][3], ''])
    for i in range(1, len(sqe)):
        is_new = True
        for j in range(1, len(market)):
            if sqe[i][1] == market[j][1]:
                is_new = False
                out[j - 1][3] = sqe[i][3]
                break
        if is_new:
            out.append([sqe[i][1], sqe[i][2], '', sqe[i][3]])
    # convert to html table
    title = ['url', 'code_type', data.inp["market"]["client"][0], data.inp["sqe"]["client"][0]]
    df = pd.DataFrame(out, columns=title)
    return df.to_html(index=False)


def urlToHtml(_url):
    return _url.replace("&", "&amp;")


def csvToHtml(file):
    df1 = pd.read_csv(file)
    return df1.to_html(index=False)


def html_data():
    return ('<ac:layout>\n'
            '  <ac:layout-section ac:type="two_equal">\n'
            '    <ac:layout-cell>\n'
            '      <h3>Basic information:</h3>\n'
            '      <ul>\n'
            '        <li>\n'
            f'          <strong>Start date: </strong><time datetime="{data.inp["report_time"]}"/></li>\n'
            '        <li>\n'
            '          <strong>Bixby Apps\' version:</strong><ul>\n'
            '            <li>Market<ul>\n'
            f'                <li>Agent/Client: <a href="{urlToHtml(data.inp["market"]["client"][1])}">version {data.inp["market"]["client"][0]}</a></li>\n'
            f'                <li>Wake-up: <a href="{urlToHtml(data.inp["market"]["wakeup"][1])}">version {data.inp["market"]["wakeup"][0]}</a></li>\n'
            f'                <li>Dictation: <a href="{urlToHtml(data.inp["market"]["dictation"][1])}">version {data.inp["market"]["dictation"][0]}</a></li>\n'
            '              </ul>\n'
            '            </li>\n'
            '            <li>SQE<ul>\n'
            f'                <li>Agent/Client: <a href="{urlToHtml(data.inp["sqe"]["client"][1])}">version {data.inp["sqe"]["client"][0]}</a></li>\n'
            f'                <li>Wake-up: <a href="{urlToHtml(data.inp["sqe"]["wakeup"][1])}">version {data.inp["sqe"]["wakeup"][0]}</a></li>\n'
            f'                <li>Dictation: <a href="{urlToHtml(data.inp["sqe"]["dictation"][1])}">version {data.inp["sqe"]["dictation"][0]}</a></li>\n'
            '              </ul>\n'
            '            </li>\n'
            '          </ul>\n'
            '        </li>\n'
            '      </ul>\n'
            '    </ac:layout-cell>\n'
            '    <ac:layout-cell>\n'
            '      <ul>\n'
            '        <li>\n'
            f'          <strong>Binary version: </strong><a class="external-link" href="{data.inp["binary"][0]}" style="text-align: left;">{data.inp["binary"][1]}</a>\n'
            '        </li>\n'
            '        <li>\n'
            f'          <strong>Device 1: </strong>{data.inp["model"]}\n'
            '          <ul>\n'
            f'            <li>Service-ID: {data.inp["market"]["service_id"]}</li>\n'
            '          </ul>\n'
            '        </li>\n'
            '        <li>\n'
            f'          <strong>Device 2: </strong>{data.inp["model"]}\n'
            '          <ul>\n'
            f'            <li>Service-ID:  {data.inp["sqe"]["service_id"]}</li>\n'
            '          </ul>\n'
            '        </li>\n'
            '      </ul>\n'
            '      <p>\n'
            '        <br/>\n'
            '      </p>\n'
            '    </ac:layout-cell>\n'
            '  </ac:layout-section>\n'
            '  <ac:layout-section ac:type="single">\n'
            '    <ac:layout-cell>\n'
            '      <ac:structured-macro ac:macro-id="f6d37b1d-5079-4463-a826-6c2c61423b55" ac:name="ui-tabs" ac:schema-version="1">\n'
            '        <ac:rich-text-body>\n'
            '          <ac:structured-macro ac:macro-id="a3e2681d-7e76-4e1a-8611-ea50a0265f05" ac:name="ui-tab" ac:schema-version="1">\n'
            '            <ac:parameter ac:name="title">AppVersion API POST call Test</ac:parameter>\n'
            '            <ac:rich-text-body>\n'
            '              <ul>\n'
            '                <li>\n'
            f'                  <strong>Reference</strong>: <a href="{urlToHtml(sumoApi.getAppVersionLink())}">AppVersion Sumologic search-link</a>\n'
            '                </li>\n'
            '                <li>\n'
            '                  <p>Screenshot</p>\n'
            '                  <ac:structured-macro ac:macro-id="98faf4a1-2a35-490c-a3c8-a557e86c354c" ac:name="expand" ac:schema-version="1">\n'
            '                    <ac:rich-text-body>\n'
            '                      <ul>\n'
            '                        <li>Sumologic log:</li>\n'
            '                      </ul>\n'
            '                      <p style="margin-left: 40.0px;">\n'
            '                        <ac:image>\n'
            f'                          <ri:attachment ri:filename="AppVersionApi_v{data.inp["sqe"]["client"][0]}.png"/>\n'
            '                        </ac:image>\n'
            '                      </p>\n'
            '                      <ul>\n'
            '                        <li>LogFilter Log:</li>\n'
            '                      </ul>\n'
            '                      <p style="margin-left: 40.0px;">\n'
            '                        <ac:image>\n'
            f'                          <ri:attachment ri:filename="AppVersionApi_LogFilter_v{data.inp["sqe"]["client"][0]}.png"/>\n'
            '                        </ac:image>\n'
            '                      </p>\n'
            '                    </ac:rich-text-body>\n'
            '                  </ac:structured-macro>\n'
            '                </li>\n'
            '              </ul>\n'
            '              <p>\n'
            '                <br/>\n'
            '              </p>\n'
            '              <ul>\n'
            '                <li>\n'
            '                  <p>Soft/Raw data</p>\n'
            '                  <p>\n'
            '                    <br/>\n'
            '                  </p>\n'
            f'                  {csvToHtml("output/AppVersionApi_v%s.csv" % data.inp["sqe"]["client"][0])}'
            '                  <p>\n'
            '                    <br/>\n'
            '                  </p>\n'
            '                </li>\n'
            '              </ul>\n'
            '            </ac:rich-text-body>\n'
            '          </ac:structured-macro>\n'
            '          <ac:structured-macro ac:macro-id="bd3046a1-db3d-4427-8313-50bf31ee3c3f" ac:name="ui-tab" ac:schema-version="1">\n'
            '            <ac:parameter ac:name="title">API call count comparison</ac:parameter>\n'
            '            <ac:rich-text-body>\n'
            '              <ul>\n'
            '                <li>\n'
            '                  <strong>Reference:</strong><ul>\n'
            '                    <li>Market version: \n'
            f'                      <a href="{urlToHtml(sumoApi.getApiCallCountLink(data.inp["market"]["service_id"], data.inp["market"]["client"][0]))}">Market - API call count Sumologic search-link</a>\n'
            '                    </li>\n'
            f'                    <li>SQE version: <a href="{urlToHtml(sumoApi.getApiCallCountLink(data.inp["sqe"]["service_id"], data.inp["sqe"]["client"][0]))}">SQE Release - API call count Sumologic search-link</a>\n'
            '                    </li>\n'
            '                  </ul>\n'
            '                </li>\n'
            '                <li>Screenshot</li>\n'
            '                <li>\n'
            '                  <ac:structured-macro ac:macro-id="3ed177aa-c711-43af-950a-290ab2d7dae8" ac:name="expand" ac:schema-version="1">\n'
            '                    <ac:rich-text-body>\n'
            '                      <ul>\n'
            '                        <li>Market version:</li>\n'
            '                      </ul>\n'
            '                      <p style="margin-left: 40.0px;">\n'
            '                        <ac:image>\n'
            f'                          <ri:attachment ri:filename="ApiCallCount_v{data.inp["market"]["client"][0]}.png"/>\n'
            '                        </ac:image>\n'
            '                      </p>\n'
            '                      <ul>\n'
            '                        <li>SQE version:</li>\n'
            '                      </ul>\n'
            '                      <p style="margin-left: 40.0px;">\n'
            '                        <ac:image>\n'
            f'                          <ri:attachment ri:filename="ApiCallCount_v{data.inp["sqe"]["client"][0]}.png"/>\n'
            '                        </ac:image>\n'
            '                      </p>\n'
            '                      <p>\n'
            '                        <br/>\n'
            '                      </p>\n'
            '                    </ac:rich-text-body>\n'
            '                  </ac:structured-macro>\n'
            '                </li>\n'
            '                <li>\n'
            '                  <p>Comparison</p>\n'
            '                  <ac:structured-macro ac:macro-id="3c40dd67-776a-4e1e-8820-b964d84be44a" ac:name="expand" ac:schema-version="1">\n'
            '                    <ac:rich-text-body>\n'
            '                      <p>\n'
            '                        <ac:structured-macro ac:macro-id="6f018275-a12a-4010-9b05-007110981368" ac:name="view-file" ac:schema-version="1">\n'
            '                          <ac:parameter ac:name="name">\n'
            f'                            <ri:attachment ri:filename="ApiCallCount_v{data.inp["market"]["client"][0]}.csv"/>\n'
            '                          </ac:parameter>\n'
            '                          <ac:parameter ac:name="height">150</ac:parameter>\n'
            '                        </ac:structured-macro>\n'
            '                        <ac:structured-macro ac:macro-id="c311ec98-1eaa-4e24-b670-23b04d66746a" ac:name="view-file" ac:schema-version="1">\n'
            '                          <ac:parameter ac:name="name">\n'
            f'                            <ri:attachment ri:filename="ApiCallCount_v{data.inp["sqe"]["client"][0]}.csv"/>\n'
            '                          </ac:parameter>\n'
            '                          <ac:parameter ac:name="height">150</ac:parameter>\n'
            '                        </ac:structured-macro>\n'
            '                      </p>\n'
            f'{compareCsv()}\n'
            '                    </ac:rich-text-body>\n'
            '                  </ac:structured-macro>\n'
            '                </li>\n'
            '              </ul>\n'
            '            </ac:rich-text-body>\n'
            '          </ac:structured-macro>\n'
            '          <ac:structured-macro ac:macro-id="fd6f62e2-ecdf-4dad-b784-c109e3ffc05c" ac:name="ui-tab" ac:schema-version="1">\n'
            '            <ac:parameter ac:name="title">SamsungAnalytics Log verification Test</ac:parameter>\n'
            '            <ac:rich-text-body>\n'
            '              <ul>\n'
            '                <li>\n'
            '                  <ac:structured-macro ac:macro-id="ce34f78a-0037-4c1e-93df-46d8f9b52f92" ac:name="children" ac:schema-version="2">\n'
            '                    <ac:parameter ac:name="all">true</ac:parameter>\n'
            '                  </ac:structured-macro>\n'
            '                  <ul>\n'
            '                    <li>\n'
            '                      <p>For each event-ID</p>\n'
            '                      <ul>\n'
            '                        <li>Conclusion\n'
            '                          <ul>\n'
            '                            <li>\n'
            '                              <p>\n'
            '                                <span style="color: rgb(51,153,102);">FOUND</span>\n'
            '                              </p>\n'
            '                            </li>\n'
            '                            <li>\n'
            '                              <span style="color: rgb(255,0,0);">NOT FOUND</span>\n'
            '                            </li>\n'
            '                          </ul>\n'
            '                        </li>\n'
            '                      </ul>\n'
            '                    </li>\n'
            '                  </ul>\n'
            '                </li>\n'
            '              </ul>\n'
            '            </ac:rich-text-body>\n'
            '          </ac:structured-macro>\n'
            '        </ac:rich-text-body>\n'
            '      </ac:structured-macro>\n'
            '    </ac:layout-cell>\n'
            '  </ac:layout-section>\n'
            '</ac:layout>')


def data_create():
    return {"title": "%s - BixB - Verification logs" % data.inp["report_time"],
            "type": "page",
            "space": {
                "key": "AICLIENTCO"
            },
            "status": "current",
            "ancestors": [
                {
                    "id": 1423198376
                }
            ],
            "body": {
                "storage": {
                    "value": html_data(),
                    "representation": "storage"
                }
            }
            }


def createPage():
    create_response = requests.post(url, headers=headers, data=json.dumps(data_create()))
    print(create_response.text)
    if create_response.status_code == 200:
        rp = json.loads(create_response.text)
        return rp
    else:
        return None


def uploadAttachment(page_id, file_name):
    headers_upload = {
        "Authorization": f"Bearer {secret_key}",
        "X-Atlassian-Token": "no-check"
    }
    f = open("output/%s" % file_name, 'rb')
    files = {"file": (file_name, f)}
    resp = requests.post(base_url + "rest/api/content/" + page_id + "/child/attachment", files=files,
                         headers=headers_upload)
    f.close()
    print(resp.text)


def get_last_posted():
    f = open("input/last_posted.json")
    lp = json.load(f)
    f.close()
    print(f'Last posted: {lp}')
    return lp['id']


def upload_file(_id):
    uploadAttachment(_id, f'AppVersionApi_v{data.inp["sqe"]["client"][0]}.png')
    uploadAttachment(_id, f'ApiCallCount_v{data.inp["market"]["client"][0]}.png')
    uploadAttachment(_id, f'ApiCallCount_v{data.inp["market"]["client"][0]}.csv')
    uploadAttachment(_id, f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.png')
    uploadAttachment(_id, f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.csv')
    f = Path(f'output/AppVersionApi_v{data.inp["sqe"]["client"][0]}.png')
    if f.is_file():
        uploadAttachment(_id, f'AppVersionApi_LogFilter_v{data.inp["sqe"]["client"][0]}.png')


def get_file_exist(file_path):
    if Path(f'output/{file_path}').is_file():
        return '✅'
    return '❎'


def save_last_posted(rp):
    f = open("input/last_posted.json", "w")
    save_data = {'id': rp['id'], 'link': rp['_links']['base'] + rp['_links']['webui']}
    print(save_data)
    json.dump(save_data, f)
    f.close()


class MainScreen:
    def post(self):
        print(html_data())
        rp = createPage()
        if rp is None:
            return
        self.id = rp['id']
        save_last_posted(rp)

    def upload(self):
        if self.id == '':
            return
        upload_file(self.id)

    def __init__(self, master):
        self.content_frame = ctk.CTkFrame(master)
        self.content_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(7, minsize=60)
        self.content_frame.grid_rowconfigure(8, minsize=60)
        ctk.CTkLabel(self.content_frame, text=f'AppVersionApi_v{data.inp["sqe"]["client"][0]}.png') \
            .grid(row=0, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'AppVersionApi_v{data.inp["sqe"]["client"][0]}.png')) \
            .grid(row=0, column=1)
        ctk.CTkLabel(self.content_frame, text=f'AppVersionApi_LogFilter_v{data.inp["sqe"]["client"][0]}.png') \
            .grid(row=1, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'AppVersionApi_LogFilter_v{data.inp["sqe"]["client"][0]}.png')) \
            .grid(row=1, column=1)
        ctk.CTkLabel(self.content_frame, text=f'AppVersionApi_v{data.inp["sqe"]["client"][0]}.csv') \
            .grid(row=2, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'AppVersionApi_v{data.inp["sqe"]["client"][0]}.csv')) \
            .grid(row=2, column=1)
        ctk.CTkLabel(self.content_frame, text=f'ApiCallCount_v{data.inp["market"]["client"][0]}.png') \
            .grid(row=3, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'ApiCallCount_v{data.inp["market"]["client"][0]}.png')) \
            .grid(row=3, column=1)
        ctk.CTkLabel(self.content_frame, text=f'ApiCallCount_v{data.inp["market"]["client"][0]}.csv') \
            .grid(row=4, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'ApiCallCount_v{data.inp["market"]["client"][0]}.csv')) \
            .grid(row=4, column=1)
        ctk.CTkLabel(self.content_frame, text=f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.png') \
            .grid(row=5, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.png')) \
            .grid(row=5, column=1)
        ctk.CTkLabel(self.content_frame, text=f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.csv') \
            .grid(row=6, column=0)
        ctk.CTkLabel(self.content_frame, text=get_file_exist(f'ApiCallCount_v{data.inp["sqe"]["client"][0]}.csv')) \
            .grid(row=6, column=1)

        ctk.CTkButton(self.content_frame, text='Post to wiki', command=self.post, width=180, height=40) \
            .grid(row=7, column=0, columnspan=2)
        ctk.CTkButton(self.content_frame, text='Upload attachment', command=self.upload, width=180, height=40) \
            .grid(row=8, column=0, columnspan=2)
        self.id = get_last_posted()


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
