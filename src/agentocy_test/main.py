#!/usr/bin/env python
import sys
import warnings
import time
import streamlit as st

# from agentocy_test.crew import AgentocyTest
from crew import AgentocyTest

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    AgentocyTest().crew().kickoff(inputs=inputs)

st.set_page_config(
    page_title="AI Agency",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    )

if "step" not in st.session_state:
    st.session_state.step = 1

# session state form values
if "form_values" not in st.session_state:
    st.session_state.form_values = {
        "company_name": "Netflix",
        "linkedin_checkbox": True,
        "instagram_checkbox": True,
        "facebook_checkbox": True,
        "blog_post_checkbox": True,
        "company_description": "Netflix is a global entertainment powerhouse, offering a vast library of movies, TV shows, documentaries, and original content available for streaming anytime, anywhere. With a commitment to providing diverse and engaging stories from around the world, Netflix has revolutionized how we experience entertainment. Whether you’re into thrilling dramas, heartwarming comedies, or binge-worthy series, Netflix delivers endless options for every taste, making it the go-to platform for on-demand entertainment.",
        "social_media_examples": """**LinkedIn post:**
    Last week in New York, industry leaders gathered for an insightful session with Amy Reinhard, Netflix's President of Advertising, before getting an exclusive sneak peek of "Squid Game: The Experience" ahead of its official opening. 

    Here's a brief overview of the key takeaways:

    🎥 Engaging Content: Netflix continues to be the platform where audiences are deeply engaged with popular series and films. This high level of attention translates into meaningful opportunities for brands to connect with viewers.

    🤝 Programmatic Partnerships: We are enhancing our advertising capabilities through strategic partnerships with The Trade Desk, Google’s DV360, and Microsoft. These collaborations provide advertisers with improved access to our inventory, offering more choice and flexibility. Look out for the launch of our programmatic guarantee on November 1st!

    🔍 Innovative Solutions: Our foundational advertising solutions, such as 'Top 10' targeting, sponsorships, and creative formats like Pause Ads and Keep Watching Ads, are proving to be highly effective. Notably, our sponsorships can achieve three times more ad recall compared to traditional linear TV.

    We are committed to providing innovative and effective advertising solutions that drive results. Exciting times ahead for brands looking to make a significant impact!

    hashtag#NetflixAds hashtag#AWNewYork hashtag#ProgrammaticAdvertising hashtag#BrandEngagement
                            """
            
    }
    
# Callbacks for session state management
# def go_to_step2(company_name,linkedin_checkbox,instagram_checkbox,facebook_checkbox,blog_post_checkbox,company_description,social_media_examples):
def go_to_step2():
    # Checking for the company_name field
    if not (st.session_state.form_values["company_name"]):
        st.warning("Please fill out the Company Name field")
    # Checking for at least one platform selected for content generation
    elif not (st.session_state.form_values["linkedin_checkbox"] or st.session_state.form_values["instagram_checkbox"] or st.session_state.form_values["facebook_checkbox"] or st.session_state.form_values["blog_post_checkbox"]):
        st.warning("Please select at least one platform")
    elif not (st.session_state.form_values["company_description"]):
        st.warning("Please fill out the Company Description")                              
    else:
        with st.spinner("Generating your content..."):
            time.sleep(2)
            st.session_state.step = 2
            st.rerun()
    
        
def go_to_step1():
    st.session_state.step = 1



def main():
    # Step 1
    if st.session_state.step == 1:
        # Sidebar Section
        with st.sidebar:
            with st.form("Form"):
                st.session_state.form_values["company_name"] = st.text_input("Company Name", placeholder="Netflix", value=st.session_state.form_values["company_name"], key="company_name")
                st.markdown("#####")
                
                # Check boxs for selecting what to genarate.  
                st.write("Which platforms would you like to generate content for? ")
                st.session_state.form_values["linkedin_checkbox"] = st.checkbox("LinkedIn", value=st.session_state.form_values["linkedin_checkbox"], key="linkedin_checkbox")
                st.session_state.form_values["instagram_checkbox"] = st.checkbox("Instagram", value=st.session_state.form_values["instagram_checkbox"], key="instagram_checkbox")
                st.session_state.form_values["facebook_checkbox"] = st.checkbox("Facebook", value=st.session_state.form_values["facebook_checkbox"], key="facebook_checkbox")
                st.session_state.form_values["blog_post_checkbox"] = st.checkbox("Blog Post", value=st.session_state.form_values["blog_post_checkbox"], key="blog_post_checkbox")
                st.markdown("#####")
                
                # Expander with the company description text input area.
                st.write("Additional context:")

                with st.expander("Company Description"):
                    st.session_state.form_values["company_description"] = st.text_area("", placeholder="Describe your company here...", value=st.session_state.form_values["company_description"], key = "company_description", max_chars=800)
                with st.expander("Social media examples"):
                    st.session_state.form_values["social_media_examples"] = st.text_area(
                        "",
                        placeholder="Add some social media examples...",
                        key = "social_media_examples",
                        max_chars=4000,
                        value=st.session_state.form_values["social_media_examples"],
                    )
                
                
                # Form Submit button
                st.markdown("#####")
                submit_button = st.form_submit_button()
                if submit_button:                   
                    go_to_step2()
                    
        # Main section
        st.title("AI content generator")
        st.write("Fill out your company information in the sidebar and submit it to generate the content.")
                    
                
    # Step 2             
    if st.session_state.step == 2:
        # print(st.session_state.form_values)
        with st.sidebar:
            st.markdown("## Info")
            company_name_value = st.session_state.form_values["company_name"]
            st.markdown(f"Company Name: {company_name_value}")
            st.markdown("### Platforms:")
            selected_items = {
                "linkedin_checkbox": "LinkedIn",
                "instagram_checkbox": "Instagram",
                "facebook_checkbox": "Facebook",
                "blog_post_checkbox": "Blog Post"
            }
            # Loop through only selected checkboxes
            for key, value in selected_items.items():
                if st.session_state.form_values[key]:  # Check if the checkbox is selected
                    st.markdown(f"- {value}")
            st.markdown("####")
  
            # Go back button
            st.button("Go back", on_click=go_to_step1)
        
        # Main Section
        # Display results in tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 LinkedIn",
                "💼 Instagram",
                "🎯 Facebook",
                "💡 Blog Post",
            ]
        )
        
        with tab1:
            st.subheader("LinkedIn:")

if __name__ == "__main__":
    main()


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         AgentocyTest().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         AgentocyTest().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         AgentocyTest().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")
