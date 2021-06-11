from numpy import empty
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import streamlit as st
from PIL import Image


img=Image.open("xss.png")
st.image(img,width=700)
st.title("XSS SCANNER")
st.text("Cross-site scripting (XSS) is a type of security vulnerability typically found in \nweb applications. XSS attacks enable attackers to inject client-side scripts into \nweb pages viewed by other users.")
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")



def get_form_details(form):

    details = {}
    
    action = form.attrs.get("action").lower()
    
    method = form.attrs.get("method", "get").lower()
    
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details


def submit_form(form_details, url, value):
    
    
    target_url = urljoin(url, form_details["action"])
    
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
           
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
       
        return requests.get(target_url, params=data)


def scan_xss(url):
   
    forms = get_all_forms(url)
    st.write(f"[+] Detected {len(forms)} forms on {url}.")
   
    js_script = "javascript:alert(1) , <img src=1 href=1 onerror=javascript:alert(1)></img> , <script>alert(1);</script> , <script\x20type=text/javascript>javascript:alert(1);</script>  " 
   
    is_vulnerable = False
    
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            st.write(f"[+] XSS Detected on {url}")
            st.write(f"[*] Form details:")
            st.write(form_details)
            is_vulnerable = True
            
    return is_vulnerable

empty=""
url = st.text_input("Enter Url here ")
if url == empty :
    print("")
else:
    st.write(scan_xss(url))   
st.text("Enter these URL's for Practice purpose.\n1: https://cashbin.co.uk/search.php?search= \n2: https://xss-game.appspot.com/level1/frame \n3: http://sudo.co.il/xss/level0.php \n4: http://sudo.co.il/xss/level1.php ")

st.text(" \n\n\nProject by husnain shahid 🐱‍💻🐱‍🏍")



