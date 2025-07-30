import unittest
from tsadmetrics import *

from sklearn.metrics import recall_score, precision_score, fbeta_score
import numpy as np
import random

class TestPointWiseMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.num_tests = 100  # Número de conjuntos de datos aleatorios a generar para las pruebas
        self.test_cases = []
        for _ in range(self.num_tests):
            y_true = np.random.choice([0, 1], size=(10000,))
            y_pred = np.random.choice([0, 1], size=(10000,))
            self.test_cases.append((y_true, y_pred))

    def test_point_wise_recall(self):
        """
        Prueba para la función point_wise_recall.
        """
        for y_true, y_pred in self.test_cases:
            with self.subTest(y_true=y_true, y_pred=y_pred):
                recall = point_wise_recall(y_true, y_pred)
                expected_recall = recall_score(y_true, y_pred)
                self.assertAlmostEqual(recall, expected_recall, places=4)

    def test_point_wise_precision(self):
        """
        Prueba para la función point_wise_precision.
        """
        for y_true, y_pred in self.test_cases:
            with self.subTest(y_true=y_true, y_pred=y_pred):
                precision = point_wise_precision(y_true, y_pred)
                expected_precision = precision_score(y_true, y_pred)
                self.assertAlmostEqual(precision, expected_precision, places=4)

    def test_point_wise_f_score(self):
        """
        Prueba para la función point_wise_f_score.
        """
        for y_true, y_pred in self.test_cases:
            with self.subTest(y_true=y_true, y_pred=y_pred):
                beta = random.randint(0,1000000)
                f_score = point_wise_f_score(y_true, y_pred, beta=1)
                expected_f_score = fbeta_score(y_true, y_pred, beta=1)
                self.assertAlmostEqual(f_score, expected_f_score, places=4)

class TestPointAdjustedMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true = np.array([0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
        self.y_pred = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0])

    def test_point_adjusted_recall(self):
        """
        Prueba para la función point_wise_recall.
        """
        recall = point_adjusted_recall(self.y_true, self.y_pred)
        expected_recall = 1
        self.assertAlmostEqual(recall, expected_recall, places=4)
    def test_point_adjusted_precision(self):
        """
        Prueba para la función point_adjusted_precision.
        """
        precision = round(point_adjusted_precision(self.y_true, self.y_pred),2)
        expected_precision = 0.87
        self.assertAlmostEqual(precision, expected_precision, places=4)

    def test_point_adjusted_f_score(self):
        """
        Prueba para la función point_adjusted_f_score.
        """
        f_score = round(point_adjusted_f_score(self.y_true, self.y_pred),2)
        expected_f_score = 0.93
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_point_adjusted_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            point_adjusted_f_score(y_true, y_pred)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                f_score = point_adjusted_f_score(y_true, y_pred)
        except Exception as e:
            self.fail(f"point_adjusted_f_score raised an exception {e}")

class TestDelayThPointAdjustedMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true  = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

    

    def test_delay_th_point_adjusted_f_score(self):
        """
        Prueba para la función delay_th_point_adjusted_f_score.
        """
        f_score = round(delay_th_point_adjusted_f_score(self.y_true, self.y_pred1, 2),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
        f_score = round(delay_th_point_adjusted_f_score(self.y_true, self.y_pred2, 2),2)
        expected_f_score = 1
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

    def test_delay_th_point_adjusted_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            delay_th_point_adjusted_f_score(y_true, y_pred,7)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                f_score = delay_th_point_adjusted_f_score(y_true, y_pred, 7)
        except Exception as e:
            self.fail(f"delay_th_point_adjusted_f_score raised an exception {e}")

class TestPointAdjustedMetricsAtK(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true  = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])


    def test_point_adjusted_at_k_f_score(self):
        """
        Prueba para la función point_adjusted_at_k_f_score.
        """
        f_score = round(point_adjusted_at_k_f_score(self.y_true, self.y_pred1,0.2),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(point_adjusted_at_k_f_score(self.y_true, self.y_pred2,0.2),2)
        expected_f_score = 0.22
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_point_adjusted_at_k_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            point_adjusted_at_k_f_score(y_true, y_pred,0.3)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                f_score = point_adjusted_at_k_f_score(y_true, y_pred,0.3)
        except Exception as e:
            self.fail(f"point_adjusted_at_k_f_score raised an exception {e}")

class TestLatencySparsityAwareMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true  = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

    def test_latency_sparsity_aw_f_score(self):
        """
        Prueba para la función latency_sparsity_aw_f_score.
        """
        f_score = round(latency_sparsity_aw_f_score(self.y_true, self.y_pred1,2),2)
        expected_f_score = 0.71
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(latency_sparsity_aw_f_score(self.y_true, self.y_pred2,2),2)
        expected_f_score = 1
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_latency_sparsity_aw_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            latency_sparsity_aw_f_score(y_true, y_pred,3)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                f_score = latency_sparsity_aw_f_score(y_true, y_pred,3)
        except Exception as e:
            self.fail(f"latency_sparsity_aw_f_score raised an exception {e}")

class TestSegmentWiseMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true  = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])


    def test_segment_wise_f_score(self):
        """
        Prueba para la función segment_wise_f_score.
        """
        f_score = round(segment_wise_f_score(self.y_true, self.y_pred1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(segment_wise_f_score(self.y_true, self.y_pred2),2)
        expected_f_score = 1
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

    
        
    def test_segment_wise_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            segment_wise_f_score(y_true, y_pred,7)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(10,))
                y_pred = np.random.choice([0, 1], size=(10,))
                f_score = segment_wise_f_score(y_true, y_pred)
                
        except Exception as e:
            self.fail(f"segment_wise_f_score raised an exception {e}")

class TestCompositeMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true  = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])




    def test_composite_f_score(self):
        """
        Prueba para la función composite_f_score.
        """
        f_score = round(composite_f_score(self.y_true, self.y_pred1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(composite_f_score(self.y_true, self.y_pred2),2)
        expected_f_score = 1
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        
    def test_composite_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            composite_f_score(y_true, y_pred,7)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(10,))
                y_pred = np.random.choice([0, 1], size=(10,))
                f_score = composite_f_score(y_true, y_pred)
                
        except Exception as e:
            self.fail(f"composite_f_score raised an exception {e}")

class TestTimeTolerantMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true =   np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 =  np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 =  np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

    def test_time_tolerant_recall(self):
        """
        Prueba para la función time_tolerant_recall.
        """
        recall = round(time_tolerant_recall(self.y_true, self.y_pred1,2),2)
        expected_recall = 0.5
        self.assertAlmostEqual(recall, expected_recall, places=4)

        recall = round(time_tolerant_recall(self.y_true, self.y_pred2,2),3)
        expected_recall = 0.375
        self.assertAlmostEqual(recall, expected_recall, places=4)

    def test_time_tolerant_precision(self):
        """
        Prueba para la función time_tolerant_precision.
        """
        precision = round(time_tolerant_precision(self.y_true, self.y_pred1,2),2)
        expected_precision = 1
        self.assertAlmostEqual(precision, expected_precision, places=4)

        precision = round(time_tolerant_precision(self.y_true, self.y_pred2,2),2)
        expected_precision = 1
        self.assertAlmostEqual(precision, expected_precision, places=4)

    def test_time_tolerant_f_score(self):
        """
        Prueba para la función time_tolerant_f_score.
        """
        f_score = round(time_tolerant_f_score(self.y_true, self.y_pred1,2),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(time_tolerant_f_score(self.y_true, self.y_pred2,2),2)
        expected_f_score = 0.55
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_time_tolerant_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            time_tolerant_f_score(y_true, y_pred,7)
            for _ in range(1000):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                t = random.randint(1,100)
                f_score = time_tolerant_f_score(y_true, y_pred,t)
        except Exception as e:
            self.fail(f"time_tolerant_f_score raised an exception {e}")


class TestRangeBasedMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

        self.y_true2  = np.array([0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])
        self.y_pred21 = np.array([0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred22 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])
    

    def test_range_based_f_score(self):
        """
        Prueba para la función range_based_f_score.
        """
        f_score = round(range_based_f_score(self.y_true1, self.y_pred1, beta=1,p_alpha=0.2,r_alpha=0.2,cardinality_mode='one',p_bias='flat',r_bias='flat'),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(range_based_f_score(self.y_true1, self.y_pred2,beta=1,p_alpha=0.2,r_alpha=0.2,cardinality_mode='one',p_bias='flat',r_bias='flat'),2)
        expected_f_score = 0.46
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(range_based_f_score(self.y_true2, self.y_pred21,beta=1,p_alpha=0.2,r_alpha=0.2,cardinality_mode='one',p_bias='flat',r_bias='flat'),2)
        expected_f_score = 0.71
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(range_based_f_score(self.y_true2, self.y_pred22,beta=1,p_alpha=0.2,r_alpha=0.2,cardinality_mode='one',p_bias='flat',r_bias='flat'),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_range_based_consistency(self):
        try:
            modes = ['flat','front','back','middle']
            modes_c = ['one','reciprocal']

            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            range_based_f_score(y_true, y_pred,beta=2,p_alpha=random.random(),r_alpha=random.random(),cardinality_mode=random.choice(modes_c),p_bias=random.choice(modes),r_bias=random.choice(modes))
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))
                f_score = range_based_f_score(y_true, y_pred,beta=2,p_alpha=random.random(),r_alpha=random.random(),cardinality_mode=random.choice(modes_c),p_bias=random.choice(modes),r_bias=random.choice(modes))
        except Exception as e:
            self.fail(f"range_based_f_score raised an exception {e}")

class TestTSAwareMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

        self.y_true2 = np.array([0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])
        self.y_pred21 = np.array([0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred22 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])

    

    def test_ts_aware_f_score(self):
        """
        Prueba para la función ts_aware_f_score.
        """
        f_score = round(ts_aware_f_score(self.y_true1, self.y_pred1,1, 0.5, 0, 0.5),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(ts_aware_f_score(self.y_true1, self.y_pred2,1, 0.5, 0, 0.5),2)
        expected_f_score = 0.12
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(ts_aware_f_score(self.y_true2, self.y_pred21,1, 0.5, 0, 0.5),2)
        expected_f_score = 0.77
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(ts_aware_f_score(self.y_true2, self.y_pred22,1, 0.5, 0, 0.5),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_ts_aware_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            ts_aware_f_score(y_true, y_pred, 1, random.random(), 0, random.random())
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                f_score = ts_aware_f_score(y_true, y_pred, 1, random.random(), 0, random.random())
        except Exception as e:
            self.fail(f"ts_aware_f_score raised an exception {e}")

class TestEnhancedTSAwareMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

        self.y_true2 = np.array([0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])
        self.y_pred21 = np.array([0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred22 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])

    

    def test_enhanced_ts_aware_f_score(self):
        """
        Prueba para la función ts_aware_f_score.
        """
        f_score = round(enhanced_ts_aware_f_score(self.y_true1, self.y_pred1, 0.5, 0.1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(enhanced_ts_aware_f_score(self.y_true1, self.y_pred2, 0.5, 0.1),2)
        expected_f_score = 0.72
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(enhanced_ts_aware_f_score(self.y_true2, self.y_pred21, 0.5, 0.1),2)
        expected_f_score = 0.77
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(enhanced_ts_aware_f_score(self.y_true2, self.y_pred22, 0.5, 0.1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_enhanced_ts_aware_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            enhanced_ts_aware_f_score(y_true, y_pred, random.random(), random.random())
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                f_score = enhanced_ts_aware_f_score(y_true, y_pred, random.random(), random.random())
        except Exception as e:
            self.fail(f"enhanced_ts_aware_f_score raised an exception {e}")


class TestAffiliationBasedMetrics(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

        self.y_true2 = np.array([0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])
        self.y_pred21 = np.array([0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred22 = np.array([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0])

    

    def test_affiliation_based_f_score(self):
        """
        Prueba para la función ts_aware_f_score.
        """
        f_score = round(affiliation_based_f_score(self.y_true1, self.y_pred1,1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(affiliation_based_f_score(self.y_true1, self.y_pred2,1),2)
        expected_f_score = 0.77
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(affiliation_based_f_score(self.y_true2, self.y_pred21,1),2)
        expected_f_score = 0.77
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(affiliation_based_f_score(self.y_true2, self.y_pred22,1),2)
        expected_f_score = 0.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_affiliation_based_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            affiliation_based_f_score(y_true, y_pred, 1)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                f_score = affiliation_based_f_score(y_true, y_pred, 1)
        except Exception as e:
            self.fail(f"affiliation_based_f_score raised an exception {e}")



class TestNABScore(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.y_true1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1])
        self.y_pred1 = np.array([0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.y_pred2 = np.array([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

        self.y_true2  = np.array([0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1])
        self.y_pred21 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1])
        self.y_pred22 = np.array([0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0])

    

    def test_nab_score(self):
        """
        Prueba para la función ts_aware_f_score.
        """
        f_score = round(nab_score(self.y_true1, self.y_pred1),2)
        expected_f_score = 50
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(nab_score(self.y_true1, self.y_pred2),2)
        expected_f_score = 100
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(nab_score(self.y_true2, self.y_pred21),2)
        expected_f_score = 33.33
        self.assertAlmostEqual(f_score, expected_f_score, places=4)

        f_score = round(nab_score(self.y_true2, self.y_pred22),2)
        expected_f_score = 66.67
        self.assertAlmostEqual(f_score, expected_f_score, places=4)
        
    def test_nab_score_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            nab_score(y_true, y_pred)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = nab_score(y_true, y_pred)
        except Exception as e:
            self.fail(f"nab_score raised an exception {e}")


class TestAverageDetectionCount(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_average_detection_count_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            average_detection_count(y_true, y_pred)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = average_detection_count(y_true, y_pred)
        except Exception as e:
            self.fail(f"average_detection_count raised an exception {e}")

class TestAbsoluteDetectionDistance(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_absolute_detection_distance_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            absolute_detection_distance(y_true, y_pred)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = absolute_detection_distance(y_true, y_pred)
        except Exception as e:
            self.fail(f"absolute_detection_distance raised an exception {e}")

class TestTotalDetectedInRange(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_total_detected_in_range_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            total_detected_in_range(y_true, y_pred,k=4)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = total_detected_in_range(y_true, y_pred,k=4)
        except Exception as e:
            self.fail(f"total_detected_in_range raised an exception {e}")

class TestDetectionAccuracyInRange(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_detection_accuracy_in_range_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            detection_accuracy_in_range(y_true, y_pred,k=4)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = detection_accuracy_in_range(y_true, y_pred,k=4)
        except Exception as e:
            self.fail(f"detection_accuracy_in_range raised an exception {e}")


class TestWeightedDetectionDifference(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_weighted_detection_difference_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            weighted_detection_difference(y_true, y_pred,k=4)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = weighted_detection_difference(y_true, y_pred,k=4)
        except Exception as e:
            self.fail(f"weighted_detection_difference raised an exception {e}")

class TestPATE(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_pate_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            binary_pate(y_true, y_pred, early=5, delay=5)
            for _ in range(10):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = binary_pate(y_true, y_pred, early=5, delay=5)
        except Exception as e:
            self.fail(f"binary_pate raised an exception {e}")


class TestMeanTimeToDetect(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_mean_time_to_detect_consistency(self):
        try:
            y_true = np.random.choice([0, 1], size=(100,))
            y_pred = np.zeros(100)
            mean_time_to_detect(y_true, y_pred)
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = mean_time_to_detect(y_true, y_pred)
        except Exception as e:
            self.fail(f"mean_time_to_detect raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
