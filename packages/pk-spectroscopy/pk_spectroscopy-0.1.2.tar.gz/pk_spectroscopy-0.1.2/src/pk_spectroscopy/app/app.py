import os
import io
import csv

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pk_spectroscopy import pK_Spectroscopy, TitrationMode

# Change app page parameters
st.set_page_config(page_title='pK Spectroscopy')

st.title('pK spectroscopy app')
st.markdown('[Get more detail in Github repository ➡](https://github.com/Sciencealone/pk_spectroscopy)')

# Select titration mode
titration_mode_label = st.sidebar.radio('Select titration mode', ('Volumetric', 'Coulometric'))
if titration_mode_label == 'Volumetric':
    titration_mode = TitrationMode.VOLUMETRIC
else:
    titration_mode = TitrationMode.COULOMETRIC

# Explain the data format
with st.sidebar.expander('Data format explanation', expanded=False):
    st.write('''
    - CSV file with separators **semicolons (;)**
    - line 1: **name (optional)**
    - line 2: **sample volume (ml)**
    - line 3: **titrant concentration (M)** for volumetric mode or **titration current (A)** for coulometric mode
    - lines 4+: **titration data: volume-pH or time-pH**
    '''
    )

# Load source data
uploaded_file = st.sidebar.file_uploader('Load sample data in CSV format', type='csv')
if uploaded_file is not None:
    string_io = io.StringIO(uploaded_file.getvalue().decode('utf-8'))
    reader = csv.reader(string_io, delimiter=';')
    row_counter = 0
    volumes = []
    ph_values = []
    sample_name = ''
    sample_volume = None
    alkaline_concentration = None
    for row in reader:
        if row_counter == 0:
            sample_name = row[0]
        elif row_counter == 1:
            sample_volume = float(row[0])
        elif row_counter == 2:
            alkaline_concentration = float(row[0])
        else:
            volume, ph = row[0], row[1]
            volumes.append(float(volume))
            ph_values.append(float(ph))
        row_counter += 1

    st.sidebar.markdown('''---''')
    if titration_mode == 'Volumetric':
        parameters = [
            ('Sample name', sample_name),
            ('Sample volume', sample_volume),
            ('Alkaline concentration', alkaline_concentration),
            ('Data points', len(volumes))
        ]
    else:
        parameters = [
            ('Sample name',sample_name),
            ('Sample volume', sample_volume),
            ('Current', alkaline_concentration),
            ('Data points', len(volumes))
        ]

    for label, item in parameters:
            st.sidebar.write(f'{label}: {item}')

    # Create the pk-spectroscopy class instance and make the computations
    pks = pK_Spectroscopy(mode=titration_mode)
    pks.load_data(sample_volume, alkaline_concentration, volumes, ph_values)

    # Display titration curve expander
    with st.expander('Source data'):
        # Check we have any data
        if len(volumes) > 0:
            title = 'Titration curve'
            if sample_name:
                title = f'{title} ({sample_name})'

            if titration_mode == TitrationMode.VOLUMETRIC:
                x_axis_label = 'Titrant volume, ml'
                x_values = volumes
            else:
                x_axis_label = 'Titration time, s'
                x_values = volumes

            fig = px.line(
                pd.DataFrame({x_axis_label:x_values, 'pH': ph_values}),
                x=x_axis_label,
                y='pH',
            )
            fig.add_trace(
                go.Scatter(
                    x=x_values[:pks.valid_points],
                    y=ph_values[:pks.valid_points],
                    mode='markers',
                    name='Valid data',
                ),
            )
            st.plotly_chart(fig, key='titration')
        else:
            st.write('Not enough data!')

    # Gather main control variables expander
    with st.expander('Parameters', expanded=True):
        pk_start = st.number_input('Start pK (0 recommended):', value=0., min_value=0., max_value=10.)
        pk_end = st.number_input('End pK (10 recommended):', value=10., min_value=0., max_value=10.)
        d_pk = st.number_input('pK step (0.05-0.1 recommended):', value=.05, min_value=0., max_value=1.)
        integration_constant = st.checkbox('Use integration constant (recommended).', value=True)

    # Check values
    if pk_start > pk_end:
        pk_start, pk_end = pk_end, pk_start
    if d_pk > pk_end - pk_start:
        d_pk = 0.05

    # Get results
    peaks, error = pks.make_calculation(pk_start, pk_end, d_pk, integration_constant)

    # Check results for validity
    if peaks is None:
        st.error('Error in calculations! Please check the titration mode, source data, and parameters.')
    else:
        # Display the results
        result_df = pd.DataFrame(peaks)
        result_df = result_df[['concentration', 'mean', 'interval']].copy()
        if not result_df.empty:
            with st.expander('Results', expanded=True):
                st.write('Peaks:')
                st.write(result_df)

                # Provide download data
                prefix, ext = os.path.splitext(uploaded_file.name)
                csv = result_df.to_csv().encode('utf-8')
                st.download_button(
                    'Download table (CSV)',
                    csv,
                    prefix + '.csv',
                    'text/csv',
                    key='download-csv'
                )
                st.write(f'Error: {error:.5}')

                # Plot chart
                fig = px.bar(
                    result_df,
                    x='mean',
                    y='concentration',
                    range_x=[pk_start, pk_end],
                )
                fig.update_traces(width=d_pk)
                st.plotly_chart(fig, key='pk_spectrum')

else:
    st.write('⬅ Waiting for a data file in the sidebar.')
