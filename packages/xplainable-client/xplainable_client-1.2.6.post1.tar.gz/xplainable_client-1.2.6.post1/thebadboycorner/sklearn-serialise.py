from sklearn.pipeline import Pipeline
from sklearn.pipeline import *
from sklearn.compose import *
from sklearn.preprocessing import *
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


def serialize_pipeline(pipeline: Pipeline):
    """Extracts the state of the pipeline via __getstate__, handling nested pipelines and column transformers."""
    assert isinstance(pipeline, Pipeline), f"pipeline not of type sklearn.Pipeline: {type(pipeline)}"

    state = {"class": pipeline.__class__}
    steps = []
    for name, step in pipeline.steps:
        if isinstance(step, Pipeline):
            steps.append(serialize_pipeline(step))
        elif isinstance(step, ColumnTransformer):
            steps.append(serialize_column_transformer(step))
        else:
            steps.append(
                {
                    'class': step.__class__,
                    'state': step.__getstate__(),
                }
            )
    state.update(
        {"steps": steps}
    )
    return state


def serialize_column_transformer(ct):
    print(ct)
    return ct
    """Serializes a ColumnTransformer, handling nested transformers."""
    state = {}
    state['class'] = ct.__class__
    state['transformers'] = []
    for name, transformer, columns in ct.transformers:
        if transformer == 'drop' or transformer == 'passthrough':
            transformer_state = transformer
        elif isinstance(transformer, Pipeline):
            transformer_state = serialize_pipeline(transformer)
        elif isinstance(transformer, ColumnTransformer):
            transformer_state = serialize_column_transformer(transformer)
        else:
            transformer_state = {
                'class': transformer.__class__,
                'state': transformer.__getstate__(),
            }
        state['transformers'].append((name, transformer_state, columns))
    # Store additional attributes of ColumnTransformer
    state['remainder'] = ct.remainder
    state['sparse_threshold'] = ct.sparse_threshold
    state['n_jobs'] = ct.n_jobs
    state['transformer_weights'] = ct.transformer_weights
    state['verbose'] = ct.verbose
    state['verbose_feature_names_out'] = ct.verbose_feature_names_out
    return state


def deserialize_pipeline(state):
    """Reconstructs the pipeline from the state via __setstate__, handling nested pipelines and column transformers."""
    pipeline_class = state['class']
    steps = []
    for name, step_state in state['steps']:
        if step_state['class'] == Pipeline:
            # It's a nested pipeline
            step = deserialize_pipeline(step_state)
        elif step_state['class'] == ColumnTransformer:
            # It's a ColumnTransformer
            step = deserialize_column_transformer(step_state)
        else:
            # Reconstruct the estimator
            step_class = step_state['class']
            step = step_class.__new__(step_class)
            step.__setstate__(step_state['state'])
        steps.append((name, step))
    pipeline = pipeline_class(steps=steps)
    return pipeline


def deserialize_column_transformer(state):
    """Deserializes a ColumnTransformer from its state."""
    ct_class = state['class']
    transformers = []
    for name, transformer_state, columns in state['transformers']:
        if transformer_state == 'drop' or transformer_state == 'passthrough':
            transformer = transformer_state
        elif transformer_state['class'] == Pipeline:
            transformer = deserialize_pipeline(transformer_state)
        elif transformer_state['class'] == ColumnTransformer:
            transformer = deserialize_column_transformer(transformer_state)
        else:
            transformer_class = transformer_state['class']
            transformer = transformer_class.__new__(transformer_class)
            transformer.__setstate__(transformer_state['state'])
        transformers.append((name, transformer, columns))
    # Reconstruct the ColumnTransformer
    ct = ct_class(transformers=transformers,
                  remainder=state.get('remainder', 'drop'),
                  sparse_threshold=state.get('sparse_threshold', 0.3),
                  n_jobs=state.get('n_jobs', None),
                  transformer_weights=state.get('transformer_weights', None),
                  verbose=state.get('verbose', False),
                  verbose_feature_names_out=state.get('verbose_feature_names_out', True))
    return ct



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

# print(pipeline)
# print(pipeline.steps)
# print()


print(serialize_pipeline(pipeline))
