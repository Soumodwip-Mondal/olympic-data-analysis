import streamlit as st
from preprocess import preprosess
import helper
from helper import get_medal_tally
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff


df = preprosess()
# --- Sidebar ---
st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image(
    'https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png'
)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    year, country = helper.get_year_country(df)
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_data = get_medal_tally(df, country=selected_country, year=str(selected_year))

    # Dynamic title
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🏆 Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} - Overall Performance")
    else:
        st.title(f"{selected_country} Performance in {selected_year} Olympics")

    st.table(medal_data)

# =====================================================================
# 📊 OVERALL ANALYSIS SECTION
# =====================================================================
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("📈 Top Statistics")

    # --- Display stats in 2 rows ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.subheader(editions)
    with col2:
        st.header("Hosts")
        st.subheader(cities)
    with col3:
        st.header("Sports")
        st.subheader(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.subheader(events)
    with col2:
        st.header("Nations")
        st.subheader(nations)
    with col3:
        st.header("Athletes")
        st.subheader(athletes)

    # --- Nations Over Time ---
    st.title("🌍 Participating Nations Over the Years")
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="count", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- Events Over Time ---
    st.title("🏆 Events Over the Years")
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="count", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- Athletes Over Time ---
    st.title("👟 Athletes Over the Years")
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="count", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- Number of Events Over Time (Every Sport) ---
    st.title("📊 Number of Events Over Time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(heatmap_data, annot=True, ax=ax, cmap="YlGnBu")
    st.pyplot(fig)

    # --- Most Successful Athletes ---
    st.title("🥇 Most Successful Athletes")
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)

    # Handle empty result gracefully
    if x is not None and not x.empty:
        st.table(x)
    else:
        st.info("No data available for this sport.")

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    # st.title(selected_country + " excels in the following sports")
    # pt = helper.country_event_heatmap(df,selected_country)
    # fig, ax = plt.subplots(figsize=(20, 20))
    # ax = sns.heatmap(pt,annot=True)
    # st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successfull_in_country(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['gold']==1]['Age'].dropna()
    x3 = athlete_df[athlete_df['silver']==1]['Age'].dropna()
    x4 = athlete_df[athlete_df['bronze']==1]['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['gold'] == 1]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height vs Weight Analysis')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    if not temp_df.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(
            data=temp_df,
            x='Weight',
            y='Height',
            hue='Sex',
            s=70,
            alpha=0.7,
            ax=ax
        )
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected sport.")


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


