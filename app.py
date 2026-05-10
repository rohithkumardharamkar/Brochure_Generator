import os
import time
import streamlit as st

from dotenv import load_dotenv
from google import genai

from scraper import fetch_website_content



load_dotenv()



client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


brochure_system_prompt = """
You are an AI assistant that creates professional company brochures.

Use markdown formatting.

Include:
- Company overview
- Products/services
- Culture
- Careers
- Customers
- Mission

Make the brochure:
- professional
- attractive
- easy to read
- beginner friendly
"""



def create_brochure(company_name, url):

    # Fetch website content
    website_content = fetch_website_content(url)

    # Final AI Prompt
    final_prompt = f"""
    Company Name:
    {company_name}

    Website URL:
    {url}

    Website Content:
    {website_content}

    Create a professional company brochure.
    """

    time.sleep(2)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=brochure_system_prompt + final_prompt
    )

    return response.text


st.set_page_config(
    page_title="AI Brochure Generator",

)

st.title("AI Brochure Generator")

st.write(
    "Generate professional company brochures using Gemini AI"
)



company_name = st.text_input(
    "Company Name"
)

website_url = st.text_input(
    "Website URL"
)



if st.button("Generate Brochure"):

    if company_name and website_url:

        with st.spinner(
            "Generating brochure..."
        ):

            try:

                result = create_brochure(
                    company_name,
                    website_url
                )

                st.markdown(result)

            except Exception as e:
                if "429" in str(e):

                    st.error(
                        "Gemini quota exceeded.\n\n"
                        "Wait 1 minute and try again."
                    )

                else:

                    st.error(
                        f"Error: {e}"
                    )

    else:

        st.warning(
            "Please enter all fields"
        )