from typing import List, Any

from django.shortcuts import render
import speech_recognition as sr
from django.http import HttpResponse
import spacy
nlp = spacy.load("en_core_web_sm")
from spacy import displacy
from PIL import Image
import webcolors
from word2number import w2n
import re
import json
import random
from google.cloud import translate_v2 as translate
import os
import xml.etree.ElementTree as ET


museum_items = ["ship", "carriage"]
obj_hist = []
weather_state = "sun"
code = []
story = []
story_hist =[]

def index(request):
    story_hist.clear()
    obj_hist.clear()
    code.clear()
    story.clear()
    global weather_state
    weather_state = "sun"
    return render(request, 'polls/index.html')


def custom_action(request):
    return render(request, 'polls/readyToDraw.html')


def goLeft(request):
    code.append("goLeft")
    return render(request, 'polls/readyToDraw.html', {'actions': code})


def fly(request):
    code.append("fly")
    return render(request, 'polls/readyToDraw.html', {'actions': code})


def goRight(request):
    code.append("goRight")
    return render(request, 'polls/readyToDraw.html', {'actions': code})


def ascend(request):
    code.append("ascend")
    return render(request, 'polls/readyToDraw.html', {'actions': code})


def write_code(request):
    fiil = request.GET["n"]
    translate_client = translate.Client()
    result = translate_client.translate(fiil, target_language="en")
    verb = result['translatedText']
    f1 = open("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/verbs.txt", "a")
    f1.write(verb )
    readFile = open("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/test.xml")
    lines = readFile.readlines()
    readFile.close()
    w = open("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/test.xml", 'w')
    w.writelines([item for item in lines[:-1]])
    w.close()
    f = open("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/test.xml", "a")
    for x in code:
        if x == "goRight":
            f.write("\t<action name = 'goRight' id = '"+ verb +"'></action>\n")
        elif x == "goLeft":
            f.write("\t<action name = 'goLeft' id = '"+ verb +"'></action>\n")
        elif x == "fly":
            f.write("\t<action name = 'fly' id = '"+ verb +"'></action>\n")
        elif x == "ascend":
            f.write("\t<action name = 'ascend' id = '"+ verb +"'></action>\n")
    f.write("</list>\n")

    return render(request, 'polls/readyToDraw.html')


def actions(id):
    actions = []
    tree = ET.parse("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/test.xml")
    root = tree.getroot()
    for child in root:
        if child.attrib["id"] == id:
            actions.append(child.attrib["name"])
    return actions


def show_info(request):
    return render(request, 'polls/doc.html')


def create_new_canvas(request):
    return HttpResponse("Started recording")


def recordAndDraw(request):
    global weather_state
    context = record()
    cumle = context["origin"]
    story.append(cumle)
    s = process_Story()
    sentence = context["text"]
    obj_list = sentence_processing(sentence)
    for m in obj_list:
        obj = json.loads(m)
        if "state" in obj:
            weather_state = obj["state"]
        else:
            name = obj["name"]
            fileName = "/Users/apple/Downloads/filtered/" + name + ".ndjson"
            print(obj["action"])
            action = actions(obj["action"])
            if not os.path.exists(fileName):
                error = "Sorry but this word is not in our vocabulary yet, Please try another sentence"
                return render(request, 'polls/demo.html', {'error': error, 'json': obj_hist})
            f = open(fileName, "r")
            qdImages = f.read()
            p = re.findall(r'{(.*?)}', qdImages)
            i = random.randrange(0, len(p), 1)
            y = json.loads("{" + p[i] + "}")
            obj["strokeArray"] = y["drawing"]
            obj_hist.append(json.dumps(obj))
    return render(request, 'polls/demo.html', {'story': "".join(s), 'sentence': sentence, 'json': obj_hist,
                                               'weather': weather_state, 'story_hist': story_hist})


def start_demo(request):
    return render(request, 'polls/demo.html')


def save_page(request):
    obj_hist.clear()
    s = process_Story()
    s1 = "".join(s)
    size = len(story_hist)
    story_hist.append({"story": s1, "file": str(size)+".png"})
    story.clear()
    return render(request, 'polls/demo.html', {'story_hist': story_hist, 'weather': weather_state, 'var': "output.png"})


def draw_objects(request):
    name = "tree"
    draw = []
    fileName = "/Users/apple/Desktop/dataset/" + name + ".ndjson"
    f = open(fileName, "r")
    qdImages = f.read()
    p = re.findall(r'{(.*?)}', qdImages)
    for x in range(300):
        obj = Object2(name=name)
        y = json.loads("{" + p[x] + "}")
        obj.setStrokeArray(y["drawing"])
        obj.setID(y["key_id"])
        draw.append(obj.to_json())
    return render(request, 'polls/drawing.html', {'objs': draw})


def sentence_processing(sentence):
    doc = nlp(sentence)

    main_lst_json = []
    weather = isWeather(doc)
    if (weather):
        main_lst_json.append(Weather(state=weather).to_json())
    else:
        main_lst = extract_main_object(doc)
        for main in main_lst:
            main_obj = match_features(extract_features(doc, main), main)
            conj_lst = list(main.conjuncts)
            for conj in conj_lst:

                conj_obj = match_features(extract_features(doc, conj), conj)
                if (main_obj.action != None):
                    conj_obj.action = main_obj.action
                else:
                    main_obj.action = conj_obj.action

                if (main_obj.location != "random"):
                    conj_obj.location = main_obj.location
                else:
                    main_obj.location = conj_obj.location

                main_lst_json.append(conj_obj.to_json())

            main_lst_json.append(main_obj.to_json())
    print(sentence)
    return main_lst_json



def record():
    r = sr.Recognizer()
    text = ""
    translated = ""
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        sentence = r.recognize_google(audio, language="tr-TR")
        translate_client = translate.Client()
        result = translate_client.translate(
            sentence, target_language="en")
        translated = result['translatedText']
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    context = {'origin': sentence, 'text': translated, 'error': text}
    return context



class Object:
    def __init__(self, name, color="black", size=1, number=1, location="random", action=None, prev = False):
        self.name = name
        self.color = color
        self.size = size
        self.number = number
        self.location = location
        self.action = action
        self.prev = prev
        self.strokeArray = []

    def print(self):
        print("Name: ", self.name, "\tColor:", self.color, " Size:", self.size, " Number:", self.number, " Location:",
              self.location)

    def to_json(self):
        return json.dumps(self.__dict__)

    def setStrokeArray(self, strokeArray):
        self.strokeArray = strokeArray


class Weather:
    def __init__(self, state):
        self.state = state

    def to_json(self):
        return json.dumps(self.__dict__)

class Object2:
    def __init__(self, name, color="black", size=1, number=1, location="random", prev = False):
        self.name = name
        self.color = color
        self.size = size
        self.number = number
        self.location = location
        self.strokeArray = []
        self.id = 0
        self.prev = prev

    def print(self):
        print("Name: ", self.name, "\tColor:", self.color, " Size:", self.size, " Number:", self.number, " Location:",
              self.location, self.action)

    def to_json(self):
        return json.dumps(self.__dict__)

    def setStrokeArray(self, strokeArray):
        self.strokeArray = strokeArray

    def setID(self, id):
        self.id = id


# Functions to identify what information a feature gives about the object
def isColor(feature):
    return feature in webcolors.CSS3_NAMES_TO_HEX


def isNumber(feature):
    try:
        w2n.word_to_num(feature)
        return True
    except:
        return False


## Functions to identify what information a feature gives about the object
size_map = [
    ["big", "enormous", "giant", "gigantic", "fat", "great", "huge", "immense", "large", "massive", "overweight",
     "wide", "titanic", "thick", "tall"],
    ["little", "small", "mini", "miniature", "petite", "tiny", "thin", "slim", "short"]]


def isSize(feature_txt):
    if (feature_txt in size_map[0]):
        return 1.5
    elif (feature_txt in size_map[1]):
        return 0.5
    else:
        return False

weather_map = [["rain", "raining", "rainy"], ["snow", "snowing", "snowy"], ["sun", "sunny", "sunning:)"],
                   ["cloudy"], ["weather"]]


def isWeather(doc):
    for token in doc:
        feature_txt = token.lemma_.lower()
        #        print("is weather: ", feature_txt)
        if (feature_txt in weather_map[0]):
            return "rain"
        elif (feature_txt in weather_map[1]):
            return "snow"
        elif (feature_txt in weather_map[2]):
            return "sun"
        elif (feature_txt in weather_map[3]):
            return "cloud"
        elif (feature_txt in weather_map[4]):
            return "weather"
    return False


prep_map = [["on", "above", "over", "up"], ["beneath", "below", "down", "under", "underneath"]]


def isPreposition(feature):
    """if (feature.dep_ == "prep"):
        if (feature.lemma_ in prep_map[0]):
            return "on"
        elif (feature.lemma_ in prep_map[1]):
            return "under"
    else:
        return False"""
    return feature.dep_ == "prep"


action_map = [["fly","flying"], ["run","running"], ["walk","walking","go","going"]]
def isAction(feature):
    if (feature.lemma_ in action_map[0]):
        return {"Action": "fly", "Custom": False}
    elif (feature.lemma_ in action_map[1]):
        return {"Action": "run", "Custom": False}
    elif (feature.lemma_ in action_map[2]):
        return {"Action": "walk", "Custom": False}
    else:
        with open("/Users/apple/Desktop/comp491/COMP491_Senior_Project/mysite/static/verbs.txt") as verbs:
            if feature.lemma_ in verbs.read():
                return {"Action": actions(feature.lemma_), "Custom": True}
    return False


def extract_main_object(doc):
    main_lst = [chunk.root for chunk in doc.noun_chunks if
                chunk.root.dep_ == "ROOT" or chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "attr"]
    if(not main_lst):
        try:
            main_lst = [[token for token in doc if token.pos_ == "NOUN"][0]]
        except:
            print("extract_main_object error")
    return main_lst



def get_chunks(doc, main_obj_token):
    for chunk in doc.noun_chunks:
        if (chunk.root == main_obj_token):
            return [token for token in chunk if token != main_obj_token]



# Extract the relevant information of the main object
def extract_features(doc,obj_token):
    feature_lst = []
    stack = []
    if(obj_token.ancestors):
        stack += [ancestor for ancestor in obj_token.ancestors]
    if(obj_token.children):
        stack +=  [children for children in obj_token.children]
   # stack = [ancestor for ancestor in obj_token.ancestors] + [children for children in obj_token.children]
    while stack:
        current = stack.pop()
        if (current.pos_ != "NOUN"):
            feature_lst.append(current)
            stack += [children for children in current.children]
    return feature_lst


# Creates an "Object" based on the given information
def match_features(feature_lst, main_obj_token):
    ob = Object(name=main_obj_token.lemma_)

    if (main_obj_token.tag_ == "NNS"):
        ob.number = random.randint(2, 5)

    for feature in feature_lst:
        feature_txt = feature.lemma_
        size = isSize(feature_txt)
        if (feature_txt == "the"):
            ob.prev = True

        elif (size):
            ob.size = size

        elif (isColor(feature_txt)):
            ob.color = feature_txt

        elif (isNumber(feature_txt)):
            number = w2n.word_to_num(feature_txt)
            ob.number = number

        elif (isPreposition(feature)):
            location = [child.lemma_ for child in feature.children if (child.tag_ == "NN")][0]
            ob.location = {"Preposition": feature.lemma_,
                           "Location": location}
        elif (isAction(feature)):
            ob.action = isAction(feature)

    return ob



def process_Story():
    new_story = []
    global story
    for sentence in story:
        new_story.append(sentence.lower().capitalize()+". ")
    return new_story