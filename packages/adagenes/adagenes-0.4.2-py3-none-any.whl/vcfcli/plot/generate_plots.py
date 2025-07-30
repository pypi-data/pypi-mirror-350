import json, traceback
import plotly
import plotly.express as px
from vcfcli.plot import generate_treatment_sunburst_data, generate_treatment_drugs_pmid_sunburst_data,generate_clinical_significance_sunburst_data_biomarker_set


def generate_sunburst_plot(variant_data, qid, plot_type):
    if plot_type == "treatment-sunburst":
        #df = generate_treatment_sunburst_data(variant_data, qid)
        df = generate_treatment_drugs_pmid_sunburst_data(variant_data, qid)
        try:
            fig = px.sunburst(df, names='Drug_Class', path=['Variant', 'Drug_Class','Drugs', 'EvLevel','PMID' ],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0
                              )
            #fig.update_layout(showlegend=False)
            #fig.update_coloraxes(showscale=False)

            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                paper_bgcolor="#c2d7e9"
            )
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return graphJSON
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
            return "<html></html>"
    elif plot_type == "treatment-sunburst-cancer-type":
        df = generate_treatment_drugs_pmid_sunburst_data(variant_data, qid)

        try:
            fig = px.sunburst(df, names='EvLevel', path=['Variant', 'Cancer Type', 'EvLevel', 'Drugs', 'PMID'],
                              values='num',
                              color='Response Type',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                paper_bgcolor="#c2d7e9"
            )
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return graphJSON
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "<html></html>"
    elif plot_type == "treatments_all_sunburst_1":
        df = generate_clinical_significance_sunburst_data_biomarker_set(variant_data, None)

        try:
            fig = px.sunburst(df, names='Drugs', path=['PID', 'Drug_Class', 'Drugs', 'EvLevel', 'Biomarker', 'PMID'],
                              values='num',
                              color='Response',
                              color_continuous_scale='RdBu',
                              color_continuous_midpoint=0.00
                              )
            fig.update_layout(
                margin=dict(l=10, r=0, t=0, b=0, pad=0),
                paper_bgcolor="#c2d7e9"
            )
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return graphJSON
        except:
            print("error generating treatment sunburst plot")
            print(traceback.format_exc())
        return "<html></html>"

    #return render_template('base.html', graphJSON={})
    return {}
