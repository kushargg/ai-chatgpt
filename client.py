from openai import OpenAI

# Replace "CORRECT_API_KEY" with your actual OpenAI API key (without quotes)
client = OpenAI(api_key="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")

try:
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
          {"role": "user", "content": "what is coding"}
      ]
  )
  print(completion.choices[0].message.content)
except Exception as err:
  # Handle the error more gracefully, log the error message, etc.
  print(f"An error occurred: {err}")