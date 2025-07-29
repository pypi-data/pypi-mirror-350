from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension
import re

class UnderlineExtension(Extension):
    def extendMarkdown(self, md):
        UNDERLINE_RE = r'(\+\+)(.+?)\1'
        md.inlinePatterns.register(SimpleTagInlineProcessor(UNDERLINE_RE, 'u'), 'underline', 175)

def makeExtension(**kwargs):
    return UnderlineExtension(**kwargs)
