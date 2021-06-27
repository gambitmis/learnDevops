from flask import Flask,render_template,request,url_for,stream_with_context,redirect
import socket
import datetime
import platform
import pytz
import os
import psutil
import multiprocessing
import speedtest
import inspect
import pymysql.cursors

app = Flask(__name__)

# Connect to the database
def connectDB():
    connection = pymysql.connect(host='db',
                                user='root',
                                password='ITI%C10uD',
                                database='demo1',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

def getHostnameAndIpAddr():
    try:
        hostName = socket.gethostname()
        hostIP = socket.gethostbyname(hostName)
        return hostName, hostIP
    except:
        hostName = "Error"
        hostIP = "Error"
        return hostName, hostIP

"""
@app.route("/")
def show():
    test = request.environ
    return "{}".format(test)
"""
@app.errorhandler(404)
def handle_404(e):
    return 'Not found, but we HANDLED IT'

@app.route("/")
def showtHttpReq():
    # Flask Env
    httpRequest = request.environ
    # Hostname and IPaddr
    hostName, hostIP = getHostnameAndIpAddr()

    # datetime 
    tz_th = pytz.timezone('Asia/Bangkok')
    now_utc = datetime.datetime.now(tz=pytz.UTC)
    now_th = now_utc.astimezone(tz_th)

    # Opertaion system info
    os = platform.platform()
    #processor = platform.processor()
    #machine = platform.machine()
    #system = platform.system()
    uname = platform.uname()
    cpu_count = multiprocessing.cpu_count()
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage1 = (load1/multiprocessing.cpu_count()) * 100
    cpu_usage5 = (load5/multiprocessing.cpu_count()) * 100
    cpu_usage15 = (load15/multiprocessing.cpu_count()) * 100
    memUsage = psutil.virtual_memory()[2]
    #test = memUsage

    flask_env = {
        "sockerInfo":httpRequest['werkzeug.socket'],
        "httpMethod":httpRequest['REQUEST_METHOD'],
        "requestUri":httpRequest['REQUEST_URI'],
        "remoteAddr":httpRequest['REMOTE_ADDR'],
        "remotePort":httpRequest['REMOTE_PORT'],
        "httpHost":httpRequest['HTTP_HOST'],
        "userAgent":httpRequest['HTTP_USER_AGENT'],
        "httpAccept":httpRequest['HTTP_ACCEPT'],
        "httpAcceptEncoding":httpRequest['HTTP_ACCEPT_ENCODING'],
        "serverProto":httpRequest['SERVER_PROTOCOL'],
    }

    os_env = {
        "uname": uname,
        "cpuCount":cpu_count,
        "cpuLoad1":load1,
        "cpuLoad5":load5,
        "cpuLoad15":load15,
        "memUsage":memUsage,
        "now_th":now_th,
        "now_utc":now_utc,
        "hostName":hostName,
        "hostIP":hostIP
    }

    return render_template("httpReq.html",flask_env=flask_env,os_env=os_env)


"""
SPEEDTEST
https://pyshark.com/test-internet-speed-using-python/
https://www.geeksforgeeks.org/test-internet-speed-using-python/
https://github.com/sivel/speedtest-cli/wiki
https://www.geeksforgeeks.org/python-ways-to-create-a-dictionary-of-lists/
"""


@app.route('/speedtest/run')
def runspdtest():
    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    #s.get_best_server(s.set_mini_server("http://speedtest-hyi1.ais-idc.net"))
    s.download(threads=threads)
    s.upload(threads=threads)
    #s.results.share()
    res = s.results.dict()
    return render_template("speedtest.html",res=res)


@app.route('/speedtest/list')
def listspdtest():
    s = speedtest.Speedtest()
    listspdtest = s.get_servers()
    return render_template("listSpeedtestServer.html",listspdtest=listspdtest)

@app.route('/speedtest',methods=['GET','POST'])
def spdtest():
    res ={}
    if request.method == 'POST':
        button='RE-RUN'
        servers = []
        threads = None
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)
        s.results.share()
        res = s.results.dict()
    elif request.method == 'GET':
        button='RUN'
    else:
        button='ERROR'
    return render_template("speedtest.html",button=button,res=res)

@app.route('/speedtest/save', methods=['GET'])
def spdtestSave():
    
    download = int(float(request.args.get('download')))
    upload = int(float(request.args.get('upload')))
    ping = request.args.get('ping')
    zio = request.args.get('zio')
    
    dbconn = connectDB()
    with dbconn:
        with dbconn.cursor() as cursor:
            sql = "INSERT INTO `speedtest` (`donwload`, `upload`, `ping`, `datetime`) VALUES ((%s / 1000000), (%s / 1000000), %s, %s)"
            cursor.execute(sql,(download,upload,ping,zio))
            dbconn.commit() 
    return redirect(url_for('spdtest'))

@app.route('/nmap')
def nmap():
    return "ffff"


