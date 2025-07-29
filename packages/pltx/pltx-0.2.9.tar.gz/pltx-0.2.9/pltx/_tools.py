import itertools
from pathlib import Path
from typing import Union, Tuple
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from sklearn.calibration import label_binarize
from sklearn.metrics import roc_curve, auc, confusion_matrix


def plot_confusion_matrix(
    cm: np.ndarray,
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Confusion matrix",
    cmap=plt.cm.Blues,
):
    """
    绘制预测结果与真实结果的混淆矩阵

    参数:
    - cm: np.ndarray, 混淆矩阵
    - classes: list, 默认为None, 类别标签
    - figsize: Tuple[int, int], 默认为None, 图像尺寸
    - title: str, 默认为"Confusion matrix", 图表标题
    - cmap: 颜色图谱，默认为plt.cm.Blues
    """
    # 增加图像尺寸，设置更大的底部边距
    if figsize:
        plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()

    # 设置刻度标签
    classes = classes or [i for i in range(cm.shape[0])]
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, ha="right")  # 将标签旋转45度，右对齐
    plt.yticks(tick_marks, classes)

    # 添加数值标注
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    # 调整布局，确保所有元素都显示完整
    plt.tight_layout()

    # 添加标签，并调整位置
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

    # 调整底部边距，确保x轴标签完全显示
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def plot_confusion_matrix2(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Confusion matrix",
    cmap=plt.cm.Blues,
):
    """
    绘制预测结果与真实结果的混淆矩阵

    参数:
    - y_true: np.ndarray or list, 真实标签
    - y_pred: np.ndarray or list, 预测标签
    - classes: list, 默认为None, 类别标签
    - figsize: Tuple[int, int], 默认为None, 图像尺寸
    - title: str, 默认为"Confusion matrix", 图表标题
    - cmap: 颜色图谱，默认为plt.cm.Blues
    """
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_pred = y_pred if isinstance(y_pred, np.ndarray) else np.array(y_pred)
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, classes, figsize, title, cmap)


def plot_roc(
    y_true: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
    figsize: Tuple[int, int] = None,
    title="Receiver Operating Characteristic",
    xlabel="False Positive Rate",
    ylabel="True Positive Rate",
):
    """
    绘制ROC曲线。

    参数:
    - y_true: 真实标签，可以是numpy数组或列表。
    - y_prob: 预测为正类的概率，可以是numpy数组或列表。
    - figsize: 图形大小，可选，默认为None。
    - title: 图形标题，可选，默认为"Receiver Operating Characteristic"。
    - xlabel: X轴标签，可选，默认为"False Positive Rate"。
    - ylabel: Y轴标签，可选，默认为"True Positive Rate"。
    """
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_prob = y_prob if isinstance(y_prob, np.ndarray) else np.array(y_prob)
    fpr, tpr, thesholds_ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)  # 曲线下面积

    # 绘制 ROC曲线
    if figsize:
        plt.figure(figsize=figsize)
    plt.title(title)
    plt.plot(fpr, tpr, "b", label="AUC = %0.5f" % roc_auc)
    plt.legend(loc="lower right")
    plt.plot([0, 1], [0, 1], "r--")
    plt.xlim([-0.1, 1.0])
    plt.ylim([-0.1, 1.01])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()


def plot_multi_class_roc(
    y_true: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Receiver Operating Characteristic",
    xlabel="False Positive Rate",
    ylabel="True Positive Rate",
):
    """
    绘制宏平均ROC曲线
    参数:
    y_true: 真实标签
    y_pred: 预测概率
    classes: 类别列表
    """
    # 计算每个类别的ROC曲线和AUC
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_prob = y_prob if isinstance(y_prob, np.ndarray) else np.array(y_prob)
    classes = classes or [i for i in range(y_prob.shape[1])]
    if len(y_true.shape) == 1:
        y_true = label_binarize(y_true, classes=[i for i in range(len(classes))])
 
    # 计算每个类别的假阳性率和真阳性率
    for i in range(y_true.shape[1]):
        fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_prob[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # 绘制ROC曲线
    if figsize:
        plt.figure(figsize=figsize)
    for i, cls in enumerate(classes):
        plt.plot(
            fpr[i],
            tpr[i],
            color="#1f77b4",
            linestyle="-",
            label="Class {} ROC  AUC={:.4f}".format(cls, roc_auc[i]),
            lw=2,
        )
    plt.plot([0, 1], [0, 1], color="r", linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()


def plot_corr(df, title='Feature correlation heatmap', cmap='coolwarm', figsize=(12, 8)):
    """
    绘制特征相关性热力图。
    
    参数:
    - df: 包含要分析的特征的DataFrame。
    - title: 图表的标题，默认为'Feature correlation heatmap'。
    - cmap: 颜色图谱，默认为'coolwarm'。
    - figsize: 图表的大小，默认为(12, 8)。
    """
    # 导入必要的库
    import seaborn as sns
    
    # 计算相关系数矩阵
    corr_matrix = df.corr()

    # 绘制热力图
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap=cmap)
    plt.title(title)
    plt.show()


def plot_lines(*data_lists: list, x: list = None, labels: list[str] = None, title='Linear Figure', 
               xlabel='X', ylabel='Value', figsize=(12, 8), show_grid=True,  markers: list[str] = None, **kwargs):
    """
    绘制折线图。

    参数:
    *data_lists: 一个或多个数据列表，每个列表包含一组要绘制的y轴数据。
    x: x轴数据列表。如果未提供，则默认为从1到数据列表长度的整数序列。
    labels: 用于图例的标签列表。如果提供，则必须与data_lists的长度相匹配。
    title: 图表的标题。默认为'Linear Figure'。
    xlabel: x轴的标签。默认为'X'。
    ylabel: y轴的标签。默认为'Value'。
    figsize: 指定图形的宽度和高度，默认为(12, 8)。
    show_grid: 是否显示网格线。默认为True。
    markers: 用于绘制折线的标记样式列表。默认为["o-", "*-", "s-", "x-", "^-"]，循环使用。
            "ob:": "o"为圆点, "b"为蓝色, ":"为点线
            marker=['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_','.',',']
            color=['b','g','r','c','m','y','k','w']
            linestyle=['-','--','-.',':']
    **kwargs: 其他参数传递给matplotlib的plot函数, 如: linewidth=5, markersize=20。
    """
    if markers is None:
        markers = ["o-", "*-", "s-", "x-", "^-"]

    # 如果未提供x轴数据，则默认为从1到数据列表长度的整数序列
    x = range(1, len(data_lists[0]) + 1) if x is None else x
    # 创建指定大小的新图形
    plt.figure(figsize=figsize)

    # 如果未提供标签，则直接绘制折线图；否则，添加图例标签
    if labels is not None:
        # 遍历每个数据列表并绘制折线图
        for i, data_list in enumerate(data_lists):
            plt.plot(x, data_list, markers[i % len(markers)], label=labels[i], **kwargs)
        
        # 添加图例
        plt.legend()
    else:
        # 遍历每个数据列表并绘制折线图
        for i, data_list in enumerate(data_lists):
            plt.plot(x, data_list, markers[i % len(markers)], **kwargs)
    
    # 如果提供了标题、x轴标签、y轴标签，则添加到图形中
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    
    
    
    # 添加网格线以便更好地观察
    plt.grid(show_grid)
    # 显示图形
    plt.show()


def plot_image_boxes(image, bboxes: list = None, bbox_data_type: str = 'center_width_height'):
    """
    在给定的图像上绘制目标检测框。
    
    参数:
    - image: 图像路径（字符串或Path对象）或图像数据（numpy数组）。
    - bboxes: 目标检测框的列表，其中每个框是一个包含[x, y, width, height]的数组, (x, y)是左上角坐标。
    - bbox_data_type: 边界框的类型，可以是'left_top_width_height'或'left_top_right_bottom', 'center_width_height'

    Example:
    >>> plot_image_boxes('path/to/image.jpg', [[100, 100, 50, 50], [200, 200, 30, 30]])
    >>> pred = YOLO.predict('path/to/image.jpg')
    >>> plot_image_boxes(Image.fromarray(pred.orig_img), pred.boxes.xywh.tolist(), bbox_data_type='center_width_height')
    >>> plot_image_boxes(Image.fromarray(pred.orig_img), pred.boxes.xyxy.tolist(), bbox_data_type='left_top_right_bottom')
    """
    assert bbox_data_type in ['left_top_width_height', 'left_top_right_bottom', 'center_width_height'], \
        'bbox_data_type must be "left_top_width_height", "left_top_right_bottom" or "center_width_height"'
    
    # 检查image参数是否为路径形式，如果是，则读取图片
    if isinstance(image, (str, Path)):
        # 读取图片
        image = plt.imread(image)

    # 创建一个子图
    _, ax = plt.subplots(1)
    # 在子图上显示图像
    ax.imshow(image)

    # 如果有边界框数据，绘制边界框
    if bboxes:
        for bbox in bboxes:
            # 从bbox列表中提取边界框的坐标和尺寸
            x, y, w, h = bbox
            if bbox_data_type == 'center_width_height':  # yolo xywh
                cx, cy, w, h = bbox
                x = cx - w / 2
                y = cy - h / 2
            elif bbox_data_type == 'left_top_right_bottom':  # yolo xyxy
                x, y, x2, y2 = bbox
                w = x2 - x
                h = y2 - y
            # 创建一个矩形框，边缘颜色为红，线宽为2，不填充
            rect = patches.Rectangle((x, y), w, h, edgecolor='red', linewidth=2, fill=False)
            # 将矩形框添加到图像上
            ax.add_patch(rect)

    # 关闭坐标轴显示，以使图像更清晰
    ax.axis('off')
    # 显示图像
    plt.show()
