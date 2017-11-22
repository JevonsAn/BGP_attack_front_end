# -*- coding: UTF-8 -*-
import json

path_peizhi = "peizhi/"
f1 = open(path_peizhi + "node.txt", "r")  # "BGP # 1.5.0.2/29|1.2.0.19/29 # 1005 # ASN-1005 # 1.5.0.0/16"
n = [0, 0, 0, 0]
nodes = []
iprr_name = {}
for line in f1.readlines():
    if line[-1] == "\n":
        line = line[:-1]
    s = {}
    s["click"] = 0
    string = line.strip().split("#")
    if len(string) == 3:
        if string[0] == "HOST":
            s['id'] = "host" + str(n[2])
            s['name'] = str(n[2])
            n[2] += 1
            ip = string[1].split("|")[0]
            s["ip"] = ip
            s["type"] = "host"
            s["ASN"] = string[2]
            iprr_name[ip] = s['id']
            nodes.append(s)
        elif string[0] == "OSPF":
            s['id'] = "router" + str(n[1])
            s['name'] = str(n[1])
            n[1] += 1
            s["type"] = "router"
            s["ASN"] = string[2]
            s["ip"] = []
            for ip in string[1].split("|"):
                iprr_name[ip] = s['id']
                s["ip"].append(ip)
            nodes.append(s)
        elif string[0] == "BGP":
            s['id'] = "BGP-router" + str(n[0])
            s['name'] = str(n[0])
            n[0] += 1
            s["ASN"] = string[2]
            s["ip"] = []
            s["type"] = "BGP-router"
            for ip in string[1].split("|"):
                iprr_name[ip] = s['id']
                s["ip"].append(ip)
            nodes.append(s)
    elif len(string) == 5:
        if string[0] == "BGP":
            s['id'] = "BGP-router" + str(n[0])
            s['name'] = str(n[0])
            n[0] += 1
            s["ASN"] = string[2]
            s["ip"] = []
            s["type"] = "BGP-router"
            s["asname"] = string[3]
            s["prefix"] = string[4]
            for ip in string[1].split("|"):
                iprr_name[ip] = s['id']
                s["ip"].append(ip)
            nodes.append(s)

f1.close()
f2 = open(path_peizhi + "link.txt", "r")  # " 1001 # 1.1.0.18/29 # 1003 # 1.1.0.19/29 # 50M # P2C"
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
