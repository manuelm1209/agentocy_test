#!/usr/bin/env python
import sys
import warnings
import time
import streamlit as st
from datetime import datetime
# For Google Analytics
import streamlit.components.v1 as components


from crew import AgentocyTest
# from agentocy_test.crew import AgentocyTest

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(company_name,topic,company_description,social_media_examples):
    """
    Run the crew.
    """
    inputs = {
        "company_name" : company_name,
        "topic": topic,
        "company_description": company_description,
        "social_media_examples": social_media_examples,
        "current_year": datetime.now().year
    }
    crew_output = AgentocyTest().crew().kickoff(inputs=inputs)
    return(crew_output)

st.set_page_config(
    page_title="AI Agency",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    )

st.markdown(
    """
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-X0X8PRHHV0"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-X0X8PRHHV0');
        </script>
    """, unsafe_allow_html=True)

if "crew_output" not in st.session_state:
    st.session_state.crew_output = {}

if "step" not in st.session_state:
    st.session_state.step = 1

# session state form values
if "form_values" not in st.session_state:
    st.session_state.form_values = {
        "company_name": "Netflix",
        "topic": "Movies about Colombia",
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
# def go_to_step2(company_name,blog_post_checkbox,company_description,social_media_examples):
def go_to_step2():
    # Checking for the company_name field
    if not (st.session_state.form_values["company_name"]):
        st.warning("Please fill out the Company Name field")
    # Checking for the topic field
    if not (st.session_state.form_values["topic"]):
        st.warning("Please fill out the Topic field")
    # Checking for at least one platform selected for content generation
    elif not (st.session_state.form_values["company_description"]):
        st.warning("Please fill out the Company Description")                              
    else:
        st.caption("It may take up to two minutes to complete.")
        with st.spinner("Generating your content..."):
            crew_output = run(st.session_state.form_values["company_name"], st.session_state.form_values["topic"],st.session_state.form_values["company_description"],st.session_state.form_values["social_media_examples"])
            st.session_state.crew_output = crew_output
            # time.sleep(2)
            st.session_state.step = 2
            st.rerun()
    
        
def go_to_step1():
    st.session_state.step = 1



def main():
    # Step 1
    if st.session_state.step == 1:
        # Sidebar Section
        with st.sidebar:
            st.text("Fill out your company information and submit it to generate the content.")
            with st.expander("AI Agents and tasks:",expanded=False):
                st.markdown('''
                            ### Agents:
                            - Lead Market Analyst.
                            - Chief Data Strategist.
                            - Creative Content Director.
                            - Chief Content Officer.
                            ### Tasks and tools:
                            - Web search.
                            - Web scrape.
                            - Website RAG Search.
                            - Analyze market data.
                            - Create content.
                            - Blog post creation.
                            - Social Media post creation.
                            - Quality assurance.
                            ''')
            with st.form("Form"):
                st.session_state.form_values["company_name"] = st.text_input("Company Name:", placeholder="Netflix", value=st.session_state.form_values["company_name"], key="company_name")
                st.session_state.form_values["topic"] = st.text_input("Topic:", placeholder="Latest movies", value=st.session_state.form_values["topic"], key="topic")
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
        st.title("Social media and blog post AI content generator")
        st.write("")
        st.markdown("#")
        # Waiting List Call to action
        with st.container(border=True):
            st.markdown("### Join the Waiting List 🤞")
            st.text("I’m excited to share a product I’m working on for solopreneurs and small businesses.\nMy goal is to create something truly helpful and valuable for your journey. Sign up to stay updated and be among the first to give it a try!")
            st.link_button("Join the Waitlist", "https://agentocy.com/waiting-list/", type="primary")
        st.markdown("######")
        with st.container(border=True):
            st.markdown('''
                        ## AI Assistants for Solopreneurs and small business
                        
    Managing a small business or working as a solopreneur often means juggling many roles at once. This platform is here to lend a helping hand, offering tools to simplify tasks like creating content, drafting blog posts, and organizing ideas—all in one place.

    #### What You Can Expect:
    - More Time for What Matters: Automate routine tasks and free up your day.
    - Creative Support: Get fresh ideas and thoughtful suggestions to make your work easier.
    - Room to Grow: The platform will continue evolving to meet the needs of people like you.

    #### Why Join?

    This project is a work in progress, and I’m building it with your unique challenges in mind. By joining now, you’ll be part of its early stages and have the chance to shape its future. Let’s make running a small business or working solo a bit more manageable, together.
                        ''')
        
                    
                
    # Step 2             
    if st.session_state.step == 2:
        
        # Waiting List Call to action
        with st.container(border=True):
            st.markdown("### Join the Waiting List 🤞")
            st.text("I’m excited to share a product I’m working on for solopreneurs and small businesses.\nMy goal is to create something truly helpful and valuable for your journey. Sign up to stay updated and be among the first to give it a try!")
            st.link_button("Join the Waitlist", "https://agentocy.com/waiting-list/", type="primary")
        st.markdown("######")
        
        # print(st.session_state.form_values)
        with st.sidebar:
            st.markdown("# Input Information:")
            st.markdown("######")
            company_name_value = st.session_state.form_values["company_name"]
            topic = st.session_state.form_values["topic"]
            company_description = st.session_state.form_values["company_description"]
            social_media_examples = st.session_state.form_values["social_media_examples"]
            
            st.markdown(f"Company Name: {company_name_value}")
            st.markdown(f"Topic: {topic}")
            with st.expander("Company Description"):
                st.write(company_description)
            with st.expander("Social media examples"):
                st.text(social_media_examples)
  
            # Go back button
            st.button("Go back", on_click=go_to_step1)
        
        # Main Section
        # Display results in tabs
        tab1, tab2 = st.tabs(
            [
                "🐦 Social Media",
                "📝 Blog Post",
            ]
        )
        
        with tab1:
            st.markdown("######")
            
            with st.container(border=True):
                rows = [st.columns(2, vertical_alignment="top", gap="large"), st.columns(2, vertical_alignment="top", gap="large")]
                columns = rows[0] + rows[1]
                
                # Iterate through the posts and assign each one to a column
                for col, post in zip(columns, st.session_state.crew_output.pydantic.social_media_posts):
                    with col:
                        st.markdown("######")
                        st.subheader(post.platform)
                        
                        # Stream generator
                        def stream_data():
                            for word in post.content.split(" "):
                                yield word + " "
                                time.sleep(0.02)
                                
                        st.write_stream(stream_data)  # Display the streamed post content     
        
                # for post in st.session_state.crew_output.pydantic.social_media_posts:

                    
                #     st.subheader(post.platform)
                    
                #     # Stream generator
                #     def stream_data():
                #         for word in post.content.split(" "):
                #             yield word + " "
                #             time.sleep(0.02)
                            
                #     st.write_stream(stream_data)
                #     st.divider()
            
        with tab2:
            st.markdown("######")
            st.markdown(st.session_state.crew_output.pydantic.article)

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
