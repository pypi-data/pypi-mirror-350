# Galtea SDK

<p align="center">
  <img src="https://galtea.ai/img/galtea_mod.png" alt="Galtea" width="500" height="auto"/>
</p>

<p align="center">
  <strong>Comprehensive AI/LLM Testing & Evaluation Framework</strong>
</p>

<p align="center">
	<a href="https://pypi.org/project/galtea/">
		<img src="https://img.shields.io/pypi/v/galtea.svg" alt="PyPI version">
	</a>
	<a href="https://pypi.org/project/galtea/">
		<img src="https://img.shields.io/pypi/pyversions/galtea.svg" alt="Python versions">
	</a>
	<a href="https://www.apache.org/licenses/LICENSE-2.0">
		<img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License">
	</a>
</p>

## Overview

Galtea SDK empowers AI engineers, ML engineers and data scientists to rigorously test and evaluate their AI/LLM models. With a focus on reliability and transparency, Galtea offers:

1. **Automated Test Dataset Generation** - Create comprehensive test datasets tailored to your AI application
2. **Sophisticated Model Evaluation** - Evaluate your locally deployed models across multiple dimensions

## Installation

```bash
pip install galtea
```

## Quick Start

```python
from galtea import Galtea
import os

# Initialize with your API key
galtea = Galtea(api_key=os.getenv("GALTEA_API_KEY"))

# Create a test
test = galtea.tests.create(
    name="factual-accuracy-test",
    type="QUALITY",
    product_id="your-product-id",
    ground_truth_file_path="path/to/ground-truth.pdf"
)

# Create a model version to evaluate
version = galtea.versions.create(
    name="gpt-4-self-hosted-v1",
    product_id="your-product-id",
    optional_props={
        "description": "Self-hosted GPT-4 equivalent model",
        "endpoint": "http://your-model-endpoint.com/v1/chat"
    }
)

# Set up an evaluation
evaluation = galtea.evaluations.create(
    test_id=test.id,
    version_id=version.id
)

# Run the evaluation with your model's outputs
galtea.evaluation_tasks.create(
    metrics=["factual-accuracy", "coherence", "relevance"],
    evaluation_id=evaluation.id,
    input="What is the capital of France?",
    actual_output="The capital of France is Paris.",
    expected_output="Paris is the capital of France.",
    context="From Wikipedia: Paris is the capital and most populous city of France..."
)
```

## Core Features

### 1. Automated Test Dataset Generation

Create comprehensive test datasets to validate your AI/LLM models:

- **Quality Tests**: Assess response quality, coherence, and factual accuracy
- **Adversarial Tests**: Stress-test your models against edge cases and potential vulnerabilities
- **Ground Truth Integration**: Upload ground truth documents to validate factual responses
- **Custom Test Types**: Define tests tailored to your specific use cases and requirements

```python
# Create a custom test with your own dataset
test = galtea.tests.create(
    name="medical-knowledge-test",
    type="QUALITY",
    product_id="your-product-id",
    ground_truth_file_path="medical_reference.pdf"
)
```

### 2. Comprehensive Model Evaluation

Evaluate your locally deployed models with sophisticated metrics:

- **Multi-dimensional Analysis**: Analyze outputs across various dimensions including accuracy, relevance, and coherence
- **Customizable Metrics**: Define your own evaluation criteria and rubrics
- **Batch Processing**: Run evaluations on large datasets efficiently
- **Detailed Reports**: Get comprehensive insights into your model's performance

```python
# Define custom evaluation metrics
custom_metric = galtea.metrics.create(
    name="medical-accuracy",
    evaluation_steps=[
        "check for medical terminology correctness",
        "verify against medical literature",
        "assess recommendations against standard protocols"
    ]
)

# Run batch evaluation
import pandas as pd

# Load your test data
test_data = pd.read_json("medical_queries.json")

# Evaluate each query with your model
for _, row in test_data.iterrows():
    # Get response from your model (implementation depends on your setup)
    model_response = your_model.generate_response(row["query"])

    # Evaluate the response
    galtea.evaluation_tasks.create(
        metrics=["medical-accuracy", "coherence", "toxicity"],
        evaluation_id=evaluation.id,
        input=row["query"],
        actual_output=model_response,
        expected_output=row["expected_answer"],
        context=row["medical_context"]
    )
```

## Managing Your AI Products

Galtea provides a complete ecosystem for managing your AI products:

### Products

Represent your AI applications or models:

```python
# List your products
products = galtea.products.list()

# Select a product to work with
product = products[0]
```

### Versions

Track different versions or deployments of your models:

```python
# Create a new version of your model
version = galtea.versions.create(
    name="gpt-4-fine-tuned-v2",
    product_id=product.id,
    optional_props={
        "description": "Fine-tuned GPT-4 for medical domain",
        "foundational_model": "gpt-4",
        "system_prompt": "You are a helpful medical assistant..."
    }
)

# List versions of your product
versions = galtea.versions.list(product_id=product.id)
```

### Tests

Create and manage test datasets:

```python
# Create a test
test = galtea.tests.create(
    name="medical-qa-test",
    type="QUALITY",
    product_id=product.id,
    ground_truth_file_path="medical_data.pdf"
)

# Download a test file
test_file = galtea.tests.download(test, output_dir="tests")
```

### Evaluations

Link tests with model versions for evaluation:

```python
# Create an evaluation
evaluation = galtea.evaluations.create(
    test_id=test.id,
    version_id=version.id
)

# List evaluations for a product
evaluations = galtea.evaluations.list(product_id=product.id)
```

## Advanced Usage

### Custom Metrics

Define custom evaluation criteria specific to your needs:

```python
# Create a custom metric
custom_metric_1 = galtea.metrics.create(
    name="patient-safety-score-v1",
    evaluation_steps=[
        "check for dangerous recommendations",
        "assess completeness of safety warnings",
        "verify adherence to medical protocols"
    ]
)
custom_metric_2 = galtea.metrics.create(
    name="patient-safety-score-v2",
    criteria="Evaluate responses for patient safety considerations",
)
# You can only provide either evaluation_steps or criteria
```

### Batch Processing

Efficiently evaluate your model on large datasets:

```python
import pandas as pd
import os

# Load your test queries from a JSON file
queries_file = os.path.join(os.path.dirname(__file__), 'test_data.json')
df = pd.read_json(queries_file)

# Process each query
for idx, row in df.iterrows():
    # Get your model's response to the query
    model_response = call_your_model(row['query'])

    # Evaluate the response
    galtea.evaluation_tasks.create(
        metrics=["accuracy", "relevance", custom_metric.name],
        evaluation_id=evaluation.id,
        input=row['query'],
        actual_output=model_response,
        expected_output=row['expected_output'],
        context=row['context']
    )
```

## API Reference

### Main Classes

- **`Galtea`**: Main client for interacting with the Galtea platform

### Product Management

- **`galtea.products.list(offset=None, limit=None)`**: List available products
- **`galtea.products.get(product_id)`**: Get a specific product by ID

### Test Management

- **`galtea.tests.create(name, type, product_id, ground_truth_file_path=None, test_file_path=None)`**: Create a new test
- **`galtea.tests.get(test_id)`**: Retrieve a test by ID
- **`galtea.tests.list(product_id, offset=None, limit=None)`**: List tests for a product
- **`galtea.tests.download(test, output_dir)`**: Download test files in the selected directory.

### Test Cases Management

- **`galtea.test_cases.create(test_id, input, expected_output, context=None)`**: Create a new test case
- **`galtea.test_cases.get(test_case_id)`**: Get a test case by ID
- **`galtea.test_cases.list(test_id, offset=None, limit=None)`**: List test cases for a test
- **`galtea.test_cases.delete(test_case_id)`**: Delete a test case by ID

### Version Management

- **`galtea.versions.create(product_id, name, optional_props={})`**: Create a new model version
- **`galtea.versions.get(version_id)`**: Get a version by ID
- **`galtea.versions.list(product_id, offset=None, limit=None)`**: List versions for a product

### Metric Management

- **`galtea.metrics.create(name, criteria=None, evaluation_steps=None)`**: Create a custom metric
- **`galtea.metrics.get(metric_type_id)`**: Get a metric by ID
- **`galtea.metrics.list(offset=None, limit=None)`**: List available metrics

### Evaluation Management

- **`galtea.evaluations.create(test_id, version_id)`**: Create an evaluation
- **`galtea.evaluations.get(evaluation_id)`**: Get an evaluation by ID
- **`galtea.evaluations.list(product_id, offset=None, limit=None)`**: List evaluations for a product

### Evaluation Tasks Management

- **`galtea.evaluation_tasks.list(evaluation_id, offset=None, limit=None)`**: List tasks performed for an evaluation
- **`galtea.evaluation_tasks.get(evaluation_id, task_id)`**: Get a specific task by ID
- **`galtea.evaluation_tasks.create(evaluation_id, task_type, input, actual_output, expected_output=None, context=None)`** or **`galtea.evaluation_tasks.create(metrics, evaluation_id, input, actual_output, expected_output=None, context=None)`**: Create a new evaluation task which serves to evaluate model outputs

## Getting Help

- **Documentation**: [https://docs.galtea.ai/](https://docs.galtea.ai/)
- **Support**: [support@galtea.ai](mailto:support@galtea.ai)

## Authors

This software has been developed by the members of the product team of Galtea Solutions S.L.

## License

Apache License 2.0
