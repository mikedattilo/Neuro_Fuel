# Initialize Groq client
def initialize_groq_client(api_key):
    from groq import Groq
    try:
        client = Groq(api_key=api_key)
        print("Groq client initialized successfully.")
        return client
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        raise

# Create function to generate a text script using Groq client
def generate_text_script(client):
    from datetime import datetime

    # Code to create a topic for the day
    daily_topics = {
        "Monday": "Start your week with purpose",
        "Tuesday": "The power of consistency",
        "Wednesday": "Overcoming self-doubt",
        "Thursday": "Discipline beats motivation",
        "Friday": "Success is built daily",
        "Saturday": "Rest is productive too",
        "Sunday": "Prepare your mind for the week ahead"
    }

    # Get current day of the week, then apply it. Includes fallback in case of error
    day_of_week = datetime.now().strftime("%A")
    topic = daily_topics.get(day_of_week, "Personal growth and mindset")

    # Create content instructions
    content_instructions = f'''
    You are a creative short-form scriptwriter for a YouTube Shorts channel. Write a short, punchy script that is engaging, emotional, or inspiring. The script must be:

    - No more than 30 words
    - Written in a way that grabs attention in the first sentence
    - Focused on the single topic outlined below
    - Easy to narrate aloud in under 30 seconds
    - Written in a conversational tone, like it's being said directly to the viewer
    - Do NOT write in first or second person.
    - DO NOT write anything that is not the script. Nothing about "here's the script" or "this is the script". Just write the script.
    - DO NOT include any footnotes, explanations, or additional context.

    End the script with a thought-provoking or emotional punch. 
    Do not include emojis or hashtags.

    Topic: {topic}
    '''

    # Create a chat completion
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user",
            "content": content_instructions},
        ]
    )

    return response.choices[0].message.content