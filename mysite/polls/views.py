
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
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET


museum_items = {}
obj_hist = []
weather_state = "sun"
code = []
story = []
s=""


def index(request):
    obj_hist.clear()
    code.clear()
    story.clear()
    global weather_state
    weather_state = "sun"
    return render(request, 'polls/index.html')

def index_en(request):
    obj_hist.clear()
    code.clear()
    story.clear()
    global weather_state
    weather_state = "sun"
    return render(request, 'polls/index_en.html')


def custom_action(request):
    return render(request, 'polls/readyToDraw.html')

def custom_action_en(request):
    return render(request, 'polls/readyToDraw_en.html')


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

def goLeft_en(request):
    code.append("goLeft")
    return render(request, 'polls/readyToDraw_en.html', {'actions': code})


def fly_en(request):
    code.append("fly")
    return render(request, 'polls/readyToDraw_en.html', {'actions': code})


def goRight_en(request):
    code.append("goRight")
    return render(request, 'polls/readyToDraw_en.html', {'actions': code})


def ascend_en(request):
    code.append("ascend")
    return render(request, 'polls/readyToDraw_en.html', {'actions': code})


def write_code(request):
    fiil = request.GET["n"]
    translate_client = translate.Client()
    result = translate_client.translate(fiil, target_language="en")
    verb = result['translatedText']
    f1 = open("static/test.xml", "a")
    f1.write(verb)
    readFile = open("static/test.xml")
    lines = readFile.readlines()
    readFile.close()
    w = open("static/test.xml", 'w')
    w.writelines([item for item in lines[:-1]])
    w.close()
    f = open("static/test.xml", "a")
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


def write_code_en(request):
    verb = request.GET["n"]
    f1 = open("static/verbs.txt", "a")
    f1.write(verb)
    readFile = open("static/test.xml")
    lines = readFile.readlines()
    readFile.close()
    w = open("static/test.xml", 'w')
    w.writelines([item for item in lines[:-1]])
    w.close()
    f = open("static/test.xml", "a")
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

    return render(request, 'polls/readyToDraw_en.html')


def actions(id):
    actions = []
    tree = ET.parse("static/test.xml")
    root = tree.getroot()
    for child in root:
        if child.attrib["id"] == id:
            actions.append(child.attrib["name"])
    return actions


def show_info(request):
    return render(request, 'polls/doc.html')

def show_info_en(request):
    return render(request, 'polls/doc_en.html')


def create_new_canvas(request):
    return HttpResponse("Started recording")


def recordAndDraw(request):
    global s
    print(museum_items.keys())
    global weather_state
    context = record()
    if "error" in context:
        return render(request, 'polls/demo.html', {'story': "".join(s), 'error': context["error"], 'json': obj_hist, 'weather': weather_state})
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
            if name in museum_items.keys():
                print("here")
                file_path = "../static/museum_imgs/" + name + "." + museum_items[name]
                obj["file_path"] = file_path
                obj_hist.append(json.dumps(obj))
                print(obj)
            else:
                fileName = "/Users/apple/Downloads/filteredDataset/" + name + ".ndjson"
                print(obj["action"])
                action = actions(obj["action"])
                if not os.path.exists(fileName):
                    error = "Sorry but this word is not in our vocabulary yet, Please try another sentence"
                    return render(request, 'polls/demo.html', {'story': "".join(s), 'error': error, 'json': obj_hist, 'weather': weather_state})

                f = open(fileName, "r")
                qdImages = f.read()
                p = re.findall(r'{(.*?)}', qdImages)
                i = random.randrange(0, len(p), 1)
                y = json.loads("{" + p[i] + "}")
                obj["strokeArray"] = y["drawing"]
                obj_hist.append(json.dumps(obj))
    return render(request, 'polls/demo.html', {'story': "".join(s), 'sentence': sentence, 'json': obj_hist,
                                               'weather': weather_state})


def recordAndDraw_en(request):
    global s
    global weather_state
    context = record_en()
    if "error" in context:
        return render(request, 'polls/demo_en.html', {'story': "".join(s), 'error': context["error"], 'json': obj_hist, 'weather': weather_state})
    cumle = context["origin"]
    story.append(cumle)
    s = process_Story()
    obj_list = sentence_processing(cumle)
    print(museum_items.keys())
    for m in obj_list:
        obj = json.loads(m)
        if "state" in obj:
            weather_state = obj["state"]
        else:
            defined_obj_ind = -1
            if (obj["prev"]):
                for object_ind in range(0, len(obj_hist)):
                    a = json.loads(obj_hist[object_ind])
                    if a["name"] == obj["name"]:
                        defined_obj_ind = object_ind
                        a["location"] = obj["location"]
                        a["action"] = obj["action"]
                        obj_hist[defined_obj_ind] = json.dumps(a)

            if(defined_obj_ind == -1):

                name = obj["name"]
                if name in museum_items.keys():
                    print("here")
                    file_path = "../static/museum_imgs/" + name + "." + museum_items[name]
                    obj["file_path"] = file_path
                    obj_hist.append(json.dumps(obj))
                    print(obj)
                else:
                    fileName = "/Users/apple/Downloads/filteredDataset/" + name + ".ndjson"
                    print(obj["action"])
                    action = actions(obj["action"])
                    if not os.path.exists(fileName):
                        error = "Sorry but this word is not in our vocabulary yet, Please try another sentence"
                        return render(request, 'polls/demo_en.html', {'story': "".join(s), 'error': error, 'json': obj_hist, 'weather': weather_state})
                    f = open(fileName, "r")
                    qdImages = f.read()
                    p = re.findall(r'{(.*?)}', qdImages)
                    i = random.randrange(0, len(p), 1)
                    y = json.loads("{" + p[i] + "}")
                    obj["strokeArray"] = y["drawing"]
                    obj_hist.append(json.dumps(obj))
    return render(request, 'polls/demo_en.html', {'story': "".join(s), 'sentence': cumle, 'json': obj_hist,
                                                  'weather': weather_state})


def draw_text(request):
    global weather_state
    cumle = request.GET["text"]
    story.append(cumle)
    s = process_Story()
    obj_list = sentence_processing(cumle)
    print(museum_items.keys())
    for m in obj_list:
        obj = json.loads(m)
        if "state" in obj:
            weather_state = obj["state"]
        else:
            defined_obj_ind = -1
            print(json.dumps(obj))
            if obj["prev"]:
                for object_ind in range(0, len(obj_hist)):
                    a = json.loads(obj_hist[object_ind])
                    if a["name"] == obj["name"]:
                        defined_obj_ind = object_ind
                        a["location"] = obj["location"]
                        a["action"] = obj["action"]
                        obj_hist[defined_obj_ind] = json.dumps(a)

            if(defined_obj_ind == -1):

                name = obj["name"]
                if name in museum_items.keys():
                    print("here")
                    file_path = "../static/museum_imgs/" + name + "." + museum_items[name]
                    obj["file_path"] = file_path
                    obj_hist.append(json.dumps(obj))
                    print(obj)
                else:
                    fileName = "/Users/apple/Downloads/filteredDataset/" + name + ".ndjson"
                    print(obj["action"])
                    action = actions(obj["action"])
                    if not os.path.exists(fileName):
                        error = "Sorry but this word is not in our vocabulary yet, Please try another sentence"
                        return render(request, 'polls/demo_en.html', {'story': "".join(s), 'error': error, 'json': obj_hist, 'weather': weather_state})
                    f = open(fileName, "r")
                    qdImages = f.read()
                    p = re.findall(r'{(.*?)}', qdImages)
                    i = random.randrange(0, len(p), 1)
                    y = json.loads("{" + p[i] + "}")
                    obj["strokeArray"] = y["drawing"]
                    obj_hist.append(json.dumps(obj))
    return render(request, 'polls/demo_en.html', {'story': "".join(s), 'sentence': cumle, 'json': obj_hist,
                                                  'weather': weather_state})

def find_defined_object(obj):
    print(obj);
    if(obj.prev):
        for object_ind in range(0, len(obj_hist)):
            if obj_hist[object_ind]["name"] == obj.name:
                return object_ind
    return -1


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_image = request.FILES['file_image']
        fs = FileSystemStorage()
        item_name, extension = uploaded_image.name.split(".", 1)
        museum_items[item_name] = extension
        name = fs.save(uploaded_image.name, uploaded_image)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'polls/upload.html', context)


def start_demo(request):
    story.clear()
    return render(request, 'polls/demo.html')

def start_demo_en(request):
    story.clear()
    return render(request, 'polls/demo_en.html')


def save_page(request):
    obj_hist.clear()
    s = process_Story()
    s1 = "".join(s)
    return render(request, 'polls/demo.html', {'story': "".join(s), 'json': obj_hist, 'weather': weather_state})


def save_page_en(request):
    obj_hist.clear()
    s = process_Story()
    s1 = "".join(s)
    return render(request, 'polls/demo_en.html', {'story': "".join(s), 'json': obj_hist,  'weather': weather_state})


def draw_objects(request):
    name = "tree"
    draw = []
    fileName = "E:\dataset\simplified\\" + name + ".ndjson"
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
                if (not conj.lemma_ == "-PRON-"):
                    main_lst_json.append(conj_obj.to_json())
            if (not main.lemma_ == "-PRON-"):
                main_lst_json.append(main_obj.to_json())

    print(sentence)
    return main_lst_json


def record():
    r = sr.Recognizer()
    text = ""
    translated = ""
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=15)

    try:
        sentence = r.recognize_google(audio, language="tr-TR")
        translate_client = translate.Client()
        result = translate_client.translate(
            sentence, target_language="en")
        translated = result['translatedText']
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
        return {'error': text}
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        return {'error': text}
    context = {'origin': sentence, 'text': translated}
    return context


def record_en():
    r = sr.Recognizer()
    text = ""
    translated = ""
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=15)
    try:
        sentence = r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
        return {'error': text}
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        return {'error': text}
    context = {'origin': sentence}
    return context


class ImageObject:
    def __init__(self, name, file_path, size=1,location="random", action=None):
        self.name = name
        self.file_path = file_path
        self.size = size
        self.location = location
        self.action = action

    def to_json(self):
        return json.dumps(self.__dict__)


class Object:
    def __init__(self, name, color="black", size=1, number=1, location="random", action=None, prev=False):
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
    def __init__(self, name, color="black", size=1, number=1, location="random"):
        self.name = name
        self.color = color
        self.size = size
        self.number = number
        self.location = location
        self.strokeArray = []
        self.id = 0

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


prep_map = [["on", "above", "over", "up"], ["beneath", "below", "down", "under", "underneath"],["in","inside"]]


def isPreposition(feature):
    if (feature.dep_ == "prep"):
        if (feature.lemma_ in prep_map[0]):
            return "on"
        elif (feature.lemma_ in prep_map[1]):
            return "under"
        elif (feature.lemma_ in prep_map[2]):
            return "in"
    else:
        return False



action_map = [["fly","flying"], ["run","running"], ["walk","walking","go","going"]]
def isAction(feature):
    if (feature.lemma_ in action_map[0]):
        return {"Action": "fly", "Custom": False}
    elif (feature.lemma_ in action_map[1]):
        return {"Action": "walk", "Custom": False}
    elif (feature.lemma_ in action_map[2]):
        return {"Action": "walk", "Custom": False}
    else:
        with open("static/verbs.txt") as verbs:
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
            location = [child.lemma_ for child in feature.children if ((child.tag_ == "NN") or (child.tag_ == "NNS"))][0]
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
