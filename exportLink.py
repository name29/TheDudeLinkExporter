#!/usr/bin/env python
import os
import re
import sys

if ( len(sys.argv) < 2 ):
	print "USAGE: "+sys.argv[0]+" FILE_DUDE_DB"
	exit(1)

print "Convert file "+sys.argv[1]
os.system("echo '.dump' | sqlite3 "+sys.argv[1]+" | grep \"\\\"objs\\\"\" | cut -d'(' -f2 | tr -d ')' | tr -d ';' | tr -d \"X\\'\"  > objs.txt")
f = open("objs.txt","r")


devices=dict()
maps=dict()
nets=dict()
links=dict()
#history=dict()

print "Parsing file "+sys.argv[1]

for line in f.readlines():
        line = line.strip().rstrip().replace(" ","")
        sp=line.split(",")
        id=sp[0]
        hex=sp[1]

        #DEVICE
	#IP HEX
	#SYS_ID
        device_search = re.search('^0961646472657373657300(.*?)076167656E744944.+7379732D696400(.*?)087379732D6E616D6500.+', hex, re.IGNORECASE)
        if ( device_search ):
		ip_hex=device_search.group(1)
		try:
			ip="%d.%d.%d.%d" % (  int(ip_hex[2:4], 16) ,int(ip_hex[4:6], 16) ,int(ip_hex[6:8], 16), int(ip_hex[8:10], 16))
		except ValueError:
			print "Unable to export IP "+ip_hex+" (OBJS ID "+id+")"
			ip=""
		devices[device_search.group(2)]=ip
	#MAPS 
	#SYS-ID
	#SYS-NAME
        map_search = re.search('^0A61636B6564436F6C6F7200.+7379732D696400(.*?)087379732D6E616D6500(.*?)087379732D7479706500.+',hex, re.IGNORECASE)
        if ( map_search ):
		maps[map_search.group(1)]=map_search.group(2).decode("hex").strip()

	#NETS
	#SYS-ID
	#SYS-NAME
        net_search = re.search('^0F6E65744D6170456C656D656E74494400.+7379732D696400(.*?)087379732D6E616D6500(.*?)087379732D7479706500.+',hex, re.IGNORECASE)
        if ( net_search ):
		nets[net_search.group(1)]=net_search.group(2).decode("hex").strip()

        #HISTORY
	#FIRST DEVICE_MASTER_SYS_ID (SYS_ID OF MASTER OBJECT)
	#SECOND NETELEMENT_ID (SYS_ID OF LINK OBJECT)

#       	history_search = re.search('^07686973746F727900.+6D617374657244657669636500(.*?)0F.+6E65744D6170456C656D656E74494400(.*?)086E65744D6170494400.+7379732D696400(.*?)087379732D6E616D6500.+',hex, re.IGNORECASE)

#	if ( history_search ):
#		tmp=dict()
#		tmp["device_master_id"]=history_search.group(1)
#		tmp["netelement_id"]=history_search.group(2)
#		tmp["sys_id"]=history_search.group(3)
#		history[history_search.group(3)]=tmp
#		#history[MASTER_SYSID]=SYS_ID OF LINK OBJECT
        #LINK
	#ITEM_ID
	#LINK FROM
	#LINK ID
	#LINK TO
	#SYS_ID
       	link_search = re.search('^0E6974656D41636B6564436F6C6F72.+6974656D494400(.*?)096974656D496D616765.+6C696E6B46726F6D00(.*?)066C696E6B494400(.*?)066C696E6B546F00(.*?)0C6C696E6B557365576964746800.+7379732D696400(.*?)087379732D6E616D6500.+',hex, re.IGNORECASE)

	if ( link_search ):
		tmp=dict()
		tmp["item_id"]=link_search.group(1)
		tmp["link_from"]=link_search.group(2)
		tmp["link_id"]=link_search.group(3)
		tmp["link_to"]=link_search.group(4)
		tmp["sys_id"]=link_search.group(5)
		links[link_search.group(5)]=tmp

f.close()

human_links=list()

#print devices
#print history
#print links

#for master_id,link_id in history.items():
#	master_link=links[link_id]
#	slave_link=links[master_link["link_from"]]
#	slave_id=slave_link["item_id"]
#	human_links[devices[master_id]]=devices[slave_id]	
#print human_links


print ""
print ""
print ""
human_links=list()

for link_id, value in links.items():
	if ( value["link_to"] == "04FFFFFFFF" ):
		#Slave link
		continue

	if value["link_from"] not in links:
		print "Unable to find FROM link",value["link_from"]
		continue

	if value["link_to"] not in links:
		print "Unable to find TO link",value["link_to"]
		continue
		
	master_link=links[value["link_from"]]
	slave_link=links[value["link_to"]]
	slave_id=slave_link["item_id"]
	master_id=master_link["item_id"]

	if master_id == "04FFFFFFFF" or slave_id == "04FFFFFFFF":
		print "BUG: one of the end points is undefined"
		continue

	if master_id not in devices:
		if master_id not in maps:
			if master_id not in nets:
				print "Unable to find device MASTER ",master_id
				continue
			else:
				m=nets[master_id]
		else:
			m=maps[master_id]

	else:
		m=devices[master_id]

	if slave_id not in devices:
		if slave_id not in maps:
			if slave_id not in nets:
				print "Unable to find device SLAVE  ",slave_id
				continue
			else:
				m=nets[slave_id]
		else:
			s=maps[slave_id]
	else:
		s=devices[slave_id]


	tmp=dict()
	tmp["master"]=m
	tmp["slave"]=s
	human_links.append(tmp)

print human_links

print "Done"
