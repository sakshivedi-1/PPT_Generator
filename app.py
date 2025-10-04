import streamlit as st
import re

# Import our separated modules
from UI import render_ui
from gemini_client import generate_content
from pexels_client import get_image_url
from ppt_generator import create_presentation


# Initialize session state for the presentation buffer
if "presentation_buffer" not in st.session_state:
    st.session_state.presentation_buffer = None

# Render the UI and get user inputs
user_inputs = render_ui()

# Check if the generate button was pressed
if user_inputs["generate_button"]:
    # Validate inputs
    if not user_inputs["google_api_key"] or not user_inputs["pexels_api_key"]:
        st.warning("Please enter both your Google Gemini and Pexels API keys in the sidebar.")
    elif not user_inputs["topic"]:
        st.warning("Please enter a topic for the presentation.")
    else:
        # If inputs are valid, run the generation process
        with st.spinner("Generating your presentation... This can take a minute or two."):
            
            # Step 1: Generate Outline
            st.info("Step 1/4: Generating slide outline...")
            outline_prompt = (
                f"Generate a slide outline for a {user_inputs['domain']} presentation on the topic: '{user_inputs['topic']}'. "
                f"The presentation should have a title slide and exactly {user_inputs['slide_count']} content slides. "
                f"Do not include a Q&A or Thank You slide. "
                f"The user has provided this additional context: '{user_inputs['additional_context']}'. "
                f"Format the output as a numbered list of slide titles. Example:\n"
                f"1. Title of Presentation\n2. First Content Slide Title\n3. Second Content Slide Title"
            )
            outline_str = generate_content(user_inputs["google_api_key"], outline_prompt)

            if not outline_str:
                st.error("Failed to generate outline. Please check your API key or try again.")
            else:
                slide_titles = [line.strip() for line in outline_str.split('\n') if re.match(r'^\d+\.\s*', line)]
                slide_titles = [re.sub(r'^\d+\.\s*', '', title) for title in slide_titles]

                if not slide_titles:
                    st.error("The AI did not return a valid outline. Please try a different topic.")
                else:
                    st.success("✅ Outline Generated!")
                    st.write(slide_titles)

                    all_slides_data = [{"title": slide_titles[0], "subtitle": f"A {user_inputs['domain']} Presentation by AI"}]
                    progress_bar = st.progress(0, text="Step 2/4: Generating slide content...")
                    total_slides = len(slide_titles[1:])

                    # Loop through outline to generate content for each slide
                    for i, title in enumerate(slide_titles[1:]):
                        progress_text = f"Generating content for slide {i+1}/{total_slides}: '{title}'"
                        progress_bar.progress((i + 1) / total_slides, text=progress_text)
                        
                        content_prompt = (
                            f"For a presentation on '{user_inputs['topic']}', generate 3-5 concise bullet points for the slide titled '{title}'. "
                            f"The overall presentation is for a {user_inputs['domain']} audience. "
                            f"Context: {user_inputs['additional_context']}. "
                            f"Format each bullet point on a new line, starting with a hyphen."
                        )
                        slide_content_str = generate_content(user_inputs["google_api_key"], content_prompt)
                        slide_bullets = slide_content_str.split('\n') if slide_content_str else []

                        image_query_prompt = (
                            f"Based on this slide title '{title}' and content '{slide_content_str}', "
                            f"provide a single, concise, and visually descriptive search query for a stock photo. "
                            f"The query should be 2-5 words. Do not add quotes."
                        )
                        image_query = generate_content(user_inputs["google_api_key"], image_query_prompt)
                        image_url = get_image_url(user_inputs["pexels_api_key"], image_query) if image_query else None

                        all_slides_data.append({"title": title, "content": slide_bullets, "image_url": image_url})

                    # Final step: Assemble the presentation
                    progress_bar.progress(1.0, text="Step 4/4: Assembling the PowerPoint file...")
                    presentation_buffer = create_presentation(all_slides_data)
                    st.session_state.presentation_buffer = presentation_buffer
                    
                    progress_bar.empty()
                    st.success("🎉 Your presentation is ready for download!")

# The download button logic remains here, as it depends on the app's state
if st.session_state.presentation_buffer:
    file_name = f"{user_inputs['topic'].replace(' ', '_') or 'presentation'}.pptx"
    st.download_button(
        label="Download Presentation (.pptx)",
        data=st.session_state.presentation_buffer,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )