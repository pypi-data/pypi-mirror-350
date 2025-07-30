import pandas as pd
import numpy as np
from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
    ClassifierMixin,
    RegressorMixin,
)
from Mylib import myfuncs
from sklearn import metrics
from sklearn.decomposition import IncrementalPCA, KernelPCA
from sklearn.manifold import LocallyLinearEmbedding
import pandas as pd
from Mylib import myfuncs
from sklearn.preprocessing import (
    OneHotEncoder,
    MinMaxScaler,
    OrdinalEncoder,
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnsDeleter(BaseEstimator, TransformerMixin):
    """Xóa cột

    Attributes:
        columns: tên các cột cần xóa
    """

    def __init__(self, columns) -> None:
        super().__init__()
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        X = X.drop(columns=self.columns)

        self.cols = X.columns.tolist()
        return X

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class ClassifierEvaluator:
    """Đánh giá model cho tập train-val hoặc tập test cho bài toán classification

    Hàm chính:
    - evaluate():

    Lưu ý:
    - KHi đánh giá 1 tập (vd: đánh giá tập test) thì truyền cho train_feature_data, train_target_data, còn val_feature_data và val_target_data **bỏ trống**

    Attributes:
        model (_type_):
        class_names (_type_): Các label
        train_feature_data (_type_):
        train_target_data (_type_):
        val_feature_data (_type_, optional): Defaults to None.
        val_target_data (_type_, optional):  Defaults to None.

    """

    def __init__(
        self,
        model,
        class_names,
        train_feature_data,
        train_target_data,
        val_feature_data=None,
        val_target_data=None,
    ):
        self.model = model
        self.class_names = class_names
        self.train_feature_data = train_feature_data
        self.train_target_data = train_target_data
        self.val_feature_data = val_feature_data
        self.val_target_data = val_target_data

    def evaluate_train_classifier(self):
        # Dự đoán
        train_pred = self.model.predict(self.train_feature_data)
        train_pred = [int(item) for item in train_pred]

        val_pred = self.model.predict(self.val_feature_data)
        val_pred = [int(item) for item in val_pred]

        # Accuracy
        train_accuracy = metrics.accuracy_score(self.train_target_data, train_pred)
        val_accuracy = metrics.accuracy_score(self.val_target_data, val_pred)

        # Classification report
        class_names = np.asarray(self.class_names)
        train_target_data = [int(item) for item in self.train_target_data]
        val_target_data = [int(item) for item in self.val_target_data]

        named_train_target_data = class_names[train_target_data]
        named_train_pred = class_names[train_pred]
        named_val_target_data = class_names[val_target_data]
        named_val_pred = class_names[val_pred]

        train_classification_report = metrics.classification_report(
            named_train_target_data, named_train_pred
        )
        val_classification_report = metrics.classification_report(
            named_val_target_data, named_val_pred
        )

        # Confusion matrix
        train_confusion_matrix = metrics.confusion_matrix(
            named_train_target_data, named_train_pred, labels=class_names
        )
        np.fill_diagonal(train_confusion_matrix, 0)
        train_confusion_matrix = myfuncs.get_heatmap_for_confusion_matrix_30(
            train_confusion_matrix, class_names
        )

        val_confusion_matrix = metrics.confusion_matrix(
            named_val_target_data, named_val_pred, labels=class_names
        )
        np.fill_diagonal(val_confusion_matrix, 0)
        val_confusion_matrix = myfuncs.get_heatmap_for_confusion_matrix_30(
            val_confusion_matrix, class_names
        )

        model_results_text = f"Train accuracy: {train_accuracy}\n"
        model_results_text += f"Val accuracy: {val_accuracy}\n"
        model_results_text += (
            f"Train classification_report: \n{train_classification_report}\n"
        )
        model_results_text += (
            f"Val classification_report: \n{val_classification_report}"
        )

        return model_results_text, train_confusion_matrix, val_confusion_matrix

    def evaluate_test_classifier(self):
        test_pred = self.model.predict(self.train_feature_data)
        test_pred = [int(item) for item in test_pred]

        # Accuracy
        test_accuracy = metrics.accuracy_score(self.train_target_data, test_pred)

        # Classification report
        class_names = np.asarray(self.class_names)
        train_target_data = [int(item) for item in self.train_target_data]

        named_train_target_data = class_names[train_target_data]
        named_train_pred = class_names[test_pred]

        test_classification_report = metrics.classification_report(
            named_train_target_data, named_train_pred
        )

        # Confusion matrix
        test_confusion_matrix = metrics.confusion_matrix(
            named_train_target_data, named_train_pred, labels=class_names
        )
        np.fill_diagonal(test_confusion_matrix, 0)
        test_confusion_matrix = myfuncs.get_heatmap_for_confusion_matrix_30(
            test_confusion_matrix, class_names
        )

        model_results_text = f"Test Accuracy: {test_accuracy}\n"
        model_results_text += (
            f"Test Classification_report: \n{test_classification_report}\n"
        )

        return model_results_text, test_confusion_matrix

    def evaluate(self):
        return (
            self.evaluate_train_classifier()
            if self.val_feature_data is not None
            else self.evaluate_test_classifier()
        )


class RegressorEvaluator:
    """Đánh giá model cho tập train-val hoặc tập test cho bài toán regression

    Hàm chính:
    - evaluate():

    Lưu ý:
    - KHi đánh giá 1 tập (vd: đánh giá tập test) thì truyền cho train_feature_data, train_target_data, còn val_feature_data và val_target_data **bỏ trống**

    Attributes:
        model (_type_):
        train_feature_data (_type_):
        train_target_data (_type_):
        val_feature_data (_type_, optional): Defaults to None.
        val_target_data (_type_, optional):  Defaults to None.

    """

    def __init__(
        self,
        model,
        train_feature_data,
        train_target_data,
        val_feature_data=None,
        val_target_data=None,
    ):
        self.model = model
        self.train_feature_data = train_feature_data
        self.train_target_data = train_target_data
        self.val_feature_data = val_feature_data
        self.val_target_data = val_target_data

    def evaluate_train_regressor(self):
        train_pred = self.model.predict(self.train_target_data)
        val_pred = self.model.predict(self.val_target_data)

        # RMSE
        train_rmse = np.sqrt(
            metrics.mean_squared_error(self.train_target_data, train_pred)
        )
        val_rmse = np.sqrt(metrics.mean_squared_error(self.val_target_data, val_pred))

        # MAE
        train_mae = metrics.mean_absolute_error(self.train_target_data, train_pred)
        val_mae = metrics.mean_absolute_error(self.val_target_data, val_pred)

        model_results_text = f"Train RMSE: {train_rmse}\n"
        model_results_text += f"Val RMSE: {val_rmse}\n"
        model_results_text += f"Train MAE: {train_mae}\n"
        model_results_text += f"Val MAE: {val_mae}\n"

        return model_results_text

    def evaluate_test_regressor(self):
        test_pred = self.model.predict(self.train_target_data)

        # RMSE
        test_rmse = np.sqrt(
            metrics.mean_squared_error(self.train_target_data, test_pred)
        )

        # MAE
        test_mae = metrics.mean_absolute_error(self.train_target_data, test_pred)

        model_results_text = f"Test RMSE: {test_rmse}\n"
        model_results_text = f"Test MAE: {test_mae}\n"

        return model_results_text

    def evaluate(self):
        return (
            self.evaluate_train_regressor()
            if self.val_feature_data is not None
            else self.evaluate_test_regressor()
        )


class BestModelSearcher:
    """Searcher đi tìm model tốt nhất và train, val scoring tương ứng

    Hàm chính:
        - next()

    Examples:
        Với **scoring = accuracy và target_score = 0.99**

        Tìm model thỏa val_accuracy > 0.99 và train_accuracy > 0.99 (1) và val_accuracy là lớn nhất trong số đó

        Nếu không thỏa (1) thì lấy theo val_accuracy lớn nhất

    Attributes:
        models (_type_): Model tốt nhất đang ở trong này
        train_scorings (_type_):
        val_scorings (_type_):
        target_score (_type_): Chỉ tiêu đề ra
        scoring (_type_): Chỉ số đánh giá


    """

    def __init__(self, models, train_scorings, val_scorings, target_score, scoring):
        self.models = models
        self.train_scorings = train_scorings
        self.val_scorings = val_scorings
        self.target_score = target_score
        self.scoring = scoring

    def find_train_val_scorings_to_find_the_best(self):
        sign_for_score = 1  # Nếu scoring cần min thì lấy âm -> quy về tìm lớn nhất thôi
        if self.scoring in myfuncs.SCORINGS_PREFER_MININUM:
            self.target_score = -self.target_score
            sign_for_score = -1

        self.train_scorings_to_find_the_best = np.asarray(
            [item * sign_for_score for item in self.train_scorings]
        )
        self.val_scorings_to_find_the_best = np.asarray(
            [item * sign_for_score for item in self.val_scorings]
        )

    def next(self):
        self.find_train_val_scorings_to_find_the_best()

        indexs_good_model = np.where(
            (self.val_scorings_to_find_the_best > self.target_score)
            & (self.train_scorings_to_find_the_best > self.target_score)
        )[0]

        index_best_model = None
        if (
            len(indexs_good_model) == 0
        ):  # Nếu ko có model nào đạt chỉ tiêu thì lấy cái tốt nhất
            index_best_model = np.argmax(self.val_scorings_to_find_the_best)
        else:
            val_series = pd.Series(
                self.val_scorings_to_find_the_best[indexs_good_model],
                index=indexs_good_model,
            )
            index_best_model = val_series.idxmax()

        best_model = self.models[index_best_model]
        train_scoring = self.train_scorings[index_best_model]
        val_scoring = self.val_scorings[index_best_model]

        return best_model, index_best_model, train_scoring, val_scoring


class CustomStackingClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, estimators, final_estimator, weights=None):
        self.estimators = estimators
        self.final_estimator = final_estimator
        self.weights = weights

        if self.weights is None:
            self.weights = [1] * len(self.estimators)

    def fit(self, X, y):
        for estimator in self.estimators:
            estimator.fit(X, y)

        new_feature = self.get_new_feature_through_estimators(X)

        self.final_estimator.fit(new_feature, y)

        return self

    def fit_model_incremental_learning(self, X, y):
        for estimator in self.estimators:
            myfuncs.fit_model_incremental_learning(estimator, X, y)

        new_feature = self.get_new_feature_through_estimators(X)

        myfuncs.fit_model_incremental_learning(self.final_estimator, new_feature, y)

        return self

    def predict(self, X):
        new_feature = self.get_new_feature_through_estimators(X)

        return self.final_estimator.predict(new_feature)

    def predict_proba(self, X):

        new_feature = self.get_new_feature_through_estimators(X)

        return self.final_estimator.predict_proba(new_feature)

    def get_new_feature_through_estimators(self, X):
        """Get new feature thông qua các estimators

        VD: nếu có 3 estimators và có 4 label cần phân loại thì kích thước của kết quả là (N, 3 * 4) = (N, 12)

        với N: số sample
        """
        list_predict_proba = [
            estimator.predict_proba(X) * weight
            for estimator, weight in zip(self.estimators, self.weights)
        ]
        new_feature = np.hstack(list_predict_proba)

        return new_feature


class CustomIncrementalPCA(BaseEstimator, TransformerMixin):
    def __init__(self, n_components, batch_size) -> None:
        super().__init__()
        self.n_components = n_components
        self.batch_size = batch_size

    def fit(self, X, y=None):
        X = np.asarray(X)

        self.transformer = IncrementalPCA(n_components=self.n_components)

        num_train_samples = len(X)
        list_X_batch = [
            X[i : i + self.batch_size, :]
            for i in range(0, num_train_samples, self.batch_size)
        ]

        for X_batch in list_X_batch:
            self.transformer.partial_fit(X_batch)

    def transform(self, X, y=None):
        X = self.transformer.transform(X)

        X = pd.DataFrame(X)

        self.cols = X.columns

        return X

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class BatchRBFKernelPCA(BaseEstimator, TransformerMixin):
    def __init__(self, n_components, batch_size, gamma="scale") -> None:
        super().__init__()
        self.n_components = n_components
        self.batch_size = batch_size
        self.gamma = gamma

    def fit(self, X, y=None):
        X = np.asarray(X)

        self.transformer = KernelPCA(
            kernel="rbf", n_components=self.n_components, gamma=self.gamma
        )

        num_train_samples = len(X)
        list_X_batch = [
            X[i : i + self.batch_size, :]
            for i in range(0, num_train_samples, self.batch_size)
        ]

        for X_batch in list_X_batch:
            self.transformer.fit(X_batch)

    def transform(self, X, y=None):
        X = self.transformer.transform(X)

        X = pd.DataFrame(X)

        self.cols = X.columns

        return X

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class CustomLocallyLinearEmbedding(BaseEstimator, TransformerMixin):
    def __init__(self, n_components, n_neighbors, batch_size) -> None:
        super().__init__()
        self.n_components = n_components
        self.batch_size = batch_size
        self.n_neighbors = n_neighbors

    def fit(self, X, y=None):
        X = np.asarray(X)

        self.transformer = LocallyLinearEmbedding(
            n_components=self.n_components, n_neighbors=self.n_neighbors
        )

        num_train_samples = len(X)
        list_X_batch = [
            X[i : i + self.batch_size, :]
            for i in range(0, num_train_samples, self.batch_size)
        ]

        for X_batch in list_X_batch:
            self.transformer.fit(X_batch)

    def transform(self, X, y=None):
        X = self.transformer.transform(X)

        X = pd.DataFrame(X)

        self.cols = X.columns

        return X

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class MultiplyWeightsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, weights) -> None:
        super().__init__()
        self.weights = weights

    def fit(self, X, y=None):

        return self

    def transform(self, X, y=None):
        for col_name, weight in self.weights.items():
            X[col_name] = X[col_name] * weight

        self.cols = X.columns.tolist()

        return X

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class DuringFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, feature_ordinal_dict) -> None:
        super().__init__()
        self.feature_ordinal_dict = feature_ordinal_dict

    def fit(self, X, y=None):
        # Lấy các cột numeric, nominal, ordinal
        (
            numeric_cols,
            numericcat_cols,
            _,
            binary_cols,
            nominal_cols,
            _,
        ) = myfuncs.get_different_types_feature_cols_from_df_14(X)

        numeric_cols = (
            numeric_cols + numericcat_cols + binary_cols
        )  # Bao gồm cột numeric, numericcat và binary

        ordinal_cols = list(self.feature_ordinal_dict.keys())

        nominal_cols_pipeline = Pipeline(
            steps=[
                ("1", OneHotEncoder(sparse_output=False, drop="first")),
                ("2", MinMaxScaler()),
            ]
        )

        ordinal_cols_pipeline = Pipeline(
            steps=[
                (
                    "1",
                    OrdinalEncoder(categories=list(self.feature_ordinal_dict.values())),
                ),
                ("2", MinMaxScaler()),
            ]
        )

        self.column_transformer = ColumnTransformer(
            transformers=[
                ("1", MinMaxScaler(), numeric_cols),
                ("2", nominal_cols_pipeline, nominal_cols),
                ("3", ordinal_cols_pipeline, ordinal_cols),
            ],
        )

        self.column_transformer.fit(X)

    def transform(self, X, y=None):
        X = self.column_transformer.transform(X)

        self.cols = myfuncs.get_real_column_name_from_get_feature_names_out(
            self.column_transformer.get_feature_names_out()
        )

        return pd.DataFrame(X, columns=self.cols)

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names_out(self, input_features=None):
        return self.cols


class NamedColumnTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_transformer) -> None:
        super().__init__()
        self.column_transformer = column_transformer

    def fit(self, X, y=None):
        self.column_transformer.fit(X)

    def transform(self, X, y=None):
        X = self.column_transformer.transform(X)

        cols = myfuncs.fix_name_by_LGBM_standard(
            myfuncs.get_real_column_name_from_get_feature_names_out(
                self.column_transformer.get_feature_names_out()
            )
        )

        return pd.DataFrame(
            X,
            columns=cols,
        )

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)


class CustomManyLayersStackingClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, list_estimators, final_estimator, list_weights=None):
        """Phiên bản nhiều layers của CustomStackingClassifier <br>

        Examples:
        ```
        list_estimators = [[LogisticRegression(), XGBClassifier(), RandomForest()], [XGBClassifier(), RandomForest()]]
        final_estimator = LogisticRegression()
        ```
        Khi đó cấu trúc của model như sau:
        ```
        layer 1: LogisticRegression(), XGBClassifier(), RandomForest()
        layer 2: XGBClassifier(), RandomForest()
        layer cuối: LogisticRegression()
        ```
        Ví dụ nếu có dùng weights, thì lưu ý weights phải có cấu trúc tương ứng với list_estimators, vd theo ở trên thì :
        ```
        weights = [[1,2,3], [2,3]]
        ```

        Args:
            list_estimators (_type_): _description_
            final_estimator (_type_): _description_
            weights (_type_, optional): trọng số ứng với cấu trúc của **list_estimators** đấy nhen !!!!!!. Defaults to None.
        """
        self.list_estimators = list_estimators
        self.final_estimator = final_estimator
        self.list_weights = list_weights

        if self.list_weights is None:
            self.list_weights = myfuncs.create_list_constants_followed_by_list_list(
                self.list_estimators
            )

    def fit_one_estimators_and_convert_X(self, estimators, weights, X, y):
        result = []

        for estimator, weight in zip(estimators, weights):
            estimator.fit(X, y)
            result.append(estimator.predict_proba(X) * weight)

        return np.hstack(result)

    def fit(self, X, y):
        for estimators, weights in zip(self.list_estimators, self.list_weights):
            X = self.fit_one_estimators_and_convert_X(estimators, weights, X, y)

        self.final_estimator.fit(X, y)

    def fit_model_incremental_learning_one_estimators_and_convert_X(
        self, estimators, weights, X, y
    ):
        result = []

        for estimator, weight in zip(estimators, weights):
            myfuncs.fit_model_incremental_learning(estimator, X, y)
            result.append(estimator.predict_proba(X) * weight)

        return np.hstack(result)

    def fit_model_incremental_learning(self, X, y):
        for estimators, weights in zip(self.list_estimators, self.list_weights):
            X = self.fit_model_incremental_learning_one_estimators_and_convert_X(
                estimators, weights, X, y
            )

        myfuncs.fit_model_incremental_learning(self.final_estimator, X, y)

    def predict(self, X):
        new_feature = self.get_new_feature_through_list_estimators(X)

        return self.final_estimator.predict(new_feature)

    def predict_proba(self, X):
        new_feature = self.get_new_feature_through_list_estimators(X)

        return self.final_estimator.predict_proba(new_feature)

    def get_new_feature_through_estimators(self, estimators, weights, X):
        result = []

        for estimator, weight in zip(estimators, weights):
            result.append(estimator.predict_proba(X) * weight)

        return np.hstack(result)

    def get_new_feature_through_list_estimators(self, X):
        for estimators, weights in zip(self.list_estimators, self.list_weights):
            X = self.get_new_feature_through_estimators(estimators, weights, X)

        return X


class CustomStackingRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, estimators, final_estimator, weights=None):
        self.estimators = estimators
        self.final_estimator = final_estimator
        self.weights = weights

        if self.weights is None:
            self.weights = [1] * len(self.estimators)

    def fit(self, X, y):
        for estimator in self.estimators:
            estimator.fit(X, y)

        new_feature = self.get_new_feature_through_estimators(X)
        self.final_estimator.fit(new_feature, y)

        return self

    def fit_model_incremental_learning(self, X, y):
        for estimator in self.estimators:
            myfuncs.fit_model_incremental_learning(estimator, X, y)

        new_feature = self.get_new_feature_through_estimators(X)
        myfuncs.fit_model_incremental_learning(self.final_estimator, new_feature, y)

        return self

    def predict(self, X):
        new_feature = self.get_new_feature_through_estimators(X)

        return self.final_estimator.predict(new_feature)

    def predict_proba(self, X):

        new_feature = self.get_new_feature_through_estimators(X)

        return self.final_estimator.predict_proba(new_feature)

    def get_new_feature_through_estimators(self, X):
        """Get new feature thông qua các estimators và lưu ý đây là regression nhé"""
        list_predict_proba = [
            estimator.predict(X) * weight
            for estimator, weight in zip(self.estimators, self.weights)
        ]
        new_feature = np.hstack(list_predict_proba)

        return new_feature
