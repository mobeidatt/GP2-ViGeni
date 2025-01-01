# -*- coding: utf-8 -*-
"""ViGeni Code GP2.ipynb


pip install moviepy transformers torch pillow

pip install SpeechRecognition

"""# Vid to Text"""

pip install AudioSegment

import speech_recognition as sr
import moviepy.editor as mp
import os
from pydub import AudioSegment

video_path = "/content/The Bird and the Whale — US English accent (TheFableCottage.com).mp4"

clip = mp.VideoFileClip(video_path)
clip.audio.write_audiofile(r"converted.wav")

# Load the audio file with pydub (can handle large audio files more efficiently)
audio = AudioSegment.from_wav("converted.wav")

chunk_length_ms = 30 * 1000  # 30 seconds
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

r = sr.Recognizer()

full_result = ""
for i, chunk in enumerate(chunks):
    chunk_path = f"chunk_{i}.wav"
    chunk.export(chunk_path, format="wav")

    with sr.AudioFile(chunk_path) as source:
        audio_file = r.record(source)
        try:
            result = r.recognize_google(audio_file)
            full_result += result + " "
        except sr.UnknownValueError:
            print(f"Chunk {i}: Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Chunk {i}: Could not request results from Google Speech Recognition service; {e}")

    os.remove(chunk_path)

# Exporting the result to a text file
with open('recognized.txt', mode='w') as file:
    file.write(full_result)
    print("ready!")

"""##Summrized Text

"""

from transformers import pipeline

summarizer = pipeline("summarization")

text = ""
with open("recognized.txt", "r") as file:
    text = file.read()

original_length = max(1, int(len(text.split()) * 0.3))
summary = summarizer(text, max_length=original_length, min_length=int(original_length*0.8), do_sample=False)

print(summary)

summary_text = summary[0]["summary_text"]

len(summary_text.split())

if len(summary_text.split()) < 100:
  current_loops = 3 #0-99
elif len(summary_text.split()) < 200:
  current_loops = 4 #100-199
elif len(summary_text.split()) < 300:
  current_loops = 5 #200-299
elif len(summary_text.split()) < 400:
  current_loops = 6 #300-399
elif len(summary_text.split()) < 600 and len(summary_text.split()) >= 400:
  current_loops = 7 #400-599
elif len(summary_text.split()) < 800 and len(summary_text.split()) >= 600:
  current_loops = 8 #600-799
elif len(summary_text.split()) < 1000 and len(summary_text.split()) >= 800:
  current_loops = 9 #800-999
elif len(summary_text.split()) >= 1000:
  current_loops = 10 #1000+

int(len(summary_text.split())/current_loops)

" ".join(summary_text.split()[0:10])

li = []
group_size = len(summary_text.split()) // current_loops

for i in range(0, len(summary_text.split()), group_size):
    if len(li) == current_loops - 1:
        li.append(" ".join(summary_text.split()[i:]))
        break
    li.append(" ".join(summary_text.split()[i:i + group_size]))

print(li)

len(li)

pip install openai

pip install openai fpdf requests

"""# **Create A Title for the Story**"""

final_string = "create title image for this prompts " + summary_text

final_string

"""# Title image"""

from openai import OpenAI
from IPython.display import Image, display
import requests
import time
client = OpenAI(api_key="API KEY")


response = client.images.generate(
model="dall-e-3",
prompt=final_string,
size="1024x1024",
quality="standard",n=1,
    )

image_url = response.data[0].url
print(final_string)

image_data = requests.get(image_url).content
file_name = "Title_image_.png"
with open(file_name, "wb") as image_file:
     image_file.write(image_data)

display(Image(url=image_url))

time.sleep(10)

print("Images saved successfully.")

"""# Content images"""

client = OpenAI(api_key="API KEY")

z = 0
for i in li:
    response = client.images.generate(
        model="dall-e-3",
        prompt=i,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print(li[z])

    image_data = requests.get(image_url).content
    file_name = f"generated_image_{z}.png"
    with open(file_name, "wb") as image_file:
        image_file.write(image_data)

    display(Image(url=image_url))

    z += 1
    time.sleep(10)

print("Images saved successfully.")

from IPython.display import Image, display

# Number of images you saved
num_images = z  # Replace z with the actual number of images saved

for i in range(num_images):
    file_name = f"generated_image_{i}.png"

splited=text.split(" ")
numOfWords=len(splited)/len(li)
numOfWords=int(numOfWords)
numOfWords

with open('/content/recognized.txt', 'r') as file:
    words = file.read().split()

# Group words into chunks of 20
chunks = []
for i in range(0, len(words), numOfWords):
    chunk = " ".join(words[i:i+numOfWords])
    chunks.append(chunk)

client = OpenAI(api_key="API KEY")


response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt=f"Create a title for the story based on the following summary:\n{summary_text}",
  max_tokens=17
)

title = response.choices[0].text.strip()
title

from fpdf import FPDF
import os
from openai import OpenAI

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

logo_path = "/content/My logo.jpeg"
title_image_path = "/content/Title_image_.png"

def apply_page_theme(pdf):
    pdf.set_fill_color(230, 240, 255)  # Light blue background color
    pdf.rect(0, 0, 210, 297, 'F')  # Fill the entire page with the background color

    # Add a decorative frame
    pdf.set_draw_color(100, 130, 180)  # Soft blue frame color
    pdf.set_line_width(1.5)
    pdf.rect(12, 12, 186, 273)  # Draw a slightly inset frame

    # Add the logo
    pdf.image(logo_path, x=170, y=10, w=25)  # Adjust x, y, and w for position and size

# Title Page
pdf.add_page()
apply_page_theme(pdf)

# Add the title text with smaller font and nicer style
pdf.set_font("Times", "B", size=18)  # Smaller size and nicer font (Times Bold)
pdf.set_text_color(40, 70, 120)  # Soft blue text color
pdf.set_xy(10, 50)  # Position the title
pdf.multi_cell(0, 10, txt=title, align="C")  # Center the title text

# Add the title image
pdf.image(title_image_path, x=35, y=80, w=140)  # Adjust x, y, and w for positioning

# Additional Pages (With or Without Images)
w = 0
for i in range(len(li)):  # 'li' contains the split summary text
    file_name = f"generated_image_{i}.png"

    # Add a new page
    pdf.add_page()
    apply_page_theme(pdf)  # Apply the theme to this page

    # Use the unique caption as the title for each page
    ##pdf.set_font("Arial", "B", size=13)
    ##pdf.set_text_color(60, 90, 130)  # Darker blue text color for title
    ##pdf.set_xy(12, 45)  # Position the title below the logo
    ##pdf.multi_cell(0, 10, txt=li[i], align="C")

    # Add a space for the image or extra padding if there's no image
    pdf.ln(10)

    if os.path.exists(file_name):
        # Center the image on the page with extra padding for a "storybook" layout
        pdf.image(file_name, x=31, y=33, w=150, h=145)  # Position image with more padding
    else:
        # Add placeholder text for pages without images (optional)
        pdf.set_font("Arial", "I", size=15)
        pdf.set_text_color(100, 100, 100)
        pdf.set_xy(25, 120)
        pdf.multi_cell(0, 10, txt="No image available for this section.", align="C")

    # Add a text area for additional description or content
    pdf.set_font("Arial", "", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(25, 180)
    pdf.multi_cell(163, 10, txt=chunks[w], align="L")
    w += 1

# Save the decorated storybook PDF to a file
pdf.output("storybook.pdf")
print("Your Story is Ready!!")
