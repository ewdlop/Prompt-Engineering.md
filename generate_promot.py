#!/usr/bin/python3

#!pip install PyPDF2 jieba nltk

import re
import os

# Optional imports with fallback
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("Warning: PyPDF2 not available. PDF reading will not work.")

try:
    import nltk
    from nltk.tokenize import sent_tokenize
    # Ensure you have downloaded the punctuation tokenizer
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)  # For newer NLTK versions
        # Test if tokenizer works
        sent_tokenize("Test sentence.")
        HAS_NLTK = True
    except Exception as e:
        HAS_NLTK = False
        print(f"Warning: NLTK punkt tokenizer not available: {e}")
except ImportError:
    HAS_NLTK = False
    print("Warning: NLTK not available. Using basic sentence splitting.")

try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False
    print("Warning: jieba not available. Chinese text processing will not work.")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file if PyPDF2 is available"""
    if not HAS_PYPDF2:
        raise ImportError("PyPDF2 is required for PDF processing. Install it with: pip install PyPDF2")
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_file(file_path):
    """Extract text from a plain text file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Text file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def simple_sentence_split(text):
    """Basic sentence splitting using regex patterns"""
    # Split on sentence-ending punctuation followed by whitespace and capital letter
    sentences = re.split(r'[.!?]+\s+(?=[A-Z])', text.strip())
    # Filter out empty sentences and strip whitespace
    return [s.strip() for s in sentences if s.strip()]

def generate_prompts(text, num_prompts=5):
    """Generate prompts from text using available tokenizers"""
    if HAS_NLTK:
        sentences = sent_tokenize(text)
    else:
        sentences = simple_sentence_split(text)
    
    prompts = sentences[:num_prompts]  # Generate prompts from the first few sentences
    return prompts

def generate_中文_prompts(text, num_prompts=5):
    """Generate Chinese prompts using jieba if available"""
    if not HAS_JIEBA:
        print("Warning: jieba not available. Using character-based splitting for Chinese text.")
        # Simple fallback: split by Chinese punctuation
        sentences = re.split(r'[。！？]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
    else:
        # Use jieba to tokenize Chinese text into sentences
        sentences = list(jieba.cut(text, cut_all=False))
    
    prompts = sentences[:num_prompts]  # Generate prompts from the first few sentences
    return prompts
  

def main():
    """Main function with error handling and sample text"""
    pdf_path = 'example.pdf'  # Replace with the path to your PDF file
    text_path = 'example.txt'  # Alternative text file
    
    # Try to read from PDF first, then text file, then use sample text
    text = None
    if os.path.exists(pdf_path):
        try:
            text = extract_text_from_pdf(pdf_path)
            print("Generated Prompts from PDF:")
        except Exception as e:
            print(f"Error processing PDF: {e}")
    
    if text is None and os.path.exists(text_path):
        try:
            text = extract_text_from_file(text_path)
            print("Generated Prompts from text file:")
        except Exception as e:
            print(f"Error processing text file: {e}")
    
    if text is not None:
        prompts = generate_prompts(text)
        for i, prompt in enumerate(prompts, start=1):
            print(f"{i}. {prompt}")
    else:
        print(f"No input files found ('{pdf_path}' or '{text_path}'). Using sample text...")
        use_sample_text()

def use_sample_text():
    """Use sample text when PDF is not available"""
    sample_text = """
    Prompt engineering is the art of crafting effective instructions for AI models. 
    It involves understanding how language models interpret and respond to different types of input. 
    Good prompts are clear, specific, and provide enough context for the model to generate useful responses. 
    The field has evolved rapidly with the advancement of large language models. 
    Practitioners experiment with various techniques to optimize AI performance across different tasks.
    """
    
    print("\n=== English Prompts ===")
    prompts = generate_prompts(sample_text.strip())
    for i, prompt in enumerate(prompts, start=1):
        print(f"{i}. {prompt}")
    
    # Test Chinese text processing
    chinese_text = "人工智能是未来的技术。机器学习让计算机能够自我学习。深度学习模拟人脑神经网络。自然语言处理帮助机器理解人类语言。"
    
    print("\n=== Chinese Prompts ===")
    chinese_prompts = generate_中文_prompts(chinese_text)
    for i, prompt in enumerate(chinese_prompts, start=1):
        print(f"{i}. {prompt}")

if __name__ == "__main__":
    main()

#python generate_promot.py
