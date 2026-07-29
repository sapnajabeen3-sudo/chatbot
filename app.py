import streamlit as st
import requests
import json


# ------------------ Page Config ------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ------------------ CSS ------------------

st.markdown("""
<style>

/* Hide Streamlit Branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}


/* App Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color:white;
}


/* Header */

.title{
    text-align:center;
    font-size:52px;
    font-weight:900;
    color:white;
    margin-top:-20px;
}


.subtitle{
    text-align:center;
    color:#7dd3fc;
    font-size:22px;
    margin-bottom:30px;
}


/* Chat Bubble */

[data-testid="stChatMessage"]{
    border-radius:18px;
    padding:20px;
    margin-bottom:18px;
    border:1px solid rgba(255,255,255,.08);
    box-shadow:0 8px 25px rgba(0,0,0,.35);
}


/* Chat Text */

[data-testid="stChatMessageContent"] p{
    font-size:24px !important;
    font-weight:700 !important;
    line-height:1.8;
    color:white;
}


/* Chat Input */

textarea{
    font-size:22px !important;
    font-weight:600;
}


/* Sidebar */

section[data-testid="stSidebar"]{
    background:#111827;
}


section[data-testid="stSidebar"] *{
    color:white !important;
    font-size:19px !important;
}


/* Button */

.stButton>button{
    width:100%;
    border-radius:10px;
    font-size:18px;
    font-weight:bold;
    background:#2563eb;
    color:white;
}

</style>
""", unsafe_allow_html=True)



# ------------------ Header ------------------

st.markdown(
"""
<div class="title">
🤖 AI Assistant
</div>

<div class="subtitle">
Powered by Ollama • Llama 3.2
</div>

""",
unsafe_allow_html=True
)



# ------------------ Sidebar ------------------

with st.sidebar:

    st.markdown("# 🤖 AI Assistant")

    st.success("🟢 Ollama Connected")


    st.divider()


    st.markdown("## 🧠 Current Model")

    st.info("Llama 3.2")


    st.divider()


    st.markdown("## 🚀 Features")

    st.markdown("""
✅ **100% Local AI**

🔒 **No API Key Required**

🌐 **Offline Mode**

⚡ **Fast Responses**

💬 **Conversation Memory**

🧠 **Powered by Llama 3.2**
""")


    st.divider()


    if st.button("🗑 Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    st.caption("Made with ❤️ using Streamlit + Ollama")



# ------------------ Initialize Memory ------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



# ------------------ Display Chat History ------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])



# ------------------ User Input ------------------

prompt = st.chat_input(
    "Type your message..."
)



if prompt:


    # Save user message

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    # Display user message

    with st.chat_message("user"):

        st.markdown(prompt)



    # Assistant response

    with st.chat_message("assistant"):


        try:


            response = requests.post(

                "http://localhost:11434/api/chat",

                headers={
                    "Content-Type":"application/json"
                },

                json={

                    "model":"llama3.2",

                    "messages":st.session_state.messages,

                    "stream":True

                },

                stream=True,

                timeout=120

            )


            response.raise_for_status()



            # Stream Ollama Response

            def stream_response():


                for line in response.iter_lines():


                    if line:


                        data = json.loads(
                            line.decode("utf-8")
                        )


                        if (
                            "message" in data
                            and "content" in data["message"]
                        ):

                            yield data["message"]["content"]



            full_response = st.write_stream(
                stream_response()
            )



            # Save assistant response

            st.session_state.messages.append(

                {
                    "role":"assistant",
                    "content":full_response
                }

            )



        # Connection Error

        except requests.exceptions.ConnectionError:


            error_msg = (

                "⚠️ **Could not connect to Ollama**\n\n"

                "Please make sure Ollama is running.\n\n"

                "Run this command:\n\n"

                "`ollama run llama3.2`\n\n"

                "Then refresh the page."

            )


            st.error(error_msg)


            st.session_state.messages.append(

                {
                    "role":"assistant",
                    "content":error_msg
                }

            )



        # Timeout Error

        except requests.exceptions.Timeout:


            error_msg = (

                "⏳ **Response timeout**\n\n"

                "The model took too long. Try again."

            )


            st.error(error_msg)


            st.session_state.messages.append(

                {
                    "role":"assistant",
                    "content":error_msg
                }

            )



        # Other Errors

        except Exception as e:


            error_msg = (

                f"❌ **Error:** {str(e)}"

            )


            st.error(error_msg)


            st.session_state.messages.append(

                {
                    "role":"assistant",
                    "content":error_msg
                }

            )