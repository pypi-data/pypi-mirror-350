from sklearn.preprocessing import StandardScaler, MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def scale_data(df, columns, method='standard'):
    scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def normalize_column(df, column):
    df[column] = df[column] / df[column].abs().max()
    return df


def summary_statistics(df):
    return df.describe()


def plot_boxplot(df, column):
    sns.boxplot(x=df[column])
    plt.show()


def identify_outliers_std(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    upper = mean + threshold * std
    lower = mean - threshold * std
    return df[(df[column] > upper) | (df[column] < lower)]


def remove_outliers_std(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    upper = mean + threshold * std
    lower = mean - threshold * std
    return df[(df[column] <= upper) & (df[column] >= lower)]


def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]
