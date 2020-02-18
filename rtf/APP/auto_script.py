import json
import time
import subprocess
import argparse
from enum import Enum


MASTER_CONFIG_FILENAME = "master_config_file.json"
CONTROL_CONFIG_FILENAME = "control_config_file.json"


class Configs(Enum):
    site_id = "site"
    device_id = "SCT-81"
    host = "10.9.1.6"
    port = 1883
    webui_host = "127.0.0.1"
    webui_port = 8081

    def __str__(self):
        return f'{self.value}'


def read_template_config(filename):
    with open(filename) as conf:
        _conf = json.load(conf)

    return _conf


def create_master_config_file(sites, master_id,
                              host=None,
                              port=None,
                              webui_host=None,
                              webui_port=None):
    config = {"broker_host": Configs.host.value if host is None else host,
              "broker_port": Configs.port.value if port is None else port,
              "device_id": master_id,
              "sites": sites,
              "webui_host": Configs.webui_host.value if webui_host is None else webui_host,
              "webui_port": Configs.webui_port.value if webui_port is None else webui_port,
              "Handler": "HTO92-20F",
              "Environment": "F1",
              "jobsource": "filesystem",
              "jobformat": "xml.micronas",
              "skip_jobdata_verification": True,
              "filesystemdatasource.path": "./tests",
              "filesystemdatasource.jobpattern": "le306426001.xml"
              }

    dump_to_file(True, config)


def create_control_config_file(num, master_id, host=None, port=None):
    config = {"broker_host": Configs.host.value,
              "broker_port": Configs.port.value,
              "device_id": master_id,
              "site_id": num
              }

    dump_to_file(False, config)


def dump_to_file(is_master, config):
    if is_master:
        file_name = MASTER_CONFIG_FILENAME
    else:
        file_name = CONTROL_CONFIG_FILENAME

    json_c = json.dumps(config, indent=4)

    with open(file_name, 'w') as f:
        f.write(json_c)


def file_parser():
    parser = argparse.ArgumentParser(prog="auto-script.py", usage="%(prog)s [app typ: 'master', 'control'] [master id]")
    parser.add_argument('typ', help='application typ')
    parser.add_argument('mid', help='master id')
    parser.add_argument('-conf', help='define if only the config file must to be generated', action='count', default=0)
    parser.add_argument('-host', help='host ip')
    parser.add_argument('-port', help='host port', type=int)
    parser.add_argument('-web_host', help='webui host name')
    parser.add_argument('-web_port', help='webui host port', type=int)
    parser.add_argument('-num_apps', help='num of to generate apps', default=1, type=int)
    parser.add_argument('-handler', help='handler', default=0)
    parser.add_argument('-env', help='env', default=0)
    parser.add_argument('-browser', help='activate browser', action='count', default=0)

    args = parser.parse_args()
    return args


def kill_process(process_list):
    import sys
    for proc in process_list:
        proc.kill()

    sys.exit(0)


def start_apps():
    args = file_parser()
    num_apps = args.num_apps
    app_typ = args.typ
    master_id = args.mid
    pid_list = []
    run = True

    print(app_typ)
    if app_typ == 'master':
        # generate list of site ids
        sites = [str(x) for x in range(num_apps)]
        create_master_config_file(sites, master_id, host=args.host, port=args.port,
                                  webui_host=args.web_host, webui_port=args.web_port)
        # TODO: only one master is supported for now
        if not args.conf:
            master = subprocess.Popen("py launch_master.py --f master_config_file.json")
            pid_list.append(master)
            time.sleep(2)
            # start webserver
            if args.browser:
                configuration = read_template_config(MASTER_CONFIG_FILENAME)
                webui_host = configuration["webui_host"]
                webui_port = configuration["webui_port"]
                subprocess.run(f"start http://{webui_host}:{webui_port}", shell=True)
        else:
            run = False

    elif app_typ == 'control':
        for id in range(num_apps):
            create_control_config_file(str(id), master_id, host=args.host, port=args.port)
            if not args.conf:
                control = subprocess.Popen("py launch_control.py --f control_config_file.json")
                pid_list.append(control)
                time.sleep(2)
            else:
                run = False

    while run:
        input("press enter to terminate")
        break

    if not args.conf:
        kill_process(pid_list)


start_apps()
