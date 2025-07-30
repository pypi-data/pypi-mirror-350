def drop_missing(df, subset=None):
    return df.dropna(subset=subset)


def drop_duplicates(df):
    return df.drop_duplicates()


def detect_outliers_zscore(df, column, threshold=3):
    from scipy.stats import zscore
    return df[(zscore(df[column].dropna()) < threshold)]


def drop_low_variance_columns(df, threshold=0.0):
    from sklearn.feature_selection import VarianceThreshold
    selector = VarianceThreshold(threshold)
    selector.fit(df.select_dtypes(include=['float64', 'int64']))
    cols = df.select_dtypes(include=['float64', 'int64']).columns[selector.get_support()]
    return df[cols]


def drop_columns_single_value(df):
    return df.loc[:, df.nunique() > 1]


def drop_columns_low_uniqueness(df, threshold=0.01):
    return df.loc[:, df.nunique() / len(df) > threshold]


def identify_duplicate_rows(df):
    return df[df.duplicated()]


def remove_duplicate_rows(df):
    return df.drop_duplicates()