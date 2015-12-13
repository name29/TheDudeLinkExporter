file_mappa="Dispositivi.csv";
root_netxms="test";

f = open(file_mappa,'r')
#CODE
azienda = session.findObjectByName(root_netxms.strip())
azienda_map = session.findObjectByName(root_netxms.strip()+" Maps")

if ( azienda ):
	devices = csv.reader(f,delimiter=',',quotechar='"')
	for row in devices:
		nodeId=-1
	        nome=row[1]
        	ip=row[2]
	        mappastr=row[5]
	        print "Nome:",nome,"IP:",ip,"Mappa:",mappastr
		mappa = session.findObjectByName(mappastr.strip())
		if ( not mappa ):
			m = NXCObjectCreationData(objects.GenericObject.OBJECT_CONTAINER, mappastr.strip(), azienda.getObjectId());
			mappa = session.createObject(m)
		else:
			mappa = mappa.getObjectId()
		try:
#			cd = NXCObjectCreationData(objects.GenericObject.OBJECT_NODE, nome, mappa);
#			cd.setPrimaryName(ip)
#			nodeId = session.createObject(cd)
#			print '"%s" created, id=%d' % (nome, nodeId)
			pass
		except:
			print "Errore"
else:
	print "Errore lettura mappa TOP"
