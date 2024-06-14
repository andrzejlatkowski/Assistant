import python_weather
import asyncio
from datetime import datetime, timedelta
from text_to_speach import play_audio

def get_weather_text(when, temperature, description):
    if when == 'today':
        return f'Now it is {temperature} degrees Celsius, and the weather is {description}'
    elif when == 'tomorrow':
        return f"Tomorrow's highest temperature is {temperature} degrees Celsius, and it will be {description}"
    elif when == 'the day after tomorrow':
        return f"The day after tomorrow's highest temperature is {temperature} degrees Celsius, and it will be {description}"
    else:
        return "Invalid option"

async def get_weather(city, when):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

        if when == 'today':
            text = get_weather_text('today', weather.temperature, weather.description)
        else:
            forecast_dict = {}
            for daily in weather.daily_forecasts:
                date = str(daily.date)
                hi_temp = daily.highest_temperature
                desc = [hourly.description for hourly in daily.hourly_forecasts]
                most_common_desc = max(set(desc), key=desc.count)
                forecast_dict[date] = (hi_temp, most_common_desc)

            tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            the_day_after_tomorrow_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

            if when == 'tomorrow':
                text = get_weather_text('tomorrow', *forecast_dict.get(tomorrow_date, (None, None)))
            elif when == 'the day after tomorrow':
                text = get_weather_text('the day after tomorrow', *forecast_dict.get(the_day_after_tomorrow_date, (None, None)))
            else:
                text = "Invalid option"

        print(text)
        play_audio(text)

# testing
# asyncio.run(get_weather('warsaw', 'today'))
# asyncio.run(get_weather('warsaw', 'tomorrow'))
# asyncio.run(get_weather('warsaw', 'the day after tomorrow'))