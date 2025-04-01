# Install Library Google Play Scrapper
# !pip install google-play-scraper

# Import Library
import pandas as pd
from google_play_scraper import app, Sort, reviews

from datetime import time

# Set Google Play App ID
APP_ID = 'com.ruangguru.livestudents'     # Example: com.whatsapp, com.kai
LANG = 'id'                               # Language code (en, fr, es, etc.)
COUNTRY = 'id'                            # Country code (us, fr, etc.)
TARGET_COUNT = 11000                      # Total number of reviews to scrape
BATCH_SIZE = 200                          # Maximum reviews per request

def run_scraper():
    # Get app info
    try:
        app_info = app(APP_ID)
        print(f"\n📱 App Name: {app_info['title']}")
        print(" \nAverage Rating: {app_info['score']}")
        print(" \nInstalls: {app_info['installs']}")
        print(" \nGenre: {app_info['genre']}\n")
    except Exception as e:
        print(f"\n Error getting app info: {str(e)}")
        return

    all_reviews = []
    count = 0
    next_token = None  # Pagination token

    print("⏳ Scraping reviews...")
    while count < TARGET_COUNT:
        try:
            result, next_token = reviews(
                app_id=APP_ID,
                lang=LANG,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=BATCH_SIZE,  # Max per request
                continuation_token=next_token,  # Pagination token
            )

            if not result:
                break  # Stop if no more reviews

            all_reviews.extend(result)
            count = len(all_reviews)
            print(f"✅ Scraped {count} reviews...")

            if next_token is None:  # Stop when no more pages
                break

        except Exception as e:
            print(f"❌ Error scraping reviews: {str(e)}")
            break

    # Process reviews  #This line and the following lines were incorrectly indented
    reviews_df = pd.DataFrame([{
        'ulasan': review['content'],
    } for review in all_reviews])

    # Show preview
    print(f"\n✅ Successfully scraped {len(reviews_df)} reviews!")
    print("\nPreview of reviews:")
    display(reviews_df.head(5))

    # Save to CSV
    csv_filename = f"{APP_ID}_reviews.csv"
    reviews_df.to_csv(csv_filename, index=False)

if __name__ == "__main__":
    run_scraper()
