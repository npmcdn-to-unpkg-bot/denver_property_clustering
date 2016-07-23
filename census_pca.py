import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from sklearn.preprocessing import StandardScaler, Imputer
from sklearn.decomposition import PCA
import pandas as pd
import psycopg2
import os


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


def load_census_data_by_year(db_password,year):
    """Pull Census Data for each census tract in Denver"""

    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

    cursor = conn.cursor()
    cursor.execute("Select census_code, value,census_tract, yr from census_info where yr = %s;",(year,))
    census_df =pd.DataFrame(cursor.fetchall(),columns=['census_code','value','census_tract', 'yr'])
    conn.close()
    return census_df


def pivot_census_data(unpivoted_dataframe):
    """Pivots census dataframe

    IN: 19584x4 DF
    OUT: 144x137 DF
    """
    pivoted_census_df = unpivoted_dataframe.pivot(index='census_tract',columns='census_code',values='value')
    census_dataframe = pivoted_census_df.reset_index()
    return census_dataframe

def fix_data(df):
    df_final = missing_val_imputer(df)
    X = df_final
    return X

def missing_val_imputer(df):
    imr = Imputer(missing_values="NaN",strategy='mean',axis=0)
    imr = imr.fit(df)
    imputed_data = imr.transform(df.values)
    return imputed_data


if __name__ == '__main__':
    db_password = os.environ['AWS_DENVER_POSTGRES']
    census_df = pivot_census_data(load_census_data_by_year(db_password,2010))
    X = fix_data(census_df)
    stdsc = StandardScaler()
    x = stdsc.fit_transform(X)
    pca = PCA(n_components=10)
    X_pca = pca.fit_transform(x)

    scree_plot(10, pca)
