import unittest
from pymgcv.transformer import SmoothConTransformer
import pandas as pd
import numpy as np

class TestSmoothConTransformer(unittest.TestCase):
    def setUp(self):
        # Initialize the transformer with default settings
        self.transformer = SmoothConTransformer()

    def test_obj_specifications(self):
        # Specifications of 'obj' to test
        obj_specs = [
            "s(x)",
            "s(x, bs='bs')",
            "s(x, bs='tp')",
            "te(x, y)",
            "ti(x, y)"
        ]

        # Mock data assuming x and y are numerical covariates
        data = {'x': list(range(20)), 'y': list(range(20))}
        data = pd.DataFrame(data)

        # Loop over each obj spec and test the fit, transform, and fit_transform methods
        for obj in obj_specs:
            with self.subTest(obj=obj):
                # fit
                self.transformer.fit(obj=obj, data=data)
                self.assertIsNotNone(self.transformer.smooth_con_obj, msg=f"fit failed for {obj}")
                
                # transform
                result_transform = self.transformer.transform(data=data)
                self.assertIsNotNone(result_transform, msg=f"transform failed for {obj}")
                
                # fit_transform
                result_fit_transform = self.transformer.fit_transform(obj=obj, data=data)
                self.assertIsNotNone(result_fit_transform, msg=f"fit_transform failed for {obj}")


class TestSmoothConTransformerExtensions(unittest.TestCase):
    def setUp(self):
        # Initialize the transformer
        self.transformer = SmoothConTransformer()
        # Assume 'obj' and 'data' are setup correctly for the test environment
        # Normally you would use real data and a real smooth specification object
        obj = "s(x)"
        data = {'x': list(range(20))}
        data = pd.DataFrame(data)
        self.transformer.fit(obj=obj, data=data)  # Preparing the object

    def test_get_anything(self):
        # Test to retrieve an element 'sp' from smooth_con_obj
        # This assumes 'sp' is a valid element name in the returned R object
        result = self.transformer.get_anything('sp')
        self.assertIsNotNone(result, "Failed to retrieve 'sp'")

    def test_get_design(self):
        # Retrieve the design matrix and test if it's a numpy array
        design_matrix = self.transformer.get_design()
        self.assertIsInstance(design_matrix, np.ndarray, "The design matrix should be a NumPy array")

        self.assertEqual(design_matrix.shape, (20, 10))

def test_get_penalty(self):
    # Retrieve the penalty matrix from the transformer
    penalty_matrices = self.transformer.get_penalty()
    self.assertIsInstance(penalty_matrices, list, "Penalty matrices should be a list")
    self.assertTrue(all(isinstance(mat, np.ndarray) for mat in penalty_matrices), "All items in penalty matrices should be NumPy arrays")

    self.assertEqual(penalty_matrices[0].shape, (10, 10))


if __name__ == '__main__':
    unittest.main()

