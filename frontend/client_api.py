import streamlit as st
import requests

st.title("Smart Video Search")

# --- Number of links ---
num_links = st.number_input(
    "Enter the number of links:",
    min_value=1,
    max_value=5,
    step=1,
    value=1,
    key="num_input"
)

if "links" not in st.session_state:
    st.session_state.links = [""] * num_links

if "show_expander" not in st.session_state:
    st.session_state.show_expander = False

if st.button("Open/Edit Links"):
    st.session_state.show_expander = True

# Adjust links list length
if len(st.session_state.links) < num_links:
    st.session_state.links += [""] * (num_links - len(st.session_state.links))
elif len(st.session_state.links) > num_links:
    st.session_state.links = st.session_state.links[:num_links]

# Expander for link inputs
if st.session_state.show_expander:
    with st.expander("Enter your links", expanded=True):
        for i in range(num_links):
            st.session_state.links[i] = st.text_input(
                f"Link {i + 1}",
                value=st.session_state.links[i],
                key=f"link_{i}"
            )

# Prompt input
st.subheader("Enter your prompt")
prompt = st.text_area(
    "Type your prompt here...",
    placeholder="Write something here...",
    height=150,
    key="user_prompt"
)

# Start button
if st.button("Start"):
    # --- Validation ---
    empty_links = [i + 1 for i, link in enumerate(st.session_state.links) if not link.strip()]

    if empty_links:
        st.error(f"Please fill all link fields! Empty: {empty_links}")
    elif not prompt.strip():
        st.error("Please enter a prompt!")
    else:
        # --- Send to backend ---
        payload = {
            "links": st.session_state.links,
            "prompt": prompt
        }

        response = requests.post("http://localhost:5000/process", json=payload)

        if response.status_code == 200:
            st.success("Data sent successfully!")
            st.write("Backend response:", response.json())
        else:
            st.error(f"Error sending data: {response.status_code}")
