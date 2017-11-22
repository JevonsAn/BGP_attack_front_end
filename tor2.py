# -*- coding: UTF-8 -*-
import tornado.web
import tornado.ioloop
import os
import json
import random
from peijson import nodes, links, iprr_name, json_str, path_peizhi

canshu = {}


class Ping2Handler(tornado.web.RequestHandler):

    def get(self):

        self.write(str(1))


class PinHandler(tornado.web.RequestHandler):

    def get(self):
        graph = self.get_argument("graph")

        try:
            if graph == "1":
                fpin = open("peizhi/ping.txt", "r")
            elif graph == "2":
                fpin = open("peizhi/ping.txt", "r")
            else:
                fpin = open("peizhi/ping.txt", "r")

            ping = fpin.readlines()[-1].strip()
            icmp_sep = ping.split(" ")[4].split("=")[-1]
            rtt = ping.split(" ")[6].split("=")[-1]
            if "icmp_sep" not in canshu:
                canshu["icmp_sep"] = icmp_sep
            else:
                last_seq = canshu["icmp_sep"]
                if icmp_sep == last_seq:
                    rtt = "0"
                canshu["icmp_sep"] = icmp_sep
        except Exception as e:
            print e
            rtt = "0"
        finally:
            fpin.close()
        # self.write(rtt)
        self.write(str(random.uniform(0, 2)))


class PingstartHandler(tornado.web.RequestHandler):

    def get(self):
        ip1 = self.get_argument("ip1")
        ip2 = self.get_argument("ip2")
        print("ip1:"+ip1+"\nip2:"+ip2)
        self.write(str(random.uniform(0, 2)))


class JsoHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(json_str)


class JsoHandler2(tornado.web.RequestHandler):

    def get(self):
        nodes2 = []
        n_control = -1
        n_attack = -1
        n_js = []
        js_ips = canshu["IPs"].split(" ")
        name_attack = ""
        for key in iprr_name:
            if key.split("/")[0] == canshu["IP1"]:
                name_attack = iprr_name[key]
        for i in xrange(len(nodes)):
            nodes2.append(nodes[i])
            if nodes[i]["type"] == "host" and nodes[i]["ip"].split("/")[0] == canshu["control_ip"]:
                n_control = i
            elif nodes[i]["id"] == name_attack:
                n_attack = i
            elif nodes[i]["type"] == "host" and nodes[i]["ip"].split("/")[0] in js_ips:
                n_js.append(i)
        nodes2[n_control]["type"] = "host_control"
        nodes2[n_attack]["type"] = nodes2[n_attack]["type"] + "_attack"
        for i in n_js:
            nodes2[i]["type"] = "host_js"

        self.write(json.dumps({"nodes": nodes2, "links": links}, sort_keys=True,
                              separators=(',', ': ')))


class ShoHandler(tornado.web.RequestHandler):

    def get(self):
        if "IP1" not in canshu:
            self.write("还没有发动过攻击！！")
        else:
            IP1 = canshu["IP1"]
            control_ip = canshu["control_ip"]
            IPs = canshu["IPs"]
            date = canshu["date"]
            time = canshu["time"]
            chixu = canshu["chixu"]
            meici = canshu["meici"]
            jiange = canshu["jiange"]
            wait = canshu["wait"]
            fuzai = canshu["fuzai"]
            fengzhi = canshu["fengzhi"]
            params = [IP1, control_ip, IPs, wait, date + " " +
                      time.replace("-", ":"), chixu, meici, jiange, fuzai, fengzhi]
            self.render("show.html", params=params)

    def post(self):
        IP1 = self.get_argument("attack_IP_address")
        control_ip = self.get_argument("control_IP_address")
        IPs = self.get_argument("js_IP_address")
        date = self.get_argument("date").replace("/", "-")
        time = self.get_argument("time").replace(":", "-")
        chixu = self.get_argument("chixu")
        meici = self.get_argument("meici")
        jiange = self.get_argument("jiange")
        wait = self.get_argument("wait")
        fuzai = self.get_argument("fuzai")
        fengzhi = self.get_argument("fengzhi")

        if wait == "":
            wait = "None"

        # print "attack_ip:%s\nbot_ip:%s\nwait:%s\nstart_time:%s-%s\nattack_time:%s\nper_attack_time:%s\nattack_frequency:%s\nlength:%s\nmax:%s\n" %\
        #     (IP1, IPs, wait, date, time, chixu, meici, jiange, fuzai, fengzhi)

        canshu["IP1"] = IP1
        canshu["control_ip"] = control_ip
        canshu["IPs"] = IPs
        canshu["date"] = date
        canshu["time"] = time
        canshu["chixu"] = chixu
        canshu["meici"] = meici
        canshu["jiange"] = jiange
        canshu["wait"] = wait
        canshu["fuzai"] = fuzai
        canshu["fengzhi"] = fengzhi

        # path = "../../"
        # info = open(path + "attack_info.txt", "w")
        # info.write("attack_ip:%s\nbot_ip:%s\nwait:%s\nstart_time:%s-%s\nattack_time:%s\nper_attack_time:%s\nattack_frequency:%s\nlength:%s\nmax:%s\n" %
        #            (IP1, IPs, wait, date, time, chixu, meici, jiange, fuzai, fengzhi))
        # info.close()

        # ip_name = {}
        # f_ip = open(path_peizhi + "host-ip-id.txt", "r")
        # for line in f_ip.readlines():
        #     line = line.strip().split(" ")
        #     ip_name[line[0]] = line[1]
        # path4 = "/home/quagga/"

        # os.popen("docker exec " +
        #          ip_name[control_ip] + " python " + path4 + "bot_control.py &")

        params = [IP1, control_ip, IPs, wait, date + "-" + time, chixu, meici, jiange, fuzai, fengzhi]

        self.render("show.html", params=params)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("form3.html")


class GrapHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("graph.html")


class XieHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("xielou.html")

    def post(self):
        asn = self.get_argument("zhixing")
        aslist = self.get_argument("aslist")
        f_xielou = open("peizhi/dis.conf", "w")
        f_xielou.write("[info]\n")
        f_xielou.write("asn=%s\naslist=[%s]" % (asn, aslist))
        self.write("开始泄漏")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", GrapHandler),
    (r"/form", MainHandler),
    (r"/show", ShoHandler),
    (r"/xielou", XieHandler),

    (r"/myjson", JsoHandler),
    (r"/myjson2", JsoHandler2),
    (r"/ping", PinHandler),
    (r"/ping2", Ping2Handler),
    (r"/pingstart", PingstartHandler)

], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
