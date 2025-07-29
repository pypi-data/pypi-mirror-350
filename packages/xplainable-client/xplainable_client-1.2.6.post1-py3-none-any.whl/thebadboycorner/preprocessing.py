from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import *
from sklearn.compose import *
from sklearn.preprocessing import *
import pandas as pd
import pickle
import inspect


def remove_column(column_name: list[str]):
    return lambda x: x.drop([column_name])


df = pd.read_csv('telco_customer_churn.csv')

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

x, y = df.drop('Churn', axis=1), df['Churn']
x = x[["SeniorCitizen", "MonthlyCharges"]]
print(x.columns)


# Create a column transformer to drop the 'senior citizen' column
preprocessor = ColumnTransformer(
    transformers=[
        # ('drop_senior_citizen', FunctionTransformer(remove_column(["SeniorCitizen"])), ['SeniorCitizen']),
        ('minmax_age', MinMaxScaler(), ['MonthlyCharges'])  # Apply MinMaxScaler to the 'age' column
    ],
    remainder='passthrough'  # Keep other columns as is
)


# Define the full pipeline with the preprocessor
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    # Add any other steps like scaling, model training, etc.
])


import json
import inspect
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler
import inspect


def serialize_function(func):
    """Serialize a function by capturing its source code."""
    try:
        source = inspect.getsource(func)
    except OSError:
        source = None
    func_name = func.__name__
    func_module = func.__module__
    return {
        '__class__': 'function',
        '__module__': func_module,
        '__name__': func_name,
        '__source__': source
    }


def deserialize_function(data):
    """Deserialize a function from its serialized representation."""
    func_name = data['__name__']
    func_module = data['__module__']
    source = data.get('__source__')
    if source:
        # Recreate the function from source code
        # Warning: using exec is potentially dangerous
        namespace = {}
        exec(source, namespace)
        func = namespace.get(func_name)
        if func is None:
            raise ValueError(f"Function {func_name} not found in source")
        return func
    else:
        # Import the module and get the function
        module = __import__(func_module, fromlist=[func_name])
        func = getattr(module, func_name)
        return func


def serialize(obj):
    """Recursively serialize an object to a JSON-serializable structure."""
    print(type(obj))
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple, set)):
        return [serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {serialize(key): serialize(value) for key, value in obj.items()}
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif inspect.isfunction(obj):
        return serialize_function(obj)
    elif isinstance(obj, FunctionTransformer):
        func_serialized = serialize(obj.func)
        state = obj.__dict__.copy()
        print(obj.__getstate__())
        print(state)
        state['func'] = func_serialized
        serialized_state = serialize(state)
        return {
            '__class__': obj.__class__.__name__,
            '__module__': obj.__class__.__module__,
            '__state__': serialized_state
        }
    else:
        print(1, type(obj))
        class_name = obj.__class__.__name__
        module = obj.__class__.__module__
        if hasattr(obj, '__getstate__'):
            state = obj.__getstate__()
        elif hasattr(obj, '__dict__'):
            state = obj.__dict__
        else:
            raise TypeError(f"Cannot serialize object of type {type(obj)}")
        print(obj.__getstate__())
        print(obj.__dict__)
        # print(state, '\n')
        serialized_state = serialize(state)
        return {
            '__class__': class_name,
            '__module__': module,
            '__state__': serialized_state
        }


def deserialize(data):
    """Recursively deserialize a JSON structure back into an object."""
    if isinstance(data, (int, float, str, bool, type(None))):
        return data
    elif isinstance(data, list):
        return [deserialize(item) for item in data]
    elif isinstance(data, dict):
        if data.get('__class__') == 'function':
            return deserialize_function(data)
        elif '__class__' in data and '__state__' in data and '__module__' in data:
            class_name = data['__class__']
            module_name = data['__module__']
            state = data['__state__']
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            obj = cls.__new__(cls)
            deserialized_state = deserialize(state)
            if isinstance(obj, FunctionTransformer):
                func_serialized = deserialized_state.get('func')
                if func_serialized:
                    func = deserialize(func_serialized)
                    deserialized_state['func'] = func
                obj.__dict__.update(deserialized_state)
            else:
                if hasattr(obj, '__setstate__'):
                    obj.__setstate__(deserialized_state)
                elif hasattr(obj, '__dict__'):
                    obj.__dict__.update(deserialized_state)
                else:
                    raise TypeError(f"Cannot set state for object of type {type(obj)}")
            return obj
        else:
            return {deserialize(key): deserialize(value) for key, value in data.items()}
    else:
        raise TypeError(f"Cannot deserialize type {type(data)}")


# Example usage:
# Define your custom function at the module level
def remove_column(col_name):
    return lambda X: X.drop(columns=[col_name])


print(pipeline)
print("\n\n")

# Serialize the pipeline
serialized_pipeline = serialize(pipeline)
serialized_json = json.dumps(serialized_pipeline)

# Deserialize the pipeline
deserialized_data = json.loads(serialized_json)
restored_pipeline = deserialize(deserialized_data)


print(restored_pipeline)
print("\n\n")





exit()

print(preprocessor.__getstate__())
print(preprocessor.__getstate__()["transformers"][0][1].__getstate__())
for k, v in preprocessor.__getstate__().items():
    print(k, type(v), v)

exit()
# Create a column transformer to drop the 'senior citizen' column
preprocessor = ColumnTransformer(
    transformers=[
        ('drop_senior_citizen', eval("FunctionTransformer(lambda X: X.drop(columns=['SeniorCitizen'], axis=1))"), ['SeniorCitizen']),
        ('minmax_age', MinMaxScaler(), ['MonthlyCharges'])  # Apply MinMaxScaler to the 'age' column
    ],
    remainder='passthrough'  # Keep other columns as is
)

print(preprocessor)
print()
print(inspect.getsource(remove_column))


a = lambda X: X.drop(columns=['SeniorCitizen'], axis=1)
print(a.__getstate__())

exit()
# Fit and transform the data using the pipeline
print(x)
pipeline.fit_transform(x)
print(pipeline.transform(x))
print(pipeline)
print('\n\n')
print(pipeline.__getstate__())

# print('\n\n')
# print(pickle.dumps(pipeline))
