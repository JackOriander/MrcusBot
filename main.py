import openai
import requests
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
import os
import random

# OpenAI credentials
openai.api_key = "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"

# Instagram credentials
username = "daily_headlines_of_jack"
password = "713103aritra"

# News API credentials
news_api_key = "dd27e596a31646cf8045079ba26bafae"

# Previous headline
previous_headline = ""

while True:
    # Fetch the latest news headline from the News API
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={news_api_key}&q=West%20Bengal')
    data = response.json()
    headline = data['articles'][0]['title']

    # Check if the news headline is different from the previous one
    if headline != previous_headline:
        # Improve the headline using OpenAI's GPT-3
        prompt = f"Improve this headline: {headline}"
        model = "text-davinci-002"
        temperature = 0.5
        max_tokens = 60
        output = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        improved_headline = output.choices[0].text.strip()

        # Add some text to provide context
        context = "Here's the latest news from West Bengal."
        text = improved_headline + "\n\n" + context

        # Choose a random background color
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Create a new image with the text and the background color
        img = Image.new('RGB', (1080, 1080), color=color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=50)
        w, h = draw.textsize(text, font=font)
        draw.text(((1080-w)/2, (1080-h)/2), text, font=font, fill='white')

        # Save the image
        img.save('news.png')

        # Post the image on Instagram
        bot = Bot()
        bot.login(username=username, password=password)
        bot.upload_photo('news.png', caption=text)

        # Delete the image from the local directory
        os.remove('news.png')

        # Update the previous headline
        previous_headline = headline

    # Wait for 10 minutes before checking for a new news headline
    time.sleep(600)

