from requests import post
import pypdf as pdf
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from os.path import exists

class PDF:
    """
## 📄 PDF

easily extract ,and use your pdf content by this class

## Quick start

PDF class needs two parameters 

`pdf_path -> The path of your pdf file as string`

`use_for_telegram -> Set this option True if you use this for a telegram bot (False as default)

## ----------------------------------------------------

```
#import from our module
from Aiology import PDF

#variables
pdf_path = "YOUR_PDF_FILE_PATH"

#define your pdf
pdf = PDF(pdf_path)

#read pdf content
result = pdf.get_pdf_content()

#print result
print(result)
```
    """
    def __init__(self,pdf_path : str,use_for_telegram : bool = False):
        if not exists(pdf_path):
            raise Exception(f"There is no pdf file in {pdf_path} address !!")
        
        self.telegram_usage = use_for_telegram
        self.reader = pdf.PdfReader(pdf_path)
        self.pdf_pages_num = self.reader.get_num_pages()
        self.content = ""

        for i in range(self.pdf_pages_num):
            if self.telegram_usage:
                self.content += self.reader.get_page(i).extract_text()
            else:
                self.content += get_display(reshape(self.reader.get_page(i).extract_text()))

    def get_pdf_content(self):
        """
        ## Get pdf content

        This function get your pdf content and return them back

        `get_pdf_content() -> pdf content` 
        """
        return self.content
    
    def get_pdf_page_content(self,page_num : int):
        """
        ## Get pdf content

        This function get your pdf content by its page number and return them back

        `get_pdf_content(page_number : int) -> pdf content of that page` 
        """
        if page_num > self.pdf_pages_num:
            raise Exception(f"This pdf has {self.pdf_pages_num} pages , you can't have page {page_num} content !!")
        elif page_num > 0:
            if self.telegram_usage:
                return self.reader.get_page(page_num-1).extract_text()
            else:
                return get_display(reshape(self.reader.get_page(page_num-1).extract_text()))
        else:
            raise Exception(f"{page_num} is an invalid page number !!")
        


class AI:
    """
## 🤖 AI

You can easily exteract your pdf files data , then ask the ai everything
about your pdf content by using AI , and it will answer your question immediately

## Quick start

AI class needs two parameters 

`api_key -> The ai api_key , this module only support Gemini api_keys !!`

`use_for_telegram -> Set this option True if you use this for a telegram bot (False as default)

## ------------------------------------------------------------------------------
```
#import from our module 
from Aiology import PDF , AI

#needed variables
my_pdf_path = "YOUR_PDF_PATH_HERE"
my_gemini_api_key = "YOUR_API_KEY_HERE"

#open and read pdf content
pdf = PDF(my_pdf_path)

#call AI from our module and pass these parameters
ai = AI(my_gemini_api_key)

#ask your question
result = ai.ask_pdf_question("Make this pdf understandable for me",pdf)

#print result
print(result)
```
    """
    def __init__(self,api_key : str,use_for_telegram : bool = False):
        self.api_key = api_key
        self.telegram_usage = use_for_telegram

    def ask_question(self,text):
        """
        ## Ask question from ai

        By this function , you can send your question ,and receive its answer

        `ask_question(text : str) -> response text`
        """
        header = {"Content-Type":"application/json"}

        data = {"contents":[
                        {"parts":
                            [
                                {"text":text},
                            ]
                        }
                    ]}
        
        try:
            res = post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}",
                    headers=header,json=data)
        except:
            raise Exception(f"Internet connection error !!")
        
        if res.ok:
            final_text = ""
            result = res.json()
            for texts in result["candidates"][0]["content"]["parts"]:
                if self.telegram_usage:
                    final_text += texts["text"]
                else:
                    final_text += get_display(reshape(texts["text"]))

            return final_text
        else:
            raise Exception(f"Unexpected error happened !! your error code is {res.status_code}\nContent : {res.content}")

    def ask_pdf_question(self,text : str,pdf : PDF,pdf_page : int =None):
        """
        ## Ask question about your pdf

        By this function , you can easily pass your pdf ,and ask different questions about it

        `ask_pdf_question(text : str , pdf : PDF) -> response text`
        """
        content =  pdf.content
        
        if pdf_page != None:
            content = pdf.get_pdf_page_content(pdf_page)

        header = {"Content-Type":"application/json"}

        data = {"contents":[
                        {"parts":
                            [
                                {"text":content},
                                {"text":text}
                            ]
                        }
                    ]}
        
        try:
            res = post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}",
                    headers=header,json=data)
        except:
            raise Exception(f"Internet connection error !!")
            
        if res.ok:
            final_text = ""
            result = res.json()
            for texts in result["candidates"][0]["content"]["parts"]:
                if self.telegram_usage:
                    final_text += texts["text"]
                else:
                    final_text += get_display(reshape(texts["text"]))

            return final_text
        else:
            raise Exception(f"Unexpected error happened !! your error code is {res.status_code}\nContent : {res.content}")