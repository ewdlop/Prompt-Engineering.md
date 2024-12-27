#!/usr/bin/python3

#!pip install PyPDF2 jieba nltk

import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize

# Ensure you have downloaded the punctuation tokenizer
nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_prompts(text, num_prompts=5):
    sentences = sent_tokenize(text)
    prompts = sentences[:num_prompts]  # Generate prompts from the first few sentences
    return prompts

def generate_中文_prompts(text, num_prompts=5):
    # Use jieba to tokenize Chinese text into sentences
    sentences = list(jieba.cut(text, cut_all=False))
    prompts = sentences[:num_prompts]  # Generate prompts from the first few sentences
    return prompts
  

def main():
    pdf_path = 'example.pdf'  # Replace with the path to your PDF file
    text = extract_text_from_pdf(pdf_path)
    prompts = generate_prompts(text)
    
    print("Generated Prompts:")
    for i, prompt in enumerate(prompts, start=1):
        print(f"{i}. {prompt}")

if __name__ == "__main__":
    main()

#python generate_promot.py
