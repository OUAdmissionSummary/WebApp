import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

@st.cache
def getDataFrame():
    # get csv from to df https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/edit?usp=sharing
    df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/export?format=csv')
    # get csv from https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/edit?usp=sharing to df
    df2 = pd.read_csv('https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/export?format=csv')
    # combine df1 and df2
    df = pd.concat([df1, df2], axis=0)
        # delete all duplicate rows
    df = df.drop_duplicates(keep='first')
    # Remove all the '%" in the average column
    df['Average'] = df['Average'].str.replace('%', '')
    df['Average'] = df['Average'].str.replace('~', '')
    df['Average'] = df['Average'].str.replace(',', '')
    # remove all + in the average column
    df['Average'] = df['Average'].str.replace('+', '')
    # Delete rows where average  NaN
    df = df.dropna(how = 'any', subset=['Average'])

    blacklisted_avgs = {'99.75 (gr.12 data, adv func, bio, chem)': '99.75',
                        'Top6 98, 5 in AP CS and 7 in both IB Math and Physics': '98',
                        '96ish': '96.5',
                        '94-95': '94.5',
                        '98.5-99ish': '98.5',
                        'sub 90’s': '97.5',
                        '4.0/4.66': '98',
                        '96.6 g11': '96.3',
                        '94.7 gr12 sem 1 96.6 gr11': '96.3',
                        'probably 97.5': '97.5',
                        '39/42(IB)': '97',
                        '97-98ish': '97.5',
                        '99 (based on g11 final and g12 midterm, not likely to maintain)' : '99',
                        '99.75 (gr.12 data adv func bio chem)': '99.75',
                        'Top6 98 5 in AP CS and 7 in both IB Math and Physics': '98',
                        'sub 90’s or somethin': '97.5',
                        'around 95 idk what they look at': '95',
                        '99 (based on g11 final and g12 midterm not likely to maintain)': '99',
                        'around 95 idk': '95',
                        '99.8 (based on midterm)': '99.8',
                        '89 with calc 93 without': '89',
                        '91 (5 courses)': '91',
                        '98? 2 IB courses both predicted a 7 and a 5 in AP CS A': '98',
                        '95 (2 g12 final 2 g12 midterm 1 g11 final 1 g11 midterm)': '95',
                        '95 (grade 11 marks) ' : '95',
                        }

    # make sure that if the data frame has value that is a key of the dictionary, it will be replaced with the value

    df['Average'] = df['Average'].replace(blacklisted_avgs)

    return df


def getStats(dfStats, unis, programs):
    dfStats = dfStats.reset_index(drop=True)
    # get accepted
    dfStats_accepted = dfStats[dfStats['Status'] == 'Accepted'].reset_index(drop=True)
    # get 101
    dfStats_accepted101 = dfStats_accepted[dfStats_accepted['Type (101/105)'] == '101'].reset_index(drop=True)
    # get 105
    dfStats_accepted105 = dfStats_accepted[dfStats_accepted['Type (101/105)'].str.contains('105')].reset_index(drop=True)

    # get avgs
    dfStats_accepted['Average'] = dfStats_accepted['Average'].astype(float)
    dfStats_accepted101['Average'] = dfStats_accepted101['Average'].astype(float)
    dfStats_accepted105['Average'] = dfStats_accepted105['Average'].astype(float)

    # print averages
    AdmissionAverage = str(dfStats_accepted['Average'].mean())
    AdmissionAverage101 = str(dfStats_accepted101['Average'].mean())
    AdmissionAverage105 = str(dfStats_accepted105['Average'].mean())

    return AdmissionAverage, AdmissionAverage101, AdmissionAverage105

def getDF(uni_names = [],program_names = []):
    df_uni_stats = pd.DataFrame()
    df_program_stats = pd.DataFrame()
    for i in range(len(uni_names)):
        # append this to a df df[df['School'].str.contains(uni_names[i], na=False, case=False)]
        df_uni = df[df['School'].str.contains(uni_names[i], na=False, case=False)]
        # concat it to the df_program_stats
        df_uni_stats = pd.concat([df_uni_stats, df_uni])
    if len(program_names) == 0:
        return df_program_stats, uni_names, program_names
    if len(uni_names) == 0:
        df_uni_stats = df
    for i in range(len(program_names)):
        df_program = df_uni_stats[df_uni_stats['Program'].str.contains(program_names[i], na=False, case=False)]
        df_program_stats = pd.concat([df_program_stats, df_program])

    return df_program_stats, uni_names, program_names


st.title("Ontario Universities Admissions - Data Analysis")
df = getDataFrame()
# create 2 boxes where user can input multiple inputs
uni_names = st.sidebar.text_input("University Names", "")
program_names = st.sidebar.text_input("Program Names", "")

# if we get input from the two variables
if uni_names or program_names:
    # split the input into a list
    uni_names = uni_names.split(",")
    program_names = program_names.split(",")
    # get the df
    df_program_stats, uni_names, program_names = getDF(uni_names, program_names)
    st.write(df_program_stats)

    # make a header stats
    st.header("Admission Statistics")
    # get the stats
    AdmissionAverage, AdmissionAverage101, AdmissionAverage105 = getStats(df_program_stats, uni_names, program_names)
    # print the stats
    st.write("Average Admission Rate:", AdmissionAverage)
    st.write("Average Admission Rate for 101:", AdmissionAverage101)
    st.write("Average Admission Rate for 105:", AdmissionAverage105)
    # visualize histogram
    st.subheader("Histogram of Admission Rates")
    
    # graph the data sort the x-axis using px.histogram
    df_program_stats = df_program_stats.sort_values(by=['Average'], ascending=False)
    fig = px.histogram(df_program_stats, x="Average", title="Histogram of Admission Rates")
    st.plotly_chart(fig)


else:
    st.write(df)

