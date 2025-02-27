import requests
from crdclib import crdclib
import yaml

cdsmodelfiles = ['https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model.yml', 'https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model-props.yml']
idcmodelfile = r".\model-desc\old-idc-model.yml"
idcpropsfile = r".\model-desc\old-idc-model-props.yml"

def getFiles(url):
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        return req.text
    else:
        print("No content")

def yaml2json(yamlstring):
    jsonthing = yaml.load(yamlstring, Loader=yaml.SafeLoader)
    return jsonthing
        
idcmodel = {'Handle': 'IDC', 'Version': '0.0.1'}

modelurl = cdsmodelfiles[0]
propsurl = cdsmodelfiles[1]
#print(url)
modelyaml = getFiles(modelurl)
propyaml = getFiles(propsurl)

modeljson = yaml2json(modelyaml)
#print(modeljson)
propjson = yaml2json(propyaml)

#Get the nodes from the relationships
idcnodelist = ['image']
imagerels = modeljson['Relationships']['of_image']
print(imagerels)
for entry in imagerels['Ends']:
    idcnodelist.append(entry['Src'])
print(idcnodelist)

#Copy the model info from CDS to IDC
temp = {}
for node in idcnodelist:
    temp[node] = modeljson['Nodes'][node]
idcmodel['Nodes'] = temp
ofimage = {}
ofimage['of_image'] = imagerels
idcmodel['Relationships'] = ofimage
crdclib.writeYAML(idcmodelfile, idcmodel)

#Now create the props json
tempprop = {}
idcprops = {}
for node in idcnodelist:
    proplist = idcmodel['Nodes'][node]['Props']
    for prop in proplist:
        tempprop[prop] = propjson['PropDefinitions'][prop]
idcprops['PropDefinitions'] = tempprop
crdclib.writeYAML(idcpropsfile, idcprops)