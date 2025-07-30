from vcfcli.plot.generate_plots.generate_sunburst_plots import generate_sunburst_plot
import vcfcli.plot.generate_data.generate_radarplot_data
import vcfcli.plot.generate_plots.generate_radarplot


def generate_plot_graph_data(variant_data, qid, plot_type, width=None, height=None, genome_version=None):
    """
    Generates plot data for all Onkopus plots implemented in Plotly. Returns the JSON graph to display the plot

    :param variant_data:
    :param qid:
    :param plot_type:
    :param width:
    :param height:
    :return:
    """
    if "snvs" in variant_data:
        variant_data = variant_data["snvs"]

    if plot_type == "pathogenicity-scores-radar":
        df = vcfcli.plot.generate_data.generate_radarplot_data.generate_single_biomarker_radar_plot_data(variant_data,qid)
        dfs=[]
        dfs.append(df)
        names = vcfcli.plot.generate_data.generate_biomarker_identifiers(variant_data)
        if (width is not None) and (height is not None):
            return vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(dfs,names, "pathogenicity-scores-radar",width=width,height=height)
        else:
            return vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(dfs, names,
                                                                                     "pathogenicity-scores-radar")
    elif plot_type == 'pathogenicity-scores-radar-set':
        dfs = vcfcli.plot.generate_data.generate_radarplot_data.generate_multiple_biomarker_radar_plot_data(variant_data)
        names=vcfcli.plot.generate_data.generate_biomarker_identifiers(variant_data)
        if (width is not None) and (height is not None):
            graph = vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(dfs,names, "pathogenicity-scores-radar",width=width,height=height)
            return graph
        else:
            return vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(dfs, names,
                                                                                     "pathogenicity-scores-radar")
    elif plot_type == 'pathogenicity-scores-radar-categorical':
        dfs = vcfcli.plot.generate_data.generate_radarplot_data.generate_multiple_biomarker_radar_plot_data(variant_data)
        names = vcfcli.plot.generate_data.generate_biomarker_identifiers(variant_data)
        df_cat = vcfcli.plot.generate_data.generate_radarplot_data.generate_categorical_scores(dfs)
        if (width is not None) and (height is not None):
            graph = vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(df_cat,names, "pathogenicity-scores-radar",width=width,height=height)
            return graph
        else:
            return vcfcli.plot.generate_plots.generate_radarplot.generate_radar_plot(dfs, names,
                                                                                     "pathogenicity-scores-radar")
    elif (plot_type == "treatment-sunburst") \
            or (plot_type == "treatment-sunburst-cancer-type") \
            or (plot_type == "treatment-sunburst-match-type-drugs") \
            or (plot_type == "treatment-sunburst-match-type-drugs-all") \
            or (plot_type == "treatment-sunburst-match-type-drug-classes") \
            or (plot_type == "treatment-sunburst-response-type") \
            or (plot_type == "treatments-all-drug-class-drugs") \
            or (plot_type == "treatments-all-cancer-type") \
            or (plot_type == "treatments-all-sunburst-match-type-drug-classes-all") \
            or (plot_type == "treatments-all-sunburst-match-type-drugs-all") \
            or (plot_type == "treatments-all-sunburst-response-type") \
            :
        return generate_sunburst_plot(variant_data, qid, plot_type)
    elif plot_type == "chromosome-positions":
        ideogram_data = vcfcli.plot.generate_data.generate_chromosome_positions_data(variant_data, genome_version)
        return ideogram_data
    elif plot_type == "protein-data":
        graphJSON = vcfcli.plot.generate_data.generate_protein_plot(variant_data)
        return graphJSON

    return {}
