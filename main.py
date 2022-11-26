from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image
import sys
import time
subscription_key = "1854de91d4f2494cae17fd2246a207d0"
endpoint = "https://20221126-shiva9ro.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_tags(filepath):
    local_image=open(filepath,"rb")
    tags_result=computervision_client.tag_image_in_stream(local_image)
    tags=tags_result.tags
    tags_name=[]
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

def detect_ojbects(filepath):
    local_image=open(filepath,"rb")
    detect_object_results=computervision_client.detect_objects_in_stream(local_image)
    ojbects=detect_object_results.objects
    return ojbects

import streamlit as st
from PIL import ImageDraw,ImageFont

st.title("物体検出アプリ")
uploaded_file=st.file_uploader("Choose an image...)",type=["jpg","png"])
if uploaded_file is not None:
    img=Image.open(uploaded_file)
    img_path=f"img/{uploaded_file.name}"
    img.save(img_path)
    objects = detect_ojbects(img_path)

    draw=ImageDraw.Draw(img)
    for object in objects:
        x=object.rectangle.x
        y=object.rectangle.y
        w=object.rectangle.w
        h=object.rectangle.h
        caption = object.object_property
        font = ImageFont.truetype(font="./meiryo.ttc",size=100)
        text_w,text_h=draw.textsize(caption,font=font)
        draw.rectangle([(x,y),(x+text_w,y+text_h)],fill="green")
        draw.rectangle([(x,y),(x+w,y+h)],fill=None,outline="green",width=5)
        draw.text((x,y),caption,fill="white",font=font)
st.image(img)
tags_name=get_tags(img_path)
tags_name=", ".join(tags_name)
st.markdown("**認識されたコンテンツタグ**")
st.markdown(f">{tags_name}")

