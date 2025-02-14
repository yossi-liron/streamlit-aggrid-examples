import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode

@st.cache_data()
def get_data():
    df = pd.DataFrame(
        np.random.randint(0, 100, 50).reshape(-1, 5), columns= list("abcde")
    )
    return df

data = get_data()
gb = GridOptionsBuilder.from_dataframe(data)
go = gb.build()

save_btn = st.button("Save Columns State")
load_btn = st.button("Load Columns State")

colState = None
if load_btn:
    colState = st.session_state.get('grid_state')

ag = AgGrid(
    data, 
    gridOptions=go, 
    fit_columns_on_grid_load=True, 
    key='an_unique_key',
    allow_unsafe_jscode=True,
    update_on=[('stateUpdated',0)], 
    columns_state=colState,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
)

if save_btn:
    st.session_state['grid_state'] = ag.grid_response['columnsState']

a = ag.grid_response['columnsState']
a








st.stop()


st.subheader("Controling Ag-Grid redraw in Streamlit.")
st.markdown("""
The grid will redraw itself and reload the data whenever the key of the component changes.  
If ```key=None``` or not set at all, streamlit will compute a hash from AgGrid() parameters to use as a unique key.  
This can be simulated by changing the grid height, for instance, with the slider:
""")

c1,_ = st.columns([3,2])

height = c1.slider('Height (px)', min_value=100, max_value=800, value=400)

st.markdown("""
As there is no key parameter set, whenever the height parameter changes grid is redrawn.  
This behavior can be prevented by setting a fixed key on aggrid call (check the box below):  
""")

use_fixed_key = st.checkbox("Use fixed key in AgGrid call", value=False)
if use_fixed_key:
    key="'an_unique_key'"
else:
    key=None

st.markdown(f"""
However, blocking redraw, also blocks grid from rendering new data, unless the ```reload_data```  parameter is set to true.  
(note that grid return value shows new data, however as redraw is blocked grid does not show the new values)
""")
reload_data=False
c1,c2,_ = st.columns([1,2,1])
button = c1.button("Generate 10 new random lines of data")
reload_data_option = c2.checkbox("Set reload_data as true on next app refresh.", value=False)

if button:
    st.cache_data.clear()
    if reload_data_option:
        reload_data=True


key_md = ", key=None" if not key else f",key={key}"
st.markdown(f"""
Grid call below is:
```python
AgGrid(data, grid_options, {key_md}, reload_data={reload_data}, height={height})
```""")






data = get_data()
gb = GridOptionsBuilder.from_dataframe(data)

data['id']=data.index

#make all columns editable
gb.configure_columns(list('abcde'), editable=True, cellRenderer='agAnimateShowChangeCellRenderer')

#Create a calculated column that updates when data is edited. Use agAnimateShowChangeCellRenderer to show changes   
#gb.configure_column('row total', valueGetter='Number(data.a) + Number(data.b) + Number(data.c) + Number(data.d) + Number(data.e)', cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])
go = gb.build()

go['getRowId'] = JsCode("""function (params) { return params.data.id; }""")

if st.button("randomize"):
    import random 
    for i in range(10):
        x,y,v = random.randint(0,data.shape[0]-1), random.randint(0,data.shape[1]-1), random.randint(10000,100000) 
        #st.write(x,y,v, data.shape)
        data.iloc[x,y] = v
 
# Setting a fixed key for the component will prevent the grid to reinitialize when dataframe parameter change, simulated here 
# by pressing the button on the side bar.  
# Data will only be refreshed when the parameter reload_data is set to True

if use_fixed_key:
    ag = AgGrid(
        data, 
        gridOptions=go, 
        height=height, 
        fit_columns_on_grid_load=True, 
        key='an_unique_key',
        reload_data=reload_data,
        allow_unsafe_jscode=True
    )
else:
    ag = AgGrid(
        data, 
        gridOptions=go, 
        height=height, 
        fit_columns_on_grid_load=True
    )

st.subheader("Returned Data")
st.dataframe(ag['data'])

st.subheader("Grid Options")
st.write(go)