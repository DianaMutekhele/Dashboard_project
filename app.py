# -*- coding: utf-8 -*-
"""App

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uhsXk_OcsFh81JO243EeFDkHxNF55Zi8
"""

import panel as pn
pn.extension()
def f(x):
  return x * x
pn.interact(f, x=10)

# Commented out IPython magic to ensure Python compatibility.
# %pip install hvplot panel pandas jupyterlab

from bokeh.sampledata.autompg import autompg_clean as df
import hvplot.pandas
import panel as pn
import holoviews as hv
hv.extension('bokeh')
pn.extension('tabulator')
PALETTE = ["#ff6f69", "#ffcc5c", "#88d8b0", ]

pn.extension()

import pandas as pd
bankdeposit = pd.read_csv("sample_data/bankdeposit.csv")

bankdeposit= bankdeposit.rename(columns={' December ':'December', ' 12th jan ':'12th_jan', ' 19th jan ':'19th-jan',' 26th jan ':'26th_jan', ' January ':'January', ' WK1 FEB ':'WK1_FEB', ' WK1 FEB2 ':'WK1_FEB2', ' WK1 FEB3 ':'WK1FEB3',
       ' WK1 FEB4 ':'WK1_FEB4', ' WK1 mar ':'WK1_mar'})
bankdeposit.head(5)

bankdeposit.info()

#Convert the object data types to integers in every column
bankdeposit['December'] = pd.to_numeric(bankdeposit['December'],errors='coerce').fillna(0).astype('int')

bankdeposit['12th_jan'] = pd.to_numeric(bankdeposit['12th_jan'],errors='coerce').fillna(0).astype('int')

bankdeposit['19th-jan'] = pd.to_numeric(bankdeposit['19th-jan'],errors='coerce').fillna(0).astype('int')

bankdeposit['26th_jan'] = pd.to_numeric(bankdeposit['26th_jan'],errors='coerce').fillna(0).astype('int')

bankdeposit['January'] = pd.to_numeric(bankdeposit['January'],errors='coerce').fillna(0).astype('int')

bankdeposit['WK1_FEB'] = pd.to_numeric(bankdeposit['WK1_FEB'],errors='coerce').fillna(0).astype('int')

bankdeposit['WK1_FEB2'] = pd.to_numeric(bankdeposit['WK1_FEB2'],errors='coerce').fillna(0).astype('int')

bankdeposit['WK1FEB3'] = pd.to_numeric(bankdeposit['WK1FEB3'],errors='coerce').fillna(0).astype('int')

bankdeposit['WK1_FEB4'] = pd.to_numeric(bankdeposit['WK1_FEB4'],errors='coerce').fillna(0).astype('int')

bankdeposit['WK1_mar'] = pd.to_numeric(bankdeposit['WK1_mar'],errors='coerce').fillna(0).astype('int')

bankdeposit.info()

(
    bankdeposit[
        (bankdeposit.January == 0) & 
        (bankdeposit.Branch.isin(['Mombasa','Milimani']))
    ]
    .groupby(['unit', 'RM'])['December'].sum()
    .to_frame()
    .reset_index()
).head(1)

from pandas.io.parsers.base_parser import Index
# Make DataFrame Pipeline Interactive
ibankdeposit = bankdeposit.interactive()

# Define Panel widgets
month= pn.widgets.IntSlider(name='january', start=0, end=1, step=1)
Branch = pn.widgets.ToggleGroup(
    name='Branch',
    options=['Milimani', 'Eldoret', 'Mombasa', 'Industrial Area'], 
    value=['Milimani', 'Eldoret', 'Mombasa', 'Industrial Area'],
    button_type='success')
yaxis = pn.widgets.RadioButtonGroup(
    name='Y axis', 
    options=['December', '12th_jan', '19th-jan', '26th_jan','January', 'WK1_FEB', 'WK1_FEB2', 'WK1FEB3', 'WK1_FEB4', 'WK1_mar'],
    button_type='success'
)

# Combine pipeline and widgets
ipipeline = (
    ibankdeposit[
        (ibankdeposit.January == month) & 
        (ibankdeposit.Branch.isin(Branch))
    ]
    .groupby(['unit','RM'])[yaxis].sum()
    .to_frame()
    .reset_index() 
    .reset_index(drop=True)
)

ihvplot=ipipeline.hvplot.line(x='unit', y=yaxis,color=PALETTE, line_width=6)
ihvplot

itable=ipipeline.pipe(pn.widgets.Tabulator,pagination='remote',page_size=10,sizing_mode='stretch_width')
itable

#Layout using Template
template = pn.template.FastListTemplate(
    title='Interactive DataFrame Dashboards with hvplot .interactive', 
    sidebar=[month, Branch, 'Y axis' , yaxis],
    main=[ihvplot.panel(), itable.panel()],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
template.show()
#template.servable();