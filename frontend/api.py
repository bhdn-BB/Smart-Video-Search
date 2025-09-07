import streamlit as st
import requests


MIN_LINKS = 1
MAX_LINKS = 5
DEFAULT_LINKS = 1
STEP_VALUE = 1
PROMPT_HEIGHT = 150

MIN_K = 1
MAX_K = 5

BACKEND_PORT = 5002
BACKEND_HOST = "http://localhost"
BACKEND_URL = f"{BACKEND_HOST}:{BACKEND_PORT}"


# -----------------------
# Helper functions
# -----------------------

def init_session_state():
    if "links" not in st.session_state:
        st.session_state.links = [""] * DEFAULT_LINKS
    if "show_links_expander" not in st.session_state:
        st.session_state.show_links_expander = False

def update_links_list(num_links):
    current_len = len(st.session_state.links)
    if current_len < num_links:
        st.session_state.links += [""] * (num_links - current_len)
    elif current_len > num_links:
        st.session_state.links = st.session_state.links[:num_links]

def render_links_inputs(num_links):
    if st.session_state.show_links_expander:
        with st.expander("Enter your links", expanded=True):
            for i in range(num_links):
                st.session_state.links[i] = st.text_input(
                    f"Link {i + 1}",
                    value=st.session_state.links[i],
                    key=f"link_{i}"
                )

def validate_inputs(prompt):
    empty_links = [i + 1 for i, link in enumerate(st.session_state.links) if not link.strip()]
    if empty_links:
        st.error(f"Please fill all link fields! Empty: {empty_links}")
        return False
    if not prompt.strip():
        st.error("Please enter a prompt!")
        return False
    return True

def send_to_backend(payload):
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

# -----------------------
# Streamlit UI
# -----------------------

st.title("Smart Video Search")

# Initialize session state
init_session_state()

# --- User inputs ---

col1, col2 = st.columns(2)
with col1:
    top_k = st.number_input(
        "Number of fragments",
        min_value=MIN_K,
        max_value=MAX_K,
        step=STEP_VALUE,
        value=DEFAULT_LINKS,
        key="num_fragments"
    )

with col2:
    num_links = st.number_input(
        "Number of links",
        min_value=MIN_LINKS,
        max_value=MAX_LINKS,
        step=STEP_VALUE,
        value=len(st.session_state.links),
        key="num_links_input"
    )

if st.button("Open/Edit Links"):
    st.session_state.show_links_expander = True

# Adjust links list dynamically
update_links_list(num_links)
render_links_inputs(num_links)

# --- Prompt input ---
st.subheader("Enter your prompt")
prompt = st.text_area(
    "Type your prompt here...",
    placeholder="Write something here...",
    height=PROMPT_HEIGHT,
    key="user_prompt"
)

# --- Start processing ---
if st.button("Start"):
    if validate_inputs(prompt):
        payload = {
            "links": st.session_state.links,
            "prompt": prompt,
            "top_k": top_k
        }
        send_to_backend(payload)
