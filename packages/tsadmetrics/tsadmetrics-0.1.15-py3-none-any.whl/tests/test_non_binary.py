import unittest
from tsadmetrics import *
import numpy as np
import random


class TestPrecisionAtK(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([0,0,1,1])


        self.y_pred1 = np.array([0.2, 0.9, 0.3, 0.8])

        self.y_pred2 = np.array([1, 2, 3, 4])

        self.y_pred3 = np.array([3, 4, 1, 2])

        self.y_true2 =  np.array([1,1,1,0])

        self.y_pred4 = np.array([3, 4, 1, 2])


    

    def test_precision_at_k_score(self):
        """
        Prueba para la función precision_at_k_score.
        """
        score = round(precision_at_k(self.y_true1, self.y_pred1),2)
        expected_score = 0.5
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(precision_at_k(self.y_true1, self.y_pred2),2)
        expected_score = 1
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(precision_at_k(self.y_true1, self.y_pred3),2)
        expected_score = 0
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(precision_at_k(self.y_true2, self.y_pred4),2)
        expected_score = round(2/3,2)
        self.assertAlmostEqual(score, expected_score, places=4)
        
    def test_precision_at_k_score_consistency(self):
        try:
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))

                score = precision_at_k(y_true, y_pred)
        except Exception as e:
            self.fail(f"precision_at_k_score raised an exception {e}")


class TestAUCROCPW(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([0,0,1,1])


        self.y_pred1 = np.array([1, 3, 2, 4])

        self.y_pred2 = np.array([1, 2, 3, 4])

        self.y_pred3 = np.array([4, 4, 4, 4])
    

    def test_auc_roc_pw(self):
        """
        Prueba para la función auc_roc_pw.
        """
        score = round(auc_roc_pw(self.y_true1, self.y_pred1),2)
        expected_score = 0.75
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_roc_pw(self.y_true1, self.y_pred2),2)
        expected_score = 1
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_roc_pw(self.y_true1, self.y_pred3),2)
        expected_score = 0.5
        self.assertAlmostEqual(score, expected_score, places=4)

        
    def test_auc_roc_pw_consistency(self):
        try:
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))

                score = auc_roc_pw(y_true, y_pred)
        except Exception as e:
            self.fail(f"auc_roc_pw raised an exception {e}")

class TestAUCPRPW(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([0,0,1,1])


        self.y_pred1 = np.array([1, 3, 2, 4])

        self.y_pred2 = np.array([1, 2, 3, 4])

        self.y_pred3 = np.array([4, 4, 4, 4])
    

    def test_auc_pr_pw(self):
        """
        Prueba para la función auc_pr_pw.
        """
        score = round(auc_pr_pw(self.y_true1, self.y_pred1),2)
        expected_score = 0.83
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_pw(self.y_true1, self.y_pred2),2)
        expected_score = 1
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_pw(self.y_true1, self.y_pred3),2)
        expected_score = 0.5
        self.assertAlmostEqual(score, expected_score, places=4)

        
    def test_auc_pr_consistency(self):
        try:
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))

                score = auc_pr_pw(y_true, y_pred)
        except Exception as e:
            self.fail(f"auc_pr raised an exception {e}")


    

class TestAUCPRPA(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([0,0,1,1])


        self.y_pred1 = np.array([1, 3, 2, 4])

        self.y_pred2 = np.array([1, 2, 3, 4])

        self.y_pred3 = np.array([4, 4, 4, 4])

        self.y_true2 = [0,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,0,0,1,1,0
,1,1,1,0,0,1,0,0,1,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,1
,1,1,1,1,0,0,1,1,1,1,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,1]


        self.y_pred4 = [0.1280475, 0.12059283 ,0.29936968 ,0.85866402 ,0.74071874 ,0.22310849
 ,0.11281839 ,0.26133246 ,0.33696106 ,0.01442675 ,0.51962876 ,0.07828833
 ,0.45337844 ,0.09444483 ,0.91216588 ,0.18847595 ,0.26828481 ,0.65248919
 ,0.46291981 ,0.43730757 ,0.78087553 ,0.45031043 ,0.88661033 ,0.56209352
 ,0.45029423 ,0.17638205 ,0.9261279 ,0.58830652 ,0.01602648 ,0.73903379
 ,0.61831379 ,0.74779903 ,0.42682106 ,0.82583519 ,0.19709012 ,0.44925962
 ,0.62752415 ,0.52458327 ,0.46291768 ,0.33937527 ,0.34868777 ,0.12293847
 ,0.84477504 ,0.10225254 ,0.37048167 ,0.04476031 ,0.36680499 ,0.11346155
 ,0.10583112 ,0.09493136 ,0.54878736 ,0.68514489 ,0.5940307 ,0.14526962
 ,0.69385728 ,0.38888727 ,0.61495304 ,0.06795402 ,0.02894603 ,0.08293609
 ,0.22865685 ,0.63531487 ,0.97966126 ,0.31418622 ,0.8943095 ,0.22974177
 ,0.94402929 ,0.13140625 ,0.80539267 ,0.40160344 ,0.38151339 ,0.65011626
 ,0.71657942 ,0.93297398 ,0.32043329 ,0.54667941 ,0.90645979 ,0.98730183
 ,0.82351336 ,0.10404812 ,0.6962921 ,0.72890752 ,0.49700666 ,0.47461103
 ,0.59696079 ,0.85876179 ,0.247344 ,0.38187879 ,0.23906861 ,0.5266315
 ,0.08171512 ,0.27903375 ,0.61112439 ,0.20784267 ,0.90652453 ,0.87575255
 ,0.26972245 ,0.78780138 ,0.37649185 ,0.08467683]


    def test_auc_pr_pa(self):
        """
        Prueba para la función auc_pr_pa.
        """
        score = round(auc_pr_pa(self.y_true1, self.y_pred1),2)
        expected_score = 1.0
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_pa(self.y_true1, self.y_pred2),2)
        expected_score = 1.0
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_pa(self.y_true1, self.y_pred3),2)
        expected_score = 0.75
        self.assertAlmostEqual(score, expected_score, places=4)

        if len(self.y_true2) == len(self.y_pred4):
            score = round(auc_pr_pa(self.y_true2, self.y_pred4),2)
            expected_score = 0.78
            self.assertAlmostEqual(score, expected_score, places=4)

        
    def test_auc_pr_pa_consistency(self):
        y_true, y_pred = [],[]
        try:
            for _ in range(100):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))
                score = auc_pr_pa(y_true, y_pred)
        except Exception as e:
            self.fail(f"auc_roc_pr_pa raised an exception {e}")
            

class TestAUCPRSW(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([0,0,1,1])


        self.y_pred1 = np.array([1, 3, 2, 4])

        self.y_pred2 = np.array([1, 2, 3, 4])

        self.y_pred3 = np.array([4, 4, 4, 4])
    

    def test_auc_pr_sw(self):
        """
        Prueba para la función auc_pr_sw.
        """
        score = round(auc_pr_sw(self.y_true1, self.y_pred1),2)
        expected_score = 1.0
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_sw(self.y_true1, self.y_pred2),2)
        expected_score = 1
        self.assertAlmostEqual(score, expected_score, places=4)

        score = round(auc_pr_sw(self.y_true1, self.y_pred3),2)
        expected_score = 1
        self.assertAlmostEqual(score, expected_score, places=4)

        
    # def test_auc_pr_sw_consistency(self):
    #     try:
    #         for _ in range(100):
    #             y_true = np.random.choice([0, 1], size=(100,))
    #             y_pred = np.random.random( size=(100,))

    #             score = auc_pr_sw(y_true, y_pred)
    #     except Exception as e:
    #         self.fail(f"auc_pr_sw raised an exception {e}")


class TestVUSROC(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.y_true2 =  np.array([0, 1, 0, 1, 0, 0, 0, 0, 0, 0])

        self.y_pred1 = np.array( [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.y_pred2 = np.array([8, 0, 9, 1, 7, 2, 3, 4, 5, 6])


    

    def test_vus_roc(self):
        """
        Prueba para la función vus_roc.
        """
        score = round(vus_roc(self.y_true1, self.y_pred1,window=4),2)
        self.assertTrue(score <= 0.1)

        score = round(vus_roc(self.y_true2, self.y_pred2,window=4),2)
        self.assertTrue(score > 0.4)

        score = vus_roc(self.y_true2, self.y_pred2,window=0)
        self.assertTrue(score < 0.4)

        
    def test_vus_roc_consistency(self):
        try:
            for _ in range(10):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))
                score = vus_roc(y_true, y_pred, window=4)
        except Exception as e:
            self.fail(f"auc_roc raised an exception {e}")


class TestVUSPR(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
 
        self.y_true1 =  np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.y_true2 =  np.array([0, 1, 0, 1, 0, 0, 0, 0, 0, 0])

        self.y_pred1 = np.array( [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.y_pred2 = np.array([8, 0, 9, 1, 7, 2, 3, 4, 5, 6])


    

    def test_vus_pr(self):
        """
        Prueba para la función vus_pr.
        """
        score = round(vus_pr(self.y_true1, self.y_pred1,window=4),2)
        self.assertTrue(score <= 0.2)

        score = round(vus_pr(self.y_true2, self.y_pred2,window=4),2)
        self.assertTrue(score > 0.5)

        score = vus_pr(self.y_true2, self.y_pred2,window=0)
        self.assertTrue(score < 0.5)

        
    def test_vus_pr_consistency(self):
        try:
            for _ in range(10):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.random( size=(100,))
                score = vus_pr(y_true, y_pred, window=4)
        except Exception as e:
            self.fail(f"auc_roc raised an exception {e}")


class TestNonBinaryPATE(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        pass

    

        
    def test_pate_consistency(self):
        try:
            for _ in range(10):
                y_true = np.random.choice([0, 1], size=(100,))
                y_pred = np.random.choice([0, 1], size=(100,))

                score = real_pate(y_true, y_pred, early=5, delay=5)
        except Exception as e:
            self.fail(f"real_pate raised an exception {e}")