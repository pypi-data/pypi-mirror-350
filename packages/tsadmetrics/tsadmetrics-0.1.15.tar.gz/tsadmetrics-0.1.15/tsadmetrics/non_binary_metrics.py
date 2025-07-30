import numpy as np
from ._tsadeval.metrics import *
from sklearn.metrics import auc
from pate.PATE_metric import PATE
def precision_at_k(y_true : np.array, y_anomaly_scores:  np.array):
    """
    Calculate the precision at k score for anomaly detection in time series.

    This metric evaluates how many of the top-k points (with highest anomaly scores)
    actually correspond to true anomalies. It is particularly useful when we are 
    interested in identifying the most anomalous points, without needing to set a 
    fixed threshold.

    The value of k is automatically set to the number of true anomalies present in 
    y_true. That is, k = sum(y_true).

    Parameters:
        y_true (np.array):
            The ground truth binary labels for the time series data.
        y_anomaly_scores (np.array):
            The predicted anomaly scores for the time series data.

    Returns:
        float: The precision at k score.
    """
    m = PatK_pw(y_true,y_anomaly_scores)

    return m.get_score()

def auc_roc_pw(y_true : np.array, y_anomaly_scores:  np.array):
    """
    Calculate the AUC-ROC score for anomaly detection in time series.

    This is the standard Area Under the Receiver Operating Characteristic Curve (AUC-ROC),
    computed in a point-wise manner. That is, each point in the time series is treated
    independently when calculating true positives, false positives, and false negatives.

    Parameters:
        y_true (np.array):
            Ground-truth binary labels for the time series (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Continuous anomaly scores assigned to each point in the series.

    Returns:
        float: AUC-ROC score.
    """
    
    m = AUC_ROC(y_true,y_anomaly_scores)

    return m.get_score()


def auc_pr_pw(y_true : np.array ,y_anomaly_scores:  np.array):
    """
    Calculate the AUC-PR score for anomaly detection in time series.

    This is the standard Area Under the Precision-Recall Curve (AUC-PR),
    computed in a point-wise manner. That is, each point in the time series is treated
    independently when calculating precision and recall.

    Parameters:
        y_true (np.array):
            Ground-truth binary labels for the time series (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Continuous anomaly scores assigned to each point in the series.

    Returns:
        float: AUC-PR score.
    """
    m = AUC_PR_pw(y_true,y_anomaly_scores)

    return m.get_score()



def auc_pr_pa(y_true: np.array, y_anomaly_scores: np.array):
    """
    Calculate the AUC-PR score using point-adjusted evaluation for anomaly detection in time series.

    This is the standard Area Under the Precision-Recall Curve (AUC-PR), but instead of computing 
    precision and recall point-wise, it uses a point-adjusted approach. Specifically, for each 
    ground-truth anomalous segment, if at least one point within that segment is predicted as anomalous, 
    the entire segment is considered correctly detected. The adjusted predictions are then compared 
    to the ground-truth labels to compute true positives, false positives, and false negatives,
    which are used to construct the PR curve.

    Parameters:
        y_true (np.array):
            Ground-truth binary labels for the time series (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Continuous anomaly scores assigned to each point in the series.

    Returns:
        float: AUC-PR score (with point-adjusted evaluation).
    """
        
    
    precisions = [1]
    recalls = [0]
    tps,fps,fns = [],[],[]

    p_adj = PointAdjust(len(y_true),y_true,(np.array(y_anomaly_scores) >= 0.5).astype(int))
    segments= p_adj.get_gt_anomalies_segmentwise()
    idx = np.argsort(y_anomaly_scores)[::-1].astype(int)
    y_true_sorted = np.array(y_true)[idx]
    y_anomaly_scores_sorted = np.array(y_anomaly_scores)[idx]
    
    segment_mins = []
    for start,end in segments:
        anoms_scores = y_anomaly_scores[start:end+1]
        segment_mins.append([np.max(anoms_scores),end-start+1])

    for i_t in range(len(y_anomaly_scores_sorted)):
        fp,tp,fn = 0,0,0
        if i_t > 0 and y_anomaly_scores_sorted[i_t] == y_anomaly_scores_sorted[i_t-1] :
            tp = tps[-1]
            fp = fps[-1]
            fn = fns[-1]
        else:
            if y_true_sorted[i_t] == 0:
                #FP
                if len(fps)==0:
                    aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int)
                    for i in range(len(aux_y_pred)):
                        if aux_y_pred[i] == 1 and y_true[i] == 0:
                            fp+=1


                else:
                    fp=fps[i_t-1]+1
            else:
                if len(fps)==0:
                    aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int)
                    for i in range(len(aux_y_pred)):
                        if aux_y_pred[i] == 1 and y_true[i] == 0:
                            fp+=1
                else:
                    fp=fps[i_t-1]
            for score, length in segment_mins:
                if score >= y_anomaly_scores_sorted[i_t]:
                    #TP
                    tp+= length
                else:
                    #FN
                    fn+= length
        tps.append(tp)
        fns.append(fn)
        fps.append(fp)
    for tp,fp,fn in zip(tps,fps,fns):
        if tp>0:
            precisions.append(tp/(tp+fp))
            recalls.append(tp/(tp+fn))
        else:
            precisions.append(0)
            recalls.append(0)    
      
    
    recalls.append(1)
    precisions.append(0)

    auc_value = auc(recalls, precisions)
    return auc_value




def auc_pr_sw(y_true: np.array, y_anomaly_scores: np.array):
    """
    Calculate the AUC-PR score using segment-wise evaluation for anomaly detection in time series.

    This is the standard Area Under the Precision-Recall Curve (AUC-PR), but it uses a segment-wise 
    adjustment when computing precision and recall. In this evaluation, each contiguous segment of 
    anomalous ground-truth points is treated as a single unit. A true positive is counted if at least 
    one predicted anomaly overlaps with the segment. A false negative occurs when a segment is 
    completely missed, and a false positive is recorded for each predicted anomalous segment 
    that does not overlap with any ground-truth anomaly. These adjusted counts are then used 
    to compute precision and recall for constructing the PR curve.

    Parameters:
        y_true (np.array):
            Ground-truth binary labels for the time series (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Continuous anomaly scores assigned to each point in the series.

    Returns:
        float: AUC-PR score (with segment-wise evaluation).
    """

    precisions = [1]
    recalls = [0]
    tps,fps,fns = [],[],[]


    segments = []
    i=0
    while i < len(y_true):
        if y_true[i] == 1:
            start = i
            end = i
            while i < len(y_true) and y_true[i] == 1:
                end = i
                i += 1
            segments.append([start,end])
        i+=1
    idx = np.argsort(y_anomaly_scores)[::-1].astype(int)
    y_anomaly_scores_sorted = np.array(y_anomaly_scores)[idx]
    
    segment_mins = []
    for start,end in segments:
        anoms_scores = y_anomaly_scores[start:end+1]
        segment_mins.append([np.max(anoms_scores),[start,end]])

    for i_t in range(len(y_anomaly_scores_sorted)):
        fp,tp,fn = 0,0,0
        
            
        aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int) 
        for score,seg in segment_mins:
            start,end = seg
            if score >= y_anomaly_scores_sorted[i_t]:
                #TP
                tp+= 1
                if aux_y_pred[start]== 1:
                    # Extender hacia la izquierda
                    i = start - 1
                    while i >= 0 and aux_y_pred[i] == 1:
                        aux_y_pred[i] = 0
                        i -= 1
                
                if aux_y_pred[end] == 1:
                    # Extender hacia la derecha
                    i = end + 1
                    while i < len(aux_y_pred) and aux_y_pred[i] == 1:
                        aux_y_pred[i] = 0
                        i += 1
                aux_y_pred[start:end+1] = 0

            else:
                #FN
                fn+= 1
        
        if np.sum(aux_y_pred)>0:
            fpsegments = []
            i=0
            while i < len(aux_y_pred):
                if aux_y_pred[i] == 1:
                    start = i
                    end = i
                    while i < len(aux_y_pred) and aux_y_pred[i] == 1:
                        end = i
                        i += 1
                    fpsegments.append([start,end])
                i+=1
            fp = len(fpsegments)
        else:
            fp = 0
            
            
        tps.append(tp)
        fns.append(fn)
        fps.append(fp)
    for tp,fp,fn in zip(tps,fps,fns):
        if tp>0:
            precisions.append(tp/(tp+fp))
            recalls.append(tp/(tp+fn))
        else:
            precisions.append(0)
            recalls.append(0)    
      
    

    auc_value = auc(recalls, precisions)

    return auc_value


def vus_roc(y_true : np.array ,y_anomaly_scores:  np.array, window=4):
    """
    Calculate the VUS-ROC (Volume Under the ROC Surface) score for anomaly detection in time series.

    This metric extends the classical AUC-ROC by introducing a temporal tolerance parameter `l`, which
    smooths the binary ground-truth labels. The idea is to allow a flexible evaluation that tolerates
    small misalignments in the detection of anomalies. The final score is computed by integrating 
    the ROC-AUC over different values of the tolerance parameter, from 0 to `window`, thus producing
    a volume under the ROC surface.

    For more information, see the original paper:
    https://dl.acm.org/doi/10.14778/3551793.3551830

    Parameters:
        y_true (np.array):
            Ground-truth binary labels (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Anomaly scores for each time point.
        window (int):
            Maximum temporal tolerance `l` used to smooth the evaluation.

    Returns:
        float: VUS-ROC score.

    
    """
    m = VUS_ROC(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def vus_pr(y_true : np.array ,y_anomaly_scores:  np.array,  window=4):
    """
    Calculate the VUS-PR (Volume Under the PR Surface) score for anomaly detection in time series.

    This metric is an extension of the classical AUC-PR, incorporating a temporal tolerance parameter `l`
    that smooths the binary ground-truth labels. It allows for some flexibility in the detection of 
    anomalies that are temporally close to the true events. The final metric integrates the PR-AUC
    over several levels of temporal tolerance (from 0 to `window`), yielding a volume under the PR surface.

    For more information, see the original paper:
    https://dl.acm.org/doi/10.14778/3551793.3551830

    Parameters:
        y_true (np.array):
            Ground-truth binary labels (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Anomaly scores for each time point.
        window (int):
            Maximum temporal tolerance `l` used to smooth the evaluation.

    Returns:
        float: VUS-PR score.

    
    """
    m = VUS_PR(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def real_pate(y_true: np.array, y_anomaly_scores: np.array, early: int, delay: int):
    """
    Calculate PATE score for anomaly detection in time series using real-valued anomaly scores.

    This version of PATE evaluates real-valued anomaly scores by assigning weights to predictions 
    based on their temporal proximity to the true anomaly intervals. It defines an early buffer of 
    length `early` before each anomaly and a delay buffer of length `delay` after it. Detections with 
    high scores within the anomaly interval receive full weight, while those in the buffer zones are 
    assigned linearly decaying weights depending on their distance from the interval. Scores outside 
    these zones contribute to false positives, and intervals with insufficient detection are penalized 
    as false negatives.

    The final PATE score aggregates these weighted contributions across all time steps, yielding 
    a smooth performance measure that is sensitive to both the timing and confidence of the predictions.

    For more information, see the original paper:
    https://arxiv.org/abs/2405.12096

    Parameters:
        y_true (np.array):
            Ground truth binary labels (0 = normal, 1 = anomaly).
        y_anomaly_scores (np.array):
            Real-valued anomaly scores for each time point.
        early (int):
            Length of the early buffer zone before each anomaly interval.
        delay (int):
            Length of the delay buffer zone after each anomaly interval.

    Returns:
        float: The real-valued PATE score.
    """
    return PATE(y_true, y_anomaly_scores, early, delay, binary_scores=False)