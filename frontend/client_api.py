from pathlib import Path

import streamlit as st
import requests
import yaml

BASE_DIR = Path().parent.absolute()

with open(BASE_DIR / "app_config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

MIN_LINKS = 1
MAX_LINKS = 5
DEFAULT_LINKS = 1
LINK_STEP = 1
PROMPT_HEIGHT = 150

BACKEND_URL = f'http://localhost:{config['backend']['host']}/{config['backend']['port']}'

st.title(config['backend']['port'])

if "links" not in st.session_state:
    st.session_state.links = [""] * DEFAULT_LINKS

if "show_expander" not in st.session_state:
    st.session_state.show_expander = False

num_links = st.number_input(
    "Enter the number of links:",
    min_value=MIN_LINKS,
    max_value=MAX_LINKS,
    step=LINK_STEP,
    value=len(st.session_state.links),
    key="num_input"
)

if st.button("Open/Edit Links"):
    st.session_state.show_expander = True

if len(st.session_state.links) < num_links:
    st.session_state.links += [""] * (num_links - len(st.session_state.links))
elif len(st.session_state.links) > num_links:
    st.session_state.links = st.session_state.links[:num_links]

if st.session_state.show_expander:
    with st.expander("Enter your links", expanded=True):
        for i in range(num_links):
            st.session_state.links[i] = st.text_input(
                f"Link {i + 1}",
                value=st.session_state.links[i],
                key=f"link_{i}"
            )

st.subheader("Enter your prompt")
prompt = st.text_area(
    "Type your prompt here...",
    placeholder="Write something here...",
    height=PROMPT_HEIGHT,
    key="user_prompt"
)

if st.button("Start"):
    empty_links = [i + 1 for i, link in enumerate(st.session_state.links) if not link.strip()]
    if empty_links:
        st.error(f"Please fill all link fields! Empty: {empty_links}")
    elif not prompt.strip():
        st.error("Please enter a prompt!")
    else:
        payload = {
            "links": st.session_state.links,
            "prompt": prompt
        }
        try:
            response = requests.post(BACKEND_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            st.success("Data sent successfully!")
            st.write("Backend response:", data)
            if "youtube_url" in data:
                st.subheader("Video Result:")
                st.video(data["youtube_url"])
        except requests.exceptions.RequestException as e:
            st.error(f"Error sending data: {e}")