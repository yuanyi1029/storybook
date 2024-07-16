import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_SECRET"]
client = OpenAI(api_key=api_key)

def create_story(prompt):
  completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages = [
      {"role": "system", "content": "You are a bestseller story writer. You will take user's prompt and generate a 100 words short story for adults aged 20-30."},
      {"role": "user", "content": f'{prompt}'}
    ],
    max_tokens = 400,
    temperature = 0.8
  )

  story = completion.choices[0].message.content
  return story

def refine_story(story):
  completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages = [
      {"role": "system", "content": """
        Based on the story given, you will design a detailed image prompt for the cover of this story. The image prompt should
        include the theme of the story with relevant colour, suitable for adults. The image prompt should be within 50
        characters.
      """},
      {"role": "user", "content": f'{story}'}
    ],
    max_tokens = 50,
    temperature = 0.8
  )

  image_prompt = completion.choices[0].message.content
  return image_prompt

def create_image(prompt):
  completion = client.images.generate(
    model = "dall-e-2",
    prompt = f"{prompt}",
    size = "256x256",
    quality = "standard",
    n = 1
  )

  image_url = completion.data[0].url
  return image_url


st.subheader('Story Generator with OpenAI API', divider='rainbow')
with st.form(key="my_form"): 
  st.write("This is for users to write a story.")
  message = st.text_input(label="Some keywords to generate a story:")
  submitted = st.form_submit_button("Submit")

  if submitted:
    story = create_story(message)
    image_prompt = refine_story(story)
    image_url = create_image(image_prompt)

    st.balloons()
    st.write(story)
    st.image(image_url)
    st.write(image_prompt)

st.markdown("Enjoy! :sunflower:")