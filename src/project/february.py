# Rerun the experiment with more info

from scikittests import *

def febRunner():
    base = "./february/"
    if not os.path.exists(base):
        os.mkdir(base)
    os.chdir(base)
    base = os.getcwd()
    config.the["file"] = "../" + config.the["file"]
    scitest()

    with open("RandomForestModel", "rb") as f:
        model = pickle.load(f)

    data = DATA(config.currFile)
    val = np.genfromtxt(fname=config.currFile, delimiter=",", dtype=float, skip_header=1, missing_values="?", filling_values=0)
    features, bestExplains, _ = RFExplainer(data, val, None, None, model)
    print("Features:", features)
    print("Explain Set:", bestExplains)
    top = DATA(data, bestExplains)
    print("The median values for the return Explainer results with 0 evals", stats(top)[0])