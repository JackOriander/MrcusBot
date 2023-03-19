import requests
import os
import random
from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
from datetime import datetime, timedelta

# Set Google News API credentials
api_key = "dd27e596a31646cf8045079ba26bafae"

# Google News API endpoint
url = "https://newsapi.org/v2/top-headlines"

# Set country for news
country = "in"

# Set the font, font size, and text color for the headline and additional text
font_path = "/usr/share/fonts/google-crosextra-caladea/Caladea-Bold.ttf"
headline_font = ImageFont.truetype(font_path, 50)
text_font = ImageFont.truetype(font_path, 30)
text_color = (255, 255, 255)

# Set the directory for saving the image file
image_dir = "images"

# Set up the Instagram bot
bot = Bot()
bot.login(username="daily_headlines_of_jack", password="713103aritra")

# Get the current time
now = datetime.now()

# Set the time to check for news
news_time = now.replace(hour=9, minute=0, second=0, microsecond=0)

# Loop indefinitely
while True:
    # Check if it's time to get news
    if now >= news_time:
        # Get news from Google News API
        params = {
            "apiKey": api_key,
            "country": country,
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Check if news articles were found
        if len(data["articles"]) > 0:
            # Choose a random background color for the image
            bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Get the first headline and article text
            headline = data['articles'][0]['title']
            description = data['articles'][0]['description']

            # Create a new image
            img = Image.new("RGB", (1080, 1080), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Add the headline and additional text to the image
            draw.text((100, 200), headline, fill=text_color, font=headline_font)
            draw.text((100, 400), description, fill=text_color, font=text_font, spacing=10)

            # Save the image to a file
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            filename = os.path.join(image_dir, "news_image.jpg")
            img.save(filename)

            # Post the image on Instagram
            bot.upload_photo(filename, caption=f"{headline}\n\n{description}")

            print("News posted on Instagram.")
        else:
            print("No news found.")

        # Set the time to check for news tomorrow
        news_time += timedelta(days=1)

    # Sleep for 1 hour before checking the time again
    time.sleep(3600)
    now = datetime.now()
