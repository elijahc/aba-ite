# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import altair as alt
import os
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def load_ite_data():
    files = os.listdir('./data/')
    files = sorted([f for f in files if f.endswith('.csv')])
    result_yr = [int(f.split('.')[0]) for f in files]
    dfs = []
    for f,y in zip(files,result_yr):
        df = pd.read_csv('./data/'+f)
        df['year'] = int(y)
        df = df.astype({'Score':int})
        dfs.append(df)
    return pd.concat(dfs)[['Score','year','CA-0','CA-1','CA-2','CA-3']].sort_values(by=['Score','year'],ascending=True).reset_index(drop=True)
    # st.table(pd.concat(dfs))
    # df = pd.read_csv('./data/2024.ITE.scaled.csv').sort_values(by='Score').reset_index(drop=True)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to ITE Explorer! 👋")

    st.sidebar.success("Select a demo above.")
    df = load_ite_data()
    ite_cdf = df.drop(columns=['year']).groupby('Score').mean()
    # st.table(ite_cdf)
    data = pd.melt(ite_cdf.reset_index(), id_vars=['Score']).rename(columns={'value':'Percentile','variable':'year'})
    # pdf_data = pd.melt(ite_cdf.diff().reset_index(), id_vars=['Score']).rename(columns={'value':'density','variable':'year'})

    # data = data.groupby('year').transform(lambda df: df.sort_values(by=['Percentile','Score']).diff())

    chart = alt.Chart(data.query("Percentile > 1")).mark_line().encode(
        x='Score:Q',
        y='Percentile:Q',
        color='year'
    )    

    st.altair_chart(chart,use_container_width=True)
    # st.table(data.Percentile.diff())



if __name__ == "__main__":
    run()
