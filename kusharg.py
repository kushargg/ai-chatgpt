from dotenv import load_dotenv
from openai import OpenAI
import datetime

load_dotenv()

client = OpenAI()

# Get the current date and time using Python's datetime module
now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD (ISO 8601)
current_time = now.strftime("%H:%M:%S")  # Format: HH:MM:SS
current_year = now.year

# Construct the prompt *using* the current date
prompt = f"Tell me a poem about today, which is {current_date}."  # Or include the time: {current_time}
# Or include the year: {current_year}

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "Tell me about 2025"},
    {"role": "user", "content": prompt}  # Use the formatted date in the prompt
  ]
)

print(completion.choices[0].message.content)