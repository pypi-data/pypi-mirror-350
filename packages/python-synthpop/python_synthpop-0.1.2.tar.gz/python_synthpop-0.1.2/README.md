![image](https://raw.githubusercontent.com/NGO-Algorithm-Audit/python-synthpop/b09d3fe93ac21406199810e39e2a844dc1faefd0/images/Header.png)

# python-synthpop

```python-synthpop``` is an open-source library for synthetic data generation (SDG). The library includes robust implementations of Classification and Regression Trees (CART) and Gaussian Copula (GC) synthesizers, equipping users with an open-source python library to generate high-quality, privacy-preserving synthetic data. This library is a Python implementation of the CART method used in R package [synthpop](https://cran.r-project.org/web/packages/synthpop/index.html).

Synthetic data is generated in six steps:

1. **Detect data types**: detect numerical, categorial and/or datetime data;
2. **Process missing data**: process missing data: remove or impute missing values;
3. **Preprocessing**: transforms data into numerical format;
4. **Synthesizer**: fit CART or GC;
5. **Postprocessing**: map synthetic data back to its original structure and domain;
6. **Evaluation metrics**: determine quality of synthetic data, e.g., similarity, utility and privacy metrics. 

☁️ [Web app](https://algorithmaudit.eu/technical-tools/sdg/#web-app) – a demo of synthetic data generation using `python-synthpop` in the browser using [WebAssembly](https://github.com/NGO-Algorithm-Audit/local-first-web-tool).

# Installation

#### Pip

```
pip install python-synthpop
```

#### Source

```
git clone https://github.com/NGO-Algorithm-Audit/python-synthpop.git
cd python-synthpop
pip install -r requirements.txt
python setup.py install
```

# Examples

#### Social Diagnosis 2011 dataset
We will use the [Social Diagnosis 2011](https://search.r-project.org/CRAN/refmans/synthpop/html/SD2011.html) dataset as an example, which is a comprehensive survey conducted in Poland. This dataset includes a wide range of variables related to the social and economic conditions of Polish households and individuals. It covers aspects such as income, employment, education, health, and overall quality of life. 

```
In [1]:  import pandas as pd

In [2]:  df = pd.read_csv('../datasets/socialdiagnosis/data/SocialDiagnosis2011.csv', sep=';')
         df.head()
Out[2]:
	sex	age	marital	income	ls	smoke
0	FEMALE	57	MARRIED	800.0	PLEASED	NO
1	MALE	20	SINGLE	350.0	MOSTLY SATISFIED	NO
2	FEMALE	18	SINGLE	NaN	PLEASED	NO
3	FEMALE	78	WIDOWED	900.0	MIXED	NO
4	FEMALE	54	MARRIED	1500.0	MOSTLY SATISFIED	YES

```

### python-synthpop

Using default parameters the six steps are applied on the Social Diagnosis example to generate synthetic data. See also the corresponding [notebook](./example_notebooks/00_readme.ipynb).

```
In [1]:     from synthpop import MissingDataHandler, DataProcessor, CARTMethod

In [2]:     # 1. Initiate metadata
            md_handler = MissingDataHandler()

            # 1.1 Get data types
            metadata= md_handler.get_column_dtypes(df)
            print("Column Data Types:", metadata)

            Column Data Types: {'sex': 'categorical', 'age': 'numerical', 'marital': 'categorical', 'income': 'numerical', 'ls': 'categorical', 'smoke': 'categorical'}

In [3]:     # 2. Process missing data
            print("Missing data:")
            print(df.isnull().sum())

            Missing data:
            sex          0
            age          0
            marital      9
            income     683
            ls           8
            smoke       10
            dtype: int64

In [4]:     # 2.1 Detect type of missingness
            missingness_dict = md_handler.detect_missingness(df)
            print("Detected missingness type:", missingness_dict)

            Detected missingness type: {'marital': 'MAR', 'income': 'MAR', 'ls': 'MAR', 'smoke': 'MAR'}


In [5]:     # 2.2 Impute missing values
            real_df = md_handler.apply_imputation(df, missingness_dict)

            print("Missing data:")
            print(real_df.isnull().sum())

            Missing data:
            sex        0
            age        0
            marital    0
            income     0
            ls         0
            smoke      0
            dtype: int64


In [6]:     # 3. Preprocessing: Instantiate the DataProcessor with column_dtypes
            processor = DataProcessor(metadata)

            # 3.1 Preprocess the data: transforms raw data into a numerical format
            processed_data = processor.preprocess(real_df)
            print("Processed data:")
            display(processed_data.head())

            Processed data:
            sex	age	marital	income	ls	smoke
            0	0	0.503625	3	-0.517232	4	0
            1	1	-1.495187	4	-0.898113	3	0
            2	0	-1.603231	4	0.000000	4	0
            3	0	1.638086	5	-0.432591	1	0
            4	0	0.341559	3	0.075251	3	1


In [7]:     # 4. Fit the CART method
            cart = CARTMethod(metadata, smoothing=True, proper=True, minibucket=5, random_state=42)
            cart.fit(processed_data)

In [8]:     # 4.1 Preview generated synthetic data
            synthetic_processed = cart.sample(100)
            print("Synthetic processed data:")
            display(synthetic_processed.head())

            Synthetic processed data:
            sex	age	marital	income	ls	smoke
            0	1	-1.087360	3	-1.201126	4	0
            1	1	-0.882289	3	1.182255	4	0
            2	0	1.449201	5	-0.255936	2	0
            3	0	0.890598	3	0.220739	4	1
            4	0	0.313502	3	1.395039	4	0

In [9]:     # 5. Postprocessing: back to the original format and preview of data
            synthetic_df = processor.postprocess(synthetic_processed)
            print("Synthetic data in original format:")
            display(synthetic_df.head())

            Synthetic data in original format:
            sex	age	marital	income	ls	smoke
            0	FEMALE	30.377064	SINGLE	-8.000000	MOSTLY DISSATISFIED	NO
            1	MALE	54.823585	MARRIED	1861.809802	PLEASED	YES
            2	FEMALE	78.641244	MARRIED	771.239134	MOSTLY DISSATISFIED	NO
            3	MALE	53.458122	MARRIED	1758.942347	PLEASED	NO
            4	FEMALE	60.354551	SINGLE	1024.351794	PLEASED	NO

In [10]:    from synthpop.metrics import (
                MetricsReport,
                EfficacyMetrics,
                DisclosureProtection
            )

In [11]:    # 6. Evaluate the synthetic data

            # 6.1 Diagnostic report
            report = MetricsReport(real_df, synthetic_df, metadata)
            report_df = report.generate_report()
            print("=== Diagnostic Report ===")
            display(report_df)

            	column	type	missing_value_similarity	range_coverage	boundary_adherence	ks_complement	tv_complement	statistic_similarity	category_coverage	category_adherence
                0	sex	categorical	1.0	N/A	N/A	N/A	0.9764	N/A	1.0	1.0
                1	age	numerical	1.0	0.94757	1.0	0.9142	N/A	0.962239	N/A	N/A
                2	marital	categorical	1.0	N/A	N/A	N/A	0.967	N/A	0.666667	1.0
                3	income	numerical	1.0	0.408926	1.0	0.9056	N/A	0.948719	N/A	N/A
                4	ls	categorical	1.0	N/A	N/A	N/A	0.9224	N/A	0.857143	1.0
                5	smoke	categorical	1.0	N/A	N/A	N/A	0.9754	N/A	1.0	1.0

In [12]:    # 6.2 Efficacy metrics

            # 6.2.1 Regression
            reg_efficacy = EfficacyMetrics(task='regression', target_column="income")
            reg_metrics = reg_efficacy.evaluate(real_df, synthetic_df)
            print("=== Regression Efficacy Metrics ===")
            print(reg_metrics)

            === Regression Efficacy Metrics ===
            {'mse': 1669726.6979087007, 'mae': 904.2202005090558, 'r2': -0.19619130295207743}

In [13]:    # 6.2.2 Classification
            clf_efficacy = EfficacyMetrics(task='classification', target_column="smoke")
            clf_metrics = clf_efficacy.evaluate(real_df, synthetic_df)
            print("\n=== Classification Efficacy Metrics ===")
            print(clf_metrics)

            === Classification Efficacy Metrics ===
            {'accuracy': 0.6058, 'f1_score': 0.6184739077074358}

In [14]:    # 6.3 Privacy
            dp = DisclosureProtection(real_df, synthetic_df)
            dp_score = dp.score()
            dp_report = dp.report()

            print("\n=== Disclosure Protection ===")
            print(f"Score: {dp_score:.3f}")
            print("Detailed Report:", dp_report)

            === Disclosure Protection ===
            Score: 1.000
            Detailed Report: {'threshold': 0.0, 'risk_rate': 0.0, 'disclosure_protection_score': 1.0}
```