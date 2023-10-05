import json


def loadInputData():
    f = open("input/input.json")
    _inp = json.load(f)
    f.close()
    return _inp


def writeInputData(_inp):
    f = open("input/input.json", "w")
    json.dump(_inp, f, indent=3)
    f.close()


inp = loadInputData()

# *****************************************************************************************
app_version_search = {'query': '_index=partition_stg_tier2 and _sourceCategory=*prv-mbr* '
                               '"/member/api/v1/users/' + inp['user_id'] +
                               '/appversion" and "mobile" and _sourceName="/opt/bixby/member/logs/provisioning-api'
                               '-server.log"',
                      'from': inp['install_time'][0],
                      'to': inp['install_time'][1],
                      'timeZone': 'Asia/Ho_Chi_Minh'}
sqe_query = '''_index=partition_stg_tier2 "%s"
| parse "\\"resultCode\\\\\\":\\\\\\"*\\\\\\"" as resultCode nodrop
| json field=_raw "header.bixbyServiceId" as serviceId
| where serviceId matches "%s"
| json field=_raw "header.bixbyVersion" as version
| where matches (version, "%s")
| json "resp.body.result.resultCode" as resultCode
| json field=_raw "custom.url" as url
| parse regex field=resultCode "\\d{4}\\.(?<resultCode>\\d{3})"
| if(resultCode matches "2*","2XX",if(resultCode matches "3*","3XX",if(resultCode matches "4*","4XX",if(resultCode matches "5*","5XX",resultCode)))) as code_type
| count by version, url, code_type
| sort by version, url''' % (inp['sqe']['service_id'], inp['sqe']['service_id'], inp['sqe']['client'][0])

# marketApiCallCountQuery
market_query = '''_index=partition_stg_tier2 "%s"
| parse "\\"resultCode\\\\\\":\\\\\\"*\\\\\\"" as resultCode nodrop
| json field=_raw "header.bixbyServiceId" as serviceId
| where serviceId matches "%s"
| json field=_raw "header.bixbyVersion" as version
| where matches (version, "%s")
| json "resp.body.result.resultCode" as resultCode
| json field=_raw "custom.url" as url
| parse regex field=resultCode "\\d{4}\\.(?<resultCode>\\d{3})"
| if(resultCode matches "2*","2XX",if(resultCode matches "3*","3XX",if(resultCode matches "4*","4XX",if(resultCode matches "5*","5XX",resultCode)))) as code_type
| count by version, url, code_type
| sort by version, url''' % (inp['market']['service_id'], inp['market']['service_id'], inp['market']['client'][0])

# For Weblink
web_end_point = "https://bixby-stg.us2.sumologic.com/ui/#/search/create?"
version_query = \
    '_index%3Dpartition_stg_tier2%20and%20_sourceCategory%3D*prv-mbr*%20%22%2Fmember%2Fapi%2Fv1%2Fusers%2F%7B%7BuserId%7D%7D%2Fappversion%22%0AAND%20%22mobile%22%0AAND%20_sourceName%3D%22%2Fopt%2Fbixby%2Fmember%2Flogs%2Fprovisioning-api-server.log%22'
call_count_query = \
    '_index%3Dpartition_stg_tier2%20%2F*_sourceCategory%3D*msf*%20*%2F%20%7B%7BserviceId1%7D%7D%0A%2F%2F_sourceCategory%3D*%2Fprod%2Fdefault%2Fmsf-*%20%7B%7BserviceId1%7D%7D%0A%7C%20parse%20%22%5C%22resultCode%5C%5C%5C%22%3A%5C%5C%5C%22*%5C%5C%5C%22%22%20as%20resultCode%20nodrop%0A%7C%20json%20field%3D_raw%20%22header.bixbyServiceId%22%20as%20serviceId%0A%7C%20where%20serviceId%20matches%20%7B%7BserviceId1%7D%7D%0A%7C%20json%20field%3D_raw%20%22header.bixbyVersion%22%20as%20version%0A%7C%20where%20matches%20(version%2C%20%7B%7Bversion1%7D%7D)%0A%7C%20json%20%22resp.body.result.resultCode%22%20as%20resultCode%0A%7C%20json%20field%3D_raw%20%22custom.url%22%20as%20url%0A%7C%20parse%20regex%20field%3DresultCode%20%22%5Cd%7B4%7D%5C.(%3F%3CresultCode%3E%5Cd%7B3%7D)%22%0A%7C%20%20if(resultCode%20matches%20%222*%22%2C%222XX%22%2Cif(resultCode%20matches%20%223*%22%2C%223XX%22%2Cif(resultCode%20matches%20%224*%22%2C%224XX%22%2Cif(resultCode%20matches%20%225*%22%2C%225XX%22%2CresultCode))))%20as%20code_type%0A%2F%2F%7C%20where%20code_type%3D%224XX%22%20or%20code_type%3D%225XX%22%0A%2F%2F%7C%20timeslice%205m%0A%7C%20count%20by%20version%2C%20url%2C%20code_type%0A%7C%20sort%20by%20version%2C%20url%0A%2F%2F%7C%20transpose%20row%20url%20column%20code_type%2C%20version'

sqeSearch = {'query': sqe_query,
             'from': inp['test_time'][0],
             'to': inp['test_time'][1],
             'timeZone': 'Asia/Ho_Chi_Minh'}

marketSearch = {'query': market_query,
                'from': inp['test_time'][0],
                'to': inp['test_time'][1],
                'timeZone': 'Asia/Ho_Chi_Minh'}


def reloadInputData():
    global inp, app_version_search, sqe_query, market_query
    old = inp
    inp = loadInputData()
    if old == inp:
        return
    app_version_search = {'query': '_index=partition_stg_tier2 and _sourceCategory=*prv-mbr* '
                                   '"/member/api/v1/users/' + inp['user_id'] +
                                   '/appversion" and "mobile" and _sourceName="/opt/bixby/member/logs/provisioning-api'
                                   '-server.log"',
                          'from': inp['install_time'][0],
                          'to': inp['install_time'][1],
                          'timeZone': 'Asia/Ho_Chi_Minh'}
    sqe_query.replace(old['sqe']['service_id'], inp['sqe']['service_id'])\
        .replace(old['sqe']['client'][0], inp['sqe']['client'][0])
    market_query.replace(old['market']['service_id'], inp['market']['service_id'])\
        .replace(old['market']['client'][0], inp['market']['client'][0])


# The API endpoint for your account
SUMO_API_URL = 'https://api.us2.sumologic.com'
# The API requires some headers be set
# basicAuth = base64.b64encode("{AccessID}:{AccessKey}".encode('ascii')).decode("ascii")
basicAuth = \
    'c3U3ZlRNV3RLeWw4Zjk6c29Mc0JWWGpXazlDR3ViQnpuNWlka2xVMDRZQVJBRmdkNUpqQlR0ekltdFhJS1dLc2pScmNjZkpKRXd6MDk0OA=='
headers = {'Authorization': 'Basic %s' % basicAuth, 'Content-Type': 'application/json', 'Accept': 'application/json'}

# GUI
main_width = 390
# make sure main_height is not small
main_height = 320
space = 10
btn_width = int((main_width - space * 3) / 2)
btn_height = 40
btn_start = int(main_width / 2 - btn_width / 2)
column1_start = space
column2_start = int(main_width / 2 + space / 2)
