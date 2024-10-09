import altair as alt
import pandas as pd
import streamlit as st
#using template from steamline.io
# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🌱")
st.title("🌱 Carbon Offset Aggregation")
st.write(
    """

    This app aggregates and visualizes data from various Carbon Offset Registries.
    Click on the widgets below to learn more about the projects and the United Nations Sustainable Development Goals (SDGs) they fulfill.
    
    """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/all_projects.csv")
    return df

df = load_data()

#multiselect widget with the genres using `st.multiselect`.
sdgs = st.multiselect(
    "Sustainable Development Goals (SDG)",
    df.genre.unique(),
    ["Goal 1", "Goal 2", "Goal 3", "Goal 4", "Goal 5", "Goal 6", "Goal 7", "Goal 8", "Goal 9", "Goal 10",
     "Goal 11", "Goal 12", "Goal 13", "Goal 14", "Goal 15", "Goal 16", "Goal 17"]
)

# # Show a slider widget with the years using `st.slider`.
# # years = st.slider("Years", 1986, 2006, (2000, 2016))
#
# # Filter the dataframe based on the widget input and reshape it.
# df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
# df_reshaped = df_reshaped.sort_values(by="year", ascending=False)
#
#
# Display the data as a table using `st.dataframe`.
st.dataframe(
    df,
    use_container_width=True,
    # column_config={"year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)
