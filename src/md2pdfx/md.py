from markdown_it import MarkdownIt

# Instantiate MarkdownIt with the necessary plugins
md = MarkdownIt().enable('table')

def render_md(html_text: str) -> str:
    return md.render(html_text)
