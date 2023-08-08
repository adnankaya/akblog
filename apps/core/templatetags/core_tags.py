import markdown
from django.utils.safestring import mark_safe
from django import template
register = template.Library()


markdown_package_libraries = [
    "fenced_code",
    "footnotes",
    "tables",
]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(
        markdown.markdown(
            text,
            extensions=markdown_package_libraries,
            output_format='html5'
        )
    )


@register.simple_tag
def get_themes():
    return [
        "agate",
        "atom-one-dark",
        "atom-one-light",
        "default",
        "far",
        "felipec",
        "foundation",
        "github-dark",
        "github",
        "kimbie-light",
        "mono-blue",
        "monokai-sublime",
        "night-owl",
        "purebasic",
        "qtcreator-light",
        "school-book",
        "srcery",
        "stackoverflow-dark",
        "stackoverflow-light",
        "vs",
        "vs2015",
        "xt256",
    ]
