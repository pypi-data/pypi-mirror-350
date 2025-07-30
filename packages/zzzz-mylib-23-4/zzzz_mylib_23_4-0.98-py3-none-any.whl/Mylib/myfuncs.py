import pickle
import itertools
import re
import json
import pickle
import pandas as pd
import os
from sklearn.model_selection import PredefinedSplit
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
from typing import Union
from sklearn import metrics
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency
from scipy import stats
from sklearn.feature_selection import (
    SelectKBest,
    mutual_info_regression,
    mutual_info_classif,
)
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import random


SCORINGS_PREFER_MININUM = ["log_loss", "mse", "mae"]
SCORINGS_PREFER_MAXIMUM = ["accuracy"]


def get_index_of_outliers(data: Union[np.ndarray, list]):
    """Lấy **index** các giá trị outlier nằm ngoài khoảng Q1 - 1.5*IQR và Q3 + 1.5*IQR

    Args:
        data (Union[np.ndarray, list]): dữ liệu

    Returns:
        list:
    """
    data = np.asarray(data)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    result = np.where((data < lower_bound) | (data > upper_bound))[0].tolist()

    return result


def get_index_of_outliers_on_series(data: pd.Series):
    """Lấy **index** các giá trị outlier nằm ngoài khoảng Q1 - 1.5*IQR và Q3 + 1.5*IQR

    Args:
        data (pd.Series): dữ liệu kiểu **pd.Series**

    Returns:
        list:
    """
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    result = data.index[(data < lower_bound) | (data > upper_bound)].tolist()

    return result


def get_lower_and_upper_bound_of_series(data: pd.Series):
    """Tìm lowerbound, upperbound của 1 tập dữ liệu

    Công thức:
    - lower_bound = Q1 - 1.5 * IQR
    - upper_bound = Q3 + 1.5 * IQR

    Returns:
        (lower_bound, upper_bound): _description_
    """
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    return lower_bound, upper_bound


def is_number_str(string_to_check: str):
    """Check if string_to_check is a number"""

    try:
        float(string_to_check)
        return True
    except ValueError:
        return False


def is_integer_str(s: str):
    """Check if str is an integer

    Args:
        s (str): _description_
    """

    regex = "^[+-]?\d+$"
    return bool(re.match(regex, s))


def is_natural_number_str(s: str):
    """Check if str is a natural_number

    Args:
        s (str): _description_
    """

    regex = "^\+?\d+$"
    return re.match(regex, s) is not None


def split_numpy_array(
    data: np.ndarray, ratios: list, dimension=1, shuffle: bool = True
):
    """

    Args:
        data (np.ndarray): _description_
        ratios (list): Tỉ lệ các phần. Tổng phải bằng 1
        dimension (int, optional): Chiều của dữ liệu. nếu dữ liệu 2 chiều thì gán = 2. Defaults to 1.
        shuffle(bool, optional): có xáo trộn dữ liệu trước khi chia không

    Returns:
        list: list các mảng numpy

    vd:
    với dữ liệu 2 chiều:
    ```python
    split_ratios = [0.5, 0.2, 0.2, 0.1]  # Tỷ lệ mong muốn
    subsets = split_data(data, split_ratios, 2)
    ```
    """
    if sum(ratios) != 1:
        raise ValueError("Tổng của ratios phải bằng 1")

    if shuffle:
        data = np.random.permutation(data)

    len_data = len(data) if dimension == 1 else data.shape[0]
    split_indices = np.cumsum(ratios)[:-1] * len_data
    split_indices = split_indices.astype(int)
    return (
        np.split(data, split_indices)
        if dimension == 1
        else np.split(data, split_indices, axis=0)
    )


def split_dataframe_data(data: pd.DataFrame, ratios: list, shuffle: bool = True):
    """

    Args:
        data (pd.DataFrame): _description_
        ratios (list): Tỉ lệ các phần. Tổng phải bằng 1
        shuffle(bool, optional): có xáo trộn dữ liệu trước khi chia không. Defaults to True

    Returns:
        list: list các dataframe

    VD:
        ```python
    split_ratios = [0.5, 0.2, 0.2, 0.1]  # Tỷ lệ mong muốn
    subsets = split_data(data, split_ratios)
    """
    if sum(ratios) != 1:
        raise ValueError("Tổng của ratios phải bằng 1")

    if shuffle:
        data = data.sample(frac=1.0, random_state=42).reset_index(drop=True)

    split_indices = np.cumsum(ratios)[:-1] * len(data)
    split_indices = split_indices.astype(int)

    subsets = np.split(data, split_indices, axis=0)

    return [pd.DataFrame(item, columns=data.columns) for item in subsets]


def load_python_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise e


def save_python_object(file_path, obj):
    """Save python object in a file

    Args:
        file_path (_type_): ends with .pkl
    """

    try:
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise e


def get_features_target_spliter_for_CV_train_val(
    train_features, train_target, val_features, val_target
):
    """Get total features, target, spliter to do GridSearchCV or RandomisedSearchCV with type is **train-val**

    Args:
        train_features (dataframe): _description_
        train_target (dataframe): _description_
        val_features (dataframe): _description_
        val_target (dataframe): _description_
    Returns:
        features, target,       spliter


    """

    features = pd.concat([train_features, val_features], axis=0)
    target = pd.concat([train_target, val_target], axis=0)
    spliter = PredefinedSplit(
        test_fold=[-1] * len(train_features) + [0] * len(val_features)
    )

    return features, target, spliter


def get_features_target_spliter_for_CV_train_train(train_features, train_target):
    """Get total features, target, spliter to do GridSearchCV or RandomisedSearchCV with type is **train-train** <br>
    When you want to train on training set and assess on that training set


    Args:
        train_features (dataframe): _description_
        train_target (dataframe): _description_
        val_features (dataframe): _description_
        val_target (dataframe): _description_
    """

    features = pd.concat([train_features, train_features], axis=0)
    target = pd.concat([train_target, train_target], axis=0)
    spliter = PredefinedSplit(
        test_fold=[-1] * len(train_features) + [0] * len(train_features)
    )

    return features, target, spliter


def create_directories(path_to_directories: list):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories

    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)


def save_json(path: str, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"json file saved at {path}")


def load_json(path: str):
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    print(f"json file loaded succesfully from: {path}")
    return content


def get_real_column_name(column):
    """After using ColumnTransformer, the column name has format = bla__Age, so only take Age"""

    start_index = column.find("__") + 2
    column = column[start_index:]
    return column


def get_real_column_name_from_get_feature_names_out(columns):
    """Take the exact name from the list retrieved by method get_feature_names_out() of ColumnTransformer"""

    return [get_real_column_name(item) for item in columns]


def fix_name_by_LGBM_standard(cols):
    """LGBM standard state that columns name can only contain characters among letters, digit and '_'

    Returns:
        list: _description_
    """

    cols = pd.Series(cols)
    cols = cols.str.replace(r"[^A-Za-z0-9_]", "_", regex=True)
    return list(cols)


def find_feature_importances(train_data, model):
    """Find the feature importances of some models like: RF, GD, SGD, LGBM

    Returns:
        pd.DataFrame:
    """

    score = pd.DataFrame(
        data={
            "feature": train_data.columns.tolist(),
            "score": model.feature_importances_,
        }
    )
    score = score.sort_values(by="score", ascending=False)
    return score


def find_coef_from_classifier_model(train_data, model):
    """Find the feature importances of some models like: LR1, LRe

    Returns:
        pd.DataFrame:
    """

    score = pd.DataFrame(
        data={
            "feature": train_data.columns.tolist(),
            "score": np.abs(model.coef_[0]),
        }
    )
    score = score.sort_values(by="score", ascending=False)
    return score


def find_coef_from_regressor_model(train_data, model):
    """Find the feature importances of some models like: ElasticNet, Lasso

    Returns:
        pd.DataFrame:
    """

    score = pd.DataFrame(
        data={
            "feature": train_data.columns.tolist(),
            "score": np.abs(model.coef_),
        }
    )
    score = score.sort_values(by="score", ascending=False)
    return score


def find_best_n_components_of_PCA(
    train_features,
    train_target,
    val_features,
    val_target,
    placeholdout_model,
    list_n_components,
    scoring="accuracy",
):
    """Find best n_components of PCA

    Args:
        placeholdout_model (_type_): model like LR, XGB, ... without hyperparameters except random_state
        list_n_components (_type_): list of n_components used
        scoring (str, optional): scoring. Defaults to "accuracy".

    Returns:
        _type_: best n_components
    """
    features, target, splitter = get_features_target_spliter_for_CV_train_val(
        train_features, train_target, val_features, val_target
    )
    param_grid = {"1__n_components": list_n_components}
    pp = Pipeline(
        steps=[
            ("1", PCA(random_state=42)),
            ("2", placeholdout_model),
        ]
    )
    gs = GridSearchCV(pp, param_grid=param_grid, cv=splitter, scoring=scoring)
    gs.fit(features, target)
    return gs.best_params_


def find_feature_score_by_permutation_importance(
    train_features, train_target, fitted_model
):
    """Find the feature score by doing permutation_importance

    Args:
        fitted_model (_type_): fitted model, not base model

    Returns:
        DataFrame: _description_
    """
    result = permutation_importance(
        fitted_model, train_features, train_target, n_repeats=10, random_state=42
    )
    result_df = pd.DataFrame(
        data={
            "feature": train_features.columns.tolist(),
            "score": result.importances_mean * 100,
        }
    )
    result_df = result_df.sort_values(by="score", ascending=False)
    return result_df


def get_describe_stats_for_numeric_cat_cols(data):
    """Get descriptive statistics of numeric cat cols, including min, max, median

    Args:
        data (_type_): numeric cat cols
    Returns:
        Dataframe: min, max, median
    """

    min_of_cols = data.min().to_frame(name="min")
    max_of_cols = data.max().to_frame(name="max")
    median_of_cols = data.quantile([0.5]).T.rename(columns={0.5: "median"})

    result = pd.concat([min_of_cols, max_of_cols, median_of_cols], axis=1).T

    return result


def get_different_types_cols_from_df_4(df: pd.DataFrame):
    """Tìm các cột kiểu numeric, numericCat, cat, binary, nominal, ordinal  target từ df

    Lưu ý: có tìm luôn cột **target**

    Returns:
        (numeric_cols, numericCat_cols, cat_cols, binary_cols, nominal_cols, ordinal_cols, target_col):
    """

    cols = pd.Series(df.columns)
    numeric_cols = cols[cols.str.endswith("num")].tolist()
    numericCat_cols = cols[cols.str.endswith("numcat")].tolist()
    binary_cols = cols[cols.str.endswith("bin")].tolist()
    nominal_cols = cols[cols.str.endswith("nom")].tolist()
    ordinal_cols = cols[cols.str.endswith("ord")].tolist()
    cat_cols = binary_cols + nominal_cols + ordinal_cols
    target_col = cols[cols.str.endswith("target")].tolist()[0]

    return (
        numeric_cols,
        numericCat_cols,
        cat_cols,
        binary_cols,
        nominal_cols,
        ordinal_cols,
        target_col,
    )


def get_different_types_feature_cols_from_df_14(df: pd.DataFrame):
    """Tìm các cột kiểu numeric, numericCat, cat, binary, nominal, ordinal từ df

    Lưu ý: Chỉ các cột **feature** không có cột **target**
    Returns:
        (numeric_cols, numericCat_cols, cat_cols, binary_cols, nominal_cols, ordinal_cols):
    """
    cols = pd.Series(df.columns)
    numeric_cols = cols[cols.str.endswith("num")].tolist()
    numericCat_cols = cols[cols.str.endswith("numcat")].tolist()
    binary_cols = cols[cols.str.endswith("bin")].tolist()
    nominal_cols = cols[cols.str.endswith("nom")].tolist()
    ordinal_cols = cols[cols.str.endswith("ord")].tolist()
    cat_cols = binary_cols + nominal_cols + ordinal_cols

    return (
        numeric_cols,
        numericCat_cols,
        cat_cols,
        binary_cols,
        nominal_cols,
        ordinal_cols,
    )


def evaluate_model_on_one_scoring_17(model, feature, target, scoring):
    if scoring == "accuracy":
        prediction = model.predict(feature)
        return metrics.accuracy_score(target, prediction)

    if scoring == "log_loss":
        prediction = model.predict_proba(feature)
        return metrics.log_loss(target, prediction)

    if scoring == "mse":
        prediction = model.predict(feature)
        return np.sqrt(metrics.mean_squared_error(target, prediction))

    if scoring == "mae":
        prediction = model.predict(feature)
        return metrics.mean_absolute_error(target, prediction)

    raise ValueError(
        "===== Chỉ mới định nghĩa cho accuracy, log_loss, mse, mae =============="
    )


def get_classification_report_18(model, feature, target, class_names: list):
    """Tạo classfication report cho classifier"""
    class_names = np.asarray(class_names)

    target = [int(item) for item in target]
    target = class_names[target]

    prediction = model.predict(feature)
    prediction = [int(item) for item in prediction]
    prediction = class_names[prediction]

    return metrics.classification_report(target, prediction)


def find_best_model_train_val_scoring_when_using_Randomised_GridSearch_19(
    cv_results, scoring
):
    """Tìm chỉ số train-val cho mô hình tốt nhất sau khi sử dụng RandomisedSearch hoặc GridSearch

    Args:
        cv_results (_type_): Kết quả từ searcher
        scoring (_type_): Chỉ tiêu đánh giá

    Returns:
        (train_scoring, val_scoring):
    """
    cv_results = zip(cv_results["mean_test_score"], cv_results["mean_train_score"])
    cv_results = sorted(cv_results, key=lambda x: x[0], reverse=True)
    val_scoring, train_scoring = cv_results[0]

    if scoring in SCORINGS_PREFER_MININUM:
        val_scoring, train_scoring = (
            -val_scoring,
            -train_scoring,
        )

    return train_scoring, val_scoring


def get_target_col_from_df_26(df):
    """Get cột target từ df
    Returns:
        target_col: _description_
    """

    cols = pd.Series(df.columns)
    target_col = cols[cols.str.endswith("target")].tolist()[0]
    return target_col


def get_feature_cols_and_target_col_from_df_27(df):
    """Get các cột feature và cột target từ df

    Returns:
        (feature_cols, target_col): _description_
    """
    cols = pd.Series(df.columns)
    target_col = cols[cols.str.endswith("target")]
    feature_cols = cols.drop(target_col.index).tolist()
    target_col = target_col.tolist()[0]

    return feature_cols, target_col


def get_confusion_matrix_heatmap_29(model, feature, target, class_names: list):
    """Vẽ confustion matrix heatmap

    Returns:
        fig: _description_
    """
    class_names = np.asarray(class_names)

    target = [int(item) for item in target]
    target = class_names[target]

    prediction = model.predict(feature)
    prediction = [int(item) for item in prediction]
    prediction = class_names[prediction]

    labels = np.unique(target)
    cm = metrics.confusion_matrix(target, prediction, labels=labels)
    np.fill_diagonal(cm, 0)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        cbar=True,
        annot=True,
        cmap="YlOrRd",
        ax=ax,
        xticklabels=labels,
        yticklabels=labels,
    )

    return fig


def get_heatmap_for_confusion_matrix_30(confusion_matrix, labels):
    """Get heatmap cho confusion matrix

    Returns:
        fig: đối tượng chart
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        confusion_matrix,
        cbar=True,
        annot=True,
        cmap="YlOrRd",
        ax=ax,
        xticklabels=labels,
        yticklabels=labels,
    )

    return fig


def get_model_desc_for_CustomStackingClassifier_31(model_desc: dict):
    res = f"class_name: {model_desc['class_name']}\n"
    res += "estimators:\n"
    space = "   "
    for item in model_desc["estimators"]:
        res += f"{space}- {item}\n"
    res += f"final_estimator: {model_desc['final_estimator']}"
    return res


def get_model_desc_for_model_32(model_desc):
    if isinstance(model_desc, dict):
        return get_model_desc_for_CustomStackingClassifier_31(model_desc)

    return model_desc


def replace_in_category_series_33(series, replace_value_list: list):
    """Replace giá trị trong các cột kiểu category

    VD:
    ```
    a = pd.Series(['a', 'b', 'c', 'd', 'b', 'c', 'd'])

    # Thay a, b -> ab, c -> c1
    replace_value_list = [
        [['a', 'b'], 'ab'],
        [['c'], 'c1'],
    ]

    a = myfuncs.replace_in_category_series_33(a, replace_value_list)
    ```

    """
    series = series.astype("string")

    new_replace_value_list = [
        [item[0], [item[1]] * len(item[0])] for item in replace_value_list
    ]
    replace_value_dict_keys = itertools.chain(
        *[item[0] for item in new_replace_value_list]
    )
    replace_value_dict_values = itertools.chain(
        *[item[1] for item in new_replace_value_list]
    )
    replace_value_dict = dict(zip(replace_value_dict_keys, replace_value_dict_values))
    series = series.replace(replace_value_dict)
    series = series.astype("category")
    return series


def replace_outliers_with_new_value_34(series, new_value):
    """Thay thế các outliers trong 1 series thành giá trị mới"""
    lb, ub = get_lower_and_upper_bound_of_series(series)
    series[series.index[(series < lb) | (series > ub)]] = new_value
    return series


def get_label_percent_in_categorical_column_35(series):
    """Phần trăm các label trong cột categorical"""
    return series.value_counts() / len(series) * 100


def get_correlation_between_numeric_cols_36(df, numeric_cols):
    """Get hệ số tương quan của các cột numeric

    Returns:
        df: item0, item1, correlation
    """
    combinations_2 = list(itertools.combinations(numeric_cols, 2))
    res = [np.abs(df[item[0]].corr(df[item[1]])) for item in combinations_2]

    res = pd.Series(res, index=combinations_2)
    res = res.sort_values(ascending=False)

    return res


def get_correlation_between_numeric_features_and_numeric_target_37(
    df, numeric_cols, target_col
):
    correlations = [np.abs(df[col].corr(df[target_col])) for col in numeric_cols]
    res = pd.Series(correlations, index=numeric_cols)
    res = res.sort_values(ascending=False)


def plot_hist_box_violin_plots_for_numeric_cols_37(df, numeric_cols):
    """Vẽ hist, boxplot, violin cho các cột số trong df

    Returns:
        fig: _description_
    """
    subplot_titles = sum(([item, "", ""] for item in numeric_cols), [])

    fig = make_subplots(rows=len(numeric_cols), cols=3, subplot_titles=subplot_titles)

    for row, col in enumerate(numeric_cols, 1):
        data = df[col]

        # Vẽ Histogram
        fig_hist = px.histogram(
            x=data,
            nbins=100,
        )

        # Thêm đường viền cho các cột histogram
        fig_hist.update_traces(marker=dict(line=dict(width=1, color="black")))

        # Vẽ box plot
        fig_box = px.box(
            y=data,
        )

        # Vẽ violin plot
        fig_violin = px.violin(
            y=data,
            box=True,
        )

        fig.add_trace(fig_hist.data[0], row=row, col=1)
        fig.add_trace(fig_box.data[0], row=row, col=2)
        fig.add_trace(fig_violin.data[0], row=row, col=3)

    fig.update_layout(
        width=300 * 3,  # Độ rộng biểu đồ (px)
        height=len(numeric_cols) * 400,  # Độ cao biểu đồ (px)
    )

    return fig


def plot_hist_box_violin_plots_for_numeric_cols_matplotlib_37(df, numeric_cols):
    """Vẽ hist, boxplot, violin cho các cột số trong df

    Returns:
        fig: _description_
    """
    # Tạo một figure và các axes
    fig, axes = plt.subplots(
        nrows=len(numeric_cols), ncols=3, figsize=(15, len(numeric_cols) * 5)
    )

    for row, col in enumerate(numeric_cols):
        data = df[col]

        # Vẽ Histogram
        axes[row, 0].hist(data, bins=100, edgecolor="black")
        axes[row, 0].set_title(f"Histogram: {col}")
        axes[row, 0].set_xlabel(col)
        axes[row, 0].set_ylabel("Frequency")

        # Vẽ Box plot
        sns.boxplot(y=data, ax=axes[row, 1])
        axes[row, 1].set_title(f"Box plot: {col}")
        axes[row, 1].set_xlabel(col)

        # Vẽ Violin plot
        sns.violinplot(y=data, ax=axes[row, 2])
        axes[row, 2].set_title(f"Violin plot: {col}")
        axes[row, 2].set_xlabel(col)

    # Điều chỉnh không gian giữa các biểu đồ
    plt.tight_layout()
    return fig


def plot_label_percent_for_categorical_cols_38(df, cat_cols):
    """Vẽ phần trăm các label trong các cột categorical

    Returns:
        fig: _description_
    """
    fig = make_subplots(rows=len(cat_cols), cols=1, subplot_titles=cat_cols)

    for row, col in enumerate(cat_cols, 1):
        data = df[col]

        # Vẽ phân phối các label
        label_percent = data.value_counts() / len(data) * 100
        fig_bar = px.bar(x=label_percent.values, y=label_percent.index, orientation="h")

        fig.add_trace(fig_bar.data[0], row=row, col=1)

    fig.update_layout(
        width=300,  # Độ rộng biểu đồ (px)
        height=len(cat_cols) * 400,  # Độ cao biểu đồ (px)
    )

    return fig


def plot_label_percent_for_categorical_cols_matplotlib_38(df, cat_cols):
    """Vẽ phần trăm các label trong các cột categorical

    Returns:
        fig: _description_
    """
    # Tạo figure và axes
    fig, axes = plt.subplots(
        nrows=len(cat_cols), ncols=1, figsize=(8, len(cat_cols) * 3)
    )

    for row, col in enumerate(cat_cols):
        data = df[col]

        # Tính tỷ lệ phần trăm của các label
        label_percent = data.value_counts() / len(data) * 100

        # Vẽ bar plot (horizontally)
        axes[row].barh(
            label_percent.index,
            label_percent.values,
            color="skyblue",
            edgecolor="black",
        )
        axes[row].set_title(f"Label Percent for: {col}")
        axes[row].set_xlabel("Percentage (%)")
        axes[row].set_ylabel("Labels")

    # Điều chỉnh không gian giữa các biểu đồ
    plt.tight_layout()

    return fig


def do_chi_square_test_for_2_variables_39(df, cat_col1, cat_col2):
    """Thực hiện kiểm định chi square cho 2 biến categorical trong df

    Args:
        df (_type_):
        cat_col1 (_type_): cột thứ 1
        cat_col2 (_type_): cột thứ 2

    Returns:
        p_value: Giá trị p_value của kiểm định
    """
    table = df.groupby([cat_col1, cat_col2]).size().unstack()
    return chi2_contingency(table.values)[1]


def do_chi_square_test_for_categorical_cols_40(df, cat_cols):
    """Thực hiện kiểm định cho các cột categoricals trong df

    Args:
        df (_type_): _description_
        cat_cols (_type_): tên các cột categorical

    Returns:
        df: Gồm có 3 cột, item0, item1, p_value
    """
    combinations_2 = list(itertools.combinations(cat_cols, 2))
    list_p_value = [
        do_chi_square_test_for_2_variables_39(df, item[0], item[1])
        for item in combinations_2
    ]
    res = pd.Series(list_p_value, index=combinations_2)
    res = res.sort_values(ascending=True)

    return res


def do_chi_square_test_between_categorical_cols_and_target_col_41(
    df, cat_cols, target_col
):
    list_p_value = [
        do_chi_square_test_for_2_variables_39(df, col, target_col) for col in cat_cols
    ]

    res = pd.Series(list_p_value, index=cat_cols)
    res = res.sort_values(ascending=True)
    return res


def get_outlier_percent_of_numeric_cols_42(df, numeric_cols):
    """Get phần trăm các outlier ở trong các cột numeric

    Returns:
        series:
    """
    list_outlier_percent = []
    for col in numeric_cols:
        lb, ub = get_lower_and_upper_bound_of_series(df[col])
        count_outlier = np.sum((df[col] < lb) | (df[col] > ub))
        outlier_percent = count_outlier / len(df[col]) * 100
        list_outlier_percent.append(outlier_percent)

    res = pd.Series(list_outlier_percent, index=numeric_cols)
    res = res.sort_values(ascending=False)
    return res


def test_relation_between_cat_col_and_numeric_col_43(df, cat_col, numeric_col):
    """Test mức độ ảnh hưởng của 1 biến categorical đến biến numeric target

    Args:
        df (_type_): _description_
        cat_col (_type_): _description_
        target_col (_type_): Phải là biến numeric !!!!!

    Returns:
        p_value: _description_
    """
    data = df.groupby(cat_col)[numeric_col].apply(list)
    p_value = stats.kruskal(*list(data.values)).pvalue
    return p_value


def test_relation_between_numeric_features_and_cat_target_44(
    df, numeric_cols, target_col
):
    """Kiểm định mức độ ảnh hưởng của các biến numeric đến biến target phân loại

    Args:
        df (_type_): _description_
        numeric_cols (_type_): _description_
        target_col (_type_): Phải là biến phân loại

    Returns:
        series: _description_
    """
    list_p_value = [
        test_relation_between_cat_col_and_numeric_col_43(df, target_col, col)
        for col in numeric_cols
    ]
    res = pd.Series(list_p_value, index=numeric_cols)
    res = res.sort_values(ascending=True)
    return res


def get_skew_on_numeric_cols_44(df, numeric_cols):
    """Get hệ số skew của các cột numeric


    Returns:
        series: _description_
    """
    list_skew = [np.abs(stats.skew(df[col])) for col in numeric_cols]
    res = pd.Series(list_skew, index=numeric_cols)
    res = res.sort_values(ascending=False)
    return res


def do_kbest_feature_selection_for_classification_45(transformed_features, target):
    """Thực hiện select kbest choa bài toán classification

    Args:
        transformed_features (_type_): **Phải được transformed trước**
        target (_type_): _description_

    Returns:
        series: _description_
    """
    # Khởi tạo selector
    selector = SelectKBest(score_func=mutual_info_classif, k="all")  # Classification

    # Fit cái đã
    selector.fit(transformed_features, target)  # features phải được transformed trước

    # Ghi lại kết quả điểm số
    res = pd.Series(selector.scores_, index=transformed_features.columns)
    res = res.sort_values(ascending=False)
    return res


def do_kbest_feature_selection_for_regression_46(transformed_features, target):
    """Thực hiện select kbest choa bài toán regression

    Args:
        transformed_features (_type_): **Phải được transformed trước**
        target (_type_): _description_

    Returns:
        series: _description_
    """
    # Khởi tạo selector
    selector = SelectKBest(score_func=mutual_info_regression, k="all")  # Regression

    # Fit cái đã
    selector.fit(transformed_features, target)  # features phải được transformed trước

    # Ghi lại kết quả điểm số
    res = pd.Series(selector.scores_, index=transformed_features.columns)
    res = res.sort_values(ascending=False)
    return res


def find_silhouette_score_for_each_param_for_DBSCAN_47(features, list_param):
    """Get chỉ số silhouette_score cho từng cặp tham số của DBSCAN

    Args:
        features (_type_): dữ liệu các đặc trưng
        list_param (_type_): list các tuple dạng (eps, min_samples)

    Returns:
        series: _description_
    """
    scores = []

    for param in list_param:
        eps, min_samples = param
        db = DBSCAN(eps=eps, min_samples=min_samples)
        labels = db.fit_predict(features)

        # Tính silhouette score chỉ khi có ít nhất 2 cụm
        score = silhouette_score(features, labels) if len(set(labels)) > 1 else None
        scores.append(score)

    res = pd.Series(scores, index=list_param)
    res = res.sort_values(ascending=False)
    return res


def get_noise_sample_by_DBSCAN_48(features, dbscan_model):
    """Tìm các điểm noise bằng thuật toán DBSCAN

    Args:
        features (_type_): _description_
        dbscan_model (_type_): _description_

    Returns:
        df: _description_
    """
    labels = dbscan_model.fit_predict(features)
    res = features[labels == -1, :]
    return res


def get_cat_cols_from_df_49(df):
    """Get các cột categorical"""
    cols = pd.Series(df.columns)
    binary_cols = cols[cols.str.endswith("bin")].tolist()
    nominal_cols = cols[cols.str.endswith("nom")].tolist()
    ordinal_cols = cols[cols.str.endswith("ord")].tolist()
    cat_cols = binary_cols + nominal_cols + ordinal_cols

    return cat_cols


def get_numericcat_cols_from_df_50(df):
    """Get numericcat cột"""
    cols = pd.Series(df.columns)
    numericCat_cols = cols[cols.str.endswith("numcat")].tolist()

    return numericCat_cols


def get_min_max_of_numeric_cols_51(df, numeric_cols):
    """Get giá trị min, max của các cột numeric

    Returns:
        df: _description_
    """
    return df[numeric_cols].describe().loc[["min", "max"]].T


def get_numeric_cols_from_df_54(df):
    """Get numeric cột"""
    cols = pd.Series(df.columns)
    res = cols[cols.str.endswith("num")].tolist()

    return res


def log_series_55(series):
    """Tiến hành log 1 series

    Lưu ý: log(A) xác định khi A > 0 , nên ở đây thay thế các giá trị không dương bằng giá trị nhỏ nhất trong series mà > 0
    """
    if np.min(series) > 0:
        return np.log(series)

    # Tìm giá trị nhỏ nhất của series mà > 0
    min_series_g0 = np.min(series[series > 0])

    series[series < 0] = min_series_g0

    return np.log(series)


def get_descriptive_stats_for_numeric_cols_56(df, numeric_cols):
    """Get thống kê mô tả cho các cột numeric, bao gồm: min, max và min (các phần tử > 0)

    Returns:
        df: _description_
    """
    # Tìm giá trị min mà > 0 của từng cột
    list_min_g0 = pd.DataFrame(
        data={"min_g0": [np.min(df[col][df[col] > 0]) for col in numeric_cols]},
        index=numeric_cols,
    )

    # Gộp vào với max, min
    min_max = df[numeric_cols].describe().loc[["min", "max"]].T
    return pd.concat([min_max, list_min_g0], axis=1)


def log_many_columns_57(df, cols):
    """Log nhiều cột

    Args:
        df (_type_): _description_
        cols (_type_): tên các cột cần log
    """
    for col in cols:
        df[col] = log_series_55(df[col])


def replace_outliers_in_many_cols_with_new_value_58(df, cols, mode):
    """Thay thế giá trị outlier trong nhiều cột bằng giá trị mới

    Args:
        df (_type_): _description_
        cols (_type_): tên các cột
        mode (_type_): mean -> giá trị trung bình, median: giá trị trung vị
    """
    if mode == "mean":
        for col in cols:
            df[col] = replace_outliers_with_new_value_34(df[col], np.mean(df[col]))

        return

    if mode == "median":
        for col in cols:
            df[col] = replace_outliers_with_new_value_34(
                df[col], np.percentile(df[col], 50)
            )

        return


def convert_list_estimator_into_pipeline_59(list_estimator):
    return (
        Pipeline(
            steps=[
                (str(index), transformer)
                for index, transformer in enumerate(list_estimator)
            ]
        )
        if len(list_estimator) > 0
        else Pipeline(steps=[("passthrough", "passthrough")])
    )


def create_list_constants_followed_by_list_list(list_list, constant):
    result = []
    for one_list in list_list:
        result.append([constant] * len(one_list))

    return result


def train_test_split_one_df_into_three_subdfs_in_stratified(
    df, train_size, val_size, col_for_stratified
):
    """Tách df thành 3 tập con theo stratified fashion

    Args:
        df (_type_): _description_
        train_size (_type_): tỉ lệ tập train
        val_size (_type_): tỉ lệ tập val
        col_for_stratified (_type_): tên cột dùng cho stratified fashion

    Returns:
        (df_train, df_val, df_test): _description_
    """
    # Tách tập train ra trước
    df_train, df_rest = train_test_split(
        df, test_size=(1 - train_size), stratify=df[col_for_stratified]
    )

    # Phần còn lại chia thành 2 tập val , test
    test_size = 1 - train_size - val_size
    test_size_in_df_rest = test_size / (1 - train_size)
    df_val, df_test = train_test_split(
        df_rest, test_size=test_size_in_df_rest, stratify=df_rest[col_for_stratified]
    )

    return df_train, df_val, df_test


def train_test_split_one_df_into_three_subdfs(df, train_size, val_size):
    """Chia df thành 3 tập train, val và test

    Args:
        df (_type_): _description_
        train_size (_type_): _description_
        val_size (_type_): _description_

    Returns:
        (df_train, df_val, df_test): _description_
    """
    # Tách tập train ra trước
    df_train, df_rest = train_test_split(df, test_size=(1 - train_size))

    # Phần còn lại chia thành 2 tập val , test
    test_size = 1 - train_size - val_size
    test_size_in_df_rest = test_size / (1 - train_size)
    df_val, df_test = train_test_split(df_rest, test_size=test_size_in_df_rest)

    return df_train, df_val, df_test


def split_a_list_into_three_sublist(list_data, train_size, val_size):
    """Chia 1 list thành 3 list con, kiểu như chia thành 3 tập train, val, test

    Args:
        list_data (_type_): _description_
        train_size (_type_): tỉ lệ tập train (tập đầu tiên)
        val_size (_type_): tỉ lệ tập val (tập thứ hai), phần còn lại là tập thứ ba

    Returns:
        (train_data, val_data, test_data): _description_
    """
    random.shuffle(list_data)
    num_train_samples = int(train_size * len(list_data))
    num_val_samples = int(val_size * len(list_data))

    train_data = list_data[:num_train_samples]
    val_data = list_data[num_train_samples : num_train_samples + num_val_samples]
    test_data = list_data[num_train_samples + num_val_samples :]

    return train_data, val_data, test_data


def read_content_from_file_60(logs_filepath):
    with open(logs_filepath, mode="r") as file:
        content = file.read()

    return content


def write_content_to_file(result, file_path):
    with open(file_path, mode="w") as file:
        file.write(result)
