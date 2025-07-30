import numpy as np
from ._tsadeval.metrics import Binary_anomalies, pointwise_to_full_series, segmentwise_to_full_series, DelayThresholdedPointAdjust
def get_tp_tn_fp_fn_point_wise(y_true: np.array,y_pred: np.array):
    TP,TN,FP,FN=0,0,0,0
    for true,pred in zip(y_true,y_pred):
        if true==pred:
            if true==1:
                TP+=1
            else:
                TN+=1
        else:
            if true==1:
                FN+=1
            else:
                FP+=1
    return TP,TN,FP,FN


def get_events(y_true,anomaly=True):
    events = []
    start_idx = None
    v = 0
    if anomaly:
        v = 1
    else:
        v = 0

    for i, val in enumerate(y_true):
        if val == v:  # Si encontramos el inicio de un evento
            if start_idx is None:
                start_idx = i  # Establecemos el inicio del evento
        elif start_idx is not None:  # Si encontramos el final de un evento
            events.append((start_idx, i - 1))  # Agregamos el evento a la lista de eventos
            start_idx = None  # Restablecemos el inicio del evento

    if start_idx is not None:  # Si al final de la secuencia aún estamos dentro de un evento
        events.append((start_idx, len(y_true) - 1))  # Agregamos el evento final a la lista de eventos


    return events

def calculate_intersection(event1, event2):
    start_intersection = max(event1[0], event2[0])
    end_intersection = min(event1[1], event2[1])

    # If there is an intersection, return the range of the intersection, otherwise return None
    if start_intersection <= end_intersection:
        return [start_intersection, end_intersection]
    else:
        return None

def get_tp_tn_fp_fn_point_adjusted(y_true: np.array,y_pred: np.array):
    TP, TN, FP, FN = get_tp_tn_fp_fn_point_wise(y_true, y_pred)
    TP=0
    FN=0
    y_true_events = get_events(y_true,anomaly=True)
    y_pred_events = get_events(y_pred,anomaly=True)

    i_true = 0
    i_pred = 0
    while i_true<len(y_true_events):
        detected = False
        while i_pred<len(y_pred_events) and y_true_events[i_true][1]>y_pred_events[i_pred][0]:
            if calculate_intersection(y_true_events[i_true],y_pred_events[i_pred]) is not None:
                TP+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
                detected=True
                break
            elif y_true_events[i_true][0]>y_pred_events[i_pred][1]:
                i_pred+=1
        
        if not detected:
            FN+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
        i_true+=1
    
    return TP, TN, FP, FN

def get_tp_tn_fp_fn_delay_th_point_adjusted(y_true: np.array,y_pred: np.array,k: int):
    TP, TN, FP, FN = get_tp_tn_fp_fn_point_wise(y_true, y_pred)
    TP=0
    FN=0
    y_true_events = get_events(y_true,anomaly=True)
    y_pred_events = get_events(y_pred,anomaly=True)

    i_true = 0
    i_pred = 0
    while i_true<len(y_true_events):
        detected = False
        while i_pred<len(y_pred_events) and y_true_events[i_true][1]>y_pred_events[i_pred][0]:
            intersec = calculate_intersection(y_true_events[i_true],y_pred_events[i_pred])
            if intersec is not None and intersec[0]-y_true_events[i_true][0]<k:
                TP+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
                detected=True
                break
            else:
                i_pred+=1
        
        if not detected:
            FN+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
        i_true+=1
    
    return TP, TN, FP, FN

def get_tp_tn_fp_fn_point_adjusted_at_k(y_true: np.array,y_pred: np.array, k: float):
    TP, TN, FP, FN = get_tp_tn_fp_fn_point_wise(y_true, y_pred)
    TP=0
    FN=0
    y_true_events = get_events(y_true,anomaly=True)
    y_pred_events = get_events(y_pred,anomaly=True)

    i_true = 0
    i_pred = 0
    while i_true<len(y_true_events):
        detected = False
        while i_pred<len(y_pred_events) and y_true_events[i_true][1]>y_pred_events[i_pred][0]:
            intersec = calculate_intersection(y_true_events[i_true],y_pred_events[i_pred])
            if intersec is not None:
                event_size = y_true_events[i_true][1]-y_true_events[i_true][0]+1
                intersec_size = intersec[1]-intersec[0]+1
            if intersec is not None and intersec_size/event_size>=k:
                
                TP+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
                detected=True
                break
            else:
                i_pred+=1
        
        if not detected:
            FN+= y_true_events[i_true][1]-y_true_events[i_true][0]+1
        i_true+=1
    
    return TP, TN, FP, FN


def get_tp_tn_fp_fn_latency_sparsity_aw(y_true: np.array, y_pred: np.array, ni: int):
    batched_shape = (int(np.ceil(y_pred.shape[0] / ni)), 1)
    label_batch = np.zeros(batched_shape)
    pred_batch = np.zeros(batched_shape)
    actual = np.copy(y_true)
    predict = np.copy(y_pred)
    detect_state = False  # triggered when a True anomaly is detected by model
    anomaly_batch_count = 0
    i, i_ni = 0, 0
    step = ni

    while i < len(y_true) and step > 1:
        j = min(i + step, len(y_true))  # end of ni (batch) starting at i

        # Adjust step size if needed
        if step > 2 and actual[i:j].sum() > 1:
            if np.diff(np.where(actual[i:j])).max() > 1:  # if it finds an interruption in the true label continuity
                step = min(int((j - i) / 2), 2)  # reduce step size
                label_batch = np.append(label_batch, [[0]], axis=0)
                pred_batch = np.append(pred_batch, [[0]], axis=0)  # increase size
                j = i + step
            else:
                step = ni
        else:
            step = ni

        # Start rolling window scoring
        if actual[i:j].max():  # If label = T
            if not actual[i]:  # if first value is normal
                detect_state = False
            s = actual[i:j].argmax()  # this is the index of the first occurrence
            if detect_state:  # if anomaly was previously detected by model
                anomaly_batch_count += 1
                pred_batch[i_ni], label_batch[i_ni], predict[i + s:j] = 1, 1, 1
            elif predict[i:j].max():  # if alert was detected with T
                detect_state = True  # turn on detection state
                anomaly_batch_count += 1
                pred_batch[i_ni], label_batch[i_ni], predict[i + s:j] = 1, 1, 1
            else:
                detect_state = False
                label_batch[i_ni] = 1
        else:
            detect_state = False
            if predict[i:j].max():  # if False positive
                pred_batch[i_ni] = 1
        i += step
        i_ni += 1

    if ni == 1:
        return get_tp_tn_fp_fn_point_wise(actual, predict)

    return get_tp_tn_fp_fn_point_wise(label_batch.flatten().astype(int), pred_batch.flatten().astype(int))

def get_tp_fp_fn_segment_wise(y_true: np.array,y_pred: np.array):
    

    y_true_anomaly_events = get_events(y_true)
    pred_anomaly_events = get_events(y_pred)
    y_true_normal_events = get_events(y_true,False)
    pred_normal_events = get_events(y_pred,False)

    TP = 0
    FN = 0
    FP = 0
    #TP
    i = 0
    for e_p in pred_anomaly_events:
        
        c, d = e_p
        while i<len(y_true_anomaly_events):
            e_g = y_true_anomaly_events[i]
            a, b = e_g
            if a>d:
              break

            if b<c:
                i+=1
                continue

            else:
              if max(a, c) <= min(b, d):
                  TP+=1
            

            i+=1

    #FN
    FN = len(y_true_anomaly_events) - TP
    #FP
    i = 0
    for e_p in y_true_normal_events:
        
        c, d = e_p
        while i<len(pred_anomaly_events):
            e_g = pred_anomaly_events[i]
            a, b = e_g
            if a>d:
                break
            if b<c:
                i+=1
                continue
            if calculate_intersection(e_g, e_p) is not None:
                FP+=1
            i+=1
    return TP, FP, FN

def is_full_series(length: int, anomalies: np.array):
    # [1 0 1 1 0]
    return len(anomalies.shape) == 1 and len(anomalies) == length

def is_pointwise(length: int, anomalies: np.array):
    # [0 2 3]
    return len(anomalies.shape) == 1 and len(anomalies) < length

def is_segmentwise(length: int, anomalies: np.array):
    # [[0 0] [2 3]]
    return len(anomalies.shape) == 2


def transform_to_full_series(length: int, anomalies: np.array):
    if is_full_series(length, anomalies):
        return anomalies
    elif is_pointwise(anomalies):
        return pointwise_to_full_series(anomalies, length)
    elif is_segmentwise(length, anomalies):
        return segmentwise_to_full_series(anomalies, length)
    else:
        raise ValueError(f"Illegal shape of anomalies:\n{anomalies}")

def counting_method(y_true: np.array, y_pred: np.array, k: int):
    em,da,ma,fa = 0,0,0,0
    for i_gt in range(len(y_true)):
        i_pa = i_gt
        gt = y_true[i_gt]
        pa = y_pred[i_pa]
        if gt==1 and pa==1:
            em+=1
        elif gt==0 and pa==1:
            fa+=1
        elif gt==1 and pa==0:
            anom_range = y_pred[i_gt-k:i_pa+k+1]
            detected = False
            for r in anom_range:
                if r==1:
                    em+=1
                    detected=True
                    break
            if not detected:
                ma+=1
        elif gt==0 and pa==0:
            pass
    # b = DelayThresholdedPointAdjust(len(y_true),y_true,y_pred,k=k)
    # da = b.tp-em
    # ma = b.fn

    return em,da,ma,fa


#Range Based utils

def cardinality(n_intersections,mode):
    if mode == 'one':
        return 1
    elif mode == 'reciprocal':
        if n_intersections==0:
            return 1
        else:
            return float(1/n_intersections)
    else:
        raise Exception("Error, wrong cardinality mode.")
    
    
def size(anomaly_range, overlap_set, position, bias):
    if overlap_set == None:
        return 0
    
    my_value = 0
    max_value = 0
    anomaly_length = anomaly_range[1] - anomaly_range[0] + 1
    for i in range(1,anomaly_length+1):
        bias_value = position(i, anomaly_length,bias)
        max_value += bias_value
        if  anomaly_range[0]+i-1 >= overlap_set[0] and anomaly_range[0]+i-1 <= overlap_set[1]:
            my_value += bias_value
    return my_value / max_value

def position(i, anomaly_length,bias):
    if bias == 'flat':
        return 1
    elif bias == 'front-end':
        return anomaly_length - i + 1
    elif bias == 'back-end':
        return i
    elif bias == 'middle':
        if i <= anomaly_length / 2:
            return i
        else:
            return anomaly_length - i + 1
    else:
        raise Exception("Error, wrong bias value.")