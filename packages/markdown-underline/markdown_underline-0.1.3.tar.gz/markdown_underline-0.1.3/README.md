[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

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

# License

This project is licensed under the terms of the GNU General Public License v3.0.  
See the [LICENSE](./LICENSE) file for details.


