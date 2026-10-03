from markdown_it import MarkdownIt
from mdit_py_plugins.container import container_plugin

# Instantiate MarkdownIt with the necessary plugins
md = MarkdownIt().enable('table')
md.use(container_plugin, name="table-container")
md.use(container_plugin, name="table-horizontal")
md.use(container_plugin, name="table-cost-reporting")
md.use(container_plugin, name="page-break")

def render_md(html_text: str) -> str:
    return md.render(html_text)
