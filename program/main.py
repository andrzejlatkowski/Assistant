import asyncio
from text_to_speach import play_audio
from speach_to_text import recognize_speech
from weather import get_weather
from wiki import get_wikipedia_page, speak_sections, read_wikipedia_section
from stocks import speak_stock_data


async def weather_assistant():
    play_audio("Say city and when")
    recognized_speach = recognize_speech()
    city, when = recognized_speach.split(' ', 1)
    await get_weather(city, when)

async def wiki_assistant():
    play_audio("What should I look for?")
    recognized_speach = recognize_speech()
    p_wiki = get_wikipedia_page(recognized_speach)
    sections_text = speak_sections(p_wiki)
    if not sections_text:
        return

    play_audio(f'Searching for the section titles of the {recognized_speach}')
    play_audio(sections_text)
    play_audio('Which title are you interested in?')
    section_title = recognize_speech()
    words = section_title.split()

    if len(words) > 1:
        formatted_section_title = words[0].title() + ' ' + ' '.join(word.lower() for word in words[1:])
        section_title = formatted_section_title
    if not section_title:
        return
    section_text = read_wikipedia_section(p_wiki, section_title)
    if section_text:
        play_audio(f'Searching for the description of the {recognized_speach}, and the section title {section_title}')
        play_audio(section_text)
    else:
        play_audio(f'The section title {section_title} not found')


async def stock_assistant():
    word_to_num = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90
    }
    def words_to_number(words):
        words = words.lower().split()
        number = 0
        for word in words:
            if word in word_to_num:
                number += word_to_num[word]
        return number

    play_audio("Say ticker symbol and how many days ago")
    recognized_speach = recognize_speech()
    try:
        ticker_symbol, days_ago_words = recognized_speach.split(' ', 1)
        days_ago = words_to_number(days_ago_words)
        await speak_stock_data(ticker_symbol, days_ago)
    except ValueError:
        play_audio("I didn't catch that. Please say the ticker symbol and the number of days ago again.")


async def assistant():
    try:
        play_audio("This is assistant. How may I help you?")
        while True:
            recognized_text = recognize_speech()
            print("You said:", recognized_text)

            if recognized_text == 'shut down':
                play_audio("Good bye.")
                break

            if 'weather' in recognized_text:
                await weather_assistant()
            elif 'wiki' in recognized_text or 'definition' in recognized_text or 'description' in recognized_text:
                await wiki_assistant()
            elif 'stock' in recognized_text or 'stocks' in recognized_text:
                await stock_assistant()
            else:
                play_audio("How may I help you?")
                continue

            play_audio("How may I help you?")
    except (KeyboardInterrupt, asyncio.CancelledError):
        play_audio("Shutting down. Goodbye.")

try:
    asyncio.run(assistant())
except KeyboardInterrupt:
    print("Assistant was interrupted.")

