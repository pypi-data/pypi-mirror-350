import matplotlib.pyplot as plt
import sklearn.metrics
from sklearn.metrics import RocCurveDisplay
import pandas as pd
import numpy as np

def generate_roc_values(biomarker_data, module, key):

    y_pred = []

    for var in biomarker_data:
        val = biomarker_data[var][module][key]
        y_pred.append(float(val))

    return y_pred

def generate_target_values(target_module, target_feature, biomarker_data):

    y_true = []
    for var in biomarker_data:
        if target_module in biomarker_data[var]:
            if target_feature in biomarker_data[var][target_module]:
                val = float(biomarker_data[var][target_module][target_feature]) + 1
                y_true.append(val)
            else:
                y_true.append("")
        else:
            y_true.append("")
    return y_true

def plot_roc_curves(
        biomarker_data,
        modules,
        keys,
        target_module = None,
        target_feature=None,
        y = None,
        labels = None,
        outfile=None
    ):
    if y is not None:
        y_true = y

    if target_module is not None:
        y_true = generate_target_values(target_module, target_feature, biomarker_data)

    for i,module in enumerate(modules):
        key = keys[i]

        y_pred = generate_roc_values(biomarker_data, module, key)

        print("ypred ",y_pred)
        print( "y true ",y_true)
        fpr, tpr, thresholds = sklearn.metrics.roc_curve(np.array(y_true), np.array(y_pred), pos_label=2)
        if labels is not None:
            label = labels[i]
        else:
            label = module
        plt.plot(fpr,tpr, label=label)

    plt.plot([0, 1], [0, 1], "k--", label="chance level (AUC = 0.5)")
    plt.axis("square")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC")
    plt.legend()
    #plt.grid()

    if outfile is not None:
        pass
        # fig.savefig()
    else:
        plt.show()

def plot_roc_curves_def_vals(biomarker_data, outfile=None):

    y_pred=[0,1,0,0,1,1]
    y_true=[0,1,1,0,0,1]

    RocCurveDisplay.from_predictions(
        y_pred,
        y_true,
        name="mypreds",
        color="darkorange"
    )

    plt.plot([0,1],[0,1], "k--", label="chance level (AUC = 0.5)")
    plt.axis("square")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC")
    plt.legend()


    if outfile is not None:
        pass
        #fig.savefig()
    else:
        plt.show()

