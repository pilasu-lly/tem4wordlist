import spacy
import pyttsx3
import requests
import hashlib
import eng_to_ipa as p


nlp = spacy.load("en_core_web_md")


BAIDU_API_KEY = 'IPuxQP4OcLWw3EYQlXEr'  # Replace with your actual Baidu API key
BAIDU_APP_ID = '20200603000485162'  # Replace with your actual Baidu app ID


'''fword = open(input('请输入单词txt文件路径：'), 'r')
words=fword.readlines()'''

words = 'agony, agreeable, apt, beloved, boredom, carefree, charm, childish, contented, cordial, courteous, delightful, disagreeable, dramatic, dreary, easygoing, eccentric, elderly, enjoyment, entertain, enthusiasm, eternal, eventful, everlasting, fatigue, fussy, gloomy, gracious, happily, heartache, heartbreak, heartbroken, homely, homesick, hospitable, humid, ideal, imaginary, irresistible, irritable, jolly, joyful, joyous, leisure, lonesome, longing, lovable, magical, melancholy, memorable, miraculous, monotonous, mood, mysterious, overjoyed, paradise, passion, pastime, picturesque, pleased, relaxation, restless, sane, sarcastic, savoury, sensation, sentiment, serene, simplicity, sleepless, sociable, solitude, spirited, spontaneous, stale, sympathetic, talkative, temper, thoughtful, timid, tolerable, tranquil, unforgettable, unhappy, unpleasant, unsociable, unwind, youthful'.split(', ')


# Initialize the pyttsx3 engine
def read_word(word):
    engine = pyttsx3.init()
    newVoiceRate = 150
    engine.setProperty('rate',newVoiceRate)
    engine.say(word)
    engine.runAndWait()
    engine.stop()

# get the Chinese translation
def calculate_signature(app_id, word, salt, api_key):
    sign = app_id + word + str(salt) + api_key
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    return md5.hexdigest()

def translate_english_to_chinese(word):
    url = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = 123456  # Replace with a number or string
    sign = calculate_signature(BAIDU_APP_ID, word, salt, BAIDU_API_KEY)

    params = {
        'q': word,
        'from': 'en',
        'to': 'zh',
        'appid': BAIDU_APP_ID,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(url, params=params)
    data = response.json()
    translation = data['trans_result'][0]['dst']
    return translation

print('')
for word in words:
    phonetic_transcription = p.convert(word)
    # translation = translate_english_to_chinese(word)
    doc = nlp(word)
    print('\033[1;31;42m', word, end = " ")
    read_word(word)
    print('\033[1;34;42m',doc[0].pos_.lower(), end = " ")
    print('\033[1;35;42m', '\\' + phonetic_transcription + '\\', end = " ")
    # print('\033[1;31;40m', translation)
    read_word(word)
    print("\r", end="")

