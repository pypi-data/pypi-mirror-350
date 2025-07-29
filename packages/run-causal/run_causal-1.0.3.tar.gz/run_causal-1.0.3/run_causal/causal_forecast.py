import warnings
import time
import json
import os

# Streamlit
import streamlit as st
import subprocess


# Core Python Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Sklearn
from sklearn.preprocessing import StandardScaler, PowerTransformer, QuantileTransformer
from sklearn.linear_model import LinearRegression, LassoCV, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split

# Statsmodels & SciPy
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats

# Regressors
from xgboost import XGBRegressor
from catboost import CatBoostRegressor


# SHAP for interpretability
import shap


# Suppress warnings
warnings.filterwarnings("ignore")



def calculate_vif(X, threshold=10):
    """
    Remove features with VIF higher than threshold iteratively.
    """
    try:
        while True:
            vif_df = pd.DataFrame()
            vif_df["Variable"] = X.columns
            vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
            
            max_vif = vif_df["VIF"].max()
            if max_vif > threshold:
                drop_feature = vif_df.sort_values("VIF", ascending=False).iloc[0]["Variable"]
                X = X.drop(columns=[drop_feature])
            else:
                break
    except:
        pass

    return X

def apply_boxcox(y):
    """
    Apply Box-Cox (or log) transformation to y to fix normality/heteroscedasticity.
    Shift y if any values are zero or negative.
    """
    y_shift = 0
    if (y <= 0).any():
        y_shift = abs(y.min()) + 1
        y = y + y_shift

    try:
        y_transformed, lmbda = stats.boxcox(y)
    except:
        y_transformed = np.log(y)
        lmbda = None

    return y_transformed, lmbda, y_shift

def fix_ols_assumptions(X, y, vif_threshold=10.0):
    """
    Fix all key OLS assumptions:
    - Multicollinearity (via VIF)
    - Non-normality and heteroscedasticity of residuals (Box-Cox and Yeo-Johnson)
    """
    # 1. Fix multicollinearity
    X_reduced = calculate_vif(X.copy(), threshold=vif_threshold)

    # 2. Power-transform X to address linearity + scale (Yeo-Johnson works with all values)
    pt = PowerTransformer(method='yeo-johnson', standardize=True)
    X_transformed = pd.DataFrame(pt.fit_transform(X_reduced), columns=X_reduced.columns, index=X.index)

    # 3. Transform y (Box-Cox requires positive)
    y_transformed, lmbda, y_shift = apply_boxcox(y)

    return X_transformed, y_transformed, lmbda, y_shift

def inverse_boxcox(y_transformed, lmbda, y_shift):
    """
    Inverse Box-Cox transformation to get predictions back to original scale.
    """
    if lmbda is None:
        y_original = np.exp(y_transformed)
    else:
        y_original = (y_transformed * lmbda + 1) ** (1 / lmbda)

    return y_original - y_shift

def interpret_shap(row):
    val = row['SHAP_Mean']
    if val > 0.01:
        return "Higher → Higher Target"
    elif val < -0.01:
        return "Higher → Lower Target"
    else:
        return "Little Impact"


# def get_model_outputs(X_train, y_train, X_test, models_to_run=None):
#     results = {}


#     def ols_model(X, y, X_eval ):
#         X_const = sm.add_constant(X)
#         model = sm.OLS(y, X_const).fit()
#         X_eval_const = sm.add_constant(X_eval)
#         y_pred = model.predict(X_eval_const)
#         p_values = model.pvalues[1:]  # exclude intercept
#         significant_vars = list(p_values[p_values < 0.05].index)
#         coeffs = model.params
#         equation = " + ".join([f"{coeffs[i]:.4f}*{i}" for i in coeffs.index if i != 'const'])
#         equation = f"{coeffs['const']:.4f} + {equation}" if 'const' in coeffs else equation
#         return y_pred, significant_vars, equation

#     def lasso_model(X, y, X_eval ):
#         model = LassoCV(cv=5).fit(X, y)
#         y_pred = model.predict(X_eval)
#         coefs = pd.Series(model.coef_, index=X.columns)
#         significant_vars = list(coefs[coefs != 0].index)
#         equation = " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
#         if model.intercept_ != 0:
#             equation = f"{model.intercept_:.4f} + {equation}"
#         return y_pred, significant_vars, equation

#     def elastic_net_model(X, y, X_eval ):
#         model = ElasticNetCV(cv=5).fit(X, y)
#         y_pred = model.predict(X_eval)
#         coefs = pd.Series(model.coef_, index=X.columns)
#         significant_vars = list(coefs[coefs != 0].index)
#         equation = " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
#         if model.intercept_ != 0:
#             equation = f"{model.intercept_:.4f} + {equation}"
#         return y_pred, significant_vars, equation

#     def xgb_model(X, y, X_eval ):
#         model = XGBRegressor(n_estimators=100, random_state=42)
#         model.fit(X, y)
#         y_pred = model.predict(X_eval)
#         return y_pred, None, None

#     def rf_model(X, y, X_eval ):
#         model = RandomForestRegressor(n_estimators=100, random_state=42)
#         model.fit(X, y)
#         y_pred = model.predict(X_eval)
#         return y_pred, None, None

#     def dt_model(X, y, X_eval ):
#         model = DecisionTreeRegressor(random_state=42)
#         model.fit(X, y)
#         y_pred = model.predict(X_eval)
#         return y_pred, None, None

#     def svr_model(X, y, X_eval ):
#         model = SVR()
#         model.fit(X, y)
#         y_pred = model.predict(X_eval)
#         return y_pred, None, None

#     def mlp_model(X, y, X_eval ):
#         model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
#         model.fit(X, y)
#         y_pred = model.predict(X_eval)
#         return y_pred, None, None




#     def catboost_model(X_train, y_train, X_test):
#         model = CatBoostRegressor(verbose=0)
#         model.fit(X_train, y_train)

#         y_pred = model.predict(X_test)
#         explainer = shap.TreeExplainer(model)
#         shap_array = explainer.shap_values(X)
#         mean_abs_shap = np.abs(shap_array).mean(axis=0)
#         shap_df = pd.Series(mean_abs_shap, index=X.columns).sort_values(ascending=False)
#         important_vars = shap_df.head(5).index.tolist()

         
#         return y_pred, important_vars, interpretation_dict



#     def stacking_model(X_train, y_train, X_test):
#         base_models = [
#             ('rf', RandomForestRegressor(n_estimators=50, random_state=42)),
#             ('lasso', LassoCV(cv=5))
#         ]
#         final_estimator = LinearRegression()
#         model = StackingRegressor(estimators=base_models, final_estimator=final_estimator)
#         model.fit(X_train, y_train)
#         return model.predict(X_test), None, None




    
#     model_dict = {
#         "OLS": ols_model,
#         "Lasso": lasso_model,
#         "ElasticNet": elastic_net_model,
#         "XGBoost": xgb_model,
#         "RandomForest": rf_model,
#         "DecisionTree": dt_model,
#         "SVR": svr_model,
#         "MLPRegressor": mlp_model,
#         "CatBoost": catboost_model,
#         "Stacking": stacking_model,
#     }

#     # Filter if user passed model list
#     if models_to_run:
#         model_dict = {k: v for k, v in model_dict.items() if k in models_to_run}

#     for name, model_fn in model_dict.items():
#         try:
#             y_pred, significant_vars, equation = model_fn(X_train, y_train, X_test)
#             results[name] = {
#                 'y_pred': y_pred,
#                 'significant_vars': significant_vars,
#                 'equation': equation
#             }
#         except Exception as e:
#             results[name] = {
#                 'y_pred': None,
#                 'significant_vars': None,
#                 'equation': None,
#                 'error': str(e)
#             }

#     return results

def get_model_outputs(X_train, y_train, X_test, models_to_run=None, tune_hyperparams=False):
    results = {}

    def ols_model(X, y, X_eval, tune_hyperparams):
        X_const = sm.add_constant(X)
        model = sm.OLS(y, X_const).fit()
        y_pred = model.predict(sm.add_constant(X_eval))
        p_values = model.pvalues[1:]  # exclude intercept
        significant_vars = list(p_values[p_values < 0.05].index)
        coeffs = model.params
        equation = f"{coeffs['const']:.4f} + " + " + ".join([f"{coeffs[i]:.4f}*{i}" for i in coeffs.index if i != 'const'])
        return y_pred, significant_vars, equation

    def lasso_model(X, y, X_eval, tune_hyperparams):
        model = LassoCV(cv=5) if tune_hyperparams else LassoCV()
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        coefs = pd.Series(model.coef_, index=X.columns)
        significant_vars = coefs[coefs != 0].index.tolist()
        equation = f"{model.intercept_:.4f} + " + " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
        return y_pred, significant_vars, equation

    def elastic_net_model(X, y, X_eval, tune_hyperparams):
        model = ElasticNetCV(cv=5) if tune_hyperparams else ElasticNetCV()
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        coefs = pd.Series(model.coef_, index=X.columns)
        significant_vars = coefs[coefs != 0].index.tolist()
        equation = f"{model.intercept_:.4f} + " + " + ".join([f"{coefs[i]:.4f}*{i}" for i in significant_vars])
        return y_pred, significant_vars, equation

    def xgb_model(X, y, X_eval, tune_hyperparams):
        if tune_hyperparams:
            from sklearn.model_selection import GridSearchCV
            param_grid = {
                'n_estimators': [50, 100],
                'max_depth': [3, 5],
                'learning_rate': [0.01, 0.1]
            }
            model = GridSearchCV(XGBRegressor(random_state=42), param_grid, cv=3)
            model.fit(X, y)
            model = model.best_estimator_
        else:
            model = XGBRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

        y_pred = model.predict(X_eval)
        importances = model.feature_importances_
        important_vars = list(pd.Series(importances, index=X.columns).sort_values(ascending=False).head(5).index)
        return y_pred, important_vars, None

    def rf_model(X, y, X_eval, tune_hyperparams):
        if tune_hyperparams:
            from sklearn.model_selection import GridSearchCV
            param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 5]}
            model = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3)
            model.fit(X, y)
            model = model.best_estimator_
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
        y_pred = model.predict(X_eval)
        importances = model.feature_importances_
        important_vars = list(pd.Series(importances, index=X.columns).sort_values(ascending=False).head(5).index)
        return y_pred, important_vars, None

    def dt_model(X, y, X_eval, tune_hyperparams):
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        importances = model.feature_importances_
        important_vars = list(pd.Series(importances, index=X.columns).sort_values(ascending=False).head(5).index)
        return y_pred, important_vars, None

    def svr_model(X, y, X_eval, tune_hyperparams):
        if tune_hyperparams:
            from sklearn.model_selection import GridSearchCV
            param_grid = {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear']}
            model = GridSearchCV(SVR(), param_grid, cv=3)
            model.fit(X, y)
            model = model.best_estimator_
        else:
            model = SVR()
            model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def mlp_model(X, y, X_eval, tune_hyperparams):
        if tune_hyperparams:
            from sklearn.model_selection import GridSearchCV
            param_grid = {
                'hidden_layer_sizes': [(64,), (64, 32)],
                'activation': ['relu', 'tanh']
            }
            model = GridSearchCV(MLPRegressor(max_iter=500, random_state=42), param_grid, cv=3)
            model.fit(X, y)
            model = model.best_estimator_
        else:
            model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
            model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    def catboost_model(X, y, X_eval, tune_hyperparams):
        model = CatBoostRegressor(verbose=0)
        if tune_hyperparams:
            model.grid_search({
                'depth': [4, 6],
                'learning_rate': [0.03, 0.1],
                'iterations': [100, 200]
            }, X=X, y=y)
        else:
            model.fit(X, y)

        y_pred = model.predict(X_eval)
        import shap
        explainer = shap.TreeExplainer(model)
        shap_array = explainer.shap_values(X)
        mean_abs_shap = np.abs(shap_array).mean(axis=0)
        shap_df = pd.Series(mean_abs_shap, index=X.columns).sort_values(ascending=False)
        important_vars = shap_df.head(5).index.tolist()
        return y_pred, important_vars, None

    def stacking_model(X, y, X_eval, tune_hyperparams):
        base_models = [
            ('rf', RandomForestRegressor(n_estimators=50, random_state=42)),
            ('lasso', LassoCV(cv=5))
        ]
        final_estimator = LinearRegression()
        model = StackingRegressor(estimators=base_models, final_estimator=final_estimator)
        model.fit(X, y)
        y_pred = model.predict(X_eval)
        return y_pred, None, None

    model_dict = {
        "OLS": ols_model,
        "Lasso": lasso_model,
        "ElasticNet": elastic_net_model,
        "XGBoost": xgb_model,
        "RandomForest": rf_model,
        "DecisionTree": dt_model,
        "SVR": svr_model,
        "MLPRegressor": mlp_model,
        "CatBoost": catboost_model,
        "Stacking": stacking_model,
    }

    if models_to_run:
        model_dict = {k: v for k, v in model_dict.items() if k in models_to_run}
    for name, model_fn in model_dict.items():
        try:
            y_pred, important_vars, equation = model_fn(X_train, y_train, X_test, tune_hyperparams)
            results[name] = {
                "y_pred": y_pred,
                "significant_vars": important_vars,
                "equation": equation
            }
        except Exception as e:
            results[name] = {
                "y_pred": None,
                "significant_vars": None,
                "equation": None,
                "error": str(e)
            }

    return results

def get_testing_data(result_df, n, config):
    try:
        result_df[config['date_column']] = pd.to_datetime(result_df[config['date_column']], format=config['date_format'])
        result_df['yearmonth'] = result_df['yearmonth'].dt.strftime('%Y-%m-%d')
        
        # Define your grouping columns
        grouping_cols = config['grouping_columns']
        
        # Sort the data
        df = result_df.sort_values(grouping_cols + [config['date_column']])
        
        # Filter last "n" rows per group
        df = (
            df.groupby(grouping_cols, group_keys=False)
              .apply(lambda group: group.tail(n))
              .reset_index(drop=True)
        )
    except:
        return result_df
    return df

def drop_zero_rows_and_get_active_columns(subset, columns, config):

    cols_to_check = pd.Index(columns).difference(config['excluded_columns_from_drop_zero_list'])
    subset = subset[~(subset[cols_to_check] == 0).all(axis=1)]
    
    non_zero_cols = []
    for col in columns:
        if (subset[col] == 0).all():
            subset.drop(columns=col, inplace=True)
        else:
            non_zero_cols.append(col)
    return subset, non_zero_cols


def full_output_ols(df, features, target, group_cols,simulate_change, selected_causal, change_percent, models_needed=None, config=None):
    # count = 0
    df.fillna(0, inplace=True)
    df.sort_values(by=group_cols + [config['date_column']], inplace=True)

    df_out = pd.DataFrame()
    total_cases = df[group_cols].drop_duplicates().shape[0]
    for keys, group_idx in df.groupby(group_cols).groups.items():

        group = df.loc[group_idx]
        if config and config.get("drop_zero_rows_and_get_active_columns", False):
            group, features = drop_zero_rows_and_get_active_columns(group, features, config)
        
        group.fillna(0, inplace=True)

        
        X = group[features].copy().reset_index(drop=True)
        y = group[target].copy().reset_index(drop=True)

        # Apply scaling only if config says so
        if config and config.get("scale_features", False):
            scaler = StandardScaler()
            X = pd.DataFrame(scaler.fit_transform(X), columns=features)

        # Fix OLS assumptions if specified
        if config and config.get("fix_ols_violations", False):
            X, y_transformed, lmbda, y_shift = fix_ols_assumptions(X, y)
        else:
            y_transformed = y.copy()
            lmbda = None
            y_shift = 0

        n = len(X)
        if config['training_data_percent']:
            train_size = int(config['training_data_percent'] * n)
        else:
            train_size = n
        if n >= 12:
            X_train = X.iloc[:train_size]
            y_transformed = pd.Series(y_transformed, index=y.index)
            y_train = y_transformed.iloc[:train_size]

            x_changed = X.copy(deep=True)

            if simulate_change:
                if len(selected_causal) > 0:
                    for feature in selected_causal:
                        if feature in x_changed.columns:
                            percent_change = config["change_percent"].get(feature, 0)
                            x_changed[feature] *= (1 + percent_change / 100)
            # if config['tune_hyperparams']:
            #     results = get_model_outputs(X_train, y_train, x_changed, models_to_run=models_needed, tune_hyperparams = config['tune_hyperparams'])
            # else:
            results = get_model_outputs(X_train, y_train, x_changed, models_to_run=models_needed)

            for model, output in results.items():

                sig_vars_list = output['significant_vars']

                first_elements_sig_vars = output['significant_vars']
                st.markdown(f"**Significant Factors:** {first_elements_sig_vars}")

                y_pred_var = str(model) + '_y_pred'
                y_pred_transformed = output['y_pred']
                y_pred_sig_vars = str(model) + '_significant_vars'
                y_pred_equation = str(model) + '_equation'
                # print(y_pred_transformed)

                if y_pred_transformed is not None:
                    if config and config.get("fix_ols_violations", False):
                        y_pred = inverse_boxcox(y_pred_transformed, lmbda, y_shift)
                    else:
                        y_pred = y_pred_transformed

                    y_pred = np.where(np.isfinite(y_pred), y_pred, np.nan)
                else:
                    y_pred = 0

                group[y_pred_var] = y_pred
                group[y_pred_sig_vars] = [output['significant_vars']] * len(group)
                group[y_pred_equation] = [output['equation']] * len(group)
                
        df_out = pd.concat([df_out, group])

    return df_out, features

def correct_outliers(df, column, threshold=3):
    """
    Replace outliers using Z-score method by capping them to lower and upper bounds.
    """
    mean_val = df[column].mean()
    std_val = df[column].std()
    
    # Compute limits
    lower_limit = mean_val - threshold * std_val
    upper_limit = mean_val + threshold * std_val
    
    # Clip values outside the bounds
    df[column] = df[column].clip(lower=lower_limit, upper=upper_limit)
    
    return df


def main_function(config, CONFIG_PATH,simulate_change, selected_causal = None, change_percent = {}):
    # Load and prepare data
    original_data = pd.read_csv(config["data_path"])
    original_data = original_data[config["required_columns"]].copy()
    original_data.fillna(0, inplace = True)
    grouping_columns = config['grouping_columns']
    if config["baseline_forecast_check"]:
        original_data["Error_reg"] = original_data[config["original_target_column"]] - original_data[config["earlier_forecast_columns"]]
    else:
        original_data["Error_reg"] = original_data[config["original_target_column"]]
    
    if config["target_column"] not in config["required_columns"]:
        config["required_columns"].append(config["target_column"])
        save_config(config, CONFIG_PATH)
    if config['filter_granularity']:
        filter_granularity = config['filter_granularity']

        # Dynamically create a boolean mask based on all conditions
        condition = (original_data[grouping_columns[0]] == filter_granularity[0])
        for col, val in zip(grouping_columns[1:], filter_granularity[1:]):
            condition &= (original_data[col] == val)

        # Apply the condition to filter the DataFrame
        original_data = original_data[condition]
    try:
        original_data[config['date_column']] = pd.to_datetime(original_data[config['date_column']], format = config["date_format"])
        original_data[config['date_column']] = original_data[config['date_column']].dt.strftime('%Y-%m-%d')
    except:
        st.markdown("`Problem in Date Column, Please check the Format`")
        return
    original_data = original_data.groupby(grouping_columns + [config['date_column']]).sum().reset_index()
    
    if "monthly_seasonality" in config['causal_features']:
        original_data['month_no'] = original_data[config['date_column']].apply(lambda x: int(str(x).split("-")[1]))

        original_data['monthly_seasonality'] = config['monthly_seasonality']
        original_data['monthly_seasonality'] = original_data.apply(lambda row: 1 if row['month_no'] == row['monthly_seasonality'] else 0.0001, axis=1)

    
    if "quarterly_seasonality" in config['causal_features']:
        original_data['month_no'] = original_data[config['date_column']].apply(lambda x: int(str(x).split("-")[1]))

        original_data['quarter_no'] = ((original_data['month_no'] - 1) // 3) + 1
        original_data['quarterly_seasonality'] = config['quarterly_seasonality']
        original_data['quarterly_seasonality'] = original_data.apply(lambda row: 1 if row['quarter_no'] == row['quarterly_seasonality'] else 0.0001, axis=1)

    if config['outlier_correction']:
        for column in config['outlier_correction_columns']:
            original_data = correct_outliers(original_data, column, threshold=3)

    # Run modeling
    models = config["models"]
    causal_features = config["causal_features"].copy()
    grouping = config["grouping_columns"]
    target = config["target_column"]

    # Add lag features
    if config and config.get("enable_lag_feature", False):
        no_of_lags = config['no_of_lags']
        columns_with_lag_features = config["columns_with_lag_features"]

        for column in columns_with_lag_features:
            for lag in range(0, no_of_lags):
                lag += 1
                new_column = f'{column}_after_lag_{lag}'
                original_data[new_column] = original_data.groupby(config["grouping_columns"])[column].shift(lag)
                if new_column not in causal_features:
                    causal_features.append(new_column)


    
    
    result_df, features = full_output_ols(original_data, causal_features, target, grouping, simulate_change, selected_causal, change_percent, models_needed=models, config=config)
    result_df.fillna(0, inplace=True)


    original_target_column = config['original_target_column']
    # print(result_df.columns)
    if config["baseline_forecast_check"]:
        earlier_forecast_columns = config['earlier_forecast_columns']

        result_df['MAPE_TS'] = np.where(
            result_df[original_target_column] == 0, 0,
            abs((result_df[earlier_forecast_columns] - result_df[original_target_column]) / result_df[original_target_column])
        ) * 100

    else:
        result_df['MAPE_TS'] = 0
    # Filter test data
    testing_date = config["test_start_date"]
    if len(str(testing_date)) <= 2:
        testing_date = int(testing_date)
        df1 = get_testing_data(result_df, testing_date, config)
    else:
        df1 = result_df[result_df[config['date_column']] >= config["test_start_date"]]
        
    # Evaluation loop
    evaluation_results = []
    for model in models:
        final_forecast_var = f"{model}_final_forecast"
        y_pred_var = f"{model}_y_pred"
        mape_var = f"{model}_MAPE_causal"
        if config["baseline_forecast_check"]:
            earlier_forecast_columns = config['earlier_forecast_columns']
            df1[final_forecast_var] = df1[y_pred_var] + df1[earlier_forecast_columns]
            result_df[final_forecast_var] = result_df[y_pred_var] + result_df[earlier_forecast_columns]

        else:
            df1[final_forecast_var] = df1[y_pred_var]
            result_df[final_forecast_var] = result_df[y_pred_var]


        if simulate_change:
            sales_before = result_df[original_target_column].sum()
            sales_after = result_df[final_forecast_var].sum()
            st.markdown(f'**Overall Primary Sales will change from** {sales_before} to {sales_after}')

            
        df1[mape_var] = np.where(
            df1[original_target_column] == 0, 0,
            abs((df1[final_forecast_var] - df1[original_target_column]) / df1[original_target_column])
        ) * 100

        if config["baseline_forecast_check"]:
            group_mape = df1[[*grouping, mape_var, "MAPE_TS"]].groupby(grouping).mean().reset_index()
        
            group_mape["difference"] = (group_mape["MAPE_TS"] - group_mape[mape_var]) 
        else:
            group_mape = df1[[*grouping, mape_var]].groupby(grouping).mean().reset_index()

    #     better_than_ts = group_mape[group_mape[mape_var] < group_mape["MAPE_TS"]].shape[0]

    #     greater_than_5pct = group_mape[group_mape["difference"] > 5].shape[0]
    
    #     evaluation_results.append({
    #         "Model": model,
    #         "Better_than_TS_count": better_than_ts,
    #         "Greater_than_5pct_count": greater_than_5pct
    #     })
    
    # summary_df = pd.DataFrame(evaluation_results)
    # st.dataframe(df1.drop(['CatBoost_significant_vars', 'CatBoost_equation'], axis = 1))
    if config["baseline_forecast_check"]:
        col = grouping + [config['date_column']] +features + [original_target_column,config['earlier_forecast_columns'], final_forecast_var,"MAPE_TS", mape_var]
        # st.markdown(f"**MAPE TS:** `{group_mape["MAPE_TS"][0]}`")
        mape_ts_value = group_mape["MAPE_TS"][0]
        mape_causal_value  = group_mape[mape_var][0]
        st.markdown(f"**MAPE TS :** {mape_ts_value:.2f}")
        st.markdown(f"**MAPE Causal :** {mape_causal_value:.2f}")

        
    else:
        col = grouping + [config['date_column']] +features + [original_target_column, final_forecast_var, mape_var]
        mape_causal_value  = group_mape[mape_var][0]

        st.markdown(f"**MAPE Causal :** {mape_causal_value:.2f}")

    # st.dataframe(df1[col])

    # print(group_mape)
    plt = draw_graph(df1,final_forecast_var, config,simulate_change, selected_causal, change_percent)


 

    result_df[mape_var] = np.where(
        result_df[original_target_column] == 0, 0,
        abs((result_df[final_forecast_var] - result_df[original_target_column]) / result_df[original_target_column])
        ) * 100


    return group_mape[mape_var], df1[col], result_df[col], plt


def draw_graph(df1,final_forecast_var, config, simulate_change, selected_causal = None, change_percent = 0):
    # Load and prepare data
    original_data = pd.read_csv(config["data_path"])
    original_data = original_data[config["required_columns"]].copy()
    grouping_columns = config['grouping_columns']
    
    if config['filter_granularity']:
        filter_granularity = config['filter_granularity']

        # Dynamically create a boolean mask based on all conditions
        condition = (original_data[grouping_columns[0]] == filter_granularity[0])
        for col, val in zip(grouping_columns[1:], filter_granularity[1:]):
            condition &= (original_data[col] == val)

        # Apply the condition to filter the DataFrame
        original_data = original_data[condition]
    
    try:
        original_data[config['date_column']] = pd.to_datetime(original_data[config['date_column']], format = config["date_format"])
        original_data[config['date_column']] = original_data[config['date_column']].dt.strftime('%Y-%m-%d')
    except:
        st.markdown("`Problem in Date Column, Please check the Format`")
        return
    
    original_data = original_data[original_data[config['date_column']] < config["test_start_date"]]
    original_target_column = config['original_target_column']
    if config["baseline_forecast_check"]:
        earlier_forecast_columns = config['earlier_forecast_columns']
        original_data.drop(earlier_forecast_columns, axis = 1, inplace = True)

    original_data = original_data.groupby(grouping_columns + [config['date_column']]).sum().reset_index()
    df1 = df1.groupby(grouping_columns + [config['date_column']]).sum().reset_index()
    
    df = pd.concat([original_data,df1])

    if config['outlier_correction']:
        for column in config['outlier_correction_columns']:
            original_data = correct_outliers(df, column, threshold=3)

    
    filtered_df = df.copy()
    scaler = StandardScaler()
    unique_combinations = filtered_df[grouping_columns].drop_duplicates() 
    for _, row in unique_combinations.iterrows():

        if config['filter_granularity']:
            filter_granularity = config['filter_granularity']

            # Dynamically create a boolean mask based on all conditions
            condition = (filtered_df[grouping_columns[0]] == filter_granularity[0])
            for col, val in zip(grouping_columns[1:], filter_granularity[1:]):
                condition &= (filtered_df[col] == val)

            # Apply the condition to filter the DataFrame
            subset = filtered_df[condition]
    
        subset = subset.sort_values(config['date_column'])
    
        plt.figure(figsize=(10, 4))
        
        # subset[[original_target_column,final_forecast_var, earlier_forecast_columns]] = scaler.fit_transform(subset[[original_target_column,final_forecast_var,earlier_forecast_columns]])
    
        plt.plot(subset[config['date_column']], subset[original_target_column], marker='o', linestyle='-', label='Input Data', )

        if config["baseline_forecast_check"]:
            earlier_forecast_columns = config['earlier_forecast_columns']
            plt.plot(subset[config['date_column']], subset[earlier_forecast_columns], marker='.', linestyle='-', label= earlier_forecast_columns, color = 'red')


        plt.plot(subset[config['date_column']], subset[final_forecast_var], marker='*', linestyle='--', label='Forecast', color = 'orange')

        # plt.plot(subset[config['date_column']], subset['promo_lag1'], marker='.', linestyle='--', label='Promo Lag')
        
        
        plt.title(filter_granularity)
        plt.xlabel(config['date_column'])
        plt.ylabel('Values')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.legend()  # <- this adds the labels
        plt.tight_layout()
        plt.show()
        # st.pyplot(plt.gcf())
        return plt
    

def load_config(path):
    """Load config if exists, else create a new one."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        default_config = {}  # You can prefill with defaults if desired
        with open(path, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config


# Save updated config to the JSON file
def save_config(config,CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def generating_key(values):
    return ",".join(values)


def upload_data_file(config, CONFIG_PATH):

    st.markdown("### 📁 Step 1: Upload Your Data")
    with st.expander("ℹ️ Instructions"):

        st.markdown("""
        Upload a **CSV file** containing your dataset.  
        This dataset should include:

        - The **target variable** you want to forecast (e.g., sales)
        - One or more **causal features** (e.g., media spend, promotion spend, visibility)
        - Optionally, a **baseline forecast** if available
        - A **date column** and **granularity columns** (e.g., brand, region, category)

        The uploaded data will be used for causal analysis and forecasting.
        """)

    uploaded_file = st.file_uploader("Upload File", type=["csv"], label_visibility="collapsed")
    # print("uploaded_file", uploaded_file)

    if uploaded_file is not None:
        # Create a temporary directory or define one
        save_dir = "uploaded_files"
        os.makedirs(save_dir, exist_ok=True)

        # Define full path to save the file
        save_path = os.path.join(save_dir, uploaded_file.name)

        # Save file to disk
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load the file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(save_path)
        else:
            df = pd.read_excel(save_path)

        st.success(f"✅ Uploaded: {uploaded_file.name}")
        # st.dataframe(df)

        # Store file reference in config
        config = {}
        config["reset_config"] = False
        config["data_path"] = save_path  # full path

        save_config(config, CONFIG_PATH)

        return df, config
    try:
        default_path = config.get("data_path", "generating_final_data.csv")

        if os.path.exists(default_path):
            st.info(f"No file uploaded. Using default: `{default_path}`")
            df = pd.read_csv(default_path)
            return df, config
        else:
            st.warning("⚠️ No file uploaded and no default dataset found. Please upload a file to proceed.")
            st.stop()
    except:
        st.stop()
        


def get_required_columns(config, original_data, CONFIG_PATH):
    # st.subheader("🧾 Required Columns")
    # st.markdown("### ✅ Step 2: Select Required Columns")

    # st.markdown("""
    # After uploading the file, select only the **relevant columns** needed for modeling.  
    # If your dataset contains extra or irrelevant columns (e.g., IDs, metadata), you can exclude them.

    # - Use the multiselect box to choose specific columns  
    # - Or simply check **'Select all columns'** if everything is relevant
    # """)

    st.markdown("### ✅ Step 2: Select Required Columns")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        After uploading the file, select only the **relevant columns** needed for modeling.  
        If your dataset contains extra or irrelevant columns (e.g., IDs, metadata), you can exclude them.

        - Use the multiselect box to choose specific columns  
        - Or simply check **'Select all columns'** if everything is relevant
        """)

    # Checkbox to select all columns
    select_all_required = st.checkbox("Select All Columns", value=False)

    # Get list of all columns in the dataset
    all_columns = list(original_data.columns)

    # If 'Select All' is checked, preselect all columns
    default_required = all_columns if select_all_required else config.get("required_columns", [])

    # Multiselect for required columns
    config["required_columns"] = st.multiselect(
        "Select Required Columns",
        options=all_columns,
        default=default_required, label_visibility="collapsed"
    )

    save_config(config,CONFIG_PATH)
    return config

def get_grnaularity(config, CONFIG_PATH):

    st.markdown("### 🧩 Step 3: Select Grouping Columns (Granularity)")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        Select the columns that define the **granularity** for your forecast.  
        These are the dimensions by which you want to segment the data (e.g., **Banner**, **Category**, **Brand**, **Region**, etc.).

        - Forecasts and metrics will be generated separately for each unique combination of these grouping values.
        - You can select **multiple columns** for hierarchical or multi-level granularity.
        - Once done, confirm using the checkbox below.
        """)
    config["grouping_columns"] = st.multiselect(
        "Select Grouping Columns",
        options=config["required_columns"],
        default=config.get("grouping_columns", []),
        key="grouping_multiselect", label_visibility="collapsed"
    )

    config["grouping_columns_done"] = st.checkbox("Done with Grouping Columns", value=config.get("grouping_columns_done", False))
    if config["grouping_columns_done"] == False:
        st.stop()
    save_config(config, CONFIG_PATH)
    return config


def get_causal_columns(config, CONFIG_PATH):
    st.markdown("### 📊 Step 4: Select Causal Features")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        Select the features that are believed to **influence the target variable** — these are referred to as **causal features**.

        Examples of causal factors include:
        - **Media spend**
        - **Promotions**
        - **Visibility**

        🔍 **Optional Time Granularity Filters**  
        You may optionally specify if the causal impact should be analyzed at a **monthly** or **quarterly** level.  
        If selected, additional options will appear to choose specific **months** or **quarters**.

        ✅ Once you're done selecting the causal features and filters, check the confirmation box below to proceed.
        """)

    config["causal_features"] = st.multiselect("Select Causal Columns", config["required_columns"] + ['monthly_seasonality','quarterly_seasonality'], config.get("causal_features", []),key="Causal_multiselect", label_visibility="collapsed")

    # save_config(config,CONFIG_PATH)
    config["causal_features_done"] = st.checkbox("Done with Causal Features", value=config.get("causal_features_done", False))
    if config["causal_features_done"] == False:
        st.stop()

        
    save_config(config, CONFIG_PATH)
    
    return config

def get_monthly_seasonality(config, CONFIG_PATH):
    if "monthly_seasonality" in config["causal_features"]:

        valid_seasonality = list(range(13))
        default_value = config.get("monthly_seasonality", 8)

        # Ensure default_value is valid
        if default_value not in valid_seasonality:
            default_value = 0  # Fallback to 8 if invalid

        config["monthly_seasonality"] = st.selectbox(
            "Monthly Seasonality",
            valid_seasonality,
            index=valid_seasonality.index(default_value)
        )
    else:
        config["monthly_seasonality"] = 0
    save_config(config,CONFIG_PATH)
    return config

def get_quarterly_seasonality(config, CONFIG_PATH):
    if "quarterly_seasonality" in config["causal_features"]:

        valid_quarterly_seasonality = list(range(5))
        default_value = config.get("quarterly_seasonality", 2)

        # Ensure default_value is valid
        if default_value not in valid_quarterly_seasonality:
            default_value = 0  # Fallback to 8 if invalid

        config["quarterly_seasonality"] = st.selectbox(
            "Quarterly Seasonality",
            valid_quarterly_seasonality,
            index=valid_quarterly_seasonality.index(default_value)
        )
    else:
        config["quarterly_seasonality"] = 0
    save_config(config,CONFIG_PATH)
    return config

def get_date_and_format(config, CONFIG_PATH, original_data):

    st.markdown("### 📅 Step 5: Select Date Column and Date Format")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        Select the column that contains the **date or time information** for your dataset.

        This column is critical for:
        - Properly sorting and analyzing data over time  
        - Creating lag features and time-based aggregations  
        - Ensuring accurate forecasting  

        After selecting the date column, please specify the **format of the date values** in the dataset.  

        Common date formats include:  
        - `%Y-%m-%d` (e.g., 2023-04-30)  
        - `%d-%m-%Y` (e.g., 30-04-2023)  
        - `%m/%d/%Y` (e.g., 04/30/2023)  
        - `%Y/%m/%d` (e.g., 2023/04/30)  
        - `%Y%m` (e.g., 202304 for April 2023)  
        - `%Y%m%d` (e.g., 20230430)  

        Please select the format that **exactly matches** your data to ensure correct parsing.
        """)
    required_cols = config.get("required_columns", [])
    default_target = config.get("date_column", required_cols[0])

    config["date_column"] = st.selectbox(
    "Select Date Column",
    options=required_cols,
    index=required_cols.index(default_target)
    )

    config["date_format"] = st.selectbox(
        "Select Date Format",
        options=["%Y%m", "%m%Y","%Y%m%d", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%d%m%Y"]
        # options=["%Y%m"]

    )
    # if config["date_format"]:
    try:
        original_data[config['date_column']] = pd.to_datetime(original_data[config['date_column']], format = config["date_format"])
        original_data[config['date_column']] = original_data[config['date_column']].dt.strftime('%Y-%m-%d')
    except:
        st.markdown("`Problem in Date Column, Please check the Date Column Name and its format`")
        st.stop()
    save_config(config,CONFIG_PATH)
    return config

def get_target_column(config, CONFIG_PATH):

    st.markdown("### 🎯 Step 6: Baseline Forecast Selection")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        Use the checkbox below to indicate whether your dataset includes a **Baseline Forecast** column.

        - If **checked**, select both the **Target (Actual)** column and the **Baseline Forecast** column.  
        The app will calculate the **uplift** as:  
        `Uplift = Target - Baseline Forecast`  
        and model the uplift for causal analysis.

        - If **unchecked**, select only the **Target (Actual)** column.  
        The app will model the target variable directly.
        """)
    config["baseline_forecast_check"] = st.checkbox("Baseline Forecast Available", value=config.get("baseline_forecast_check", False))
    required_cols = config.get("required_columns", [])
    default_target = config.get("original_target_column", required_cols[-1] )

    if default_target not in required_cols:
        default_target = required_cols[-1]  # Fallback to first required column


    config["original_target_column"] = st.selectbox(
        "Select Target Column",
        options=required_cols,
        index=required_cols.index(default_target )
    )

    if config["baseline_forecast_check"]:

        config["earlier_forecast_columns"] = st.selectbox(
        "Select Baseline Column",
        options=required_cols,
        index=required_cols.index(config.get("earlier_forecast_columns",default_target ))
        )
        config["target_column"] = "Error_reg"
    else:
        config["target_column"] = config["original_target_column"] 
    save_config(config,CONFIG_PATH)
    return config

              
def get_model(config, CONFIG_PATH):
    st.markdown("### 🧠 Step 7: Select Model")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        Choose the **Model** you want to use for forecasting.
        Select the model that best suits your data and analysis needs.
        """)
    config["models"] = [st.selectbox(
        "Select Model",
        [
            "OLS", "Lasso", "ElasticNet", "XGBoost", "RandomForest",
            "DecisionTree", "SVR", "MLPRegressor", "CatBoost", "Stacking"
        ],
        index=(
            [
                "OLS", "Lasso", "ElasticNet", "XGBoost", "RandomForest",
                "DecisionTree", "SVR", "MLPRegressor", "CatBoost", "Stacking"
            ].index(config.get("models", ["CatBoost"])[0])
            if config.get("models") else 8  # Default to "CatBoost"
        )
    )]
    save_config(config,CONFIG_PATH)
    return config

def apply_scaling_or_fix_ols(config, CONFIG_PATH): 
    st.markdown("### 📐 Step 8: Scaling & Fix OLS Assumptions")

    # - **Hyperparameter Tuning:**  
    # When enabled, the app will automatically search for the best hyperparameters for selected models using techniques like cross-validation and grid search. This may improve accuracy but can increase computation time.


    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - **Scaling:**  
        When enabled, this option applies feature scaling (e.g., standardization) to the causal variables to improve model performance and convergence.

        - **Fix OLS Assumptions:**  
        If selected, the app will automatically fix violations of linear regression assumptions if violations are present.  
        """)

    # config["tune_hyperparams"] = st.checkbox("Hyperparameter Tuning", value=config.get("tune_hyperparams", True))
    config["scale_features"] = st.checkbox("Scale Features", value=config.get("scale_features", True))
    config["fix_ols_violations"] = st.checkbox("Fix OLS Violations", value=config.get("fix_ols_violations", True))
    save_config(config,CONFIG_PATH)
    return config

def drop_zeros(config, CONFIG_PATH):

    st.markdown("### 🚫 Step 9: Drop Zero Rows and Columns")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - Sometimes, causal feature columns may contain only zeros or mostly zeros, which can negatively impact model training.  

        - This step allows you to drop:  
        -- **Columns** where all causal values are zero (i.e., no variability).  
        -- **Rows** where all causal feature values are zero (i.e., no causal influence).  

        - Special Case:  
        -- Some causal features, like **'no of working days'**, will never be zero but may be selected as a causal factor.  
        -- You can select such columns under **'Select Non-Zero Causal Columns'** so the app ignores them when checking rows for zeros.  
        -- If all other causal factors (excluding these non-zero causal columns) are zero for a row, that row will be dropped.  
        -- If there is **no special case**, you can leave the 'Select non-zero causal columns' **blank**.

        - This ensures meaningful data is retained while removing irrelevant zero-value data.
        """)
    config["drop_zero_rows_and_get_active_columns"] = st.checkbox("Drop Zeros", value=config.get("drop_zero_rows_and_get_active_columns", True))
                
    if config["drop_zero_rows_and_get_active_columns"]:
        # Columns to apply lag features to
        config["excluded_columns_from_drop_zero_list"] = st.multiselect(
            "Select Non-Zero Causal Columns",
            config["causal_features"],
            config.get("excluded_columns_from_drop_zero_list", [])
        )

    save_config(config,CONFIG_PATH)
    return config

def apply_outlier_correction(config, CONFIG_PATH):
    st.markdown("### ⚠️ Step 10: Outlier Correction")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - Enable **Outlier Correction** to clean your data by adjusting extreme values in selected columns.  
        - When selected, choose one or more columns to apply outlier correction.  
        - This helps improve model accuracy by reducing the impact of anomalous data points.
        """)
    config["outlier_correction"] = st.checkbox("Outlier Correction", value=config.get("outlier_correction", False))

    if config["outlier_correction"]:
        # Columns to apply lag features to
        config["outlier_correction_columns"] = st.multiselect(
            "Select Columns For Outlier Correction",
            config["required_columns"],
            config.get("outlier_correction_columns", [])
        )
    save_config(config,CONFIG_PATH)
    return config

def shifting_data_by_lags(config, CONFIG_PATH):

    st.markdown("### ⏮️ Step 11: Enable Lag Features")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - Enable **Lag Features** to capture the delayed effect of causal factors on the target variable.  
        - Once enabled, specify:
            - **Number of lags** (e.g., 1, 2, 3).
            - **Causal columns** to apply the lag on.
        - Example:  
            If you select `promotion` with 2 lags, the app will generate:
            - `promotion_after_lag_1`  
            - `promotion_after_lag_2`  
        """)
    config["enable_lag_feature"] = st.checkbox("Enable Lag Features", value=config.get("enable_lag_feature", False))

    if config["enable_lag_feature"]:
        # Number of lags to create
        config["no_of_lags"] = st.slider(
            "Number of Lags", 
            min_value=1, 
            max_value=12, 
            value=config.get("no_of_lags", 3)
        )

        # Columns to apply lag features to
        config["columns_with_lag_features"] = st.multiselect(
            "Columns to Create Lag Features For",
            config["causal_features"],
            config.get("columns_with_lag_features", [])
        )

    else:
        # Clear lag-related settings if disabled
        config["no_of_lags"] = 0
        config["columns_with_lag_features"] = []
    
    save_config(config,CONFIG_PATH)
    return config


def get_training_testing_data(config, CONFIG_PATH, original_data):
    st.markdown("### 🧪 Step 12: Train/Test Split")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - Define how to split your data into training and testing sets.  
        - You can choose one of two methods:
            1. **By Percentage**  
                - Enable the checkbox to activate percentage split.  
                - Use the slider to select the training percentage (e.g., 80%).  
                - Remaining data (e.g., 20%) will be used for testing.
            2. **By Date**  
                - Leave the checkbox unchecked.  
                - Select the **Test Start Date** from available options in the dropdown.
                - All rows before this date go into training, and from this date onward into testing.
        - Make sure the date you enter matches the selected **Date Format**.
        """)

    config["split_by_percentage"] = st.checkbox("Split by Percentage", value=config.get("split_by_percentage", False))

    # Get unique dates
    try:
        original_data[config["date_column"]] = pd.to_datetime(original_data[config["date_column"]])
        # original_data[config['date_column']] = original_data[config['date_column']].dt.strftime('%Y-%m-%d')

        unique_dates = sorted(original_data[config["date_column"]].unique())
    except Exception as e:
        st.error(f"Error parsing date column: {e}")
        st.stop()

    if config["split_by_percentage"]:
        # Percentage-based split
        config["training_data_percent"] = st.slider(
            "Training Data %",
            0.1,
            0.95,
            config.get("training_data_percent", 0.8),
            step=0.05
        )
        config["testing_data_percent"] = 1 - config["training_data_percent"]
        training_percent = str(round(config["training_data_percent"] * 100)) + "%"
        testing_percent = str(round(config["testing_data_percent"] * 100)) + "%"

        # Convert percentage to test start date
        split_index = int(len(unique_dates) * config["training_data_percent"])
        if split_index >= len(unique_dates):
            split_index = len(unique_dates) - 1
        test_start_date = unique_dates[split_index]
        config["test_start_date"] = test_start_date.strftime("%Y-%m-%d")
        config["selected_date_index"] = split_index
        st.success(f"Training and Testing Data set to `{training_percent}` and `{testing_percent}` respectively")

    else:
        # Date-based split
        no_of_dates = int(len(unique_dates) * 0.8)
        selected_date = st.selectbox(
            "Select Test Start Date",
            unique_dates,
            index=config.get("selected_date_index", no_of_dates)
        )
        config["test_start_date"] = pd.to_datetime(selected_date).strftime("%Y-%m-%d")
        config["selected_date_index"] = unique_dates.index(selected_date)

        # Convert date to percent
        split_index = config["selected_date_index"]
        training_percent = split_index / len(unique_dates)
        config["training_data_percent"] = round(training_percent, 2)
        config["testing_data_percent"] = 1 - config["training_data_percent"]

        st.success(f"✅ Selected Test Start Date: `{config['test_start_date']}`")

    save_config(config, CONFIG_PATH)
    return config

def simulate_causal_features(config, CONFIG_PATH):
    st.markdown("### 🎯 Step 13: Simulate Impact of Causal Factors")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - Use this section to **simulate the impact** of causal features on the target variable.  
        - Select one or more causal columns to simulate.
        - For each selected column, a **slider** will appear to increase or decrease its values (in %).
        - This helps to understand how sensitive the target variable is to changes in specific causal drivers.
        - The app will compare the **sum of actual target** vs. **simulated forecast** after adjusting the causal inputs.
        """)
    causal_features = config.get("causal_features", [])

    # st.subheader("🔧 Simulate Impact of Causal Factors")

    simulate_change = 0

    # User input: select causal features to simulate
    selected_causal = st.multiselect("Select Causal Factors to Simulate", causal_features, label_visibility="collapsed")

    # Initialize a dictionary to hold individual change percentages
    change_percent_dict = {}

    if selected_causal:
        st.markdown("### Adjust Change Percentage for Each Selected Causal")
        cols = st.columns(len(selected_causal))  # Create one column per feature
        
        for i, causal in enumerate(selected_causal):
            with cols[i]:
                change_percent_dict[causal] = st.slider(
                    f"{causal}", -50, 50, 0, key=f"slider_{causal}"
                )

    # Save into config or session state
    config["simulated_causal_factors"] = selected_causal
    config["change_percent"] = change_percent_dict

    # Optional: show selected inputs
    if change_percent_dict:
        st.markdown("**Change Applied:**")
        for factor, percent in change_percent_dict.items():
            st.markdown(f"- `{factor}`: **{percent}%**")

    simulate_change = 1 if change_percent_dict else 0

    save_config(config,CONFIG_PATH)
    return config, simulate_change, selected_causal, change_percent_dict


def get_existing_granularities(config, original_data, CONFIG_PATH):
    st.markdown("### 🧩 Step 14: Filter Granularities")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        - This step allows you to **filter and run the model for specific granular combinations** based on the grouping columns you previously selected.
        - This is useful for validating the model's behavior **at a particular granularity level**.
        """)
    grouping_columns = config['grouping_columns']

    original_data['key'] = original_data[grouping_columns].apply(generating_key, axis=1)
    valid_filter_granularity = list(original_data['key'].unique())
    valid_filter_granularity.sort()

    default_value_list = config.get("filter_granularity", valid_filter_granularity[0])
    default_value_str = ",".join(default_value_list)



    # Ensure default is in the valid list
    if default_value_str not in valid_filter_granularity:
        default_value_str = valid_filter_granularity[0]
        # default_value_str = ",".join(default_value_list)

    # Dropdown selection (returns string)
    selected_key = st.selectbox(
        "Filter Granularity",
        valid_filter_granularity,
        index=valid_filter_granularity.index(default_value_str), label_visibility="collapsed"
    )


    # Convert selected string back to list and save to config
    config["filter_granularity"] = selected_key.split(",")
    save_config(config,CONFIG_PATH)
    return config

def run_code(config,simulate_change, selected_causal, change_percent_dict, CONFIG_PATH):

    st.markdown("### ▶️ Step 15: Run Model & View Output")

    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        #### ▶️ Run Model:
        - Once all configurations are complete, click **Run Model** to execute the forecasting pipeline.
        - The model will use your uploaded data, selected features, simulation settings, and filters to generate forecasts.
        
        #### 📊 Output Overview:
        - **Significant Factors**: Shows the causal variables significantly influencing the target (if any).
        - **MAPE (Time Series)**: Displayed if a baseline forecast was provided.
        - **MAPE (Causal Model)**: The Mean Absolute Percentage Error of the current causal model.
        - **Best MAPE Achieved**: Keeps track of the best MAPE obtained across runs and allows viewing the best configuration using **"View Best Config Details"**.

        #### 📈 Forecast Visualization:
        - Interactive graph comparing:
            - **Target Variable**
            - **Model Forecast**
            - **Baseline Forecast** (if available)

        #### 💾 Download Forecast Output:
        - Choose to download:
            - **All Data** for the selected granularity, or
            - **Testing Data Only** to evaluate performance on unseen data.
        """)
    if st.button("Run Model"):

        TRACKING_FILE = "mape_tracking.json"

        # Load existing tracking data
        if os.path.exists(TRACKING_FILE):
            with open(TRACKING_FILE, "r") as f:
                tracking_data = json.load(f)
        else:
            tracking_data = {}

        key_str = ",".join(config["filter_granularity"])

        save_config(config, CONFIG_PATH)  # Save the updated config
        st.success("✅ Config saved. Running model...")

        with st.spinner("Processing..."):
            try:
                if simulate_change:
                    mape, df1, result_df, plt = main_function(config,CONFIG_PATH, simulate_change, selected_causal, change_percent_dict)  # This will run your model with the updated config

                else:
                    mape, df1, result_df, plt = main_function(config,CONFIG_PATH, simulate_change)
            
            except:
                st.success("Data Insufficient")

                mape = [0]
                return 
        mape = mape[0]

        config_best_mape = config.copy()
        # relevant_keys = ["causal_features", "models", "target_column", "scale_features", "fix_ols_violations", "drop_zero_rows_and_get_active_columns", "excluded_columns_from_drop_zero_list", "outlier_correction", "monthly_seasonality", "quarterly_seasonality", "enable_lag_feature", "no_of_lags", "columns_with_lag_features", "original_target_column", "earlier_forecast_columns", "training_data_percent", "test_start_date", "simulated_causal_factors", "change_percent"]

        # relevant_keys = ["causal_features","models","target_column","scale_features","fix_ols_violations","training_data_percent","test_start_date","monthly_seasonality","quarterly_seasonality","simulated_causal_factors","change_percent"]
        # config_best_mape = {k: config[k] for k in relevant_keys if k in config}

        try:
            if tracking_data[key_str]['mape']:
                pass
        except:
            tracking_data[key_str] = {
                "mape": 9999,
                "config": config_best_mape
            }

        existing_entry = tracking_data.get(key_str, {"mape": float("inf")})

        if mape < existing_entry.get("mape", float("inf")):

            tracking_data[key_str] = {
                "mape": mape,
                "config": config_best_mape
            }
            with open(TRACKING_FILE, "w") as f:
                json.dump(tracking_data, f, indent=4)
            # st.success(f"📈 New best MAPE ({mape:.4f}) saved for {key_str}")
        # else:

            # st.info(f"ℹ️ MAPE ({mape:.4f}) not better than existing ({existing_entry['mape']:.4f})")
        if key_str in tracking_data:
            best_entry = tracking_data[key_str]

            # st.markdown(f"**Granularity**: `{key_str}`")
            st.markdown(f"**Best MAPE :** {best_entry['mape']:.2f}")
            with st.expander("📋 View Best Config Details", expanded=False):
                st.json(best_entry["config"])

        # st.success("✅ Done!")

        try:
            st.pyplot(plt.gcf())

            col1, col2 = st.columns(2)

            with col1:
                csv_all = result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Data",
                    data=csv_all,
                    file_name='all_data.csv',
                    mime='text/csv'
                )

            with col2:
                csv_test = df1.to_csv(index=False)
                st.download_button(
                    label="📥 Download Testing Data",
                    data=csv_test,
                    file_name='testing_data.csv',
                    mime='text/csv'
                )
        except:
            pass
    save_config(config,CONFIG_PATH)
    return config

def reset_config_file(config, CONFIG_PATH, output_config_path):

    with st.expander("🔧 Configuration Options"):
        st.markdown("""
        #### ♻️ Reset Configurations:
        - This option **resets all user selections** — including column selections, model settings, and other configurations.
        - Use this to **start fresh** with a clean setup from the beginning.
        """)
        if st.button("🔄 Reset Configuration"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            config = {}
            config["reset_config"] = False
            st.markdown("✅ Reset Successful")
            save_config(config, CONFIG_PATH)
            st.rerun()

        st.markdown("""
        #### 🗑️ Reset Output:
        - This clears the stored **Best MAPE configurations** across different granularities.
        - Use this to **delete all previous output records** if you're starting a new modeling session or want to track only fresh results.
        """)


        if st.button("🔄 Reset Output"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            output_config = {}
            st.markdown("✅ Reset Successful")
            save_config(output_config, output_config_path)
            st.rerun()
    return config

def main():

    CONFIG_PATH = "config.json"  # This is where we'll save the config

    # Create the Streamlit app UI
    st.title("📊 Dynamic Model Configurator")

    st.markdown("### 📌 Methodology Overview")
    with st.expander("ℹ️ Instructions", expanded = True):

        st.markdown("""
        This application is designed for **causal forecasting**, enabling users to understand and quantify how selected causal factors (e.g., media spend, promotion spend, visibility) drive a target variable (e.g., sales).

        It supports forecasting in two modes:

        - **With a baseline forecast**: The model learns from the **uplift**, computed as  
        `Target - Baseline`, and then forecasts the uplift. Final output is `Uplift + Baseline`.

        - **Without a baseline forecast**: The model directly learns and forecasts the target variable.
        """)


    config = load_config(CONFIG_PATH) 

    original_data, config = upload_data_file(config,CONFIG_PATH)

    # Get Required Columns
    config = get_required_columns(config, original_data, CONFIG_PATH)

    # Select the Data of Required Columns and removing all other columns from the data
    original_data = original_data[config["required_columns"]].copy()

    # Multiselect Option for Granularity, Causal Features, and Seasonality
    if config["required_columns"]:
        config = get_grnaularity(config, CONFIG_PATH)
        config = get_causal_columns(config, CONFIG_PATH)
        config = get_monthly_seasonality(config, CONFIG_PATH)
        config = get_quarterly_seasonality(config, CONFIG_PATH)

        if config["causal_features"]:
            # Get Date Column name and its format
            config = get_date_and_format(config, CONFIG_PATH, original_data)

            if config["date_column"]:
                # Get the name of Target Column
                config = get_target_column(config, CONFIG_PATH)

                # Select Model
                config = get_model(config, CONFIG_PATH)
                
                # Scaling and Fixing OLS
                config = apply_scaling_or_fix_ols(config, CONFIG_PATH)

                # Dropping Zero Rows and Get Active Columns
                config = drop_zeros(config, CONFIG_PATH)

                # Apply Outlier Correction
                config = apply_outlier_correction(config, CONFIG_PATH)


                # Enable lag features toggle
                config = shifting_data_by_lags(config, CONFIG_PATH)
                

                if config["models"]:
                    # config = get_original_and_forecast_column(config, CONFIG_PATH)
                    config = get_training_testing_data(config, CONFIG_PATH, original_data)

                    config, simulate_change, selected_causal, change_percent_dict = simulate_causal_features(config, CONFIG_PATH)

                    # config["run_model"] = st.checkbox("Add all Existing Granularities", value=config.get("run_model", False))
                    config = get_existing_granularities(config, original_data, CONFIG_PATH)

                    config = run_code(config,simulate_change, selected_causal, change_percent_dict, CONFIG_PATH)
                        
    # If Reset Button Activate
    output_config_path = "mape_tracking.json"
    config = reset_config_file(config, CONFIG_PATH, output_config_path)
                     

if __name__ == "__main__":
    main()