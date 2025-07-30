# test_synthpop.py

import unittest
import numpy as np
import pandas as pd
from synthpop.metrics import MetricsReport, EfficacyMetrics, DisclosureProtection
from synthpop.processor.data_processor import DataProcessor, InvalidDataError
from synthpop.processor.missing_data_handler import MissingDataHandler
from synthpop.method.GC import GaussianCopulaMethod

# -------------------------------
# Tests for MetricsReport
# -------------------------------
class TestMetricsReport(unittest.TestCase):
    def setUp(self):
        # Create sample real and synthetic data with various types.
        self.real_df = pd.DataFrame({
            "numeric_col": [1, 2, 3, 4, 5, np.nan],
            "categorical_col": ["a", "b", "a", "c", "b", "b"],
            "datetime_col": pd.date_range("2023-01-01", periods=6),
            "boolean_col": [True, False, True, False, True, False]
        })
        self.synthetic_df = pd.DataFrame({
            "numeric_col": [1.1, 2.1, 3.1, 4.0, 5.2, np.nan],
            "categorical_col": ["a", "b", "b", "c", "d", "b"],
            "datetime_col": pd.date_range("2023-01-01", periods=6),
            "boolean_col": [True, True, True, False, True, False]
        })
        self.metadata = {
            "numeric_col": "numerical",
            "categorical_col": "categorical",
            "datetime_col": "datetime",
            "boolean_col": "boolean"
        }
    
    def test_generate_report(self):
        report = MetricsReport(self.real_df, self.synthetic_df, self.metadata)
        report_df = report.generate_report()
        self.assertIsInstance(report_df, pd.DataFrame)
        expected_cols = {"column", "type", "missing_value_similarity", "range_coverage",
                         "boundary_adherence", "ks_complement", "tv_complement",
                         "statistic_similarity", "category_coverage", "category_adherence"}
        self.assertTrue(expected_cols.issubset(set(report_df.columns)))
        # Check that non-applicable metrics are marked as "N/A"
        num_report = report_df[report_df["type"]=="numerical"].iloc[0]
        self.assertEqual(num_report["category_coverage"], "N/A")
        cat_report = report_df[report_df["type"]=="categorical"].iloc[0]
        self.assertEqual(cat_report["range_coverage"], "N/A")

# -------------------------------
# Tests for EfficacyMetrics
# -------------------------------
class TestEfficacyMetrics(unittest.TestCase):
    def test_regression(self):
        np.random.seed(42)
        real_reg = pd.DataFrame({
            "feat1": np.random.normal(0, 1, 100),
            "feat2": np.random.normal(5, 2, 100),
            "target": np.random.normal(10, 3, 100)
        })
        synthetic_reg = pd.DataFrame({
            "feat1": np.random.normal(0, 1, 100),
            "feat2": np.random.normal(5, 2, 100),
            "target": np.random.normal(10, 3, 100)
        })
        efficacy_reg = EfficacyMetrics(task='regression', target_column="target", random_state=42)
        metrics = efficacy_reg.evaluate(real_reg, synthetic_reg)
        self.assertIn("mse", metrics)
        self.assertIn("mae", metrics)
        self.assertIn("r2", metrics)
        self.assertLessEqual(metrics["r2"], 1.0)

    def test_classification(self):
        np.random.seed(42)
        real_clf = pd.DataFrame({
            "feat1": np.random.normal(0, 1, 100),
            "feat2": np.random.normal(5, 2, 100),
            "target": np.random.choice(["A", "B"], size=100)
        })
        synthetic_clf = pd.DataFrame({
            "feat1": np.random.normal(0, 1, 100),
            "feat2": np.random.normal(5, 2, 100),
            "target": np.random.choice(["A", "B"], size=100)
        })
        efficacy_clf = EfficacyMetrics(task='classification', target_column="target", random_state=42)
        metrics = efficacy_clf.evaluate(real_clf, synthetic_clf)
        self.assertIn("accuracy", metrics)
        self.assertIn("f1_score", metrics)

# -------------------------------
# Tests for DisclosureProtection
# -------------------------------
class TestDisclosureProtection(unittest.TestCase):
    def test_score_and_report(self):
        np.random.seed(42)
        real_dp = pd.DataFrame({
            "f1": np.random.normal(0, 1, 100),
            "f2": np.random.normal(5, 2, 100)
        })
        # Create synthetic data by adding small noise
        synthetic_dp = real_dp + np.random.normal(0, 0.5, real_dp.shape)
        dp = DisclosureProtection(real_dp, synthetic_dp)
        score = dp.score()
        report = dp.report()
        self.assertIsInstance(score, float)
        self.assertIsInstance(report, dict)
        self.assertIn("threshold", report)
        self.assertIn("risk_rate", report)
        self.assertIn("disclosure_protection_score", report)

# -------------------------------
# Tests for DataProcessor
# -------------------------------
class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        # Create a DataFrame with different types.
        self.df = pd.DataFrame({
            "numeric": np.random.normal(10, 2, 50),
            "categorical": np.random.choice(["Red", "Green", "Blue"], 50),
            "boolean": np.random.choice([True, False], 50),
            "datetime": pd.date_range("2023-01-01", periods=50),
            "timedelta": pd.to_timedelta(np.random.randint(1, 100, 50), unit="D"),
            "float": np.random.uniform(0, 1, 50)
        })
        self.metadata = {
            "numeric": "numerical",
            "categorical": "categorical",
            "boolean": "boolean",
            "datetime": "datetime",
            "timedelta": "timedelta",
            "float": "numerical"
        }
        self.processor = DataProcessor(self.metadata)
    
    def test_preprocess_postprocess(self):
        # Preprocess the data
        processed = self.processor.preprocess(self.df)
        self.assertIsInstance(processed, pd.DataFrame)
        # Check that categorical columns are encoded (i.e. no string values remain)
        for col, dtype in self.metadata.items():
            if dtype == "categorical":
                self.assertTrue(np.issubdtype(processed[col].dtype, np.number) or col not in processed.columns)
        # Simulate synthetic data as processed copy then postprocess back
        synthetic_processed = processed.copy()
        recovered = self.processor.postprocess(synthetic_processed)
        self.assertIsInstance(recovered, pd.DataFrame)
        # Check that the recovered DataFrame has the original columns order.
        self.assertListEqual(list(recovered.columns), list(self.df.columns))

    def test_validate_raises_on_missing_column(self):
        # Remove one column so that validation should fail.
        df_missing = self.df.drop(columns=["numeric"])
        with self.assertRaises(InvalidDataError):
            self.processor.validate(df_missing)

# -------------------------------
# Tests for MissingDataHandler
# -------------------------------
class TestMissingDataHandler(unittest.TestCase):
    def setUp(self):
        # Create a DataFrame with missing values in different types.
        self.df = pd.DataFrame({
            "num": [1, 2, np.nan, 4, 5],
            "cat": ["a", np.nan, "b", "a", "c"],
            "bool": [True, False, np.nan, True, False],
            "datetime": pd.to_datetime(["2023-01-01", np.nan, "2023-01-03", "2023-01-04", "2023-01-05"]),
            "timedelta": pd.to_timedelta([1, 2, np.nan, 4, 5], unit="D")
        })
        self.handler = MissingDataHandler()


    def test_apply_imputation(self):
        # First, detect missingness; we won't get perfect detection, but just test that imputation runs.
        missingness = self.handler.detect_missingness(self.df)
        imputed = self.handler.apply_imputation(self.df, missingness)
        # Check that after imputation there are no missing values.
        self.assertFalse(imputed.isna().any().any())

# -------------------------------
# Tests for GaussianCopulaMethod
# -------------------------------
class TestGaussianCopulaMethod(unittest.TestCase):
    def setUp(self):
        # Create a simple DataFrame with numerical and categorical columns.
        self.df = pd.DataFrame({
            "numeric": np.random.normal(50, 10, 100),
            "categorical": np.random.choice(["Red", "Green", "Blue"], 100)
        })
        self.metadata = {
            "numeric": "numerical",
            "categorical": "categorical"
        }
        # For simplicity, we use the DataProcessor to convert data to numeric space.
        self.processor = DataProcessor(self.metadata)
        self.processed = self.processor.preprocess(self.df)
        self.gc = GaussianCopulaMethod(self.metadata)
        self.gc.fit(self.processed)
    
    def test_sample_shape(self):
        # Use the sample method with a requested number of rows.
        num_samples = 50
        synthetic = self.gc.sample(num_samples)
        self.assertIsInstance(synthetic, pd.DataFrame)
        self.assertEqual(len(synthetic), num_samples)

    def test_get_learned_distributions(self):
        # After fitting, learned distributions should be available.
        distributions = self.gc.get_learned_distributions()
        self.assertIsInstance(distributions, dict)
        # Check that keys correspond to columns in metadata.
        for col in self.metadata.keys():
            self.assertIn(col, distributions)

if __name__ == "__main__":
    unittest.main()
