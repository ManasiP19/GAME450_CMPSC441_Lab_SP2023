import random
import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"(.*) lost",
        ["Oh no, you were defeated! It's okay, though - everyone loses sometimes.", 
         "Don't worry, you'll do better next time. Keep practicing and you'll become stronger!", 
         "Looks like luck wasn't on your side this time. But don't give up - keep fighting!",
         "That was a tough battle, but you gave it your all. You should be proud of yourself.",
         "Sorry to hear that you lost. It's a tough world out there, but I know you'll bounce back."]
    ],
    [
        r"(.*) won",
        ["Congratulations! You have emerged victorious. You are truly a skilled player.",
         "Great job! You have defeated your opponent and reached your destination. I knew you could do it!",
         "Well done! You have overcome all the obstacles and proved your strength. You should be proud of yourself.",
         "Impressive! You have completed the journey and become a true adventurer. Your bravery and determination have paid off.",
         "Fantastic! You have accomplished your mission and reached your destination. I have no doubt you will go on to even greater things."]
    ]
]

chatbot = Chat(pairs, reflections)

def generate_dialogue(key_string):
    response = chatbot.respond(key_string)
    return response