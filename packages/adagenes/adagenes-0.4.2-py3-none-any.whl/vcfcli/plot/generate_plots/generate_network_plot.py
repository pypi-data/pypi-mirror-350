import pandas as pd
#from IPython.display import display, HTML
#import seaborn as sns
#import matplotlib.pyplot as plt
from pyvis import network as net

got_net = net.Network(height="750px", width="80%", bgcolor="#ffffff", font_color="black",
                  select_menu=True, heading="A Cancer Gene-drug Interation Graph")
got_net.barnes_hut()

# ex = {"A2M":[{"gene_name":"A2M"},{"gene_claim_name":"A2M"},{"entrez_id":"2"},{"interaction_claim_source":"NCI"},{"interaction_types":""},{"drug_claim_name":"COBALT"},{"drug_claim_primary_name":"COBALT"},{"drug_name":""},{"drug_concept_id":""},{"interaction_group_score":""},{"PMIDs":"6663071"},{"gene_name":"A2M"},{"gene_claim_name":"A2M"},{"entrez_id":"2"},{"interaction_claim_source":"NCI"},{"interaction_types":""},{"drug_claim_name":"PROSTAGLANDIN E1"},{"drug_claim_primary_name":"PROSTAGLANDIN E1"},{"drug_name":""},{"drug_concept_id":""},{"interaction_group_score":""},{"PMIDs":"6202298"},{"gene_name":"A2M"},{"gene_claim_name":"A2M"},{"entrez_id":"2"},{"interaction_claim_source":"PharmGKB"},{"interaction_types":""},{"drug_claim_name":"Enzymes"},{"drug_claim_primary_name":"Enzymes"},{"drug_name":""},{"drug_concept_id":""},{"interaction_group_score":""},{"PMIDs":"23280790"},{"gene_name":"A2M"},{"gene_claim_name":"A2M"},{"entrez_id":"2"},{"interaction_claim_source":"NCI"},{"interaction_types":""},{"drug_claim_name":"THROMBIN"},{"drug_claim_primary_name":"THROMBIN"},{"drug_name":"THROMBIN"},{"drug_concept_id":"chembl:CHEMBL2108110"},{"interaction_group_score":"5.3"},{"PMIDs":"2432677"}]}
# plot_list = [ #dgidb_adapter.db_request.get_gene_interactions("KRAS"),
               # dgidb_adapter.db_request.get_gene_interactions("AR")
#              dgidb_adapter.db_request.get_drugs_info("DACTOLISIB"),
#              dgidb_adapter.db_request.get_gene_interactions("NRAS"),
#              ]
def ex_from_database(plot_list):
    ## make a main dictionary of every possible results with 11 main keys
    result_dict = {}
    for plot in plot_list:
        for gene, values in plot.items():
            for dicts in values:
                for key, value in dicts.items():
                    result_dict.setdefault(key, []).append(value)
    ## make a dataframe out of it
            data_dataframe = pd.DataFrame(result_dict)

    # print(data_dataframe)
    data = {
    "Source": data_dataframe['gene_name'],
    "Target": data_dataframe['drug_name'],
    "Weight": data_dataframe['interaction_group_score'],
    "Labels": data_dataframe['interaction_types']
    }
    got_data = pd.DataFrame(data=data)

    sources = got_data['Source'].tolist()

    ## blank cells in Target col were put into '_'
    got_data['Target'] = got_data['Target'].replace(r'^\s*$','_', regex=True)
    targets = got_data['Target'].tolist()

    ## blank cells in Label col were put into '_'
    got_data['Labels'] = got_data['Labels'].replace(r'^\s*$','_', regex=True)
    labels = got_data['Labels'].tolist()

    ## blank cells in Weight col were put into zero
    got_data['Weight'] = got_data['Weight'].replace(r'^\s*$','0', regex=True)
    got_data['Weight'] = got_data['Weight'].astype(float)
    got_data['Weight'] = (got_data['Weight'] - got_data['Weight'].min()) / (got_data['Weight'].max() - got_data['Weight'].min())
    weights = got_data['Weight'].tolist()
    # print(weights)


    edge_data = zip(sources, targets, weights, labels)
    for e in edge_data:
        src = e[0]
        tar = e[1]
        w = e[2]
        la = e[3]
        # print(la)
        got_net.add_node(src, src, title=src, value=w*20, color="#D9017A")
        got_net.add_node(tar, tar, title=tar, value=w*20, color="#00A86B")
        got_net.add_edge(src, tar, label=la, value=w*20)

    got_net.set_options(
        """
        const options = {
          "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 3,
            "opacity": 1,
            "font": {
              "size": 40,
              "face": "verdana"
            },
            "scaling": {
              "max": 118
            },
            "shape": "circle",
            "shapeProperties": {
              "borderRadius": 18
            },
            "size": 100
          },
          "edges": {
            "arrowStrikethrough": false,
            "color": {
              "opacity": 0.6
            },
            "font": {
              "size": 200,
              "face": "verdana",
              "strokeWidth": 0 ,
              "align": "middle"
            },
            "hoverWidth": 5,
            "scaling": {
              "max": 54,
              "label": {
                "maxVisible": 100
              }
            },
            "selectionWidth": 2.5,
            "selfReferenceSize": 42,
            "selfReference": {
              "size": 60,
              "angle": 0.7853981633974483
            },
            "smooth": {
              "forceDirection": "none"
            }
          },
          "interaction": {
            "multiselect": true
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -200000,
              "springLength": 1000,

              "avoidOverlap": 0
            }

          }
        }
        """
    )

    # got_net.show_buttons(filter_=True)
    # got_net.show_buttons(['nodes'])
    got_net.show("gameofthrones.html", notebook=False)

# ex_from_database(plot_list)
