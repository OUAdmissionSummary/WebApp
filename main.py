import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def color_df(val):
    if val == 'Accepted':
        color = 'green'
    elif val == 'Rejected':
        color = 'red'
    else:
        color = 'yellow'
    return f'background-color: {color}'

@st.cache
def getDataFrame():
    # get csv from to df https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/edit?usp=sharing
    df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/export?format=csv')
    # get csv from to df https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/edit?usp=sharing
    df2 = pd.read_csv('https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/export?format=csv')
    # combine df1 and df2
    df = pd.concat([df1, df2], axis=0)
    # delete all duplicate rows subset Discord and Program and School
    df = df.drop_duplicates(subset=['Discord', 'Program', 'School'])
    # Remove all the '%" in the average column
    df['Average'] = df['Average'].str.replace('%', '')
    df['Average'] = df['Average'].str.replace('~', '')
    df['Average'] = df['Average'].str.replace(',', '')
    # remove all + in the average column
    df['Average'] = df['Average'].str.replace('+', '')
    # remove all ? in the average column
    df['Average'] = df['Average'].str.replace('?', '')
    # Delete rows where average  NaN
    df = df.dropna(how = 'any', subset=['Average'])
    # if Type (101/105) column is empty, fill it with '101'
    df['Type (101/105)'] = df['Type (101/105)'].fillna('101')
    

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
                        '39/42(IB)': '94.5',
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
                        '98 2 IB courses both predicted a 7 and a 5 in AP CS A': '98',
                        '95 (2 g12 final 2 g12 midterm 1 g11 final 1 g11 midterm)': '95',
                        '95 (grade 11 marks) ' : '95',
                        'idk like around 90': '90',
                        '90 grade 12 Q1 90 grade 11': '90',
                        '92 grade 12 midterms 96 grade 11': '94',
                        '94 4 g12 91 with 2 g11 prereqs': '91',
                        '92 (As of time accepted)': '92',
                        '95 (including 1 prerequisite)': '95',
                        '4A*s (equivalent to 95-100)': '97.5',
                        '4 A* (A-levels)': '97.5',
                        '94.6 based off 3 courses supposed to be 97 cause physics is gonna get pushed out 96.3 including gr11': '96.3',
                        '99.75 (Gr12 only) --> 99 (including gr11 english but my english teacher never gave out 96)': '99',
                        'Top 6: 95 on the dot': '95',
                        "mid 90's": '95',
                        "mid 90": '95',
                        "low/mid 90s": '95',
                        "99.75 (including bio chem data and adv func)": '99.75',
                        "96-97???": '96.5',
                        "95-96?": '95.5',
                        "945": '94.5',
                        "89 (final grade 12 marks)": '89',
                        "99.3 with 6 4U finals": '99.3',
                        "(39/42 IB)": '94.5',
                        "(39/42 IB)": '94.5',
                        "(92 gr12 midterms 96 gr11)":'96.3',
                        "(different education system equivalent) 87": '87',
                        "gr.11 94 gr.12 first sem 92": '93',
                        "I think 94": '94',
                        "low-mid 90": '94',
                        "low 90s": '92',
                        "low 90s": '92',
                        "low 80s": '83',
                        "Gr.11 94 first sem gr12 92": '93',
                        "Gr.11 94 first sem gr12 92": '93',
                        "gr.11 94 first sem gr.12 92": '93',
                        "deferred from coop to none": "",
                        "current avg: 96.5": '96.5',
                        "around 96?" : '96.5',
                        "around 94?" : '94.5',
                        "89 (final grade 12 marks) ": '89',
                        "95 for Top 5 92 for Top 6": '93.5',   
                        "94.2 96.7 (just realized they don't look at grade 12 interim marks)": '95.5',
                        "97.33 (Top 6 Grade 11 CS)": '97.33',
                        "98-99ish": '98.5',
                        "92 w/o gr12 english 90.8 with gr 11 english": '92',
                        "98.2(self-reported)": '98.2',
                        "35/42 (IB)": '92.8',
                        "92 top 6": '92',
                        "90-91": '90.5',
                        "96-97": '96.5',
                        "around 94": '94.5',
                        "95-96": '95.5',
                        "around 96": '96.5',
                        "94 ish": '94.5',
                        "94.83 admission avg 97 grade 12": '94.83',
                        "92 w/o gr12 eng 90.8 with gr 11 eng": '92',
                        "89-90": '89.5',
                        "87-92": '90',
                        "91 (gr11)" : '91',
                        "93 (without math)": '93',
                        "93 when I applied 95 now": '94',
                        "96 gr11 92 gr12 midterms": '96.3',
                        "92 (as of time accepted)": '92',
                        "92-95": '93.5',
                        "95ish": '95',
                        "96.5 (Grade 11 Top 6)": '96.5',
                        "99.3 with 6 4U courses": '99.3',
                        "88 Midterm 92 Gr11 Top6": '90',
                        "91 Top 6 Final": '91',
                        "92(gr11)": '92',
                        "94 Grade 11 finals 97 Grade 12 midterm": '95.5',
                        "94 time of acceptance": '94',
                        "94.6 (Gr 12)" : '94.6',
                        "95 (at time of acceptance)" : '95',
                        "95 (first sem classes)" : '95',
                        "95 (top 6 4u)": "95 top 6 4g12 2g11",
                        "96.6 (completed 5 U courses)": '96.6',
                        "96.66 using 1 gr 11 prerequisite and current af mark for calc": '96.66',
                        "96.66 using 1 gr 11 prerequisite and current af mark for calc": '96.66',
                        "96.8 gr11 (top 5)/ 95 gr12 midterms": '96.8',
                        "97.333 (Top 6 CS)": '97.333',
                        "98 probably": '98',
                        "99 (didn’t do AIF)" : '99',
                        "99 (Gonna drop after midterms cause of physics...)" : '99',
                        "99.3 6 4U": '99.3',
                        "99.3 with 6 4U courses": '99.3',
                        "93-94": '93.5',
                        "93/94": '93.5',
                        "71 hopefully 74 by finals": '71',
                        "95 top 6 4g12 2g11": '95',
                        "94.33 sent to Unis though it is a 95": '94.33',
                        "72 but my priv school courses coming in": '72',
                        "92 (Gr11)" : '92',
                        "95 top 6 4g12 2g11": '95',
                        "94 Final Top 6": '94',
                        "97-98": '97.5',
                        "95 top 6 4g12 2g11": '95',
                        "91.1 Final Top 6": '91.1',
                        "99 20 adjustment factor": '99',
                        "94 ish I think": '94',
                        "97.6 - 98.1": '97.9',
                        }

    # make sure that if the data frame has value that is a key of the dictionary, it will be replaced with the value
    df['Average'] = df['Average'].replace(blacklisted_avgs)
    # make average colum where it is equal to 95 top 6 4g12 2g11 equal 95
    df['Average'] = df['Average'].replace('95 top 6 4g12 2g11', '95')
    # for each row 
    for index, row in df.iterrows():
        # if the average column is less then 80
        try:
            if int(row['Average']) < 80.0:
                # drpo it
                df = df.drop(index)
        except:
            continue

    # color the dataframe based off the status column
    df.style.apply(color_df, axis=0, subset=['Status'])




    return df

@st.cache()
def getStats(dfStats, unis, programs):
    dfStats = dfStats.reset_index(drop=True)
    # get accepted
    dfStats_accepted = dfStats[dfStats['Status'] == 'Accepted'].reset_index(drop=True)
    # get 101
    dfStats_accepted101 = dfStats_accepted[dfStats_accepted['Type (101/105)'] == '101'].reset_index(drop=True)
    # get 105
    # dfStats_accepted105 = dfStats_accepted[dfStats_accepted['Type (101/105)'].str.contains('105')].reset_index(drop=True)

    # get avgs
    dfStats_accepted['Average'] = dfStats_accepted['Average'].astype(int)
    dfStats_accepted101['Average'] = dfStats_accepted101['Average'].astype(int)
    # dfStats_accepted105['Average'] = dfStats_accepted105['Average'].astype(float)

    # print averages
    AdmissionAverage = str(dfStats_accepted['Average'].mean())
    AdmissionAverage101 = str(dfStats_accepted101['Average'].mean())
    # AdmissionAverage105 = str(dfStats_accepted105['Average'].mean())

    return AdmissionAverage, AdmissionAverage101

@st.cache()
def getDF(df, uni_names, program_names, type_of_applicant):
    df_uni_stats = pd.DataFrame()
    df_program_stats = pd.DataFrame()
    df_type_of_applicant_stats = pd.DataFrame()

    if type_of_applicant != 'All':
        df_type = df[df['Type (101/105)'].str.contains(type_of_applicant, na=False, case=False)].reset_index(drop=True)

        df_type_of_applicant_stats = pd.concat([df_type_of_applicant_stats, df_type]).reset_index(drop=True)
    else:
        df_type_of_applicant_stats = df.reset_index(drop=True)

    if len(uni_names) != 0:
        for uni in uni_names:
            df_uni = df_type_of_applicant_stats[df_type_of_applicant_stats['School'].str.contains(uni, na=False, case=False)].reset_index(drop=True)
            df_uni_stats = pd.concat([df_uni_stats, df_uni]).reset_index(drop=True)
    else:
        df_uni_stats = df_type_of_applicant_stats.reset_index(drop=True)

    
    if len(program_names) != 0:
        for program in program_names:
            df_program = df_uni_stats[df_uni_stats['Program'].str.contains(program, na=False, case=False)].reset_index(drop=True)
            df_program_stats = pd.concat([df_program_stats, df_program]).reset_index(drop=True)
    else:
        df_program_stats = df_uni_stats.reset_index(drop=True)
    # index df_program_stats properly
    df_program_stats = df_program_stats.reset_index(drop=True)  

    return df_program_stats, uni_names, program_names


st.title("Ontario Universities Admissions - Data Analysis")
# notes
st.markdown("""
    This app is designed and built by ayo#0957(me) feel free to contact me on discord if you have any questions or comments.
    Just some general things you need to keep in mind when taking a look at the data here:
    - The data is from the Ontario Universities and University of Waterloo Applicant servers and is not from any other source.
    - The data is not updated often and is not guaranteed to be accurate, any person can enter such data.
    - There we're many conversions I had to make on my end which might make the data less accurate.
    - The data as of right now only shows 101's as I am still working out conversion factors for 105's. 
    """)
# Features
st.markdown("""
    This app has the following features:
    - Filter by University(Just enter the name of the university in the search bar on the left hand side make sure you have no spaces, and consider acrynoms people might use like UW for Waterloo).
    - Filter by Program(Just enter the name of the program in the search bar on the left hand side make sure you have no spaces, and consider acrynoms people might use like CS for Computer Science).
    - Sort by any of the columns by clicking on the column name.
    - Histogram showing frequency of each average.
    - Admission averages for each specificed data set.
    """)
df = getDataFrame()
# create 2 boxes where user can input multiple inputs
uni_names = st.sidebar.text_input("University Names(separate by commas no spaces)", "")
program_names = st.sidebar.text_input("Program Names(separate by commas no spaces)", "")
# create dropdown two options 105 and 101
# type_of_admission = st.sidebar.selectbox("Type of applicant", ["All", "101", "105"])

# split the input into a list
uni_names = uni_names.split(",")
program_names = program_names.split(",")
# get the df
df_program_stats, uni_names, program_names = getDF(df, uni_names, program_names, '101')
st.write(df_program_stats)

# make a header stats
st.header("Admission Statistics")
# get the stats
AdmissionAverage, AdmissionAverage101 = getStats(df_program_stats, uni_names, program_names)
# print the stats
st.write("Admission Average: ", AdmissionAverage)
# visualize histogram
st.subheader("Histogram of Admission Averages:")

# graph the data sort the x-axis using px.histogram
df_program_stats = df_program_stats.sort_values(by=['Average'], ascending=False)
fig = px.histogram(df_program_stats, x="Average", title="Histogram of Admission Rates")
st.plotly_chart(fig)
