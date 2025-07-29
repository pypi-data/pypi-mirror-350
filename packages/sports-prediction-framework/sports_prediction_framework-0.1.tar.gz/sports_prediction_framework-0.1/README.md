# Sports Prediction Framework

A modular and extensible machine learning framework for predicting sports outcomes and evaluating betting strategies.

This framework enables seamless data ingestion, model training, prediction, and betting simulation for sports analytics. Designed for research, experimentation, and scalable deployment, it supports tabular and graph-based models, MLflow logging, and sophisticated evaluation tools.

## Features

- Support for multiple sports (e.g., matches and races)
- Plug-and-play architecture for custom data parsers, models, and strategies
- Built-in PyTorch-based models (`FlatModel`, `GNNModel`)
- MLflow integration for parameter and metric logging
- Iterative training and testing via customizable scopes
- Built-in betting strategy simulations (Kelly, Sharpe, Flat)
- Clean abstractions (`DataWrapper`, `Trainer`, `Learner`, etc.)
- Easily extendable for new formats, models, and evaluation methods


## Installation

Install the framework locally:

```bash
pip install .
```

## Example usage

!! The framework uses database configuration from the .env file in your current working directory.
```bash
python sports_prediction_framework/examples/simulation_example.py
```


## End-to-End Example

This example demonstrates how to:

- Load and filter data
- Apply a transformer
- Define training/testing scopes
- Initialize a model
- Run a learner with nested updating
- Obtain predictions

```python
# 1. Load data with filter
func = lambda c: or_(c.Lge == "GER1", c.Lge == "ENG1")
dw = DataLoader.load_and_wrap("isdb", "Matches", func, SportType.FOOTBALL)

# 2. Transform the data
t = Transformer()
dw = t.transform(dw)

# 3. Define training and testing scopes
train_params = {'col': 'Season', 'start': 2000, 'max': 2002, 'size': 1, 'stride': 1}
test_params = {'col': 'Season', 'start': 2000, 'max': 2002, 'size': 1, 'stride': 1}

relevant_scope = [WindowSelector(ScopeExpander(dw, train_params))]
prediction_scope = [WindowSelector(ScopeExpander(dw, test_params))]
scope = DataSelector(relevant_scope, prediction_scope)

# 4. Define model parameters
model_params = {
    'embed_dim': 32,
    'out_dim': 3,
    'n_dense': 4,
    'dense_dim': 64,
    'architecture_type': 'rectangle',
    'batch_size': 64,
}
flat = FlatModel(model_params)

# 5. Define learners
l1 = Learner(Trainer(flat), Tester(flat), scope)
l = UpdatingLearner(Trainer(flat), Tester(flat), scope, [l1])

# 6. Run and get predictions
prob = l.compute(dw)
print(prob.get_dataframe())
```