import pandas as pd
import streamlit as st
import altair as alt
import ast

#using template Movie Dataset from steamline.io
#reference: Turn An Excel Sheet Into An Interactive Dashboard Using Python (Streamlit) by Coding Is Fun on YouTube
#https://www.youtube.com/watch?v=Sb0A9i6d320&t=616s

# Show the page title and description.
st.set_page_config(page_title="Carbon Offset Aggregator",
                   page_icon="🌱")
st.title("🌱 Carbon Offset Aggregator")
st.write(
    """

    This app aggregates and visualizes data from various Carbon Offset Registries.
    Click on the widgets below to learn more about the projects and the United Nations Sustainable Development Goals (SDGs) they fulfill.
    
    """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

df = load_data("data/all_projects.csv")
df_2 = load_data("data/sdg_counts.csv")
df_3 = load_data('data/sdg.csv')

#searchbar
sdg_search = st.text_input("Search by SDG number (e.g., 1, 2, 3)", value="")
# Check if there's any input
if sdg_search:
    try:
        df['SDGs'] = df['SDGs'].apply(ast.literal_eval)
        # Filter rows where the list in the 'SDGs' column contains the search term
        df_filtered = df[df["SDGs"].apply(lambda x: int(sdg_search) in x)]

    except ValueError:
        st.write("Please enter a valid number.")
else:
        df_filtered = df

location = st.sidebar.multiselect(
    "Location",
    options=df_filtered["Location"].unique()
)

registry = st.sidebar.multiselect(
    "Registry",
    options=df_filtered["Registry"].unique(),
    default=df_filtered["Registry"].unique()
)

df_selection = df_filtered.query(
    "Registry == @registry & Location == @location"
)

df_2_selection = df_2.query(
    "Registry == @registry"
)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_selection,
    use_container_width=True,
)

#chart
st.title(":bar_chart: SDG Distribution")
st.markdown("##")

# Altair Chart Code Reference: ChatGPT
data = pd.DataFrame({
    'Category': df_2_selection.iloc[:, 0].values,
    'Goal 1': df_2_selection.iloc[:, 1].values,
    'Goal 2': df_2_selection.iloc[:, 2].values,
    'Goal 3': df_2_selection.iloc[:, 3].values,
    'Goal 4': df_2_selection.iloc[:, 4].values,
    'Goal 5': df_2_selection.iloc[:, 5].values,
    'Goal 6': df_2_selection.iloc[:, 6].values,
    'Goal 7': df_2_selection.iloc[:, 7].values,
    'Goal 8': df_2_selection.iloc[:, 8].values,
    'Goal 9': df_2_selection.iloc[:, 9].values,
    'Goal 10': df_2_selection.iloc[:, 10].values,
    'Goal 11': df_2_selection.iloc[:, 11].values,
    'Goal 12': df_2_selection.iloc[:, 12].values,
    'Goal 13': df_2_selection.iloc[:, 13].values,
    'Goal 14': df_2_selection.iloc[:, 14].values,
    'Goal 15': df_2_selection.iloc[:, 15].values,
    'Goal 16': df_2_selection.iloc[:, 16].values,
    'Goal 17': df_2_selection.iloc[:, 17].values,
})

# Melt the DataFrame to get values stacked
data_melted = data.melt(id_vars='Category', var_name='ValueType', value_name='Value')

# Create a layered horizontal bar chart
chart = alt.Chart(data_melted).mark_bar().encode(
    x=alt.X('Value:Q', title='Count'),
    y=alt.Y('Category:N', title='Registry'),
    color=alt.Color('ValueType:N', legend=alt.Legend(title="SDGs"),
                    sort=[f'Goal {i}' for i in range(1, 18)])
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)

# Show SDG Details
st.title(':open_book: SDG Descriptions')

st.dataframe(
    df_3.iloc[:, :3],
    use_container_width=True,
    hide_index=True
)