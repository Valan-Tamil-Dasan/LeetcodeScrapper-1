from components import User, UserList, Report
import pandas as pd
import streamlit as st

st.write('# **LeetCode Profile Data Collection**')

file = st.file_uploader('Drop your files here')

if file:
    usernames = list(pd.read_csv(file)['Username'])

    print(usernames)

    usernames = UserList(usernames)

    for user in usernames:
        print(user)

    report = Report(usernames)

    report.to_csv()

    st.write(pd.read_csv('report.csv'))
