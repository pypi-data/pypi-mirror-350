import numpy as np
from .metric_utils import *
from .metric_utils import get_events, calculate_intersection


from ._tsadeval.metrics import *
from ._tsadeval.prts.basic_metrics_ts import ts_fscore
from pate.PATE_metric import PATE
def point_wise_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate point-wise recall for anomaly detection in time series.
    Esta métrica consiste en el recall clásico, sin tener en cuenta el contexto
    temporal.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The point-wise recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    m = Pointwise_metrics(len(y_true),y_true,y_pred)
    m.set_confusion()
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_wise_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate point-wise precision for anomaly detection in time series.
    Esta métrica consiste en la precisión clásica, sin tener en cuenta el contexto
    temporal.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The point-wise precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    m = Pointwise_metrics(len(y_true),y_true,y_pred)
    m.set_confusion()
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_wise_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate point-wise F-score for anomaly detection in time series.
    Esta métrica consiste en la F-score clásica, sin tener en cuenta el contexto
    temporal.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        beta (float): 
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The point-wise F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_wise_precision(y_true, y_pred)
    recall = point_wise_recall(y_true, y_pred)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def point_adjusted_recall(y_true: np.array, y_pred: np.array):
    """
    This metric is based on the standard recall score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment,
    if at least one point within that segment is predicted as anomalous, all points in the segment 
    are marked as correctly detected. The adjusted predictions are then compared to the ground-truth 
    labels using the standard point-wise recall formulation.
 
    

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = PointAdjust(len(y_true),y_true,y_pred)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_adjusted_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate point-adjusted precision for anomaly detection in time series.
    This metric is based on the standard precision score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment,
    if at least one point within that segment is predicted as anomalous, all points in the segment 
    are marked as correctly detected. The adjusted predictions are then compared to the ground-truth 
    labels using the standard point-wise precision formulation.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = PointAdjust(len(y_true),y_true,y_pred)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_adjusted_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate point-adjusted F-score for anomaly detection in time series.
    This metric is based on the standard F-score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment,
    if at least one point within that segment is predicted as anomalous, all points in the segment 
    are marked as correctly detected. The adjusted predictions are then compared to the ground-truth 
    labels using the standard point-wise F-Score formulation.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_adjusted_precision(y_true, y_pred)
    recall = point_adjusted_recall(y_true, y_pred)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)



def delay_th_point_adjusted_recall(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate delay thresholded point-adjusted recall for anomaly detection in time series.
    This metric is based on the standard recall score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least one point within the first k time steps of the segment is predicted as anomalous, 
    all points in the segment are marked as correctly detected. The adjusted predictions are then 
    used to compute the standard point-wise recall formulation.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (int):
            Maximum number of time steps from the start of an anomaly segment within which a 
            prediction must occur for the segment to be considered detected.

    Returns:
        float: The delay thresholded point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = DelayThresholdedPointAdjust(len(y_true),y_true,y_pred,k=k)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def delay_th_point_adjusted_precision(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate delay thresholded point-adjusted precision for anomaly detection in time series.
    This metric is based on the standard precision score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least one point within the first k time steps of the segment is predicted as anomalous, 
    all points in the segment are marked as correctly detected. The adjusted predictions are then 
    used to compute the standard point-wise precision fromulation.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (int):
            Maximum number of time steps from the start of an anomaly segment
            within which a prediction must occur for the segment to be considered detected.

    Returns:
        float: The delay thresholded point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = DelayThresholdedPointAdjust(len(y_true),y_true,y_pred,k=k)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def delay_th_point_adjusted_f_score(y_true: np.array, y_pred: np.array, k: int, beta=1):
    """
    Calculate delay thresholded point-adjusted F-score for anomaly detection in time series.
    This metric is based on the standard F-score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least one point within the first k time steps of the segment is predicted as anomalous, 
    all points in the segment are marked as correctly detected. The adjusted predictions are then 
    used to compute the standard point-wise F-Score formulation.
    
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):  
            The predicted binary labels for the time series data.
        k (int):
            Maximum number of time steps from the start of an anomaly segment within which a prediction must occur for the segment to be considered detected.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The delay thresholded point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = delay_th_point_adjusted_precision(y_true, y_pred, k)
    recall = delay_th_point_adjusted_recall(y_true, y_pred, k)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def point_adjusted_at_k_recall(y_true: np.array, y_pred: np.array, k: float):
    """
    Calculate k percent point-adjusted at K% recall for anomaly detection in time series.
    This metric is based on the standard recall score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least K% of the points within that segment are predicted as anomalous, all points in 
    the segment are marked as correctly detected. The adjusted predictions are then used 
    to compute the standard point-wise recall.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (float):
            The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.

    Returns:
        float: The point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    m = PointAdjustKPercent(len(y_true),y_true,y_pred,k=k)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_adjusted_at_k_precision(y_true: np.array, y_pred: np.array, k: float):
    """
    Calculate point-adjusted at K% precision for anomaly detection in time series.
    This metric is based on the standard precision score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least K% of the points within that segment are predicted as anomalous, all points in 
    the segment are marked as correctly detected. The adjusted predictions are then used 
    to compute the standard point-wise precision.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (float):
            The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.

    Returns:
        float: The point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    m = PointAdjustKPercent(len(y_true),y_true,y_pred,k=k)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_adjusted_at_k_f_score(y_true: np.array, y_pred: np.array, k: float, beta=1):
    """
    Calculate point-adjusted at K% F-score for anomaly detection in time series.
    This metric is based on the standard F-Score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    if at least K% of the points within that segment are predicted as anomalous, all points in 
    the segment are marked as correctly detected. The adjusted predictions are then used 
    to compute the standard F-Score precision.

    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (float):
            The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_adjusted_at_k_precision(y_true, y_pred, k)
    recall = point_adjusted_at_k_recall(y_true, y_pred, k)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def latency_sparsity_aw_recall(y_true: np.array, y_pred: np.array, ni: int):
    """
    Calculate latency and sparsity aware recall for anomaly detection in time series.
    This metric is based on the standard recall, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    all points in the segment are marked as correctly detected only after the first true positive 
    is predicted within that segment. This encourages early detection by delaying credit for correct 
    predictions until the anomaly is initially detected. Additionally, to reduce the impact of 
    scattered false positives, predictions are subsampled using a sparsity factor n, so that 
    only one prediction is considered every n time steps. The adjusted predictions are then used 
    to compute the standard point-wise recall.

    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        ni (int):
            The batch size used in the implementation to handle latency and sparsity.

    Returns:
        float: The latency and sparsity aware recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = LatencySparsityAware(len(y_true),y_true,y_pred,tw=ni)
    TP,FN = m.tp, m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def latency_sparsity_aw_precision(y_true: np.array, y_pred: np.array, ni: int):
    """
    Calculate latency and sparsity aware precision for anomaly detection in time series.
    This metric is based on the standard precision, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    all points in the segment are marked as correctly detected only after the first true positive 
    is predicted within that segment. This encourages early detection by delaying credit for correct 
    predictions until the anomaly is initially detected. Additionally, to reduce the impact of 
    scattered false positives, predictions are subsampled using a sparsity factor n, so that 
    only one prediction is considered every n time steps. The adjusted predictions are then used 
    to compute the standard point-wise precision.

    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        ni (int):
            The batch size used in the implementation to handle latency and sparsity.

    Returns:
        float: The latency and sparsity aware precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = LatencySparsityAware(len(y_true),y_true,y_pred,tw=ni)
    TP,FP = m.tp, m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def latency_sparsity_aw_f_score(y_true: np.array, y_pred: np.array, ni: int, beta=1):
    """
    Calculate latency and sparsity aware F-score for anomaly detection in time series.
    This metric is based on the standard F-score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, for each ground-truth anomalous segment, 
    all points in the segment are marked as correctly detected only after the first true positive 
    is predicted within that segment. This encourages early detection by delaying credit for correct 
    predictions until the anomaly is initially detected. Additionally, to reduce the impact of 
    scattered false positives, predictions are subsampled using a sparsity factor n, so that 
    only one prediction is considered every n time steps. The adjusted predictions are then used 
    to compute the standard point-wise F-score.

    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        ni (int):
            The batch size used in the implementation to handle latency and sparsity.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The latency and sparsity aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0

    recall = latency_sparsity_aw_recall(y_true,y_pred,ni)
    precision = latency_sparsity_aw_precision(y_true,y_pred,ni)
    if precision == 0 or recall == 0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

    
def segment_wise_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate segment-wise recall for anomaly detection in time series.
    This metric is based on the standard recall, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, each contiguous segment of anomalous points 
    is treated as a single unit. A true positive is counted if at least one point in a ground-truth 
    anomalous segment is predicted as anomalous. A false negative is counted if no point in the segment 
    is detected, and a false positive is recorded for each predicted anomalous segment that does not 
    overlap with any ground-truth anomaly. The final recall is computed using these adjusted 
    segment-level counts.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The segment-wise recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def segment_wise_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate segment-wise precision for anomaly detection in time series.
    This metric is based on the standard precision, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, each contiguous segment of anomalous points 
    is treated as a single unit. A true positive is counted if at least one point in a ground-truth 
    anomalous segment is predicted as anomalous. A false negative is counted if no point in the segment 
    is detected, and a false positive is recorded for each predicted anomalous segment that does not 
    overlap with any ground-truth anomaly. The final precision is computed using these adjusted 
    segment-level counts.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The segment-wise precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def segment_wise_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate segment-wise F-score for anomaly detection in time series.
    This metric is based on the standard F-score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, each contiguous segment of anomalous points 
    is treated as a single unit. A true positive is counted if at least one point in a ground-truth 
    anomalous segment is predicted as anomalous. A false negative is counted if no point in the segment 
    is detected, and a false positive is recorded for each predicted anomalous segment that does not 
    overlap with any ground-truth anomaly. The final F-score is computed using these adjusted 
    segment-level counts.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The segment-wise F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FN,FP = m.tp,m.fn,m.fp
    if TP==0:
        return 0
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    
    if precision == 0 or recall == 0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

def composite_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate composite F-score for anomaly detection in time series.
    This metric combines aspects of the point_wise_f_score and the segment_wise_f_score. 
    It is defined as the harmonic mean of point_wise_precision and segment_wise_recall. 
    The use of point-wise precision ensures that false positives are properly penalized, 
    a feature that segment-wise metrics typically lack.

    Implementation of https://ieeexplore.ieee.org/document/9525836

    Parameters:
        y_true (np.array): 
            The ground truth binary labels for the time series data.
        y_pred (np.array): 
            The predicted binary labels for the time series data.
        beta (float): 
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The composite F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    m = Composite_f(len(y_true),y_true,y_pred)
    #Point wise precision
    precision =  m.precision()

    #Segment wise recall
    recall = m.recall()

    if precision==0 or recall==0:
        return 0

    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

def time_tolerant_recall(y_true: np.array, y_pred: np.array, t: int) -> float:
    """
    Calculate time tolerant recall for anomaly detection in time series.
    This metric is based on the standard recall, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, a predicted anomalous point is considered 
    a true positive if it lies within a temporal window of size :math:`{\\tau}` around any ground-truth anomalous point. 
    This allows for small temporal deviations in the predictions to be tolerated. The adjusted predictions are then used 
    to compute the standard point-wise recall.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        t (int):
            The time tolerance parameter

    Returns:
        float: The time tolerant recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    
    m = Time_Tolerant(len(y_true),y_true,y_pred,d=t)
    return m.recall()

def time_tolerant_precision(y_true: np.array, y_pred: np.array, t: int) -> float:
    """
    Calculate time tolerant precision for anomaly detection in time series.
    This metric is based on the standard precision, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, a predicted anomalous point is considered 
    a true positive if it lies within a temporal window of size :math:`{\\tau}` around any ground-truth anomalous point. 
    This allows for small temporal deviations in the predictions to be tolerated. The adjusted predictions are then used 
    to compute the standard point-wise precision.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        t (int):
            The time tolerance parameter

    Returns:
        float: The time tolerant precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Time_Tolerant(len(y_true),y_true,y_pred, d=t)
    return m.precision()


def time_tolerant_f_score(y_true: np.array, y_pred: np.array, t: int, beta=1):
    """
    Calculate time tolerant F-score for anomaly detection in time series.
    This metric is based on the standard F-score, but applies a temporal adjustment 
    to the predictions before computing it. Specifically, a predicted anomalous point is considered 
    a true positive if it lies within a temporal window of size :math:`{\\tau}` around any ground-truth anomalous point. 
    This allows for small temporal deviations in the predictions to be tolerated.The adjusted predictions are then used 
    to compute the standard point-wise F-Score.

    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        t (int):
            The time tolerance parameter
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.
    
    Returns:
        float: The time tolerant F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    precision = time_tolerant_precision(y_true,y_pred,t)
    recall = time_tolerant_recall(y_true,y_pred,t)
    if precision==0 or recall==0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def range_based_recall(y_true: np.array, y_pred: np.array, alpha: float, bias='flat', cardinality_mode='one'):
    """
    Calculate range-based recall for anomaly detection in time series.

    This metric extends standard recall by evaluating detection at the level of anomalous ranges 
    rather than individual points.  For each true anomaly range, it computes a score that rewards 
    (1) detecting the existence of the range, (2) the proportion of overlap, and (3) penalties or 
    bonuses based on the position and fragmentation of predicted segments.  These components are 
    weighted by :math:`{\\alpha}` (existence vs. overlap) and further shaped by customizable bias functions 
    for positional and cardinality factors.

    For more information, see the original paper:
    https://proceedings.neurips.cc/paper_files/paper/2018/file/8f468c873a32bb0619eaeb2050ba45d1-Paper.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        alpha (float):
            Relative importance of existence reward. 0 \\leq alpha \\leq 1.
        bias (str):
            Positional bias. This should be "flat", "front", "middle", or "back".
        cardinality_mode (str, optional):
            Cardinality type. This should be "one", "reciprocal" or "udf_gamma".
    
    Returns:
        float: The range-based recall score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Range_PR(len(y_true),y_true,y_pred,cardinality=cardinality_mode, alpha=alpha,bias=bias)
    return m.recall()



def range_based_precision(y_true: np.array, y_pred: np.array, alpha: float, bias='flat', cardinality_mode='one'):
    """
    Calculate range-based precision for anomaly detection in time series.

    This metric extends standard precision by scoring predictions at the range level.  Each 
    predicted anomaly range is evaluated for (1) overlap with any true ranges, (2) the size of 
    that overlap, and (3) positional and fragmentation effects via bias functions.  Cardinality 
    penalties can be applied when a single true range is covered by multiple predicted ranges.
    These components are weighted by :math:`{\\alpha}` (existence vs. overlap) and further shaped by customizable bias functions 
    for positional and cardinality factors.

    For more information, see the original paper:
    https://proceedings.neurips.cc/paper_files/paper/2018/file/8f468c873a32bb0619eaeb2050ba45d1-Paper.pdf
    
    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        alpha (float):
            Relative importance of existence reward. 0 \\leq alpha \\leq 1.
        bias (str):
            Positional bias. This should be "flat", "front", "middle", or "back".
        cardinality_mode (str, optional):
            Cardinality type. This should be "one", "reciprocal" or "udf_gamma".
    
    Returns:
        float: The range-based precision score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Range_PR(len(y_true),y_true,y_pred,cardinality=cardinality_mode, alpha=alpha,bias=bias)
    return m.precision()
    
    
    



def range_based_f_score(y_true: np.array, y_pred: np.array, p_alpha: float, r_alpha: float,  p_bias='flat', r_bias='flat', cardinality_mode='one', beta=1) -> float:
    """
    Calculate range-based F-score for anomaly detection in time series.

    This metric combines range-based precision and range-based recall into a single harmonic mean.  
    It inherits all customizability of the underlying precision and recall—existence vs. overlap 
    weighting, positional bias, and cardinality factors—allowing fine-grained control over how 
    both missed detections and false alarms are penalized in a temporal context.

    For more information, see the original paper:
    https://proceedings.neurips.cc/paper_files/paper/2018/file/8f468c873a32bb0619eaeb2050ba45d1-Paper.pdf
    

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        p_alpha (float):
            Relative importance of existence reward for precision. 0 \\leq alpha \\leq 1.
        r_alpha (float):
            Relative importance of existence reward for recall. 0 \\leq alpha \\leq 1.
        p_bias (str):
            Positional bias for precision. This should be "flat", "front", "middle", or "back".
        r_bias (str):
            Positional bias for recall. This should be "flat", "front", "middle", or "back".
        cardinality_mode (str, optional):
            Cardinality type. This should be "one", "reciprocal" or "udf_gamma".
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.

    Returns:
        float: The range-based F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    f = ts_fscore(y_true, y_pred, beta=beta, p_alpha=p_alpha, r_alpha=r_alpha, cardinality=cardinality_mode, p_bias=p_bias, r_bias=r_bias)
    return f




def ts_aware_recall(y_true: np.array, y_pred: np.array, alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware recall for anomaly detection in time series.
    
    This metric is based on the range_based_recall, but introduces two key modifications.  
    First, a predicted anomalous segment is only counted as a true positive if it covers at least a fraction 
    :math:`{\\theta}` of the ground‑truth anomaly range. Second, each labeled anomaly is extended by a tolerance window of 
    length :math:`{\\delta}` at its end, within which any overlap contribution decays linearly from full weight down to zero.  
    Unlike the original range-based formulation, this variant omits cardinality and positional bias terms, 
    focusing solely on overlap fraction and end‑tolerance decay.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        alpha (float):
            Relative importance of the existence reward versus overlap reward (0 \\leq :math:`{\\alpha}` \\leq 1).
        delta (float):
            Tolerance window length at the end of each true anomaly segment.
                - If past_range is True, :math:`{\\delta}` must be a float in (0, 1], representing the fraction of the segment’s 
                    length to extend. E.g., :math:`{\\delta}` = 0.5 extends a segment of length 10 by 5 time steps.
                - If past_range is False, :math:`{\\delta}` must be a non-negative integer, representing an absolute number of 
                    time steps to extend each segment.
        theta (float):
            Minimum fraction (0 \\leq :math:`{\\theta}` \\leq 1) of the true anomaly range that must be overlapped by 
            predictions for the segment to count as detected.
        past_range (bool):
            Determines how :math:`{\\delta}` is interpreted.
                - True: :math:`{\\delta}` is treated as a fractional extension of each segment’s length.
                - False: :math:`{\\delta}` is treated as an absolute number of time steps.
    
    Returns:
        float: The time series aware recall score.
    """
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    return m.recall()




def ts_aware_precision(y_true: np.array, y_pred: np.array,alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware precision for anomaly detection in time series.

    This metric is based on the range_based_precision, but introduces two key modifications.  
    First, a predicted anomalous segment is only counted as a true positive if it covers at least a fraction 
    :math:`{\\theta}` of the ground‑truth anomaly range. Second, each labeled anomaly is extended by a tolerance window of 
    length :math:`{\\delta}` at its end, within which any overlap contribution decays linearly from full weight down to zero.  
    Unlike the original range-based formulation, this variant omits cardinality and positional bias terms, 
    focusing solely on overlap fraction and end‑tolerance decay.
    
    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        alpha (float):
            Relative importance of the existence reward versus overlap reward (0 \\leq :math:`{\\alpha}` \\leq 1).
        delta (float):
            Tolerance window length at the end of each true anomaly segment.
                - If past_range is True, :math:`{\\delta}` must be a float in (0, 1], representing the fraction of the segment’s 
                    length to extend. E.g., :math:`{\\delta}` = 0.5 extends a segment of length 10 by 5 time steps.
                - If past_range is False, :math:`{\\delta}` must be a non-negative integer, representing an absolute number of 
                    time steps to extend each segment.
        theta (float):
            Minimum fraction (0 \\leq :math:`{\\theta}` \\leq 1) of the true anomaly range that must be overlapped by 
            predictions for the segment to count as detected.
        past_range (bool):
            Determines how :math:`{\\delta}` is interpreted.
                - True: :math:`{\\delta}` is treated as a fractional extension of each segment’s length.
                - False: :math:`{\\delta}` is treated as an absolute number of time steps.
    
    Returns:
        float: The time series aware precision score.
    """
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    return m.precision()

    



def ts_aware_f_score(y_true: np.array, y_pred: np.array, beta: float, alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware F-score for anomaly detection in time series.

    This metric is based on the range_based_f_score, but introduces two key modifications.  
    First, a predicted anomalous segment is only counted as a true positive if it covers at least a fraction 
    :math:`{\\theta}` of the ground‑truth anomaly range. Second, each labeled anomaly is extended by a tolerance window of 
    length :math:`{\\delta}` at its end, within which any overlap contribution decays linearly from full weight down to zero.  
    Unlike the original range-based formulation, this variant omits cardinality and positional bias terms, 
    focusing solely on overlap fraction and end‑tolerance decay.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.
            Default is 1, which gives equal weight to precision and recall.
        alpha (float):
            Relative importance of the existence reward versus overlap reward (0 \\leq :math:`{\\alpha}` \\leq 1).
        delta (float):
            Tolerance window length at the end of each true anomaly segment.
                - If past_range is True, :math:`{\\delta}` must be a float in (0, 1], representing the fraction of the segment’s 
                    length to extend. E.g., :math:`{\\delta}` = 0.5 extends a segment of length 10 by 5 time steps.
                - If past_range is False, :math:`{\\delta}` must be a non-negative integer, representing an absolute number of 
                    time steps to extend each segment.
        theta (float):
            Minimum fraction (0 \\leq :math:`{\\theta}` \\leq 1) of the true anomaly range that must be overlapped by 
            predictions for the segment to count as detected.
        past_range (bool):
            Determines how :math:`{\\delta}` is interpreted.
                - True: :math:`{\\delta}` is treated as a fractional extension of each segment’s length.
                - False: :math:`{\\delta}` is treated as an absolute number of time steps.

    Returns:
        float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    precision = m.precision()
    recall = m.recall()
    if precision==0 or recall==0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)





def enhanced_ts_aware_recall(y_true: np.array, y_pred: np.array, theta: float):
    """
    Calculate enhanced time series aware recall for anomaly detection in time series.
    
    This metric is similar to the range-based recall in that it accounts for both detection existence 
    and overlap proportion. Additionally, it requires that a significant fraction :math:`{\\theta}` of each true anomaly 
    segment be detected.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        theta (float):
            Minimum fraction (0 \\leq :math:`{\\theta}` \\leq 1) of a true segment that must be overlapped 
            by predictions to count as detected.
    
    Returns:
        float: The time series aware recall score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta)
    return m.recall()




def enhanced_ts_aware_precision(y_true: np.array, y_pred: np.array, theta: float):
    """
    Calculate enhanced time series aware precision for anomaly detection in time series.
    
    This metric is similar to the range-based precision. Additionally, it requires that a significant fraction :math:`{\\theta}` 
    of each predicted segment overlaps with the ground truth. Finally, precision contributions from each event are weighted by 
    the square root of the true segment’s length, providing a compromise between point-wise and segment-wise approaches.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        theta (float):
            Minimum fraction (0 \\leq :math:`{\\theta}` \\leq 1) of a predicted segment that must be overlapped 
            by ground truth to count as detected.
    
    Returns:
        float: The time series aware precision score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta)
    return m.precision()

    



def enhanced_ts_aware_f_score(y_true: np.array, y_pred: np.array, theta_p: float, theta_r: float):
    """
    Calculate enhanced time series aware F-score for anomaly detection in time series.
    
    This metric is similar to the range-based F-score in that it accounts for both detection existence 
    and overlap proportion. Additionally, it requires that a significant fraction :math:`{\\theta_r}` of each true anomaly 
    segment be detected, and that a significant fraction :math:`{\\theta_p}` of each predicted segment overlaps with the 
    ground truth. Finally, F-score contributions from each event are weighted by the square root of the 
    true segment’s length, providing a compromise between point-wise and segment-wise approaches.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        theta_p (float):
            Minimum fraction (0 \\leq :math:`{\\theta_p}` \\leq 1) of a predicted segment that must be overlapped 
            by ground truth to count as detected.
        theta_r (float):
            Minimum fraction (0 \\leq :math:`{\\theta_r}` \\leq 1) of a true segment that must be overlapped 
            by predictions to count as detected.

    Returns:
        float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta_p, theta_r=theta_r)
    return m.result['f1']



def affiliation_based_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate affiliation based recall for anomaly detection in time series.

    This metric evaluates how well each labeled anomaly is affiliated with predicted points.
    It computes the average distance from each ground truth anomaly point to the nearest 
    predicted anomaly point.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    Returns:
        float: The affiliation based recall score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    s = m.get_score()
    return m.r


def affiliation_based_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate affiliation based F-score for anomaly detection in time series.

    This metric evaluates how well each predicted anomaly is affiliated with labeled points.
    It computes the average distance from each predicted anomaly point to the nearest 
    ground truth anomaly point.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.


    Returns:
        float: The affiliation based precision score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    s = m.get_score()
    return m.p


def affiliation_based_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate affiliation based F-score for anomaly detection in time series.

    This metric combines the affiliation-based precision and recall into a single score 
    using the harmonic mean, adjusted by a weight :math:`{\\beta}` to control the relative importance 
    of recall versus precision. Since both precision and recall are distance-based, 
    the F-score reflects a balance between how well predicted anomalies align with true 
    anomalies and vice versa.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        beta (float):
            The beta value, which determines the weight of precision in the combined score.


    Returns:
        float: The affiliation based F-score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    return m.get_score(beta)


def nab_score(y_true: np.array, y_pred: np.array):
    """
    Calculate NAB score for anomaly detection in time series.

    This metric rewards early and accurate detections of anomalies while penalizing false positives. 
    For each ground truth anomaly segment, only the first correctly predicted anomaly point contributes 
    positively to the score, with earlier detections receiving higher rewards. In contrast, every false 
    positive prediction contributes negatively.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.


    Returns:
        float: The nab score.
    """
    
    m = NAB_score(len(y_true),y_true,y_pred)
    return m.get_score()

def temporal_distance(y_true: np.array, y_pred: np.array, distance: int = 0):
    """
    Calculate temporal distane for anomaly detection in time series.

    This metric computes the sum of the distances from each labelled anomaly point to
    the closest predicted anomaly point, and from each predicted anomaly point to the
    closest labelled anomaly point. 


    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        distance (int):
            The distance type parameter for the temporal distance calculation.
                0: Euclidean distance
                1: Squared Euclidean distance


    Returns:
        float: The temporal distance.
    """
    
    m = Temporal_Distance(len(y_true),y_true,y_pred,distance=distance)
    return m.get_score()

def average_detection_count(y_true: np.array, y_pred: np.array):
    """
    Calculate average detection count for anomaly detection in time series.

    This metric computes, for each ground-truth anomalous segment, the percentage of points within that segment 
    that are predicted as anomalous. It then averages these percentages across all true anomaly events, 
    providing an estimate of detection coverage per event.

    For more information, see the original paper:
    https://ceur-ws.org/Vol-1226/paper31.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.


    Returns:
        float: The average detection count score.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    azs = b.get_gt_anomalies_segmentwise()
    a_points = b.get_predicted_anomalies_ptwise()

    counts = []
    for az in azs:
        count = 0
        for ap in a_points:
            if ap >= az[0] and ap <= az[1]:
                count+=1
        counts.append(count/(az[1] - az[0] + 1))  # Normalize by segment length
    
    return np.mean(counts)

def absolute_detection_distance(y_true: np.array, y_pred: np.array):
    """
    Calculate absolute detection distance for anomaly detection in time series.

    This metric computes, for each predicted anomaly point that overlaps a ground-truth anomaly segment, 
    the relative distance from that point to the temporal center of the corresponding segment. It then sums all 
    those distances and divides by the total number of such matching predicted points, yielding the 
    mean distance to segment centers for correctly detected points.

    For more information, see the original paper:
    https://ceur-ws.org/Vol-1226/paper31.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.


    Returns:
        float: The absolute detection distance.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    azs = b.get_gt_anomalies_segmentwise()
    a_points = b.get_predicted_anomalies_ptwise()
    if len(a_points) == 0:
        return float('inf')
    distance = 0
    for az in azs:
        for ap in a_points:
            if ap >= az[0] and ap <= az[1]:
                center = int((az[0] + az[1]) / 2)
                distance+=abs(ap - center)/max(1,int((az[0] + az[1]) / 2))
    
    return distance/len(a_points)


def total_detected_in_range(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate total detected in range for anomaly detection in time series.

    This metric measures the proportion of true anomaly events that are correctly detected.
    It is defined as:

    .. math::
        \\text{TDIR} = \\frac{EM + DA}{EM + DA + MA}

    Where:

    - EM (Exact Match):
        Number of predicted anomaly segments that exactly match a true anomaly segment.
    - DA (Detected Anomaly):
        Number of true anomaly points not exactly matched where at least one prediction falls
        within a window [i-k, i+k] around the true point index i or within the true segment range.
    - MA (Missed Anomaly):
        Number of true anomaly segments that do not overlap any predicted anomaly segment
        even within a k-step tolerance window around true points.

    For more information, see the original paper:
    https://acta.sapientia.ro/content/docs/evaluation-metrics-for-anomaly-detection.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (int):
            Half-window size for tolerance around each true anomaly point. A prediction within k
            time steps of a true point counts toward detection.

    Returns:
        float: The total detected in range score.
    """
    if np.sum(y_pred) == 0:
        return 0
    em,da,ma,_ = counting_method(y_true, y_pred, k)

    
    return (em + da)/(em + da + ma)


def detection_accuracy_in_range(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate detection accuracy in range for anomaly detection in time series.

    This metric measures the proportion of predicted anomaly events that correspond to true anomalies.
    It is defined as:

    .. math::
        \\text{DAIR} = \\frac{EM + DA}{EM + DA + FA}

    Where:

    - EM (Exact Match):
        Number of predicted anomaly segments that exactly match a true anomaly segment.
    - DA (Detected Anomaly):
        Number of true anomaly points not exactly matched where at least one prediction falls
        within a window [i-k, i+k] around the true point index i or within the true segment range.
    - FA (False Anomaly):
        Number of predicted anomaly segments that do not overlap any true anomaly segment
        even within a k-step tolerance window around true points.

    For more information, see the original paper:
    https://acta.sapientia.ro/content/docs/evaluation-metrics-for-anomaly-detection.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (int):
            Half-window size for tolerance around each true anomaly point. A prediction within k
            time steps of a true point counts toward detection.

    Returns:
        float: The detection accuracy in range score.
    """
    if np.sum(y_pred) == 0:
        return 0
    em,da,_,fa = counting_method(y_true, y_pred, k)

    
    return (em + da)/(em + da + fa)


def weighted_detection_difference(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate weighted detection difference for anomaly detection in time series.

    For each true anomaly segment, each point in the segment is assigned a weight based on a
    Gaussian function centered at the segment’s midpoint: points closer to the center receive higher
    weights, which decay with distance according to the standard deviation sigma. These weights form
    the basis for scoring both correct detections and false alarms.

    WS (Weighted Sum) is defined as the sum of Gaussian weights for all predicted anomaly points that
    fall within any true anomaly segment (extended by delta time steps at the ends).
    WF (False Alarm Weight) is the sum of Gaussian weights for all predicted anomaly points that do
    not overlap any true anomaly segment (within the same extension).

    The final score is:

        .. math::
            \\text{WDD} = \\text{WS} - \\text{WF} \\cdot \\text{FA}

    Where:

    - WS: 
        Sum of Gaussian weights for all predicted anomaly points that fall 
        within any true anomaly segment (extended by delta time steps at the ends).
    - WF:
        Sum of Gaussian weights for all predicted anomaly points that do not 
        overlap any true anomaly segment (within the same extension).
    - FA (False Anomaly):
        Number of predicted anomaly segments that do not overlap any true anomaly segment
        even within a k-step tolerance window around true points.

    For more information, see the original paper:
    https://acta.sapientia.ro/content/docs/evaluation-metrics-for-anomaly-detection.pdf

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        k (int):
            The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
        float: The weighted detection difference.
    """
    if np.sum(y_pred) == 0:
        return 0
    
    def gaussian(dt,tmax):
        if dt < tmax:
            return 1- dt/tmax
        else:
            return -1

    tmax = len(y_true)
    
    ones_indices = np.where(y_true == 1)[0]
    
    y_modified = y_true.astype(float).copy()
    
    for i in range(len(y_true)):
        if y_true[i] == 0:
            dt = np.min(np.abs(ones_indices - i)) if len(ones_indices) > 0 else tmax
            y_modified[i] = gaussian(dt, tmax)
    
    ws = 0
    wf = 0
    for i in range(len(y_pred)):
        if y_pred[i] != 1:
            ws+=y_modified[i]
        else:
            wf+=y_modified[i]

    _,_,_,fa = counting_method(y_true, y_pred, k)

    
    return ws - wf*fa


def binary_pate(y_true: np.array, y_pred: np.array, early: int, delay: int):
    """
    Calculate PATE score for anomaly detection in time series.
    
    PATE evaluates predictions by assigning weighted scores based on temporal proximity 
    to true anomaly intervals. It uses buffer zones around each true anomaly: an early buffer of length
    `early` preceding the interval and a delay buffer of length `delay` following it. Detections within
    the true interval receive full weight, while those in the early or delay buffers receive linearly
    decaying weights based on distance from the interval edges. Predictions outside these zones are
    treated as false positives, and missed intervals as false negatives. The final score balances these
    weighted detections into a single measure of performance.

    For more information, see the original paper:
    https://arxiv.org/abs/2405.12096

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.
        early (int):
            The maximum number of time steps before an anomaly must be predicted to be considered early.
        delay (int):
            The maximum number of time steps after an anomaly must be predicted to be considered delayed.

    Returns:
        float: The PATE score.
    """
    
    return PATE(y_true, y_pred, early, delay, binary_scores=True)

def mean_time_to_detect(y_true: np.array, y_pred: np.array):
    """
    Calculate mean time to detect for anomaly detection in time series.
    
    This metric quantifies the average detection delay across all true anomaly events.  
    For each ground-truth anomaly segment, let i be the index where the segment starts, 
    and let :math:`{j \geq i}` be the first index within that segment where the model predicts an anomaly.  
    The detection delay for that event is defined as:

    .. math::
        \Delta t = j - i

    The MTTD is the mean of all such :math:`{\Delta t}` values, one per true anomaly segment, and expresses 
    the average number of time steps between the true onset of an anomaly and its first detection.

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_pred (np.array):
            The predicted binary labels for the time series data.

    For more information, see the original paper:
    https://arxiv.org/pdf/2211.05244

    Returns:
        float: The mean time to detect.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    a_events = b.get_gt_anomalies_segmentwise()
    t_sum = 0
    for a,_ in a_events:
        for i in range(a,len(y_pred)):
            if y_pred[i] == 1:
                t_sum+=i-a
                break
    
    return t_sum/len(a_events)
