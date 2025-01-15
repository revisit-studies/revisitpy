import src.revisit.revisit as rvt

import altair as alt
import numpy as np
from scipy.special import erfinv, erf
import pandas as pd
import random
import itertools
import vl_convert as vlc


alt.renderers.set_embed_options(actions=False)


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


def component_function(visType=None, numPoints=None, corrValues=None):

    if corrValues is not None and visType is not None and numPoints is not None:

        # Convert NumPy array to a DataFrame
        data1 = pd.DataFrame(
            generate_correlated_data_uniform(corrValues[0], numPoints, seed=42),
            columns=['X', 'Y']
        )
        data2 = pd.DataFrame(
            generate_correlated_data_uniform(corrValues[1], numPoints, seed=42),
            columns=['X', 'Y']
        )
        
        hover = alt.selection_point(
            on="mouseover",  # Trigger the selection on hover
            nearest=False,    # Select the nearest point
            empty="none"     # Do not highlight if no point is hovered
        )
        
                # Create two scatter plots
        scatter1 = alt.Chart(data1).mark_point(fill='steelblue').encode(
            x=alt.X('X:Q', axis=alt.Axis(grid=False)),  # Disable grid lines for X-axis
            y=alt.Y('Y:Q', axis=alt.Axis(grid=False)),   # Disable grid lines for Y-axis
            color=alt.condition(hover, alt.value("red"), alt.value("blue")),  # Change color on hover
            size=alt.condition(hover, alt.value(100), alt.value(50))          
        ).add_params(
            hover  # Add the hover selection
        ).properties(
            title='Scatter Plot 1',
            width=300,
            height=300,
        )
        
        # scatter1.display_options = {"actions": False}

        # scatter2 = alt.Chart(data2).mark_point().encode(
            # x=alt.X('X:Q', axis=alt.Axis(grid=False)),  # Disable grid lines for X-axis
            # y=alt.Y('Y:Q', axis=alt.Axis(grid=False))   # Disable grid lines for Y-axis
        # ).properties(
        #     title='Scatter Plot 2',
        #     width=300,
        #     height=300
        # )

        # Horizontally concatenate the plots
        # chart = scatter1 | scatter2

        vega_lite_spec = scatter1.to_json()
        vega_spec = vlc.vegalite_to_vega(vega_lite_spec, vl_version="5.20")
        
        # vega_spec['signals'].append(
        #       {
        #         "name": "revisitAnswer",
        #         "value": {},
        #         "on": [
        #         {
        #             "events": "symbol:click",
        #             "update": "{responseId: 'vegaDemoResponse1', response: 'left'}"
        #         }
        #         ]
        #     }
        # )
        
        vega_spec['signals'].append(
            {
                "name": "revisitAnswer",
                "value": {},
                "on": [
                    {
                        "events": "symbol:mouseover",
                        "update": "{responseId: 'vegaDemoResponse1', response: 'left'}"
                    },
                    {
                        "events": "symbol:mouseout",
                        "update": "{responseId: 'vegaDemoResponse1', response: 'right'}"
                    },
                ]
            }
        )
        
    #           {
    #     "name": "hoveredSymbol",
    #     "value": null,
    #     "on": [
    #       {
    #         "events": "symbol:mouseover",
    #         "update": "datum"
    #       },
    #       {
    #         "events": "symbol:mouseout",
    #         "update": "null"
    #       }
    #     ]
    #   }
        
        
        
        return rvt.component(
            type='vega',
            # config=vega_spec,
            path='./assets/vegademo1.specs.json',
            component_name__=f'{visType}-{numPoints}-{round(corrValues[0],1)},{round(corrValues[1],1)}',
            response=[
                rvt.response(
                    **{ 
                    "id": "vegaDemoResponse1",
                    "prompt": "You selected:",
                    "location": "sidebar",
                    "type": "iframe",
                    "required":True
                    },
                       
                )
            ]
        )

    return rvt.component(
        type='questionnaire',
        component_name__='blank-component'
    )


# Generate all combinations of two values between 1 and 10
combinations = itertools.combinations(range(1, 11), 2)

# Create the dataset with values divided by 10
dataSet = [{'corrValues': [x / 10, y / 10]} for x, y in combinations]
dataSet = dataSet[:10]
# Create the dataset with values divided by 10


# dataSet = [{'corrValues': [random.random(),random.random()]} for i in range(100)]

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
    ).permute(
        factors=[{'numPoints': 10}, {'numPoints': 10}],
        order='fixed',
    ).permute(
        factors=dataSet,
        order='random',
        numSamples=50,
        component_function=component_function
    )

study = rvt.studyConfig(
    schema="https://raw.githubusercontent.com/revisit-studies/study/v2.0.0-rc1/src/parser/StudyConfigSchema.json",
    uiConfig=ui_config,
    studyMetadata=study_metadata,
    sequence=sequence
)

print(study)
