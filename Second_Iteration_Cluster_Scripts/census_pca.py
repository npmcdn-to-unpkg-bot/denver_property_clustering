import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from sklearn.preprocessing import StandardScaler, Imputer
from sklearn.decomposition import PCA
import pandas as pd
import psycopg2
import os
import generate_census_data


def scree_plot(num_components, pca):
    ind = np.arange(num_components)
    vals = pca.explained_variance_ratio_
    plt.figure(figsize=(10, 6), dpi=250)
    ax = plt.subplot(111)
    ax.bar(ind, vals, 0.35,
           color=[(0.949, 0.718, 0.004),
                  (0.898, 0.49, 0.016),
                  (0.863, 0, 0.188),
                  (0.694, 0, 0.345),
                  (0.486, 0.216, 0.541),
                  (0.204, 0.396, 0.667),
                  (0.035, 0.635, 0.459),
                  (0.486, 0.722, 0.329),
                 ])
    for i in xrange(num_components):
        ax.annotate(r"%s%%" % ((str(vals[i]*100)[:4])), (ind[i]+0.2, vals[i]), va="bottom", ha="center", fontsize=12)

    ax.set_xticklabels(ind,
                       fontsize=12)

    ax.set_ylim(0, max(vals)+0.05)
    ax.set_xlim(0-0.45, 8+0.45)

    ax.xaxis.set_tick_params(width=0)
    ax.yaxis.set_tick_params(width=2, length=12)

    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("Variance Explained (%)", fontsize=12)

    plt.title("Scree Plot for the Census Data", fontsize=16)
    plt.savefig("scree.png", dpi= 100)

def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(10, 6), dpi=250)
    ax = plt.subplot(111)
    ax.axis('off')
    ax.patch.set_visible(False)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str('test'), fontdict={'weight': 'bold', 'size': 12})

    plt.xticks([]), plt.yticks([])
    plt.ylim([-0.1,1.1])
    plt.xlim([-0.1,1.1])

    if title is not None:
        plt.title(title, fontsize=16)
    plt.show()

def missing_val_imputer(df):
    """Missing values in the final dataframe are imputed using the mean of the column. Missing values are almost exclusivly parcel level metris"""

    imr = Imputer(missing_values="NaN",strategy='mean',axis=0)
    imr = imr.fit(df)
    imputed_data = imr.transform(df.values)
    return imputed_data

def fix_data(df):
    """The is a general clean-up function that drops certain columns, pops parcel_ids and calls the imputer function"""

    df = df.drop('Unnamed: 0',axis=1)
    df = df.drop('monthd',axis=1)
    df = df.drop('census_tract', axis=1)

    df_final = missing_val_imputer(df)
    X = df_final
    return X



if __name__ == '__main__':
    db_password = os.environ['AWS_DENVER_POSTGRES']

    census_df = pd.read_csv('census_df.csv')
    census_df['monthd'] = pd.to_datetime(census_df['monthd'])
    census_df = census_df.dropna(axis=1, how='all')
    census_df = census_df.fillna(value=np.nan)


    X = fix_data(census_df)
    stdsc = StandardScaler()
    x = stdsc.fit_transform(X)
    pca = PCA(n_components=10)
    X_pca = pca.fit_transform(x)

    scree_plot(10, pca)

    plot_embedding(X_pca)
