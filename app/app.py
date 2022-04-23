import telebot

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict["language"] = "en"

Open_wether_map_api_key = "<Open_wether_map_api_key>"

owm = OWM(Open_wether_map_api_key, config_dict)
bot = telebot.TeleBot("<TOKEN>")

print("App is running!")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello, I'm a bot that will help you find out the weather anywhere in the world. \n I am Igor Chernyavsky's graduation project from the 472 group of the College of Information Technologies and Systems \n Let me help you?)\n Where would you like to know the weather?",
    )


@bot.message_handler(commands=["help"])
def send_echo(message):
    bot.reply_to(
        message,
        "To use, just enter the city or country in which you would like to know the weather\n"
        + "To play the game and find out the rules, type /game",
    )


@bot.message_handler(content_types=["audio"])
def audio(message):
    bot.send_message(message.chat.id, "Норм трек)")


@bot.message_handler(commands=["game"])
def send_echo(message):
    bot.reply_to(
        message,
        "To play, write Rock, Scissors, or Paper.\n"
        + "Rock beats scissors. Scissors beat paper. Paper beats rock.\n"
        + "You can't win)0)",
    )


@bot.message_handler(content_types=["text"])
def send_echo(message):
    if message.text.lower() == "rock":
        bot.send_message(message.chat.id, "I have paper, you lose")
    elif message.text.lower() == "scissors":
        bot.send_message(message.chat.id, "I have a rock, you lose")
    elif message.text.lower() == "paper":
        bot.send_message(message.chat.id, "I have a scissors, you lose ")
    elif message.text.lower() == "i love you":
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAAIpDl5MfV3ZH-bQTaeTc0JlKGk3rOIjAAIKAAMwEVYRamFdDZ0IQ_8YBA",
        )
    elif message.text.lower() == "привіт":
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAAIpDF5Mety13y_RePowyL50xJoVf9EqAAKdAAMwEVYRbHf-qqcxcRoYBA",
        )
    elif message.text.lower() == "jo jo":
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAAIpEF5Mfa2Z0dj0eaBkOb8Rl3sBK2jkAAIOAQACuh3kE6WNJQABl-u0YxgE",
        )
    else:
        try:
            mgr = owm.weather_manager()
            weather = mgr.weather_at_place(message.text).weather
            temperature = round(weather.temperature("celsius")["temp"])
            answer = "In " + message.text + " now " + weather.detailed_status + "\n"
            answer += "Temperature is " + str(temperature) + " °C" + "\n"
            if temperature < 0:
                answer += " It's cold outside, dress warmly "
            elif temperature < 5:
                answer += " It's time to get warm underpants "
            elif temperature < 10:
                answer += " Cool I advise you to take a spin "
            elif temperature < 20:
                answer += " The temperature is normal, wear what you want "
            else:
                answer += " Dress up for summer "
            bot.send_message(message.chat.id, answer)
        except:
            print("Error")
            bot.send_message(message.chat.id, "Mistake! City/Country not found.")


bot.polling(none_stop=True)