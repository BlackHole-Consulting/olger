import sys
import os

f = open(sys.argv[1])
csv_content = f.read()
csv_spl = csv_content.split("\n")
f.close()


#http redirector
haconfig = "\nfrontend http-in"
haconfig +=   "\n   bind *:80"
haconfig +=   "\n   mode http"
haconfig +=   "\n   redirect scheme https code 301"



# EXAMPLE PORT REDIRECTORS
#haconfig += "\nfrontend https-in9080"
#haconfig +=   "\n   bind *:9080 ssl crt /root/certs/yourcertificate.pem"
#haconfig +=   "\n   mode http"
#haconfig +=   "\n   acl is7777 dst_port 9080"
#haconfig +=   "\n   http-request replace-value Host (.*):9080 \1:443"
#haconfig +=   "\n   http-request redirect location https://%[req.hdr(Host)]%[capture.req.uri] if is7777"




haconfig = "\nfrontend web"
haconfig += "\n  bind *:"+str(443)+" ssl crt /root/certs/yourcertificate.pem"
haconfig += "\n  mode http" 
haconfig += "\n  #stats enable"
haconfig += "\n  #stats uri /haproxy?stats"
haconfig += "\n  #stats realm Strictly\ Private"
haconfig += "\n  #stats auth A_Username:YourPassword"
haconfig += "\n  #stats auth Another_User:passwd"
haconfig += "\n  balance roundrobin"
haconfig += "\n  #option httpclose"
haconfig += "\n  #option forwardfor"
haconfig += "\n  #option ssl-hello-chk"
haconfig += "\n  #http-request set-header X-Forwarded-Port %[dst_port]"
haconfig += "\n  #http-request add-header X-Forwarded-Proto https if { ssl_fc }"
haconfig += "\n  #cookie JSESSIONID prefix"

haconfig += "\n  #STANDARD FIREWALL"

#RULES TO PROTECT OF INFINITE CONECTIONS AND DATA 
haconfig += "\n  stick-table type ip size 500k expire 24h store http_req_cnt"
haconfig += "\n  http-request track-sc0 src"

# WAF RULE FOR REPETITION REQUESTS
haconfig += "\n  http-request deny deny_status 429 if { sc_http_req_cnt(0) gt 10000 }"


hafronts = ""
habacks = ""
habackends = ""
id=0

for x in csv_spl:
    try:
        spl = x.split(",")
        ha_host =  spl[0]
        domain = spl[1]
        service_type = spl[2]
        ip_service = spl[3]
        port_service = spl[4]
        url_service = spl[5]


        print (ha_host+" "+domain+" "+service_type+" "+ip_service+" "+port_service+" "+url_service)

        hafronts+= "\n  acl host_"+domain+" hdr(host) -i "+domain
        #hafronts=+ "http-request redirect code 301 location http://www.%[hdr(host)]%[req.uri] unless has_www"

        habacks += "\n  use_backend host_"+domain+" if host_"+domain
        
        habackends +='\n'
        habackends += "\nbackend host_"+domain
        habackends += "\n mode http"
        habackends += "\n balance roundrobin"
        habackends += "\n server ha"+str(id)+" "+ip_service+":"+port_service+" check verify none maxconn 20"
        habackends += "\n server ha2"+str(id)+" "+ip_service+":"+port_service+" check verify none maxconn 20"

        id+=1

    except:

        pass



f = open("data/haproxy.conf", "w")
f.write(haconfig)
f.write(hafronts)
f.write(habacks)
f.write(habackends)
f.close()

f = open("playbooks/files/haproxy.conf", "w")
f.write(haconfig)
f.write(hafronts)
f.write(habacks)
f.write(habackends)
f.close()