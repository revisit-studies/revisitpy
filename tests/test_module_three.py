import src.revisit.revisit as rvt
import altair as alt
import numpy as np
from scipy.special import erfinv, erf
import pandas as pd
import random


def generate_correlated_data_uniform(correlation, num_points, seed=None):
    """
    Generate a dataset with two variables having the specified correlation,
    with values bounded between 0 and 1.
    Parameters:
        correlation (float): Desired correlation coefficient (-1 to 1).
        num_points (int): Number of data points to generate.
        seed (int, optional): Random seed for reproducibility.
    Returns:
        np.ndarray: A 2D array of shape (num_points, 2), where each column is a variable.
    """
    if not -1 <= correlation <= 1:
        raise ValueError("Correlation must be between -1 and 1.")
    if seed is not None:
        np.random.seed(seed)
    # Generate two independent uniform random variables between 0 and 1
    x = np.random.rand(num_points)
    z = np.random.rand(num_points)
    # Apply inverse transform sampling to convert uniform to normal
    x_normal = np.sqrt(2) * erfinv(2 * x - 1)  # Inverse CDF of normal distribution
    z_normal = np.sqrt(2) * erfinv(2 * z - 1)
    # Combine them using the desired correlation
    y_normal = correlation * x_normal + np.sqrt(1 - correlation**2) * z_normal
    # Transform back to uniform distribution using normal CDF
    x_uniform = 0.5 * (1 + erf(x_normal / np.sqrt(2)))
    y_uniform = 0.5 * (1 + erf(y_normal / np.sqrt(2)))
    # Stack into a 2D array
    data = np.column_stack((x_uniform, y_uniform))
    return data


def component_function(visType=None, numPoints=None, corrValue=None):

    if corrValue is not None and visType is not None and numPoints is not None:

        # Convert NumPy array to a DataFrame
        data = pd.DataFrame(
            generate_correlated_data_uniform(corrValue, numPoints, seed=42),
            columns=['X', 'Y']
        )

        # Create the scatter plot
        chart = alt.Chart(data).mark_point().encode(
            x='X:Q',
            y='Y:Q'
        ).properties(
            title='Scatter Plot with Random Values',
            width=400,
            height=300
        )

        vega_spec = chart.to_dict()

        return rvt.component(
            type='vega',
            config=vega_spec,
            component_name__=f'vega-chart-{visType}-{numPoints}-{corrValue}'
        )

    return rvt.component(
        type='questionnaire',
        component_name__='blank-component'
    )




dataSet = [{'corrValue': random.random()} for i in range(100)]

study_metadata = rvt.studyMetadata(
    authors=["Brian Bollen"],
    organizations=["Visualization Design La"],
    title='Showcasing revisit-py',
    description='',
    date='2025-01-13',
    version='1.0'
)

ui_config = rvt.uiConfig(
  contactEmail="briancbollen@gmail.com",
  logoPath="./assets/revisitLogoSquare.svg",
  sidebar=True,
  withProgressBar=False
)

comp = rvt.component(
    component_name__='test-comp',
    type='website',
    path='fake-path'
)

sequence = rvt.sequence(order='fixed', components=[comp])


sequence.permute(
        factors=[{'visType': 'scatterPlot'}, {'visType': 'parallelCoords'}],
        order='latinSquare',
        numSamples=1
    ).permute(
        factors=[{'numPoints': 20}, {'numPoints': 100}],
        order='fixed',
    ).permute(
        factors=dataSet,
        order='random',
        component_function=component_function
    )

study = rvt.studyConfig(
    schema='fake-schema',
    uiConfig=ui_config,
    studyMetadata=study_metadata,
    sequence=sequence
)

print(study)