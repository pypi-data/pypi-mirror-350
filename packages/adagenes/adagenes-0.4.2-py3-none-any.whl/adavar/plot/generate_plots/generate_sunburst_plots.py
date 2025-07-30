import json, traceback
import plotly
import plotly.express as px
from adagenes.plot import generate_clinical_significance_sunburst_data_biomarker_set,generate_treatment_match_type_sunburst_data


def generate_sunburst_plot(variant_data, qid, plot_type, response_type="graph", font_size=24, width=2400, height=1800):
    """
    Computes data for generating Plotly sunburst plots for viewing clinical evidence data

    Provides data for the following plots:
    'treatment-sunburst':
    'treatments_all_sunburst_1':
    'treatment-sunburst-cancer-type':
    'treatment-sunburst-match-type-drugs':
    'treatment-sunburst-match-type-drugs-all':
    'treatment-sunburst-match-type-drug-classes':
    'treatment-sunburst-response-type':

    :param variant_data:
    :param qid:
    :param plot_type:
    :return:
    """
    label_color = '#505050'
    if plot_type == "treatment-sunburst":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid,
                                                    required_fields=["evidence_level_onkopus", "citation_id",
                                                                     "response_type","drug_class","drugs"])
        df = remove_duplicate_pmids(df,["Biomarker","Drug_Class","Drugs","EvLevel","Citation ID"])
        try:
            fig = px.sunburst(df, names='Drug_Class', path=['Biomarker', 'Drug_Class','Drugs', 'EvLevel','PMID' ],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0
                              )
            #fig.update_layout(showlegend=False)
            #fig.update_coloraxes(showscale=False)

            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font = dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )

            if response_type == "graph":
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graphJSON
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
            return "-"
    elif plot_type == "treatments-all-drug-class-drugs":
        df = generate_clinical_significance_sunburst_data_biomarker_set(
            variant_data, None,
            required_fields=["evidence_level_onkopus", "citation_id","response_type","drug_class","drugs"]
        )
        df = remove_duplicate_pmids(df, ["Biomarker", "Drug_Class", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df,
                              names='Drugs',
                              path=['Biomarker', 'Drug_Class', 'Drugs', 'EvLevel', 'PMID'],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            if response_type == "graph":
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graphJSON
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatments-all-cancer-type":
        df = generate_clinical_significance_sunburst_data_biomarker_set(
            variant_data, None,
            required_fields=["disease", "evidence_level_onkopus", "citation_id",
                             "response_type"]
        )
        df = remove_duplicate_pmids(df, ["Biomarker", "Cancer Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df,
                              names='Drugs',
                              path=['Biomarker', 'Cancer Type', 'EvLevel', 'Drugs', 'PMID'],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            if response_type == "graph":
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graphJSON
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatments-all-sunburst-match-type-drug-classes-all":
        df = generate_clinical_significance_sunburst_data_biomarker_set(variant_data, qid,
                                                                        required_fields=["evidence_level_onkopus",
                                                                                         "citation_id", "response_type",
                                                                                         "drug_class"]
                                                                        )
        df = remove_duplicate_pmids(df, ["Biomarker", "Match_Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs', path=['Biomarker', 'Match_Type', 'Drugs', 'EvLevel', 'PMID'], values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)

            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatments-all-sunburst-match-type-drugs-all":
        df = generate_clinical_significance_sunburst_data_biomarker_set(variant_data, qid, required_fields=["evidence_level_onkopus","citation_id","response_type"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Match_Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs', path=['Biomarker', 'Match_Type', 'Drugs', 'EvLevel', 'PMID'], values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatments-all-sunburst-response-type":
        df = generate_clinical_significance_sunburst_data_biomarker_set(variant_data, qid,
            required_fields=["evidence_level_onkopus","citation_id","response_type","drug_class"]
        )
        df = remove_duplicate_pmids(df, ["Biomarker", "Response Type", "Drug_Class", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs',
                              path=['Biomarker', 'Response Type', 'Drug_Class', 'Drugs', 'EvLevel', 'PMID'],
                              values='num',
                              color='Match_Type',
                              color_discrete_sequence=px.colors.qualitative.Safe
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatment-sunburst-cancer-type":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid,
                                                    required_fields=["disease","evidence_level_onkopus", "citation_id",
                                                                     "response_type"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Cancer Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='EvLevel', path=['Biomarker', 'Cancer Type', 'EvLevel', 'Drugs', 'PMID'],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            if response_type == "graph":
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graphJSON
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatment-sunburst-match-type-drugs":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid, required_fields=["evidence_level_onkopus","citation_id","response_type"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Match_Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs', path=['Biomarker', 'Match_Type', 'Drugs', 'EvLevel', 'PMID'], values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatment-sunburst-match-type-drugs-all":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid, required_fields=["evidence_level_onkopus","citation_id","response_type"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Match_Type", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs', path=['Biomarker', 'Match_Type', 'Drugs', 'EvLevel', 'PMID'], values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatment-sunburst-match-type-drug-classes":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid, required_fields=["evidence_level_onkopus","citation_id","response_type","drug_class"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Match_Type", "Drug_Class", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs', path=['Biomarker', 'Match_Type', 'Drug_Class', 'Drugs', 'EvLevel', 'PMID'],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"
    elif plot_type == "treatment-sunburst-response-type":
        df = generate_treatment_match_type_sunburst_data(variant_data, qid, required_fields=["evidence_level_onkopus","citation_id","response_type","drug_class"])
        df = remove_duplicate_pmids(df, ["Biomarker", "Response Type", "Drug_Class", "Drugs", "EvLevel", "Citation ID"])
        try:
            fig = px.sunburst(df, names='Drugs',
                              path=['Biomarker', 'Response Type', 'Drug_Class', 'Drugs', 'EvLevel', 'PMID'],
                              values='num',
                              color='Match_Type',
                              color_discrete_sequence=px.colors.qualitative.Safe
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                font=dict(
                    family="Arial",
                    size=font_size,
                    color=label_color
                ),
                paper_bgcolor="#ffffff",
                width=int(width),
                height=int(height)
            )
            # fig.update_layout(showlegend=False)
            # fig.update_coloraxes(showscale=False)
            if response_type == "graph":
                graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return graph_json
            else:
                return fig
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "-"

    return {}


def remove_duplicate_pmids(df, subset):
    """

    :param df:
    :return:
    """
    print("Columns ",df.columns, "sub set ",subset)
    try:
        df_new = df.drop_duplicates(subset=subset, keep='first')
        return df_new
    except:
        print(traceback.format_exc())
        return df
