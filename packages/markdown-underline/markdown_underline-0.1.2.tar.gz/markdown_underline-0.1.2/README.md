# Markdown Extension for Underline

This is an extension for [Python-Markdown](https://pypi.org/project/Markdown/) to support underlined text using ++ markers. 

```
This is ++underlined Text++ 
```

will be rendered to:

```html
<p>This is <u>underlined Text</u></p>
```

# Installation

The markdown-underline package can be installed via:

```bash
pip install markdown-underline
```

# Usage

The following python code shows how to use the underline extension:

```
import markdown

text = "This is ++underlined Text++"

html = markdown.markdown(text, extensions=['underline'])
print(html)
```


