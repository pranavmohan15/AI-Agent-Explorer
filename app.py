import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Agent SDK Explorer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Schemas ----------------

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    cooking_time: str
    instructions: List[str]


class Movie(BaseModel):
    title: str
    casting: List[str]
    total_hour: float


# ---------------- AI Functions ----------------

def recipe_generator(dish_name: str, client):

    prompt = f"""
Generate a detailed recipe for {dish_name}

Return JSON with:
title
ingredients (list)
cooking_time
instructions (list)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    recipe_json = response.choices[0].message.content
    recipe = Recipe.model_validate_json(recipe_json)

    return recipe


def movie_description(movie_name: str, client):

    prompt = f"""
Give details about the movie "{movie_name}"

Return JSON with:
title
casting (list of actors)
total_hour (runtime in hours)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    movie_json = response.choices[0].message.content
    movie = Movie.model_validate_json(movie_json)

    return movie


# ---------------- UI ----------------

st.title("🤖 AI Agent Explorer")
st.markdown("Explore the capabilities of your AI agents.")

# Sidebar
with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "OpenAI API Key",
        type="password"
    )

    if not api_key:
        st.warning("Please enter your OpenAI API key")

# Tabs
tab1, tab2 = st.tabs(["🍳 Recipe Generator", "🎬 Movie Info"])


# ---------------- Recipe Tab ----------------

with tab1:

    st.header("Recipe Generator")

    dish = st.text_input(
        "What would you like to cook?",
        placeholder="e.g. Pasta Carbonara"
    )

    if st.button("Generate Recipe"):

        if not api_key:
            st.error("API Key missing!")

        else:
            try:

                client = OpenAI(api_key=api_key)

                with st.spinner("Chef AI is cooking..."):

                    recipe = recipe_generator(dish, client)

                    st.success(f"Recipe for {recipe.title}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Ingredients")
                        for ing in recipe.ingredients:
                            st.write(f"- {ing}")

                    with col2:
                        st.subheader("Cooking Time")
                        st.write(recipe.cooking_time)

                    st.subheader("Instructions")

                    for i, step in enumerate(recipe.instructions):
                        st.write(f"{i+1}. {step}")

            except Exception as e:
                st.error(f"Error: {e}")


# ---------------- Movie Tab ----------------

with tab2:

    st.header("Movie Description")

    movie_name = st.text_input(
        "Enter movie name",
        placeholder="e.g. Thanmathra"
    )

    if st.button("Get Movie Info"):

        if not api_key:
            st.error("API Key missing!")

        else:
            try:

                client = OpenAI(api_key=api_key)

                with st.spinner("Fetching movie details..."):

                    movie = movie_description(movie_name, client)

                    st.success("Movie Information")

                    st.write("**Title:**", movie.title)

                    st.write("**Runtime (hours):**", movie.total_hour)

                    st.write("**Cast:**")

                    for actor in movie.casting:
                        st.write(f"- {actor}")

            except Exception as e:
                st.error(f"Error: {e}")