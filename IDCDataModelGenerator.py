#In theory this will take the Imaging portions of the CDS model and generate a new IDC model.
import bento_mdf
import bento_meta
import yaml

#Point to the main branch in Github.  Should be the production version
cdsmodelfiles = ['https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model.yml', 'https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model-props.yml']
idcmodelfile = r".\model-desc\idc-model.yml"
verionnum = '1.0.0'

cds_mdf = bento_mdf.mdf.MDF(*cdsmodelfiles)
idc_mdf = bento_meta.model.Model(handle="IDC", version=verionnum)
#idc_mdf = bento_mdf.mdf.MDF(idcmodelfile)


#Start by adding the nodes to IDC. Since "image" is the root of the imaging tree, we'll use the edges to
# find all the connected nodes.  And since we'll have the edges, those can be easily added here
cds_rels = cds_mdf.model.edges
imagenodes = [{'image':None}]
for key in cds_rels.keys():
    if "of_image" in key:
        # Imagenodes is the node name with the edge key
        imagenodes.append({key[1]:key})

for entry in imagenodes:
    for node, edgekey in entry.items():
        idc_mdf.add_node({"handle":node})
        if edgekey is not None:
            #print(edgekey)
            idc_mdf.add_edge({"handle":edgekey[0], "src":idc_mdf.nodes[edgekey[1]], "dst": idc_mdf.nodes[edgekey[2]]})
         
# Now go through the nodes and add the properties for each node
idcnodes = idc_mdf.nodes
for node in idcnodes.keys():
    cdsprops = cds_mdf.model.nodes[node].props
    for prop in cdsprops:
        idc_mdf.add_prop(idc_mdf.nodes[node], {'handle': prop, "value_domain":"value_set"})
 
#And now add Terms for the props
'''
idcprops = idc_mdf.props
for prop in idcprops:
    print(prop)
    if cds_mdf.model.props[prop].concept is not None:
        #print(cds_mdf.model.props[prop].concept.terms)
        for termkey, termvalue in cds_mdf.model.props[prop].concept.terms.items():
            print(f"Key: {termkey}")
            print(f"Value: {termvalue.get_attr_dict()}")
'''
bento_mdf.MDFWriter(idc_mdf).write_mdf(idcmodelfile)
#print(yaml.dump(bento_mdf.MDFWriter(idc_mdf).write_mdf()))
#print(yaml.dump(bento_mdf.MDFWriter(idc_mdf).mdf, indent=4))
#with open(idcmodelfile, 'w') as f:
#    yaml.dump((bento_mdf.MDFWriter(idc_mdf)),f, indent=4)