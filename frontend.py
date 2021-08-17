import streamlit as st
from PIL import Image
import pandas as pd
from backend import BackEnd
import matplotlib.pyplot as plt

bd = BackEnd()

st.set_page_config(layout="wide")

image = Image.open("crime.png")
st.title("Worldwide Crimes EDA")
st.image(image, width=400)


st.markdown("""
This web application performs the data research and analysis of worldwide crimes from 1979 to date.
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, Image, pandas, base64, numpy, matplotlib, altair
* **Data source:** [GDELT Conflict Events](https://www.kaggle.com/vladproex/gdelt-conflict-events-1979-2021/version/1?select=gdelt_conflict_1_0.csv)
""")

col1 = st.sidebar
col2, col3 = st.columns((2, 1))

df = bd.load_data()
# df

# sidebar - Input Selections
col1.title("User Input")
col1.subheader('Search Options')

years = sorted(df['Year'].unique(), reverse=True)
selected_year1 = col1.selectbox('Start Year', years, index=len(years)-1)
selected_year2 = col1.selectbox('End Year', years, index=0)

countries = ["ALL"]
countries.extend(sorted(df['CountryName'].unique()))
default_ix = countries.index('United States')
selected_country = col1.selectbox('Country', countries, index=default_ix)

event_root_descr_list = ["ALL"]
event_root_descr_list.extend(sorted(df['EventRootDescr'].unique()))
selected_crime_root = col1.selectbox(
    'Crime Root', event_root_descr_list, index=1)

event_descr_list = ["ALL"]
event_descr_list.extend(sorted(df['EventDescr'].unique()))

crime_dict = {}
for root_descr in event_root_descr_list[1:]:
    new_df = df[df['EventRootDescr'] == root_descr]
    crime_dict[root_descr] = ["ALL"]
    crime_dict[root_descr].extend(sorted(new_df["EventDescr"].unique()))

if selected_crime_root != "ALL":
    # event_descr_list = sorted(df['EventDescr'].unique())
    selected_crime = col1.selectbox(
        'Crime Specification', crime_dict[selected_crime_root], index=0)
else:
    selected_crime = col1.selectbox(
        'Crime Specification', ["ALL"])


# Filtering data
# default values
total_SumEvents = 0
total_CrimeRoot = 0
total_AllCrimes = 0

# All selections != "ALL"
if selected_year1 == selected_year2 and selected_country != "ALL" and selected_crime_root != "ALL" and selected_crime != "ALL":
    df_selected_country = bd.df_selected_country(
        df, selected_year1, selected_country)
    df_selected_root = bd.df_crime_root(
        df_selected_country, selected_crime_root)
    df_selected = bd.df_crime(df_selected_root, selected_crime)

    # / df_selected.loc[0, 'SumEvents']  # /.iloc[0]['SumEvents'] # but doesn't work for crime number is 0 case
    total_SumEvents = df_selected.SumEvents.sum()
    total_CrimeRoot = df_selected_root.SumEvents.sum()
    total_AllCrimes = df_selected_country.SumEvents.sum()

 # 1 selection == "ALL"
elif selected_year1 == selected_year2 and selected_country != "ALL" and selected_crime_root != "ALL" \
        and selected_crime == "ALL":
    df_selected_country = bd.df_selected_country(
        df, selected_year1, selected_country)
    df_selected = bd.df_crime_root(df_selected_country, selected_crime_root)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df_selected_country.SumEvents.sum()

elif selected_year1 == selected_year2 and selected_country == "ALL" and selected_crime_root != "ALL" \
        and selected_crime != "ALL":
    df_selected_year = bd.df_year(df, selected_year1)
    df_selected_root = bd.df_crime_root(
        df_selected_year, selected_crime_root)
    df_selected = bd.df_crime(df_selected_root, selected_crime).sort_values(
        "CountryName").reset_index(drop=True)

    total_SumEvents = df_selected.SumEvents.sum()
    total_CrimeRoot = df_selected_root.SumEvents.sum()
    total_AllCrimes = df_selected_year.SumEvents.sum()

elif selected_year1 != selected_year2 and selected_country != "ALL" and selected_crime_root != "ALL" and selected_crime != "ALL":
    df_selected_country = bd.df_country(
        df[(df.Year >= selected_year1) & (df.Year <= selected_year2)], selected_country)
    df_selected_root = bd.df_crime_root(
        df_selected_country, selected_crime_root)
    df_selected = bd.df_crime(
        df_selected_root, selected_crime).reset_index(drop=True)

    total_SumEvents = df_selected.SumEvents.sum()
    total_CrimeRoot = df_selected_root.SumEvents.sum()
    total_AllCrimes = df_selected_country.SumEvents.sum()

 # 2 selections == "ALL"
elif selected_year1 == selected_year2 and selected_country != "ALL" and selected_crime_root == "ALL" and selected_crime == "ALL":
    df_selected_country = bd.df_country(df, selected_country)
    df_selected = bd.df_selected_country(df, selected_year1, selected_country).sort_values(
        by=["EventRootDescr", "EventDescr"]).reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df_selected_country.SumEvents.sum()

elif selected_year1 == selected_year2 and selected_country == "ALL" and selected_crime_root != "ALL" and selected_crime == "ALL":
    df_selected_year = bd.df_year(df, selected_year1)
    df_selected = bd.df_crime_root(
        df_selected_year, selected_crime_root).reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df_selected_year.SumEvents.sum()

elif selected_year1 != selected_year2 and selected_country != "ALL" and selected_crime_root != "ALL" and selected_crime == "ALL":
    df_selected_country = bd.df_country(
        df[(df.Year >= selected_year1) & (df.Year <= selected_year2)], selected_country)
    df_selected = bd.df_crime_root(
        df_selected_country, selected_crime_root).reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df_selected_country.SumEvents.sum()

elif selected_year1 != selected_year2 and selected_country == "ALL" and selected_crime_root != "ALL" and selected_crime != "ALL":
    df_selected_root = bd.df_crime_root(
        df[(df.Year >= selected_year1) & (df.Year <= selected_year2)], selected_crime_root)
    df_selected = bd.df_crime(
        df_selected_root, selected_crime).reset_index(drop=True)

    total_SumEvents = df_selected.SumEvents.sum()
    total_CrimeRoot = df_selected_root.SumEvents.sum()
    total_AllCrimes = df.SumEvents.sum()

 # 3 selections == "ALL"
elif selected_year1 == selected_year2 and selected_country == "ALL" and selected_crime_root == "ALL" and selected_crime == "ALL":
    df_selected = bd.df_year(df, selected_year1).sort_values(
        "EventRootDescr").reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df.SumEvents.sum()

elif selected_year1 != selected_year2 and selected_country != "ALL" and selected_crime_root == "ALL" and selected_crime == "ALL":
    df_selected = bd.df_country(df[(df.Year >= selected_year1) & (
        df.Year <= selected_year2)], selected_country).reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df.SumEvents.sum()

elif selected_year1 != selected_year2 and selected_country == "ALL" and selected_crime_root != "ALL" and selected_crime == "ALL":
    df_selected = bd.df_crime_root(
        df[(df.Year >= selected_year1) & (df.Year <= selected_year2)], selected_crime_root).reset_index(drop=True)

    total_CrimeRoot = df_selected.SumEvents.sum()
    total_AllCrimes = df.SumEvents.sum()

 # 4 selections == "ALL"
else:
    df_selected = df
    total_SumEvents = df_selected.SumEvents.sum()
    total_AllCrimes = df_selected.SumEvents.sum()


# col2 - To Display Searched Result
col2.subheader("Search Result")
col2.write("Data Dimension: "
           + str(df_selected.shape[0]) + " rows and " + str(df_selected.shape[1]) + " columns.")

if selected_country == "ALL":
    col2.write(bd.conclusion(selected_year1, selected_year2, " the whole world",
                             selected_crime_root, selected_crime, total_SumEvents, total_CrimeRoot, total_AllCrimes))
else:
    col2.write(bd.conclusion(selected_year1, selected_year2, selected_country,
                             selected_crime_root, selected_crime, total_SumEvents, total_CrimeRoot, total_AllCrimes))

col2.write("""
***
""")

col2.dataframe(df_selected)
col2.markdown(bd.filedownload(df_selected), unsafe_allow_html=True)
col2.markdown("##")

df_plot, p = bd.bar_plotting(selected_year1, selected_year2, selected_country,
                             selected_crime_root, selected_crime, total_SumEvents, total_CrimeRoot, total_AllCrimes)
col2.dataframe(df_plot)
col2.markdown("##")
col2.write(p)
col2.markdown("##")
#plot
if selected_year1 != selected_year2:
    col2.pyplot(bd.line_plot(df_selected, selected_year1, selected_year2))






#col3
#siderbar - Number of Countries to Display
col1.markdown("##")
col1.header("Display Options")
year_list = sorted(df['Year'].unique(), reverse=True)
display_year1 = col1.selectbox(
    'Display Start Year', year_list, index=len(year_list)-1)
display_year2 = col1.selectbox('Display End Year', year_list, index=0)

num1_country = col1.slider(
    "Display Top N Countries with Most Crimes", 1, 100, 50)

df_selected = df[(df.Year >= display_year1) & (df.Year <= display_year2)]
df_selected = df_selected.groupby(["CountryName"], as_index=False)[
                                  "SumEvents"].sum()
top_n = df_selected.sort_values("SumEvents", ascending=True)[-num1_country:]

col3.subheader("Display Result")
col3.write("Top " + str(num1_country) + " Countries with Most Crimes from "
           + str(display_year1) + " to " + str(display_year2))
# col3.dataframe(top_n1)
top_n = top_n.set_index("CountryName")
plt.figure(figsize=(5, 25))
plt.subplots_adjust(top=1, bottom=0)
top_n["SumEvents"].plot(kind='barh', color='skyblue', alpha=0.8)
col3.pyplot(plt)
