import streamlit as st
import os
import openai

# --- OpenAI API Configuration ---
# Access your API key from environment variables
try:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        st.error("⚠️ OpenAI API Key not found in environment variables. Please set it.")
    else:
        # Use the new OpenAI client initialization
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"⚠️ Error configuring OpenAI API: {e}")


# --- Email Generation Logic (Using OpenAI API) ---
def generate_email_draft(prompt, intent, recipient_name="", paper_details="", other_info=""):
    """
    Generates a draft email based on intent and user inputs using the OpenAI API (>= 1.0.0 syntax).
    """
    # Check if the client was initialized successfully
    if 'client' not in locals() and 'client' not in globals():
         return "Error: OpenAI API not configured. Please set your API key as an environment variable."

    try:
        # Construct a more detailed prompt for the AI
        ai_prompt = f"""
        Draft a professional academic email with the following details:

        Recipient Name: {recipient_name if recipient_name else 'Colleague'}
        Email Intent: {intent}
        Core Message/Key Points: {prompt}
        {f'Relevant Paper/Manuscript Details: {paper_details}' if paper_details else ''}
        {f'Other Specific Information: {other_info}' if other_info else ''}

        Please structure the email appropriately with a subject line, salutation, body, and closing.
        Ensure the tone is professional and academic.
        """

        # Use the new Chat Completions API syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or another suitable OpenAI model
            messages=[
                {"role": "system", "content": "You are a helpful academic email drafting assistant."},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=500, # Adjust as needed
            temperature=0.7 # Adjust for creativity vs. focus
        )
        return response.choices[0].message.content # Access content using .content

    except Exception as e:
        return f"Error generating email draft with OpenAI API: {e}"


# --- Streamlit App UI Configuration ---
st.set_page_config(layout="wide", page_title="Academic Email Drafter AI (OpenAI)")

# --- Main Application ---
st.title("🎓 Academic Email Drafter AI (Powered by OpenAI)")
st.markdown("""
Welcome to the Academic Email Drafter AI assistant. This tool helps you craft professional emails for various academic purposes using the power of OpenAI.
Please provide a core prompt, select the email's intent, and fill in any optional details to generate a draft.

**Note:** Ensure your OpenAI API Key is set as an environment variable named `OPENAI_API_KEY` on your deployment platform.
""")

# Initialize session state for the draft if it doesn't exist
if 'draft' not in st.session_state:
    st.session_state.draft = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("📬 Compose Your Email")

    user_prompt = st.text_area(
        "Your Core Prompt / Key Message:",
        height=120,
        placeholder="e.g., Inquire about Prof. Smith's recent paper on neuroplasticity and its implications for learning."
    )

    email_intent_options = ["Inquiry", "Submission", "Thank You", "Collaboration Request", "Follow-up", "General"]
    selected_intent = st.selectbox(
        "Select Email Intent:",
        email_intent_options,
        help="Choose the primary purpose of your email."
    )

    st.markdown("---")
    st.subheader("📄 Optional Details")
    recipient_name = st.text_input(
        "Recipient's Full Name (e.g., Dr. Eleanor Vance):",
        placeholder="Dr. Eleanor Vance"
    )

    # Dynamic label for paper_details based on intent
    paper_details_label = "Relevant Paper/Manuscript Title:"
    if selected_intent == "Submission":
        paper_details_label = "Your Manuscript Title:"
    elif selected_intent == "Follow-up":
        paper_details_label = "Date of Previous Email (e.g., 2024-05-15):"

    paper_info = st.text_input(
        paper_details_label,
        placeholder="e.g., 'The Impact of X on Y' or '2024-05-15'"
    )

    other_specific_info_label = "Other Specific Information:"
    if selected_intent == "Inquiry":
        other_specific_info_label = "Specific topic of inquiry:"
    elif selected_intent == "Submission":
        other_specific_info_label = "Name of Journal/Conference:"
    elif selected_intent == "Thank You":
        other_specific_info_label = "Reason for thanks (e.g., their helpful advice):"
    elif selected_intent == "Collaboration Request":
        other_specific_info_label = "Specific area/topic of collaboration:"
    elif selected_intent == "Follow-up":
        other_specific_info_label = "Subject of previous email:"

    other_info = st.text_area(
        other_specific_info_label,
        height=80,
        placeholder="Provide context relevant to the selected intent."
    )
    st.markdown("---")
    generate_button = st.button("✨ Generate Email Draft", use_container_width=True, type="primary")

# --- Main Area for Displaying Output and Errors ---
st.header("📝 Generated Email Draft")

if st.session_state.error_message:
    st.error(st.session_state.error_message)

if generate_button:
    if not user_prompt:
        st.session_state.error_message = "⚠️ Please enter a core prompt for your email in the sidebar."
        st.session_state.draft = "" # Clear previous draft if error
    else:
        st.session_state.error_message = "" # Clear error message
        with st.spinner("🤖 Drafting your email..."):
            # Ensure client is initialized before attempting generation
            if 'client' in locals() or 'client' in globals():
                 draft = generate_email_draft(
                    prompt=user_prompt,
                    intent=selected_intent,
                    recipient_name=recipient_name,
                    paper_details=paper_info,
                    other_info=other_info
                )
                 st.session_state.draft = draft
            else:
                 st.session_state.error_message = "⚠️ OpenAI API not configured. Please set your API key as an environment variable."


            # Automatically scroll or focus might be complex in Streamlit without custom components.
            # For now, the user will see the updated text area.

if st.session_state.draft:
    st.text_area(
        "Review and Edit Your Draft:",
        st.session_state.draft,
        height=500,
        help="You can copy this draft to your email client."
    )

    # Placeholder for email sending functionality
    st.markdown("---")
    st.subheader("✉️ Sending the Email (Conceptual)")
    st.info("""
    **How to Send:** Copy the generated draft above and paste it into your preferred email client.

    **Note on Direct Sending:** Actual email sending functionality (e.g., using `smtplib` in Python) is not implemented in this web demo.
    Implementing direct email sending would require:
    1.  Secure handling of your email credentials (username, password, or app-specific passwords).
    2.  Configuration of SMTP server details (e.g., for Gmail, Outlook, or your institutional email).
    3.  Careful error handling and security considerations to protect your information.
    This is typically done in a backend system or a local application where you can securely manage such sensitive data.
    """)
else:
    if not st.session_state.error_message: # Only show this if no error is displayed
        st.info("Please fill in the details in the sidebar and click 'Generate Email Draft'.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Academic Email Drafter AI - Demo</p>", unsafe_allow_html=True)
