from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.cm as cm
from Mylib import tf_myfuncs, myfuncs
from sklearn import metrics
from tensorflow.keras import backend


class ConvNetBlock_XceptionVersion(layers.Layer):
    """Gồm các layers sau:
    - SeparableConv2D
    - SeparableConv2D
    - MaxPooling2D

    Đi kèm là sự kết hợp giữa residual connections, batch normalization và  depthwise separable convolutions (lớp SeparableConv2D)

    Attributes:
        filters (_type_): số lượng filters trong lớp SeparableConv2D
    """

    def __init__(self, filters, name=None, **kwargs):
        # super(ConvNetBlock_XceptionVersion, self).__init__()
        super().__init__(name=name, **kwargs)
        self.filters = filters

    def build(self, input_shape):
        self.BatchNormalization = layers.BatchNormalization()
        self.Activation = layers.Activation("relu")
        self.SeparableConv2D = layers.SeparableConv2D(
            self.filters, 3, padding="same", use_bias=False
        )

        self.BatchNormalization_1 = layers.BatchNormalization()
        self.Activation_1 = layers.Activation("relu")
        self.SeparableConv2D_1 = layers.SeparableConv2D(
            self.filters, 3, padding="same", use_bias=False
        )
        self.MaxPooling2D = layers.MaxPooling2D(3, strides=2, padding="same")

        self.Conv2D = layers.Conv2D(
            self.filters, 1, strides=2, padding="same", use_bias=False
        )

        super().build(input_shape)

    def call(self, x):
        residual = x

        # First part of the block
        x = self.BatchNormalization(x)
        x = self.Activation(x)
        x = self.SeparableConv2D(x)

        # Second part of the block
        x = self.BatchNormalization_1(x)
        x = self.Activation_1(x)
        x = self.SeparableConv2D_1(x)
        x = self.MaxPooling2D(x)

        # Apply residual connection
        residual = self.Conv2D(residual)
        x = layers.add([x, residual])

        return x

    def get_config(self):
        # Trả về cấu hình của lớp tùy chỉnh
        config = super().get_config()
        config.update({"filters": self.filters})
        return config

    @classmethod
    def from_config(cls, config):
        # Giải mã lại lớp từ cấu hình
        name = config.pop("name", None)
        return cls(**config)


class ConvNetBlock_Advanced(layers.Layer):
    """Gồm các layers sau:
    - Conv2D
    - Conv2D
    - MaxPooling2D

    Đi kèm là sự kết hợp giữa residual connections, batch normalization

    Attributes:
        filters (_type_): số lượng filters trong lớp Conv2D
    """

    def __init__(self, filters, **kwargs):
        super().__init__(**kwargs)
        self.filters = filters

    def build(self, input_shape):
        self.BatchNormalization = layers.BatchNormalization()
        self.Activation = layers.Activation("relu")
        self.Conv2D = layers.Conv2D(self.filters, 3, padding="same")

        self.BatchNormalization_1 = layers.BatchNormalization()
        self.Activation_1 = layers.Activation("relu")
        self.Conv2D_1 = layers.Conv2D(self.filters, 3, padding="same")
        self.MaxPooling2D = layers.MaxPooling2D(2, padding="same")

        self.Conv2D_2 = layers.Conv2D(self.filters, 1, strides=2)

        super().build(input_shape)

    def call(self, x):
        residual = x

        # First part of the block
        x = self.BatchNormalization(x)
        x = self.Activation(x)
        x = self.Conv2D(x)

        # Second part of the block
        x = self.BatchNormalization_1(x)
        x = self.Activation_1(x)
        x = self.Conv2D_1(x)
        x = self.MaxPooling2D(x)

        # Xử lí residual
        residual = self.Conv2D_2(residual)

        # Apply residual connection
        x = layers.add([x, residual])

        return x

    def get_config(self):
        # Trả về cấu hình của lớp tùy chỉnh
        config = super().get_config()
        config.update(
            {
                "filters": self.filters,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        # Giải mã lại lớp từ cấu hình
        return cls(**config)


class ConvNetBlock(layers.Layer):
    """Kết hợp các layers sau:
    - Conv2D * num_Conv2D_layer
    - MaxPooling

    Attributes:
        filters (_type_): số lượng filters trong lớp Conv2D
        num_Conv2D (int, optional): số lượng lớp num_Conv2D. Defaults to 1.
    """

    def __init__(self, filters, num_Conv2D=1, name=None, **kwargs):
        """ """
        # super(ConvNetBlock, self).__init__()
        super().__init__(name=name, **kwargs)
        self.filters = filters
        self.num_Conv2D = num_Conv2D

    def build(self, input_shape):
        self.list_Conv2D = [
            layers.Conv2D(self.filters, 3, activation="relu")
            for _ in range(self.num_Conv2D)
        ]

        self.MaxPooling2D = layers.MaxPooling2D(pool_size=2)

        super().build(input_shape)

    def call(self, x):
        for conv2D in self.list_Conv2D:
            x = conv2D(x)

        x = self.MaxPooling2D(x)

        return x

    def get_config(self):
        # Trả về cấu hình của lớp tùy chỉnh
        config = super().get_config()
        config.update(
            {
                "filters": self.filters,
                "num_Conv2D": self.num_Conv2D,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


class ImageDataPositionAugmentation(layers.Layer):
    """Tăng cường dữ liệu hình ảnh ở khía cạnh vị trí, bao gồm các lớp sau (**trong tf.keras.layers**)
    - RandomFlip
    - RandomRotation
    - RandomZoom

    Attributes:
        rotation_factor (float): Tham số cho lớp RandomRotation. Default to 0.2
        zoom_factor (float): Tham số cho lớp RandomZoom. Default to 0.2
    """

    def __init__(self, rotation_factor=0.2, zoom_factor=0.2, **kwargs):
        # super(ImageDataPositionAugmentation, self).__init__()
        super().__init__(**kwargs)
        self.rotation_factor = rotation_factor
        self.zoom_factor = zoom_factor

    def build(self, input_shape):
        self.RandomFlip = layers.RandomFlip(mode="horizontal_and_vertical")
        self.RandomRotation = layers.RandomRotation(factor=self.rotation_factor)
        self.RandomZoom = layers.RandomZoom(height_factor=self.zoom_factor)

        super().build(input_shape)

    def call(self, x):
        x = self.RandomFlip(x)
        x = self.RandomRotation(x)
        x = self.RandomZoom(x)

        return x

    def get_config(self):
        # Trả về cấu hình của lớp tùy chỉnh
        config = super().get_config()
        config.update(
            {
                "rotation_factor": self.rotation_factor,
                "zoom_factor": self.zoom_factor,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        # Giải mã lại lớp từ cấu hình
        name = config.pop("name", None)
        return cls(**config)


class PretrainedModel(layers.Layer):
    """Sử dụng các pretrained models ở trong **keras.applications**
    Attributes:
        model_name (str): Tên pretrained model, vd: vgg16, vgg19, ....
        num_trainable (int, optional): Số lượng các lớp đầu tiên cho trainable = True. Defaults to 0.
    """

    def __init__(self, model_name, num_trainable=0, **kwargs):
        if num_trainable < 0:
            raise ValueError(
                "=========ERROR: Tham số <num_trainable> trong class PretrainedModel phải >= 0   ============="
            )

        # super(ConvNetBlock, self).__init__()
        super().__init__(**kwargs)
        self.model_name = model_name
        self.num_trainable = num_trainable

    def build(self, input_shape):
        if self.model_name == "vgg16":
            self.model = keras.applications.vgg16.VGG16(
                weights="imagenet", include_top=False
            )
            self.preprocess_input = keras.applications.vgg16.preprocess_input
        elif self.model_name == "vgg19":
            self.model = keras.applications.vgg19.VGG19(
                weights="imagenet", include_top=False
            )
            self.preprocess_input = keras.applications.vgg19.preprocess_input
        else:
            raise ValueError(
                "=========ERROR: Pretrained model name is not valid============="
            )

        # Cập nhật trạng thái trainable cho các lớp đầu
        if self.num_trainable == 0:
            self.model.trainable = False
        else:
            self.model.trainable = True
            for layer in self.model.layers[: -self.num_trainable]:
                layer.trainable = False

        super().build(input_shape)

    def call(self, x):
        x = self.preprocess_input(x)
        x = self.model(x)

        return x


class GradCAMForImages:
    """Thực hiện quá trình GradCAM để xác định những phần nảo của ảnh hỗ trợ model phân loại nhiều nhất
    Attributes:
        images (np.ndarray): Tập ảnh đã được chuyển thành **array**
        model (_type_): model
        last_convnet_layer_name ([str, int]): **Tên** hoặc  **index** của layer convent cuối cùng trong model

    Hàm -> **convert()**

    Returns:
        list_superimposed_img (list[PIL.Image.Image]): 1 mảng

    Examples:
        Nhấn mạnh những phần trên ảnh giúp phân loại các lá -> 3 loại: healthy, early_blight, late_blight
        ```python
        # Lấy đường dẫn của các ảnh
        img_paths = [os.path.join(folder, file) for file in file_names]

        # Chuyển các ảnh thành các mảng numpy
        file_names_array = myclasses.ImagesToArrayConverter(image_paths=img_paths, target_size=256).convert()

        # Load model
        model = load_model("artifacts/model_trainer/CONVNET_45/best_model.keras")
        last_convnet_index = int(3) # Specify lớp convnet cuối cùng (thông qua chỉ số), mà cũng nên dùng chỉ số đi :))))

        # Kết quả thu được là 1 mảng các PIL.Image.Image
        result = myclasses.GradCAMForImages(file_names_array, model, last_convnet_index).convert()

        # Show các ảnh lên
        for image in result:
            plt.imshow(image)
        ```
    """

    def __init__(self, images, model, last_convnet_layer_name):
        self.images = images
        self.model = model
        self.last_convnet_layer_name = last_convnet_layer_name

    def create_models(self):
        """Tạo ra 2 model sau:

        **last_conv_layer_model**: model map input image -> convnet block cuối cùng

        **classifier_model**: model map convnet block cuối cùng -> final class predictions.

        Returns:
            tuple: last_conv_layer_model, classifier_model
        """
        last_conv_layer = None
        classifier_layers = None
        if isinstance(self.last_convnet_layer_name, str):
            layer_names = [layer.name for layer in self.model.layers]
            last_conv_layer = self.model.get_layer(self.last_convnet_layer_name)
            classifier_layers = self.model.layers[
                layer_names.index(self.last_convnet_layer_name) + 1 :
            ]
        else:
            last_conv_layer = self.model.layers[self.last_convnet_layer_name]
            classifier_layers = self.model.layers[self.last_convnet_layer_name + 1 :]

        # Model đầu tiên
        last_conv_layer_model = keras.Model(
            inputs=self.model.inputs, outputs=last_conv_layer.output
        )

        classifier_input = keras.Input(shape=last_conv_layer.output.shape[1:])
        x = classifier_input

        for layer in classifier_layers:
            x = layer(x)

        # Model thứ hai
        classifier_model = keras.Model(inputs=classifier_input, outputs=x)

        return last_conv_layer_model, classifier_model

    def do_gradient(self, last_conv_layer_model, classifier_model):
        with tf.GradientTape() as tape:
            last_conv_layer_output = last_conv_layer_model(self.images)
            tape.watch(last_conv_layer_output)
            preds = classifier_model(last_conv_layer_output)
            top_pred_index = tf.argmax(preds[0])
            top_class_channel = preds[:, top_pred_index]

        grads = tape.gradient(top_class_channel, last_conv_layer_output)
        return grads, last_conv_layer_output

    def get_heatmap(self, grads, last_conv_layer_output):
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2)).numpy()
        last_conv_layer_output = last_conv_layer_output.numpy()[0]

        for i in range(pooled_grads.shape[-1]):
            last_conv_layer_output[:, :, i] *= pooled_grads[i]

        heatmap = np.mean(last_conv_layer_output, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)

        return heatmap

    def convert_1image(self, img, heatmap):

        heatmap = np.uint8(255 * heatmap)

        jet = cm.get_cmap("jet")  # Dùng "jet" để tô màu lại heatmap
        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]
        jet_heatmap = keras.utils.array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
        jet_heatmap = keras.utils.img_to_array(jet_heatmap)
        superimposed_img = jet_heatmap * 0.4 + img
        superimposed_img = keras.utils.array_to_img(superimposed_img)

        return superimposed_img

    def convert(self):
        last_conv_layer_model, classifier_model = self.create_models()
        grads, last_conv_layer_output = self.do_gradient(
            last_conv_layer_model, classifier_model
        )
        heatmap = self.get_heatmap(grads, last_conv_layer_output)

        list_superimposed_img = [
            self.convert_1image(img, heatmap) for img in self.images
        ]

        return list_superimposed_img


class ImagesToArrayConverter:
    """Chuyển 1 tập ảnh  thành 1 mảng numpy

    Attributes:
        image_paths (list): Tập các đường dẫn đến các file ảnh
        target_size (int): Kích thước sau khi resize

    Hàm -> convert()

    Returns:
        result (np.ndarray):
    """

    def __init__(self, image_paths, target_size):
        self.image_paths = image_paths
        self.target_size = (target_size, target_size)

    def convert_1image(self, img_path):
        img = keras.utils.load_img(
            img_path, target_size=self.target_size
        )  # load ảnh và resize luôn
        array = keras.utils.img_to_array(img)  # Chuyển img sang array
        array = np.expand_dims(
            array, axis=0
        )  # Thêm chiều để tạo thành mảng có 1 phần tử
        return array

    def convert(self):
        return np.vstack(
            [self.convert_1image(img_path) for img_path in self.image_paths]
        )


class ClassifierEvaluator:
    """Đánh giá classifier trong Deep learning model

    Args:
        model (_type_): _description_
        class_names (_type_): _description_
        train_ds (_type_): _description_
        val_ds (_type_, optional): Nếu không có, tức là chỉ đánh giá trên 1 tập thôi (đánh giá cho tập test). Defaults to None.
    """

    def __init__(self, model, class_names, train_ds, val_ds=None):
        self.model = model
        self.class_names = class_names
        self.train_ds = train_ds
        self.val_ds = val_ds

    def evaluate_train_classifier(self):
        train_target_data, train_pred = tf_myfuncs.get_full_target_and_pred_for_DLmodel(
            self.model, self.train_ds
        )
        train_pred = [int(item) for item in train_pred]
        train_target_data = [int(item) for item in train_target_data]

        val_target_data, val_pred = tf_myfuncs.get_full_target_and_pred_for_DLmodel(
            self.model, self.val_ds
        )
        val_pred = [int(item) for item in val_pred]
        val_target_data = [int(item) for item in val_target_data]

        # Accuracy
        train_accuracy = metrics.accuracy_score(train_target_data, train_pred)
        val_accuracy = metrics.accuracy_score(val_target_data, val_pred)

        # Classification report
        class_names = np.asarray(self.class_names)
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
        test_target_data, test_pred = tf_myfuncs.get_full_target_and_pred_for_DLmodel(
            self.model, self.train_ds
        )
        test_pred = [int(item) for item in test_pred]
        test_target_data = [int(item) for item in test_target_data]

        # Accuracy
        test_accuracy = metrics.accuracy_score(test_target_data, test_pred)

        # Classification report
        class_names = np.asarray(self.class_names)
        named_test_target_data = class_names[test_target_data]
        named_test_pred = class_names[test_pred]

        test_classification_report = metrics.classification_report(
            named_test_target_data, named_test_pred
        )

        # Confusion matrix
        test_confusion_matrix = metrics.confusion_matrix(
            named_test_target_data, named_test_pred, labels=class_names
        )
        np.fill_diagonal(test_confusion_matrix, 0)
        test_confusion_matrix = myfuncs.get_heatmap_for_confusion_matrix_30(
            test_confusion_matrix, class_names
        )

        model_results_text = f"Test accuracy: {test_accuracy}\n"
        model_results_text += (
            f"Test classification_report: \n{test_classification_report}\n"
        )

        return model_results_text, test_confusion_matrix

    def evaluate(self):
        return (
            self.evaluate_train_classifier()
            if self.val_ds is not None
            else self.evaluate_test_classifier()
        )


class RegressorEvaluator:
    def __init__(self, model, train_ds, val_ds=None):
        self.model = model
        self.train_ds = train_ds
        self.val_ds = val_ds

    def evaluate_train_classifier(self):
        train_target_data, train_pred = (
            tf_myfuncs.get_full_target_and_pred_for_regression_DLmodel(
                self.model, self.train_ds
            )
        )
        val_target_data, val_pred = (
            tf_myfuncs.get_full_target_and_pred_for_regression_DLmodel(
                self.model, self.val_ds
            )
        )

        # RMSE
        train_rmse = np.sqrt(metrics.mean_squared_error(train_target_data, train_pred))
        val_rmse = np.sqrt(metrics.mean_squared_error(val_target_data, val_pred))

        # MAE
        train_mae = metrics.mean_absolute_error(train_target_data, train_pred)
        val_mae = metrics.mean_absolute_error(val_target_data, val_pred)

        model_result_text = f"Train RMSE: {train_rmse}\n"
        model_result_text += f"Val RMSE: {val_rmse}\n"
        model_result_text += f"Train MAE: {train_mae}\n"
        model_result_text += f"Val MAE: {val_mae}"

        return model_result_text

    def evaluate_test_classifier(self):
        test_target_data, test_pred = (
            tf_myfuncs.get_full_target_and_pred_for_regression_DLmodel(
                self.model, self.train_ds
            )
        )

        # RMSE
        test_rmse = np.sqrt(metrics.mean_squared_error(test_target_data, test_pred))

        # MAE
        test_mae = metrics.mean_absolute_error(test_target_data, test_pred)

        model_result_text = f"Test RMSE: {test_rmse}\n"
        model_result_text += f"Test MAE: {test_mae}\n"

        return model_result_text


class PositionalEmbedding(layers.Layer):
    def __init__(self, sequence_length, input_dim, output_dim, **kwargs):
        # TODO: d
        print("Update  PositionalEmbedding lần 1")
        # d

        super().__init__(**kwargs)
        # Các layers
        self.token_embeddings = layers.Embedding(
            input_dim=input_dim, output_dim=output_dim
        )  # Embedding layers cho token indices
        self.position_embeddings = layers.Embedding(
            input_dim=sequence_length, output_dim=output_dim
        )  # Layer này cho token positions

        # Các siêu tham số
        self.sequence_length = sequence_length
        self.input_dim = input_dim
        self.output_dim = output_dim

    def call(self, inputs):

        length = tf.shape(inputs)[-1]
        positions = tf.range(start=0, limit=length, delta=1)
        embedded_tokens = self.token_embeddings(inputs)
        embedded_positions = self.position_embeddings(positions)
        embedded = embedded_tokens + embedded_positions  # Cộng 2 embedding vectors lại

        # Save mask using Keras's _keras_mask mechanism
        embedded._keras_mask = tf.not_equal(inputs, 0)
        return embedded

    def build(self, input_shape):
        super().build(input_shape)

    def compute_mask(
        self, inputs, mask=None
    ):  # Giống với Embedding layer,  layer này nên tạo ra mask để ignore paddings 0 trong inputs
        return None

    def get_config(self):  # Để lưu được model
        config = super().get_config()
        config.update(
            {
                "output_dim": self.output_dim,
                "sequence_length": self.sequence_length,
                "input_dim": self.input_dim,
            }
        )
        return config


class TransformerEncoder(layers.Layer):
    def __init__(self, embed_dim, dense_dim, num_heads, **kwargs):
        super().__init__(**kwargs)
        # Các siêu tham số
        self.supports_masking = True  # Có hỗ trợ masking
        self.embed_dim = embed_dim  # size của input token vectors
        self.dense_dim = dense_dim  # Size của Denser layer
        self.num_heads = num_heads  # Số lượng attention heads

        # Các layers
        self.attention = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.dense_proj = keras.Sequential(
            [
                layers.Dense(dense_dim, activation="relu"),
                layers.Dense(embed_dim),
            ]
        )
        self.layernorm_1 = layers.LayerNormalization()
        self.layernorm_2 = layers.LayerNormalization()

    def call(self, inputs, mask=None):  # Tính toán là ở trong hàm call()
        if mask is not None:
            mask = mask[
                :, tf.newaxis, :
            ]  # mask được tạo ra bởi Embedding layer là 2D, nhưng attention layer thì yêu cầu 3D hoặc 4D -> thêm chiều
        attention_output = self.attention(inputs, inputs, attention_mask=mask)
        proj_input = self.layernorm_1(inputs + attention_output)
        proj_output = self.dense_proj(proj_input)
        return self.layernorm_2(proj_input + proj_output)

    def build(self, input_shape):
        super().build(input_shape)

    def get_config(self):  # Cần thiết để lưu model
        config = super().get_config()
        config.update(
            {
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "dense_dim": self.dense_dim,
            }
        )
        return config


class TransformerDecoder(layers.Layer):
    def __init__(self, embed_dim, dense_dim, num_heads, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.attention_1 = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.attention_2 = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.dense_proj = keras.Sequential(
            [
                layers.Dense(dense_dim, activation="relu"),
                layers.Dense(embed_dim),
            ]
        )
        self.layernorm_1 = layers.LayerNormalization()
        self.layernorm_2 = layers.LayerNormalization()
        self.layernorm_3 = layers.LayerNormalization()
        self.supports_masking = True

    def call(self, inputs, encoder_outputs, mask=None):
        causal_mask = self.get_causal_attention_mask(inputs)  # Get causal_mask
        padding_mask = None  # Define để né lỗi UnboundLocalError
        if mask is not None:  # Chuẩn bị input mask
            padding_mask = tf.cast(mask[:, tf.newaxis, :], dtype="int32")
            padding_mask = tf.minimum(
                padding_mask, causal_mask
            )  # merge 2 masks với nhau
        attention_output_1 = self.attention_1(
            query=inputs,
            value=inputs,
            key=inputs,
            attention_mask=causal_mask,  # pass causal_mask vào layer attention đâu tiên,
            # cái thực hiện  self-attention cho target sequence
        )
        attention_output_1 = self.layernorm_1(inputs + attention_output_1)
        attention_output_2 = self.attention_2(
            query=attention_output_1,
            value=encoder_outputs,
            key=encoder_outputs,
            attention_mask=padding_mask,  # pass combined mask cho layer attention thứ 2,
            # cái mà relates the source sequence to the target sequence.
        )
        attention_output_2 = self.layernorm_2(attention_output_1 + attention_output_2)
        proj_output = self.dense_proj(attention_output_2)
        return self.layernorm_3(attention_output_2 + proj_output)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "dense_dim": self.dense_dim,
            }
        )
        return config

    def get_causal_attention_mask(self, inputs):
        input_shape = tf.shape(inputs)
        batch_size, sequence_length = input_shape[0], input_shape[1]
        i = tf.range(sequence_length)[:, tf.newaxis]
        j = tf.range(sequence_length)
        mask = tf.cast(i >= j, dtype="int32")
        mask = tf.reshape(mask, (1, input_shape[1], input_shape[1]))
        mult = tf.concat(
            [tf.expand_dims(batch_size, -1), tf.constant([1, 1], dtype=tf.int32)],
            axis=0,
        )
        return tf.tile(mask, mult)

    def build(self, input_shape):
        # No custom weights to create, so just mark as built
        super().build(input_shape)
