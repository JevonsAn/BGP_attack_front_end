# -*- coding: UTF-8 -*-
import json

path_peizhi = "peizhi/"
f1 = open(path_peizhi + "host-asinfo.ip_level", "r")  # "BGP # 1.5.0.2/29|1.2.0.19/29 # 1005 # ASN-1005 # 1.5.0.0/16"
n = [0, 0, 0, 0]
nodes = []
iprr_name = {}
for line in f1.readlines():
    s = {}
    s["click"] = 0
    string = line.strip().split("#")
    if len(string) == 7:
        if string[2] == "BGP":
            s['id'] = "BGP-router" + str(n[0])
            s['name'] = str(n[0])
            n[0] += 1
            s["ASN"] = string[4]
            s["ip"] = []
            s["type"] = "BGP-router"
            s["asname"] = string[5]
            s["prefix"] = string[6]
            for ip in string[3].split("|"):
                iprr_name[ip] = s['id']
                s["ip"].append(ip)
            nodes.append(s)

f1.close()
f2 = open(path_peizhi + "link-list-1.ip_level", "r")  # " 1001 # 1.1.0.18/29 # 1003 # 1.1.0.19/29 # 50M # P2C"
links = []


def findn(string):
    for i in xrange(len(nodes)):
        if nodes[i]['id'] == string:
            return i
    return -1


for line in f2.readlines():
    """
        暂时还没处理
    """
    t = line.strip().split("#")

    if len(t) == 6:

        asn1 = t[0]
        ip1 = t[1]
        asn2 = t[2]
        ip2 = t[3]
        value = t[4][:-1]
        shangye = t[5]

        """
        """

        d = {
            "source": "",
            "target": "",
            "value": ""
        }
        if (ip1 not in iprr_name) or (ip2 not in iprr_name):
            print "有条link找不到对应的node"
            continue
        else:
            d["source"] = iprr_name[ip1]
            d["target"] = iprr_name[ip2]
            d["value"] = value
            d["shangye"] = shangye
            links.append(d)
    else:
        s = {}
        s["click"] = 0
        s['id'] = "switch" + str(n[3])
        s['name'] = str(n[3])
        n[3] += 1
        s["ip"] = ""
        s["type"] = "switch"
        nodes.append(s)
        for i in xrange(len(t)):
            d = {
                "target": "",
                "source": s['id'],
                "value": 1
            }
            if t[i] not in iprr_name:
                print "有条link找不到对应的node"
                continue
            else:
                d["target"] = iprr_name[t[i]]
                links.append(d)

f2.close()

json_dict = {"nodes": nodes, "links": links}

json_str = json.dumps(json_dict, sort_keys=True,
                      separators=(',', ': '))  # indent=4,
