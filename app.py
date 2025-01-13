import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import dotenv

dotenv.load_dotenv()
spreadsheet = os.environ["SPREADSHEET_URL"]

def load_goals():
    url = f"{spreadsheet}&gid=28718768"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url)
    return data

def top_scorers():
    data = load_goals()
    df = pd.DataFrame(data)
    return df.sort_values(by=("Goals"), ascending=False).head(5)

def load_assists():
    url = f"{spreadsheet}&gid=499101221"
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url)
    return data

def assist_leaders():
    data = load_assists()
    df = pd.DataFrame(data)
    return df.sort_values(by=("Assists"), ascending=False).head(5)

def raw_data(): 
    st.header("Raw Data")
    goals = load_goals()
    st.write(goals)


def goals(): 
    st.header("Golos :soccer:")
    goals = load_goals()
    fig = px.pie(goals, values='Goals', names='Player', hover_data=['Goals'], color_discrete_sequence=px.colors.qualitative.Antique)
    st.plotly_chart(fig, use_container_width=True)

    for i, row in enumerate(top_scorers().iterrows()): 
        c, scorer = row
        text = f"{i+1}. {scorer['Player']} - {scorer['Goals']}"
        if i == 0:
            text += " :star:"
        st.markdown(text)

def assists(): 
    st.header("Assistências :a:")
    assists = load_assists()
    fig = px.pie(assists, values='Assists', names='Player', hover_data=['Assists'], color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig, use_container_width=True)

    for i, row in enumerate(assist_leaders().iterrows()): 
        c, passer = row
        text = f"{i+1}. {passer['Player']} - {passer['Assists']}"
        if i == 0:
            text += " :star:"
        st.markdown(text)

st.title('Black Bulls Stats')

st.markdown(""" 
Vamos pegar ya, vamos mesmo pegar!

Bem-vindo ao campo de batalha! aqui as tropas não fogem de um bom trumuno*. Isso aqui é a "pauta" do time, local onde conseguimos ver 
os aprovados, os reprovados, os do quadro de honra e os "que só tiram 10". 
""")
goals()
assists()
