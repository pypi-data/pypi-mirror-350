from sklearn.neighbors import LocalOutlierFactor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def detect_outliers_lof(X, n_neighbors=20):
    lof = LocalOutlierFactor(n_neighbors=n_neighbors)
    yhat = lof.fit_predict(X)
    return yhat


def regression_without_outliers(X, y):
    yhat = detect_outliers_lof(X)
    X_clean = X[yhat == 1]
    y_clean = y[yhat == 1]
    model = LinearRegression().fit(X_clean, y_clean)
    y_pred = model.predict(X_clean)
    error = mean_squared_error(y_clean, y_pred, squared=False)
    return model, error
