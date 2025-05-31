import streamlit as st

# --- Email Generation Logic (Simplified & Template-Based) ---
def generate_email_draft(prompt, intent, recipient_name="", paper_details="", other_info=""):
    """
    Generates a draft email based on intent and user inputs using predefined templates.
    This function simulates the AI's drafting capability for demonstration purposes.
    """
    salutation = f"Dear {recipient_name if recipient_name else 'Colleague'},"
    # Basic closing, can be expanded
    closing = "Sincerely,\n\n[Your Name]\n[Your Title/Affiliation]\n[Your Contact Information (Optional)]"
    body = ""
    subject_prefix = f"Regarding: {intent}"

    # --- Email Templates based on Intent ---
    if intent == "Inquiry":
        subject = f"{subject_prefix} - {other_info[:30] if other_info else 'Question'}"
        body = (
            f"I hope this email finds you well.\n\n"
            f"{prompt}\n\n"
            f"I am writing to respectfully inquire about {other_info if other_info else '[the specific topic of your inquiry]'}.\n"
            f"{f'I recently came across your publication, \"{paper_details}\", and found it particularly insightful in relation to my current research.' if paper_details else ''}\n\n"
            "Any information, guidance, or relevant resources you could share would be greatly appreciated.\n\n"
            "Thank you for your time and consideration."
        )
    elif intent == "Submission":
        subject = f"{subject_prefix} - Manuscript Submission: \"{paper_details[:30] if paper_details else '[Manuscript Title]'}\""
        body = (
            f"I hope this email finds you well.\n\n"
            f"Please find attached my manuscript titled \"{paper_details if paper_details else '[Your Manuscript Title]'}\" for consideration for publication in {other_info if other_info else '[Name of Journal/Conference]'}.\n\n"
            f"{prompt}\n\n" # User prompt can contain abstract or cover letter key points
            "I believe this work aligns well with the scope of your publication and will be of interest to your readership.\n"
            "All authors have approved the manuscript and its submission.\n\n"
            "Thank you for your time and consideration. I look forward to hearing from you regarding the review process."
        )
    elif intent == "Thank You":
        subject = f"{subject_prefix} - Appreciation for {other_info[:30] if other_info else 'Your Assistance'}"
        body = (
            f"I hope this email finds you well.\n\n"
            f"{prompt}\n\n"
            f"I am writing to express my sincere gratitude for {other_info if other_info else '[the specific reason for your thanks, e.g., your insightful presentation, your help with XYZ]'}.\n"
            f"{f'Your input regarding \"{paper_details}\" was particularly valuable and has greatly assisted me.' if paper_details else ''}\n\n"
            "Thank you once again for your generosity and support."
        )
    elif intent == "Collaboration Request":
        subject = f"{subject_prefix} - Potential Research Collaboration on {other_info[:30] if other_info else 'a Project'}"
        body = (
            f"I hope this email finds you well.\n\n"
            f"{prompt}\n\n"
            f"I am writing to explore the possibility of a research collaboration concerning {other_info if other_info else '[the specific area/topic of collaboration]'}.\n"
            f"{f'My research, particularly my work on \"{paper_details}\", shares common ground with your expertise, and I believe a joint effort could lead to significant advancements.' if paper_details else 'I have been following your work with great interest and believe our research interests align.'}\n\n"
            "I would be delighted to discuss this potential collaboration further and explore how we might combine our strengths. Please let me know if you would be available for a brief meeting at your convenience.\n\n"
            "Thank you for considering this proposal."
        )
    elif intent == "Follow-up":
        subject = f"{subject_prefix} - Follow-up on {other_info[:30] if other_info else 'Previous Correspondence'}"
        body = (
            f"I hope this email finds you well.\n\n"
            f"{prompt}\n\n" # User prompt can add context to the follow-up
            f"I am writing to kindly follow up on my previous email regarding {other_info if other_info else '[the subject of your previous email]'}"
            f"{f' (sent on {paper_details})' if paper_details else ''}. " # Using paper_details for 'sent on date' as a simple field
            "I understand you have a busy schedule, but I wanted to ensure my message reached you and see if you have had a chance to consider it.\n\n"
            "Please let me know if there is any further information I can provide.\n\n"
            "Thank you for your time and attention to this matter."
        )
    else: # General Email
        subject = f"{subject_prefix} - {prompt[:30]}"
        body = f"{prompt}\n\n{other_info}"

    full_email = f"Subject: {subject}\n\n{salutation}\n\n{body}\n\n{closing}"
    return full_email

# --- Streamlit App UI Configuration ---
st.set_page_config(layout="wide", page_title="Academic Email Drafter AI")

# --- Main Application ---
st.title("🎓 Academic Email Drafter AI")
st.markdown("""
Welcome to the Academic Email Drafter AI assistant. This tool helps you craft professional emails for various academic purposes.
Please provide a core prompt, select the email's intent, and fill in any optional details to generate a draft.

**Note:** The "AI" generation in this demo is based on pre-defined templates to illustrate the concept.
For a full implementation, this would involve sophisticated NLP models.
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
            draft = generate_email_draft(
                prompt=user_prompt,
                intent=selected_intent,
                recipient_name=recipient_name,
                paper_details=paper_info,
                other_info=other_info
            )
            st.session_state.draft = draft
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
