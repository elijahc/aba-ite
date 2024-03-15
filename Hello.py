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
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to ITE Explorer! 👋")

    st.sidebar.success("Select a demo above.")

    df = pd.read_csv('./2024.ITE.scaled.csv').sort_values(by='Score').reset_index(drop=True)
    ite_cdf = df.set_index('Score')
    # st.table(ite_cdf.reset_index())
    data = pd.melt(ite_cdf.reset_index(), id_vars=['Score']).rename(columns={'value':'Percentile','variable':'year'})
    ite_pdf = ite_cdf.diff()
    pdf_data = pd.melt(ite_pdf.reset_index(), id_vars=['Score']).rename(columns={'value':'Percentile','variable':'year'})

    # data = data.groupby('year').transform(lambda df: df.sort_values(by=['Percentile','Score']).diff())

    chart = alt.Chart(data.query("Score > 10")).mark_line().encode(
        x='Score:Q',
        y='Percentile:Q',
        color='year'
    )    

    st.altair_chart(chart,use_container_width=True)
    # st.table(data.Percentile.diff())



if __name__ == "__main__":
    run()
