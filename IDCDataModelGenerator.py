#In theory this will take the Imaging portions of the CDS model and generate a new IDC model.
import bento_mdf
import bento_meta
import yaml

#Point to the main branch in Github.  Should be the production version
cdsmodelfiles = ['https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model.yml', 'https://raw.githubusercontent.com/CBIIT/cds-model/refs/heads/main/model-desc/cds-model-props.yml']
idcmodelfile = r".\model-desc\idc-model.yml"
verionnum = '1.0.0'
verbose = True

cds_mdf = bento_mdf.mdf.MDF(*cdsmodelfiles)
idc_mdf = bento_meta.model.Model(handle="IDC", version=verionnum)

#Start by adding the nodes to IDC. Since "image" is the root of the imaging tree, we'll use the edges to
# find all the connected nodes.  And since we'll have the edges, those can be easily added here
cds_rels = cds_mdf.model.edges

# Add the nodes to the model
#Start with image since that's the root node
nodeobj = bento_meta.model.Node({'handle': 'image'})
idc_mdf.add_node(nodeobj)

# Pick up all the nodes that are related to image
for edgekey in cds_rels.keys():
    if "of_image" in edgekey:
        nodeobj = bento_meta.model.Node({'handle': edgekey[1]})
        idc_mdf.add_node(nodeobj)
        
#Add the edges to the model
for edgekey, edgevalue in cds_rels.items():
    if "of_image" in edgekey:
        edgeinfo = {'handle': edgekey[0], 'src': idc_mdf.nodes[edgekey[1]], 'dst': idc_mdf.nodes[edgekey[2]], 'multiplicity': edgevalue.get_attr_dict()['multiplicity']}
        edgeobj = bento_meta.model.Edge(edgeinfo)
        idc_mdf.add_edge(edgeobj)

      
# Now go through the nodes and add the properties for each node
idcnodes = idc_mdf.nodes
for node in idcnodes.keys():
    cdsprops = cds_mdf.model.nodes[node].props
    for propname in cdsprops:
        origprop = cds_mdf.model.props[(node, propname)]
        temp = origprop.get_attr_dict()
        propobj = bento_meta.model.Property(temp)
        nodeobj = idc_mdf.nodes[node]
        idc_mdf.add_prop(nodeobj, propobj)
 
#And now add Terms for the props
idcprops = idc_mdf.props
for prop in idcprops:
    if cds_mdf.model.props[prop].concept is not None:
        for termkey, termvalue in cds_mdf.model.props[prop].concept.terms.items():
            temp = termvalue.get_attr_dict()
            propobj = idc_mdf.props[prop]
            termobj = bento_meta.model.Term(temp)
            idc_mdf.annotate(propobj, termobj)
            
            
#In theory, the model is done now.
if verbose:  
    for node in idc_mdf.nodes:
        print(f"Node: {node}")
        for prop in idc_mdf.nodes[node].props:
            print(f"Prop: {prop}")
            if idc_mdf.props[(node,prop)].concept is not None:
                for termvalue in idc_mdf.props[(node,prop)].concept.terms.items():
                    print(f"Terms: {termvalue[1].get_attr_dict()}")


bento_mdf.MDFWriter(idc_mdf).write_mdf(idcmodelfile)
#print(yaml.dump(bento_mdf.MDFWriter(idc_mdf).write_mdf()))
#print(yaml.dump(bento_mdf.MDFWriter(idc_mdf).mdf, indent=4))
#with open(idcmodelfile, 'w') as f:
#  yaml.dump((bento_mdf.MDFWriter(idc_mdf)),f, indent=4)