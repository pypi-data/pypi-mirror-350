readme_content = """# text_in_pattern

**`text_in_pattern`** is a Python library that prints user input text in a stylized ASCII-art pattern using any symbol of your choice. Each letter of the alphabet is custom-designed to form a visually striking output that can be printed to the console.

## ✨ Features

- Convert any input text into a custom visual pattern
- Choose any symbol to decorate your text
- Lightweight and beginner-friendly

## 📦 Installation

Install the package via pip:

```bash

pip install text_in_pattern

```

## 📦 Usage

```bash

from text_in_pattern import text

# Your input string and the symbol to use
name = "Hello World"
symbol = "*"

text(name, symbol)

```


## 🛠️ Function

```bash

text(name: str, symbol: str) -> None
name: The input text to display

symbol: The character used to draw the pattern

Prints the stylized text directly to the console

```