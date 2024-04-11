import ollama 
import streamlit as st

st.title("KIIT-BOT")

# init models
if "model" not in st.session_state:
    st.session_state["model"] = ""

models = [model["name"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Choose your model", models)

#initialise history
if "messages" not in st.session_state:
    st.session_state["messages"]= []
    
def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt :=st.chat_input("What is up?"):
    # add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    #This block of code generates the respose using the Phi ollama API
    with st.chat_message("assistant"):        
        message=st.write_stream(model_res_generator()) #Structures the message
        st.markdown(message) #Sends message to screen
        st.session_state["messages"].append({"role": "assistant", "content":message })