from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}"><link rel="stylesheet" href="{}">',
        static('css/main_layout.css'),
        static('css/mid_layout.css')
    )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script><script src="{}"></script>',
        static('js/main_layout.js'),
        static('js/mid_layout.js')
    )
