import numpy as np
def count_missing(df):
    return df.isna().sum()


def replace_zeros_with_nan(df):
    df = df.replace(0, np.nan)
    return df

def replace_unknowns_with_nan(df):
    df = df.replace(['UNKNOWN', 'unknown', 'Unknown'], np.nan)
    return df
    

def drop_missing_rows(df):
    return df.dropna()


def lda_on_clean_data(X, y):
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    model = LinearDiscriminantAnalysis().fit(X, y)
    return model
