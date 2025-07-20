import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('bacteria.csv')

st.title("Bacteria Resistance Visualization")

# size
df["Combined_MIC"] = df["Streptomycin"] + df["Neomycin"]
df["Size"] = (df["Combined_MIC"]) + 15

data_layer = alt.Chart(df).mark_circle(opacity=0.7).encode(
    x=alt.X("Streptomycin:Q", title="Streptomycin MIC"),
    y=alt.Y("Neomycin:Q", title="Neomycin MIC"),
    color=alt.Color("Gram_Staining:N", title="Gram Stain"),
    size=alt.Size("Size:Q", legend=None),
    tooltip=["Bacteria", "Streptomycin", "Neomycin", "Gram_Staining"]
).interactive()

# Annotation layer
ANNOTATIONS = [
    (0.3, 1.8, "🙂", "Small antibiotic dose stops growth!"),
    (12.5, 9.8, "😮", "More resistant to Streptomycin than Neomycin"),
    (9.8, 37.5, "😱", "Neomycin's not helpful at all!"),
]

annotations_df = pd.DataFrame(
    ANNOTATIONS, columns=["Streptomycin", "Neomycin", "marker", "description"]
)

annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=25, dx=-10, dy=0, align="left")
    .encode(
        x="Streptomycin:Q",
        y="Neomycin:Q",
        text="marker",
        tooltip="description"
    )
)

combined_chart = (data_layer + annotation_layer).properties(
    width=700, height=500
)
st.altair_chart(combined_chart, use_container_width=True)
