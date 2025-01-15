import marimo

__generated_with = "0.10.13"
app = marimo.App()


@app.cell
def _():
    import revisit as rvt
    import altair as alt
    import numpy as np
    from scipy.special import erfinv, erf
    import pandas as pd
    import random
    import itertools
    import vl_convert as vlc

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
            random.shuffle(corrValues)
            # Convert NumPy array to a DataFrame
            data1 = pd.DataFrame(
                generate_correlated_data_uniform(corrValues[0], numPoints, seed=42),
                columns=['X', 'Y']
            )
            data2 = pd.DataFrame(
                generate_correlated_data_uniform(corrValues[1], numPoints, seed=42),
                columns=['X', 'Y']
            )
            
            # Create Scatter plot 1
            scatter1 = alt.Chart(data1).mark_point(fill='black', stroke='black').encode(
                x=alt.X('X:Q', axis=alt.Axis(
                    labels=False,
                    ticks=False,
                    grid=False,
                    domain=True,
                    title=None

                )),
                y=alt.Y('Y:Q', axis=alt.Axis(
                    labels=False,
                    ticks=False,
                    grid=False,
                    domain=True,
                    title=None
                ))
            ).properties(
                title='',
                width=300,
                height=300,
            )
            
            # Create Scatter plot two
            scatter2 = alt.Chart(data2).mark_point(fill='black', stroke='black').encode(
                x=alt.X('X:Q', axis=alt.Axis(
                    labels=False,
                    ticks=False,
                    grid=False,
                    domain=True,
                    title=None

                )),
                y=alt.Y('Y:Q', axis=alt.Axis(
                    labels=False,
                    ticks=False,
                    grid=False,
                    domain=True,
                    title=None
                ))
            ).properties(
                title='',
                width=300,
                height=300
            )

            # Horizontally concatenate the plots
            chart = alt.hconcat(
                scatter1,
                scatter2
            ).configure_view(
                strokeWidth=0,  
                continuousWidth=300,  
                continuousHeight=300, 
                step=50               
            ).configure_concat(
                spacing=50  
            )

            vega_lite_spec = chart.to_json()
            vega_spec = vlc.vegalite_to_vega(vega_lite_spec, vl_version="5.20")
            
            # Update Signals
            vega_spec['config']["signals"] = [
                {
                    "name": "revisitAnswer",
                    "value": {},
                    "on": [
                        {
                            "events": "@concat_0_group:click",
                            "update": "{responseId: 'vegaDemoResponse1', response: 'left'}"
                        },
                        {
                            "events": "@concat_1_group:click",
                            "update": "{responseId: 'vegaDemoResponse1', response: 'right'}"
                        },
                        {
                            "events": {"source": "window", "type": "keydown"},
                            "update": "event.key === 'ArrowLeft' ? {responseId: 'vegaDemoResponse1', response: 'left'} : event.key === 'ArrowRight' ? {responseId: 'vegaDemoResponse1', response: 'right'} : revisitAnswer"
                        },
                    ]
                }
            ]
            
            # Add signal based bordering
            for entry in vega_spec['marks']:
                if entry['name'] == 'concat_0_group':
                    condition = 'left'
                else:
                    condition = 'right'
                entry['encode']['update']['stroke'] = {
                    "signal": f"revisitAnswer.response === '{condition}' ? 'blue' : null"
                },
                entry['encode']['update']['strokeWidth'] = {
                    "signal": f"revisitAnswer.response === '{condition}' ? 3 : 0"
                }
            
            return rvt.component(
                type='vega',
                config=vega_spec,
                component_name__=f'{visType}-{numPoints}-{round(corrValues[0],1)},{round(corrValues[1],1)}',
                response=[
                    rvt.response(
                        id='vegaDemoResponse1',
                        prompt='You Selected: ',
                        location='sidebar',
                        type='iframe',
                        required=True
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
    # Create the dataset with values divided by 10



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

    sequence = rvt.sequence(order='fixed')


    sequence.permute(
            factors=[{'visType': 'scatterPlot'}, {'visType': 'parallelCoords'}],
            order='latinSquare',
        ).permute(
            factors=[{'numPoints': 20}, {'numPoints': 100}],
            order='fixed',
        ).permute(
            factors=dataSet,
            order='random',
            component_function=component_function
        )

    study = rvt.studyConfig(
        schema="https://raw.githubusercontent.com/revisit-studies/study/v2.0.0-rc1/src/parser/StudyConfigSchema.json",
        uiConfig=ui_config,
        studyMetadata=study_metadata,
        sequence=sequence
    )

    print(study)
    return (
        alt,
        combinations,
        component_function,
        dataSet,
        erf,
        erfinv,
        generate_correlated_data_uniform,
        itertools,
        np,
        pd,
        random,
        rvt,
        sequence,
        study,
        study_metadata,
        ui_config,
        vlc,
    )


if __name__ == "__main__":
    app.run()

