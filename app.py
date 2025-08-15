import streamlit as st
from openai import OpenAI

st.title("Simple LLM Chat App")
st.divider()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=st.secrets["OPENROUTER_API_KEY"],
)


# set a default model
if "openai_model" not in st.session_state: # st.session_state is a dictionary-like object that stores session state variables
    st.session_state["openai_model"] = "openai/gpt-oss-20b:free"
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history if available 
for message in st.session_state.messages:
    with st.container():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# user inputs
if prompt := st.chat_input("Ask anything."): 
    # add message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # ai response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                # m["role"] is used to identify the speaker (user or assistant)
                for m in st.session_state.messages
            ],
            stream=True, 
        )
        response = st.write_stream(stream) 
    st.session_state.messages.append({"role": "assistant", "content": response})













# from openai import OpenAI
# import streamlit as st

# st.title("ChatGPT-like clone")

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=st.secrets["OPENROUTER_API_KEY"],
# )

# # client = OpenAI(api_key=st.secrets["OPENROUTER_API_KEY"])

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "openai/gpt-oss-20b:free"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})
