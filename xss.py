import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import streamlit as st

st.title("XSS SCANNER")

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # put everything to the resulting dictionary
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
   
    js_script = "javascript:alert(1) , <img src=1 href=1 onerror=javascript:alert(1)></img> , <script>alert(1);</script> " 
   
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

url = st.text_input("Enter Url ")
st.write(scan_xss(url))
