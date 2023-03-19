import requests
import random
import os
from newsapi import NewsApiClient
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
import openai

# Set up your NewsAPI API key and OpenAI API key
newsapi = NewsApiClient(api_key=os.getenv("dd27e596a31646cf8045079ba26bafae"))
openai.api_key = os.getenv("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")

# Set up your Instagram bot credentials
bot = Bot()
bot.login(username=os.getenv("daily_headlines_of_jack"), password=os.getenv("713103aritra"))

# Define a function to generate a solid color image
def generate_image(color):
    image = Image.new('RGB', (1080, 1080), color=color)
    return image

# Define a function to generate text with the OpenAI API
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# Define a function to post an image with a caption on Instagram
def post_to_instagram(image_path, caption):
    bot.upload_photo(image_path, caption=caption)

# Set up the initial background color
background_color = (255, 255, 255)

while True:
    # Get the latest news headlines for West Bengal
    news = newsapi.get_top_headlines(q="West Bengal", language="en", country="in")

    # Check if there are any articles
    if len(news["articles"]) == 0:
        print("No news found")
        continue

    # Choose a random article and extract the headline
    article = random.choice(news["articles"])
    headline = article["title"]

    # Generate additional text using OpenAI
    additional_text = generate_text(f"Tell me more about {headline}")

    # Combine the headline and additional text into a caption
    caption = f"{headline}\n\n{additional_text}"

    # Generate a random background color
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Generate the image
    image = generate_image(background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=72)
    w, h = draw.textsize(headline, font=font)
    x = (1080 - w) / 2
    y = (1080 - h) / 2
    draw.text((x, y), headline, fill=(255, 255, 255), font=font)

    # Save the image to a file
    image_path = "news.png"
    image.save(image_path)

    # Post the image to Instagram
    post_to_instagram(image_path, caption)

    # Wait for 24 hours before posting the next image
    time.sleep(24 * 60 * 60)  # in seconds
