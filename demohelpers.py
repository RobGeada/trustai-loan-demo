import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
np.random.seed(0)
import pandas as pd
import sklearn

plt.style.use('https://raw.githubusercontent.com/RobGeada/stylelibs/main/material_rh.mplstyle')


def plot_clusters(X, y, knn=None, P=None, P2=None, explanations=None):
    plt.figure(figsize=(20, 10))
    cls = np.unique(y)
    cmap = plt.get_cmap("tab10")
    centroids = None

    if knn is None:
        plt.scatter(X[:,0], X[:,1], c='k', s=20)
    else:
        predictions = knn.predict(X)
        plt.scatter(X[:, 0], X[:, 1], c=predictions, cmap=cmap, s=20)

        centroids = []
        for c in cls:
            this_cls = X[np.where(predictions == c)]
            centroid = np.mean(this_cls, 0)
            centroids.append(centroid)
            plt.annotate("Cluster {}".format(c), centroid, fontsize=50, weight="bold",
                         color=cmap(c/max(cls)),
                         ha='center',
                         va='center',
                         path_effects=[pe.withStroke(linewidth=5, foreground="k")])

        if P is not None and P2 is None and type(P) is not list:
            predicted_p_cluster = knn.predict(P)
            plt.scatter(P[0][0], P[0][1], c="red", s=100, zorder=2, label="$P$")


            for idx, centroid in enumerate(centroids):
                if idx == predicted_p_cluster:
                    plt.plot([P[0][0], centroid[0]], [P[0][1], centroid[1]], c=cmap(idx/max(cls)), zorder=1)
                else:
                    plt.plot([P[0][0], centroid[0]], [P[0][1], centroid[1]], c="gray", linestyle="--", zorder=1)
            plt.legend(fontsize=20)

        elif P is not None and P2 is not None and type(P) is not list:
            predicted_p_cluster = knn.predict(P2)
            plt.scatter(P[0][0], P[0][1], c="red", s=100, zorder=2, label="$P$")
            plt.scatter(P2[0][0], P2[0][1], c="green", s=100, zorder=2, label="$P_{cf}$")


            plt.arrow(x=P[0][0], y=P[0][1],
                      dx=(P2[0][0]-P[0][0])*.9, dy=(P2[0][1]-P[0][1])*.9,
                      linewidth=2, head_width=.15, color="k", zorder=1, length_includes_head=True)



            for idx, centroid in enumerate(centroids):
                if idx == predicted_p_cluster:
                    plt.plot([P2[0][0], centroid[0]], [P2[0][1], centroid[1]], c=cmap(idx/max(cls)), zorder=1)
                else:
                    plt.plot([P2[0][0], centroid[0]], [P2[0][1], centroid[1]], c="gray", linestyle="--", zorder=1)

            plt.legend(fontsize=20)

        elif P is not None and P2 is None and type(P) is list and explanations is None:

            predicted_p_cluster0 = knn.predict(P[0])
            predicted_p_cluster1 = knn.predict(P[1])
            plt.scatter(P[0][0][0], P[0][0][1], c="red", s=100, zorder=2, label="$P_0$")
            plt.scatter(P[1][0][0], P[1][0][1], c="blue", s=100, zorder=2, label="$P_1$")

            for pidx, ppc in enumerate([predicted_p_cluster0, predicted_p_cluster1]):
                for idx, centroid in enumerate(centroids):
                    if idx == ppc:
                        plt.plot([P[pidx][0][0], centroid[0]], [P[pidx][0][1], centroid[1]], c=cmap(idx/max(cls)), zorder=1)

            plt.legend(fontsize=20)
        else:
            pass


def get_loan_data():
    app = pd.read_csv("data/application_record.csv")
    credit = pd.read_csv("data/credit_record.csv")

    data = app.merge(credit, on="ID")
    data = data[:10000]
    data['Male?'] = data["CODE_GENDER"].apply(lambda x: 1 if x == "M" else 0)
    data['Own Car?'] = data["FLAG_OWN_CAR"].apply(lambda x: 1 if x == "Y" else 0)
    data['Own Realty?'] = data["FLAG_OWN_REALTY"].apply(lambda x: 1 if x == "Y" else 0)
    data["Partnered?"] = data['NAME_FAMILY_STATUS'].apply(
        lambda x: 0 if x in ["Single / not married", "Widowed", "Separated"] else 1)
    data['Working?'] = data['NAME_INCOME_TYPE'].apply(lambda x: 0 if x in ["Pensioner", "Student"] else 1)
    data['Live with Parents?'] = data['NAME_HOUSING_TYPE'].apply(lambda x: 1 if x == "With parents" else 0)
    data['Days Old'] = data['DAYS_BIRTH'].apply(lambda x: -x)
    data = data[data['DAYS_EMPLOYED']<0]
    data['Days Employed'] = data['DAYS_EMPLOYED'].apply(lambda x: -x)

    data["Default?"] = data["STATUS"].apply(lambda x: 0 if x in ["C", "X"] else 1)
    data = data.drop(
        ["ID", "STATUS", "MONTHS_BALANCE", "CODE_GENDER", "NAME_EDUCATION_TYPE", "FLAG_OWN_CAR", "FLAG_OWN_REALTY",
         'NAME_FAMILY_STATUS', 'NAME_INCOME_TYPE', 'NAME_HOUSING_TYPE', "FLAG_MOBIL", "FLAG_WORK_PHONE", "FLAG_PHONE",
         "FLAG_EMAIL", "OCCUPATION_TYPE", 'DAYS_BIRTH', "DAYS_EMPLOYED"], 1)
    data = data.rename(
        columns={"CNT_CHILDREN": "# Children", "AMT_INCOME_TOTAL": "Total Income", "DAYS_BIRTH": "Days Since Birth",
                 "DAYS_EMPLOYED": "Days Employed", "CNT_FAM_MEMBERS": "# Family Members"})

    debts = data[data["Default?"] == 1].index
    nodebts = data[data["Default?"] == 0][:len(debts)].index

    data = data.loc[[i for i in list(debts)+list(nodebts)]]

    X,y  = data[[x for x in list(data) if x !="Default?"]], data["Default?"]
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, train_size=.90)
    return  X_train, X_test, y_train, y_test