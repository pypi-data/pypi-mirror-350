import ast
from tensorflow.keras.layers import (
    Resizing,
    Rescaling,
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    GlobalAveragePooling2D,
    Dropout,
)

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import Input
from tensorflow.keras.optimizers import RMSprop
from Mylib.tf_myclasses import (
    ConvNetBlock_XceptionVersion,
    ConvNetBlock_Advanced,
    ConvNetBlock,
    ImageDataPositionAugmentation,
    PretrainedModel,
    ManyConvNetBlocks_XceptionVersion,
    ManyConvNetBlocks_Advanced,
    ManyConvNetBlocks,
)
from Mylib.myclasses import CustomStackingClassifier


def do_ast_literal_eval_advanced_7(text: str):
    """Kế thừa hàm ast.literal_eval() nhưng xử lí thêm trường hợp sau

    Tuple, List dạng (1.0 ; 2.0), các phần tử cách nhau bởi dấu ; thay vì dấu ,

    """
    if ";" not in text:
        return ast.literal_eval(text)

    return ast.literal_eval(text.replace(";", ","))


def convert_ML_model_string_to_object_4(text: str):
    """Chuyển 1 chuỗi (**chỉ đại diện cho mô hình Machine Learning**) thành 1 đối tượng

    Example:
        text = "LogisticRegression(C=144, penalty='l1', solver='saga', max_iter=10000,dual=True)"

        -> đối tượng LogisticRegression(C=144, dual=True, max_iter=10000, penalty='l1',solver='saga')

    Args:
        text (str): _description_


    """
    # Tách tên lớp và tham số
    class_name, params = text.split("(", 1)
    params = params[:-1]

    object_class = globals()[class_name]

    if params == "":
        return object_class()

    # Lấy tham số của đối tượng
    param_parts = params.split(",")
    param_parts = [item.strip() for item in param_parts]
    keys = [item.split("=")[0].strip() for item in param_parts]

    values = [
        do_ast_literal_eval_advanced_7(item.strip().split("=")[1].strip())
        for item in param_parts
    ]

    params = dict(zip(keys, values))

    return object_class(**params)


def convert_complex_MLmodel_yaml_to_object(yaml):
    """Chuyển một yaml thành một ML model

    Examples:
    trong file demo.yaml
    ```
    models:
        -
            class_name: CustomStackingClassifier
            estimators:
                - LogisticRegression(C = 0.1)
                - GaussianNB(var_smoothing=1e-8)
                - SGDClassifier(alpha=10, loss='log_loss')
            final_estimator: LogisticRegression(C = 0.1)
    ```

    ở đây có 2 loại model:
    - Model ensemble: CustomStackingClassifier, sử dụng Stacking
    - Model đơn giản: LogisticRegression

    **Hàm này được thiết kế để đọc được 2 loại model ở trên**


    Returns:
        model: _description_
    """

    if isinstance(yaml, dict):
        return convert_CustomStackingClassifier_yaml_to_object(yaml)

    return convert_ML_model_string_to_object_4(yaml)


def convert_CustomStackingClassifier_yaml_to_object(yaml: dict):
    """Get model CustomStackingClassifier từ yaml

    yaml có định dạng sau
    ```
    - CustomStackingClassifier
    -
      estimators:
        - LogisticRegression(C = 1.0)
        - GaussianNB(var_smoothing=1e-8)
        - SGDClassifier(alpha=10)
        - XGBClassifier(n_estimators=10, max_depth=5)
      final_estimator: XGBClassifier(n_estimators=10, max_depth=5)
    ```

    Args:
        yaml (list): _description_

    Returns:
        model: _description_
    """
    estimators = yaml.estimators
    estimators = [convert_ML_model_string_to_object_4(item) for item in estimators]

    final_estimator = yaml.final_estimator
    final_estimator = convert_ML_model_string_to_object_4(final_estimator)

    return CustomStackingClassifier(
        estimators=estimators, final_estimator=final_estimator
    )
