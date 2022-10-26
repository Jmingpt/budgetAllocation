import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from .mmmTransform import row_to_pivot
from .visualPlot import modelPlot


def mmm_model(df, ratio=0.1):
    if df is not None:
        date_range, mmm_df = row_to_pivot(df)
        X = mmm_df.drop('Revenue', axis=1)
        y = mmm_df['Revenue']

        scores = []
        for i in range(300):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=i)
            model = XGBRegressor(booster='gblinear')
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            scores.append([i, round(r2_score(y_test, y_pred), 4)])

        ops = pd.DataFrame(scores, columns=['idx', 'score']).set_index('idx').idxmax().values[0]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=ops)
        model = XGBRegressor(booster='gblinear')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        score = round(100 * r2_score(y_test, y_pred), 2)
        mae = round(mean_absolute_error(y_test, y_pred), 2)
        rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 2)

        coef = []
        for i, j in zip(model.coef_, X.columns):
            coef.append([i,j])
        plot_df = pd.DataFrame(coef, columns=['coef', 'params'])
        plot_df['mean_input'] = X_test.mean().values
        plot_df['contribution'] = plot_df['coef']*plot_df['mean_input']
        fig = modelPlot(plot_df, date_range)
        st.plotly_chart(fig, use_container_width=True)

        smr_col = st.columns((1, 1, 1))
        with smr_col[0]:
            st.write(f"Model Accuracy: **{score}%**")
        with smr_col[1]:
            st.write(f"MAE: {mae}")
        with smr_col[2]:
            st.write(f"RMSE: {rmse}")