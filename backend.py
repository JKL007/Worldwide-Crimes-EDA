import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import altair as alt


class BackEnd:
    # def __init__(self):
    @st.cache
    def load_data(self):
        url = "https://raw.githubusercontent.com/vlad-ds/gdelt-conflict/main/gdelt_conflict/gdelt_conflict_1_0.csv"
        df = pd.read_csv(url, header=0)  # df; .read_csv
        # df.drop(["NormalizedEvents1000", "EventRootCode", "EventCode",
        #          "GoldsteinScale", "AvgNumMentions", "SumNumMentions", "AvgAvgTone"], axis=1, inplace=True) #axis=1: column
        df.drop(columns=["TotalEvents", "NormalizedEvents1000", "EventRootCode", "EventCode",
                         "GoldsteinScale", "AvgNumMentions", "SumNumMentions", "AvgAvgTone"], inplace=True)
        return df

    def df_year(self, df, year):
        return df[df.Year == year].reset_index(drop=True)

    def df_country(self, df, country):
        return df[df.CountryName == country].reset_index(drop=True)

    def df_crime_root(self, df, crime_root):
        return df[df.EventRootDescr == crime_root].reset_index(drop=True)

    def df_crime(self, df, crime):
        return df[df.EventDescr == crime].reset_index(drop=True)

    def df_selected_country(self, df, selected_year, selected_country):
        df_selected_country = self.df_year(self.df_country(
            df, selected_country), selected_year).reset_index(drop=True)
        return df_selected_country

    def filedownload(self, df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="Search Outcome.csv">Download CSV File</a>'
        return href

    def conclusion(self, year1, year2, country, crime_root, crime, total_SumEvents, total_CrimeRoot, total_AllCrimes):
        if year1 == year2 and crime != "ALL":
            return ("In " + str(year1) + ", there were " + "{:,.0f}".format(total_SumEvents) + " "
                    + str(crime) + " crimes in " + str(country)
                    + ". It was %.3f" % ((total_SumEvents
                                          / total_CrimeRoot) * 100)
                    + "% of "
                    + str(crime_root)
                    + " root crimes, and %.3f" % ((total_SumEvents / total_AllCrimes) * 100)
                    + "% of all crimes of" + str(country) + " of Year " + str(year1) + " .")

        elif year1 == year2 and crime == "ALL":
            if crime_root == "ALL":
                return ("In " + str(year1) + ", there were " + "{:,.0f}".format(total_CrimeRoot) + " "
                        + str(crime_root)
                        + " crimes in " + str(country)
                        + ". It was %.3f" % ((total_CrimeRoot
                                              / total_AllCrimes) * 100)
                        + "% of all crimes of " + str(country) + " from 1979 to today.")
            else:
                return ("In " + str(year1) + ", there were " + "{:,.0f}".format(total_CrimeRoot) + " "
                        + str(crime_root)
                        + " crimes in " + str(country)
                        + ". It was %.3f" % ((total_CrimeRoot
                                              / total_AllCrimes) * 100)
                        + "% of all crimes of " + str(country) + " of Year " + str(year1) + " .")

        elif year1 != year2 and crime != "ALL":
            return ("From " + str(year1) + " to " + str(year2) + ", there have been " + "{:,.0f}".format(total_SumEvents) + " "
                    + str(crime)
                    + " crimes in " + str(country)
                    + ". It is %.3f" % ((total_SumEvents
                                         / total_CrimeRoot) * 100)
                    + "% of "
                    + str(crime_root)
                    + " root crimes, and %.3f" % ((total_SumEvents
                                                   / total_AllCrimes) * 100)
                    + "% of all crimes of " + str(country) + " of all these years.")

        elif year1 != year2 and crime == "ALL":
            if country == " the whole world" and crime_root == "ALL":
                return ("From " + str(year1) + " to " + str(year2) + ", there have been " + "{:,.0f}".format(total_SumEvents) + " "
                        + str(crime_root) + " crimes worldwide.")
            elif country != " the whole world" and crime_root == "ALL":
                return ("From " + str(year1) + " to " + str(year2) + ", have been " + "{:,.0f}".format(total_CrimeRoot) + " "
                        + str(crime_root)
                        + " crimes in " + str(country)
                        + ". It is %.3f" % ((total_CrimeRoot
                                             / total_AllCrimes) * 100)
                        + "% of all crimes of the whole world of all these years.")
            else:
                return ("From " + str(year1) + " to " + str(year2) + ", have been " + "{:,.0f}".format(total_CrimeRoot) + " "
                        + str(crime_root)
                        + " crimes in " + str(country)
                        + ". It is %.3f" % ((total_CrimeRoot
                                             / total_AllCrimes) * 100)
                        + "% of all crimes of " + str(country) + " of all these years.")

    def bar_plotting(self, selected_year1, selected_year2, selected_country, selected_crime_root, selected_crime, total_SumEvents, total_CrimeRoot, total_AllCrimes):
        if total_SumEvents == 0:
            data = {"Crime Types": [str(selected_crime_root), "Total Crimes"],
                    "Crime Numbers": [
                    total_CrimeRoot, total_AllCrimes]}
        elif total_CrimeRoot == 0:
            data = {"Crime Types": [str(selected_crime), "Total Crimes"],
                    "Crime Numbers": [
                    total_SumEvents, total_AllCrimes]}
        else:
            data = {"Crime Types": [str(selected_crime), str(selected_crime_root), "Total Crimes"],
                    "Crime Numbers": [
                    total_SumEvents, total_CrimeRoot, total_AllCrimes]}

        df_plot = pd.DataFrame(data)
        p = alt.Chart(df_plot, title=str(selected_crime) + " crime in " + str(selected_country)
                      + " (COUNTRY) from " + str(selected_year1) + " to " + str(selected_year2)).mark_bar().encode(
            x=alt.X("Crime Types",
                    sort=data["Crime Numbers"]),
            y="Crime Numbers"
        ).properties(
            height=500,
            width=alt.Step(100)
        ).configure_axisY(
            titleAngle=0,
            titleY=-10,
            titleX=-10,
        )

        return df_plot, p

    def line_plot(self, df, year1, year2):
        df = df[(df.Year >= year1) & (df.Year <= year2)]
        years = list(df.Year.unique())
        df_sum = df.groupby("Year").sum()
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.fill_between(
            years, df_sum.SumEvents, color='skyblue', alpha=0.3)
        plt.plot(years, df_sum.SumEvents,
                 color='skyblue', alpha=0.5)
        # plt.gcf().set_size_inches(4, 3)
        # plt.rcParams["figure.figsize"] = (3, 3)
        # plt.figure(figsize=(6, 4))
        plt.title("Slected Crime Trend of Searched Period")
        plt.xlabel("Year")
        plt.ylabel("Crime Number", rotation=90)
        plt.xticks(rotation=90)  # to rotate axis labels
        plt.yticks(rotation=90)
        # return st.pyplot()
        return plt
