
from django.utils.translation import gettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail import blocks
from types import SimpleNamespace
from wagtail import blocks
from wagtail.fields import StreamField
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils import timezone
from wagtail.fields import RichTextField
from enap_designsystem.blocks.base_blocks import CarouselBlock
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail import blocks
from datetime import datetime
import warnings
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, CharBlock, TextBlock, URLBlock, ListBlock, BooleanBlock, ChoiceBlock, StreamBlock, IntegerBlock
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images import get_image_model_string

from .base_blocks import BaseBlock
from .base_blocks import BaseLinkBlock
from .base_blocks import ButtonMixin
from .base_blocks import CoderedAdvTrackingSettings
from .base_blocks import LinkStructValue
from .base_blocks import BaseBlock, ButtonMixin, BaseLinkBlock, LinkStructValue, CoderedAdvTrackingSettings

class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """
    
    type_class = blocks.ChoiceBlock(
		choices=[
			('primary', 'Tipo primário'),
			('secondary', 'Tipo secundário'),
			('terciary', 'Tipo terciário'),
		],
		default='primary',
		help_text="Escolha o tipo do botão",
		label="Tipo de botão"
	)

    size_class = blocks.ChoiceBlock(
		choices=[
			('small', 'Pequeno'),
			('medium', 'Médio'),
			('large', 'Grande'),
			('extra-large', 'Extra grande'),
		],
		default='small',
		help_text="Escolha o tamanho do botão",
		label="Tamanho"
	)

    icone_bool = blocks.BooleanBlock(
        required=False,
        label=_("Icone"),
    )

    # Tentando remover campos herdados do codered
    button_style = None
    button_size = None
    page = None
    document = None
    downloadable_file = None
    class Meta:
        template = "enap_designsystem/blocks/button_block.html"
        icon = "cr-hand-pointer-o"
        label = _("Button Link")
        value_class = LinkStructValue

class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """

    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )

    class Meta:
        template = "enap_designsystem/blocks/download_block.html"
        icon = "download"
        label = _("Download")
    
class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )

    class Meta:
        template = "coderedcms/blocks/image_block.html"
        icon = "image"
        label = _("Image")

class ImageLinkBlock(BaseLinkBlock):
    """
    An <a> with an image inside it, instead of text.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_("Alternate text to show if the image doesn’t load"),
    )

    class Meta:
        template = "coderedcms/blocks/image_link_block.html"
        icon = "image"
        label = _("Image Link")
        value_class = LinkStructValue

class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """

    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_("Quote Text"),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
    )

    class Meta:
        template = "coderedcms/blocks/quote_block.html"
        icon = "openquote"
        label = _("Quote")


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "coderedcms/blocks/rich_text_block.html"

class PagePreviewBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Page to preview"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/pagepreview_block.html"
        icon = "doc-empty-inverse"
        label = _("Page Preview")



class PreviewCoursesBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Pagina de Formações"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/preview_courses.html"
        icon = "doc-empty-inverse"
        label = _("Preview de outras paginas")





class PageListBlock(BaseBlock):
    """
    Renders a preview of selected pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    # DEPRECATED: Remove in 3.0
    show_preview = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show body preview"),
    )
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagelist_block.html"
        icon = "list-ul"
        label = _("Preview ultimas paginas")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        # try to use the CoderedPage `get_index_children()`,
        # but fall back to get_children if this is a non-CoderedPage
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
            
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context




class NewsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagenoticias_block.html"
        icon = "list-ul"
        label = _("Carrossel escolher outras paginas")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CoursesCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/card_courses.html"
        icon = "list-ul"
        label = _("Carrossel de cursos")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context


class SuapCourseBlock(StructBlock):
    title = CharBlock(required=False, label="Título")
    description = CharBlock(required=False, label="Descrição")
    num_items = blocks.IntegerBlock(default=3,label=_("Máximo de cursos apresentados"),)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        num = value.get("num_items", 3)
        cursos_suap = self.get_destaques(num)
        context.update({
            "bloco_suap": value,
            "cursos_suap": cursos_suap
        })

        return context

    def get_destaques(self, limit=None):
        import requests
        try:
            resp = requests.get("https://bff-portal.enap.gov.br/v1/home/destaques", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if limit:
                data = data[: limit]
            return [SimpleNamespace(**item) for item in data]
        except Exception as e:
            return []

    class Meta:
        template = "enap_designsystem/blocks/suap/suap_courses_block.html"
        icon = "list-ul"
        label = "Cursos do SUAP"



class DropdownBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    options = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True)),
        ('page', blocks.PageChooserBlock(required=True))
    ]))

    class Meta:
        template = 'enap_designsystem/pages/mini/dropdown-holofote_blocks.html'
        icon = 'arrow_drop_down'
        label = 'Dropdown'




class EventsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected event pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page's LAYOUT tab."
        ),
    )

    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/pages/mini/eventos.html"
        icon = "date"
        label = _("Events Carousel escolhendo paginas")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CourseFeatureBlock(blocks.StructBlock):
    title_1 = blocks.CharBlock(required=True, help_text="Primeiro título da feature", default="Título da feature")
    description_1 = blocks.TextBlock(required=True, help_text="Primeira descrição da feature", default="Descrição da feature")
    title_2 = blocks.CharBlock(required=True, help_text="Segundo título da feature", default="Título da feature")
    description_2 = blocks.TextBlock(required=True, help_text="Segunda descrição da feature", default="Descrição da feature")
    image = ImageChooserBlock(required=False, help_text="Imagem da feature do curso")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_course.html"
        icon = "placeholder"
        label = "2 titulos, 2 descrições e uma imagem"
        initialized = True



class CourseModulesBlock(blocks.StructBlock):
    """Bloco de estrutura do curso com múltiplos dropdowns."""
    title = blocks.CharBlock(required=True, default="Estrutura do curso", help_text="Título da seção")
    
    modules = blocks.ListBlock(
        blocks.StructBlock([
            # Ordem invertida - module_title é o primeiro campo agora
            ("module_title", blocks.CharBlock(required=True, help_text="Título do módulo (ex: 1º Módulo)", default="1º Módulo")),
            ("module_description", blocks.TextBlock(required=True, help_text="Descrição breve do módulo", default="Descreva o módulo")),
            ("module_items", blocks.ListBlock(
                blocks.CharBlock(required=True, help_text="Item da lista de conteúdo do módulo")
            )),
        ]),
        min_num=1,
        help_text="Adicione os módulos do curso"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/feature_estrutura.html"
        icon = "list-ol"
        label = "Estrutura de Curso"
        initialized = True




class CourseIntroTopicsBlock(StructBlock):
    """Componente com introdução e tópicos fixos do curso."""
    title = CharBlock(label="Título do Curso", required=True, help_text="Título principal sobre o curso", default="Título do Curso")
    description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descrição geral do curso", default="Descreva o curso")
    image = ImageChooserBlock(label="Imagem", required=True, help_text="Imagem para destacar o curso")
    
    # Tópicos fixos com apenas descrições editáveis
    modalidade_description = RichTextBlock(label="Descrição da Modalidade", required=True, help_text="Descreva a modalidade do curso", default="Descreva a modalidade do curso")
    curso_description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descreva o conteúdo do curso", default="Descreva o conteúdo do curso")
    metodologia_description = RichTextBlock(label="Descrição da Metodologia", required=True, help_text="Descreva a metodologia do curso", default="Descreva a metodologia do curso")
    
    class Meta:
        template = 'enap_designsystem/blocks/course_intro_topics.html'
        icon = 'doc-full'
        label = 'Introdução e Tópicos de Curso'




class WhyChooseEnaptBlock(blocks.StructBlock):
    """Seção 'Por que escolher a Enap?'"""
    # Título e descrição principal
    title = blocks.CharBlock(required=True, label=_("Título principal"), default="Titulo do beneficio")
    description = blocks.TextBlock(required=False, label=_("Descrição principal"), default="Titulo do beneficio")
    
    # Benefício 1
    image_1 = ImageChooserBlock(required=False, label=_("Imagem do benefício 1"))
    title_1 = blocks.CharBlock(required=True, label=_("Título do benefício 1"), default="Metodologia ensino–aplicação")
    
    # Benefício 2
    image_2 = ImageChooserBlock(required=False, label=_("Imagem do benefício 2"))
    title_2 = blocks.CharBlock(required=True, label=_("Título do benefício 2"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 3
    image_3 = ImageChooserBlock(required=False, label=_("Imagem do benefício 3"))
    title_3 = blocks.CharBlock(required=True, label=_("Título do benefício 3"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 4
    image_4 = ImageChooserBlock(required=False, label=_("Imagem do benefício 4"))
    title_4 = blocks.CharBlock(required=True, label=_("Título do benefício 4"), default="Desenvolvimento de competências de forma inovadora")

    class Meta:
        template = 'enap_designsystem/blocks/why_choose.html'
        icon = 'placeholder'
        label = _("4 beneficios, icones e texto")





class ProcessoSeletivoBlock(blocks.StructBlock):
    """Bloco para exibir informações sobre o processo seletivo com 3 módulos."""
    title = blocks.CharBlock(required=True, default="Processo seletivo", help_text="Título da seção")
    description = blocks.TextBlock(required=True, default="Sobre o processo seletivo", help_text="Descrição do processo seletivo")
    
    # Módulo 1
    module1_title = blocks.CharBlock(required=True, default="Inscrição", help_text="Título do primeiro módulo")
    module1_description = blocks.TextBlock(required=True, help_text="Descrição do primeiro módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    # Módulo 2
    module2_title = blocks.CharBlock(required=True, default="Seleção", help_text="Título do segundo módulo")
    module2_description = blocks.TextBlock(required=True, help_text="Descrição do segundo módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    # Módulo 3
    module3_title = blocks.CharBlock(required=True, default="Resultado", help_text="Título do terceiro módulo")
    module3_description = blocks.TextBlock(required=True, help_text="Descrição do terceiro módulo", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_processo_seletivo.html"
        icon = "list-ul"
        label = "Processo Seletivo"
        initialized = True




class TeamCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir membros da equipe."""
    title = blocks.CharBlock(required=True, default="Nossa Equipe", help_text="Título da seção")
    description = blocks.TextBlock(required=True, help_text="Descrição da seção da equipe", default="Equipe de desenvolvedores e etc")
    view_all_text = blocks.CharBlock(required=False, default="Ver todos", help_text="Texto do botão 'ver todos'")
    
    members = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome do membro da equipe")),
            ("role", blocks.RichTextBlock(required=True, help_text="Cargo/função do membro")),
            ("image", ImageChooserBlock(required=False, help_text="Foto do membro da equipe")),
        ]),
        help_text="Adicione os membros da equipe",
        default=[
            {'name': 'Membro 1', 'role': 'Cargo 1', 'image': None},
            {'name': 'Membro 2', 'role': 'Cargo 2', 'image': None},
            {'name': 'Membro 3', 'role': 'Cargo 3', 'image': None},
            {'name': 'Membro 4', 'role': 'Cargo 4', 'image': None},
        ],
        collapsed=False
    )

    class Meta:
        template = 'enap_designsystem/blocks/team_carousel.html'
        icon = 'group'
        label = 'Carrossel de Equipe'




class TestimonialsCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir depoimentos ou testemunhos."""
    title = blocks.CharBlock(required=True, default="Depoimentos", help_text="Título da seção")
    description = blocks.TextBlock(required=False, help_text="Descrição opcional da seção")
    
    testimonials = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome da pessoa", default="Nome do profissional")),
            ("position", blocks.CharBlock(required=True, help_text="Cargo ou posição da pessoa", default="Cargo do profissional")),
            ("testimonial", blocks.TextBlock(required=True, help_text="Depoimento da pessoa", default="Lorem ipsum dolor sit amet, lorem ipsum dolor sit amet")),
            ("image", ImageChooserBlock(required=True, help_text="Foto da pessoa")),
        ]),
        help_text="Adicione os depoimentos"
    )
    
    class Meta:
        template = 'enap_designsystem/blocks/testimonials_carousel.html'
        icon = 'openquote'
        label = 'Carrossel de Depoimentos'







# Definição dos blocos de conteúdo para o StreamField
class HeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    level = blocks.ChoiceBlock(choices=[
        ('h2', 'Título Nível 2'),
        ('h3', 'Título Nível 3'),
        ('h4', 'Título Nível 4'),
    ], default='h2')

    class Meta:
        template = 'blocks/heading_block.html'
        icon = 'title'
        label = 'Título'


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = 'enap_designsystem/blocks/richtext_block.html'
        icon = 'doc-full'
        label = 'Texto'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True) 
    caption = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/image_block.html'
        icon = 'image'
        label = 'Imagem'

class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    attribution = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/quote_block.html'
        icon = 'openquote'
        label = 'Citação'


class VideoBlock(blocks.StructBlock):
    url = blocks.URLBlock(required=True, help_text="URL do YouTube ou Vimeo")
    caption = blocks.CharBlock(required=False)
    
    class Meta:
        template = 'enap_designsystem/blocks/video_block.html'
        icon = 'media'
        label = 'Embed Vídeo'

ARTICLE_STREAMBLOCKS = [
    ('richtext', RichTextBlock()),
    ("button", ButtonBlock()),
    ('image', ImageBlock()),
    ('quote', QuoteBlock()),
    ('carousel', CarouselBlock()),
    ("download", DownloadBlock()),
    ("embed_video", VideoBlock()),
    ("noticias_carousel", NewsCarouselBlock()),
    ("eventos_carousel", EventsCarouselBlock()),
]

class ArticlePage(Page):
    """
    Página de artigo, adequada para notícias ou conteúdo de blog.
    """

    class Meta:
        verbose_name = _("ENAP Artigo")
        verbose_name_plural = _("ENAP Artigos")

    template = "enap_designsystem/blocks/article_page.html"

    # Campo para o conteúdo principal
    body = StreamField(
        ARTICLE_STREAMBLOCKS,
        null=True,
        blank=True,
        verbose_name=_("Conteúdo"),
        use_json_field=True,
    )

    # Campos de metadados do artigo
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Legenda"),
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Autor"),
        related_name='enap_articlepage_set',
    )
    
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Exibir autor como"),
        help_text=_("Substitui como o nome do autor é exibido neste artigo."),
    )
    
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Data de publicação para exibição"),
    )

    # Campos para SEO e compartilhamento
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Imagem destacada"),
        help_text=_("Imagem usada para compartilhamento em redes sociais e listagens"),
    )

    # Propriedades para SEO e exibição de metadados
    @property
    def seo_author(self) -> str:
        """
        Obtém o nome do autor usando uma estratégia de fallback.
        """
        if self.author_display:
            return self.author_display
        if self.author:
            return self.author.get_full_name()
        if self.owner:
            return self.owner.get_full_name()
        return ""

    @property
    def seo_published_at(self) -> datetime:
        """
        Obtém a data de publicação para exibição.
        """
        if self.date_display:
            return self.date_display
        return self.first_published_at

    @property
    def seo_description(self) -> str:
        """
        Obtém a descrição usando uma estratégia de fallback.
        """
        if self.search_description:
            return self.search_description
        if self.caption:
            return self.caption
        return self.get_body_preview(100)

    @property
    def get_body_preview(self, length=100) -> str:
        """
        Obtém uma prévia do conteúdo do artigo.
        """
        text = ""
        for block in self.body:
            if block.block_type == 'richtext':
                text += block.value.source
            elif block.block_type == 'heading':
                text += block.value['heading'] + " "
        
        # Remover tags HTML e limitar caracteres
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text[:length] + "..." if len(text) > length else text

    @property
    def url_filter(self):
        if hasattr(self, 'full_url') and self.full_url:
            return self.full_url
        return self.get_url_parts()[2] if self.get_url_parts() else ""
    
        
    # Configuração de busca
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('caption', boost=2),
        index.FilterField('author'),
        index.FilterField('author_display'),
        index.FilterField('date_display'),
        index.FilterField("url", name="url_filter"),
    ]

    # Painéis de conteúdo para o admin
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('caption'),
        FieldPanel('featured_image'),
        MultiFieldPanel(
            [
                FieldPanel('author'),
                FieldPanel('author_display'),
                FieldPanel('date_display'),
            ],
            heading=_("Informações de Publicação"),
        ),
    ]
    
    def get_searchable_content(self):
        content = super().get_searchable_content()
        content.append(self.caption or "")
        content.append(self.seo_description or "")
        content.append(self.get_body_preview())
        return content
    
    # Métodos auxiliares para templates
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Você pode adicionar variáveis de contexto específicas para artigos aqui
        return context


class ArticleIndexPage(Page):
    """
    Página de índice que mostra uma lista de artigos.
    """

    class Meta:
        verbose_name = _("ENAP Página de Índice de Artigos")
        verbose_name_plural = _("ENAP Páginas de Índice de Artigos")

    template = "enap_designsystem/pages/article_index_page.html"

    # Introdução para a página de listagem
    intro = models.TextField(
        blank=True,
        verbose_name=_("Introdução"),
    )
    
    # Opções de exibição dos artigos
    show_images = models.BooleanField(
        default=True,
        verbose_name=_("Exibir imagens"),
    )
    
    show_captions = models.BooleanField(
        default=True,
        verbose_name=_("Exibir legendas"),
    )
    
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_("Exibir autor e informações de data"),
    )
    
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_("Exibir texto de prévia"),
    )
    
    articles_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Artigos por página"),
    )

    # Configuração de busca
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    # Painéis de conteúdo para o admin
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel(
            [
                FieldPanel('show_images'),
                FieldPanel('show_captions'),
                FieldPanel('show_meta'),
                FieldPanel('show_preview_text'),
                FieldPanel('articles_per_page'),
            ],
            heading=_("Exibição de artigos"),
        ),
    ]

    def get_searchable_content(self):
        content = super().get_searchable_content()
        content.append(self.intro or "")
        content.append(self.search_description or "")
        return content
    
    def get_context(self, request, *args, **kwargs):
        """
        Adiciona artigos ao contexto.
        """
        context = super().get_context(request, *args, **kwargs)
        
        # Obtém todos os artigos
        articles = ArticlePage.objects.live().descendant_of(self)
        
        # Ordena por data (mais recente primeiro)
        articles = articles.order_by('-date_display', '-first_published_at')
        
        # Paginação
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        paginator = Paginator(articles, self.articles_per_page)
        page = request.GET.get('page')
        
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        
        context['articles'] = articles
        return context


class ENAPNoticiasIndexPage(Page):
	subpage_types = ['enap_designsystem.ENAPNoticiaImportada', 'enap_designsystem.ENAPNoticia']

	class Meta:
		verbose_name = _("ENAP Índice de Notícias")
		verbose_name_plural = _("ENAP Índice de Notícias")

	template = "enap_designsystem/pages/article/enap_noticias_index.html"

	def get_context(self, request):
		context = super().get_context(request)

		start = int(request.GET.get("start", 0))
		page_size = 30
		page_number = (start // page_size) + 1

		children = []

	# Evita erro no preview antes da página existir na árvore
		if self.pk and self.live:
			children = self.get_children().live().specific().type(
				ENAPNoticiaImportada, ENAPNoticia
			).order_by("-first_published_at")

			paginator = Paginator(children, page_size)
			page = paginator.get_page(page_number)

			context["articles"] = page
			context["start"] = start
			context["page"] = page
			context["page_size"] = page_size
			context["start_prev"] = (page.previous_page_number - 1) * page_size if page.has_previous() else None
			context["start_next"] = (page.next_page_number - 1) * page_size if page.has_next() else None
		else:
			# Em preview de página nova, sem filhos
			context["articles"] = []
			context["start"] = 0
			context["page"] = None
			context["page_size"] = page_size
			context["start_prev"] = None
			context["start_next"] = None

		return context

class ENAPNoticia(Page):
	"""Modelo base para novas notícias (customizável depois)."""

	class Meta:
		verbose_name = _("ENAP Notícia")
		verbose_name_plural = _("ENAP Notícias")

	template = "enap_designsystem/pages/article/enap_noticia.html"

class ENAPNoticiaImportada(Page):
    """Página exclusiva para exibir artigos importados do Joomla, sem edição."""

    descricao_html = models.TextField(
        verbose_name="Descrição (Introtext)",
        blank=True,
        help_text="Conteúdo HTML do campo 'introtext' do Joomla."
    )

    conteudo_html = models.TextField(
        verbose_name="Conteúdo (Fulltext)",
        blank=True,
        help_text="Conteúdo HTML do campo 'fulltext' do Joomla."
    )

    xref_categoria = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Categoria Joomla (Texto Livre)"
    )

    imagem_externa = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem Externa (image_intro)"
    )

    imagem_interna = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem Interna (image_fulltext)"
    )

    navbar = models.ForeignKey(
        "EnapNavbarSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("navbar"),
        FieldPanel("xref_categoria"),
        FieldPanel("imagem_externa"),
        FieldPanel("imagem_interna"),
        FieldPanel("descricao_html"),
        FieldPanel("conteudo_html"),
    ]

    template = "enap_designsystem/pages/article/joomla/enap_noticia_importada.html"

    class Meta:
        verbose_name = _("ENAP Noticias Joomla")
        verbose_name_plural = _("ENAP Noticias Joomla")

class ENAPDummyPage(Page):
	"""Página usada apenas como container na árvore, sem conteúdo visível."""

	class Meta:
		verbose_name = "Container (não exibido)"
		verbose_name_plural = "Containers"

	# Redireciona para o primeiro filho disponível, caso não tenha, 404
	def serve(self, request):
		# redireciona para o primeiro filho
		first_child = self.get_children().live().first()
		if first_child:
			return redirect(first_child.url)
		from django.http import Http404
		raise Http404("Sem conteúdo filho para redirecionar.")


class SectionCardTitleCenterBlock(StructBlock):
    """Componente de seção com cards e título centralizado."""
    # Campos da seção
    title = CharBlock(required=False, label="Título da Seção", default="Título da Seção")
    highlight_text = CharBlock(
        required=False, 
        label="Texto Destacado", 
        help_text="Parte do título que terá gradiente (opcional)",
        default=""
    )
    subtitle = RichTextBlock(
        required=False, 
        label="Subtítulo da Seção",
        default="<p>Subtítulo da seção com informações relevantes.</p>"
    )
    
    # Cards como itens internos
    cards = ListBlock(
        StructBlock([
            ('title', CharBlock(required=False, label="Título do Card", default="Título do Card")),
            ('description', RichTextBlock(
                required=False, 
                label="Descrição do Card", 
                default="<p>Descrição detalhada do card com informações importantes para o usuário.</p>"
            )),
            ('icon_class', CharBlock(
                required=True, 
                label="Classe do Ícone", 
                help_text="Cole o código do Font Awesome aqui (ex: 'fa-solid fa-book')",
                default="fa-solid fa-star"
            )),
            ('link_text', CharBlock(required=False, label="Texto do Link", default="Acessar")),
            ('link_url', URLBlock(required=False, label="URL do Link", default="https://gov.br/")),
            ('highlight_color', CharBlock(
                required=True, 
                label="Cor de Destaque", 
                help_text="Insira um código de cor HEX (ex: #FF7E38)",
                default="#FF7E38"
            )),
        ]),
        label="Cards"
    )

    class Meta:
        template = 'enap_designsystem/blocks/section_card_title_center.html'
        icon = 'placeholder'
        label = 'Seção de Cards (Título Centralizado)'




class SectionTabsCardsBlock(StructBlock):
    """Componente de seção com abas e cards dinâmicos."""
    # Campos da seção
    title = CharBlock(required=True, label="Título da Seção", default="Título da Seção")
    highlight_text = CharBlock(
        required=False, 
        label="Texto Destacado", 
        help_text="Parte do título que terá gradiente (opcional)",
        default=""
    )
    subtitle = RichTextBlock(
        required=True, 
        label="Subtítulo da Seção",
        default="<p>Subtítulo da seção com informações relevantes.</p>"
    )
    
    # Configuração das abas
    tabs = ListBlock(
        StructBlock([
            ('tab_title', CharBlock(required=True, label="Título da Aba", default="Título da Aba")),
            ('is_default_active', BooleanBlock(required=False, label="Ativar por padrão", default=False)),
            ('cards', ListBlock(
                StructBlock([
                    ('title', CharBlock(required=False, label="Título do Card", default="Título do Card")),
                    ('description', RichTextBlock(
                        required=False, 
                        label="Descrição do Card", 
                        default="<p>Descrição detalhada do card com informações importantes para o usuário.</p>"
                    )),
                    ('icon_class', CharBlock(
                        required=False, 
                        label="Classe do Ícone", 
                        help_text="Cole o código do Font Awesome aqui (ex: 'fa-solid fa-book')",
                        default="fa-solid fa-star"
                    )),
                    ('link_text', CharBlock(required=False, label="Texto do Link", default="Acessar")),
                    ('link_url', URLBlock(required=False, label="URL do Link", default="https://gov.br/")),
                    ('highlight_color', CharBlock(
                        required=True, 
                        label="Cor de Destaque", 
                        help_text="Insira um código de cor HEX (ex: #5E17EB)",
                        default="#FF7E38"
                    )),
                ]),
                label="Cards",
                default=[]
            )),
            ('layout_type', ChoiceBlock(
                choices=[
                    ('grid', 'Grid - Cards em forma de grade'),
                    ('list', 'Lista - Cards em formato de lista')
                ],
                default='grid',
                label="Tipo de Layout"
            )),
            ('columns', ChoiceBlock(
                choices=[
                    ('2', '2 Colunas'),
                    ('3', '3 Colunas'),
                    ('4', '4 Colunas'),
                    ('5', '5 Colunas')
                ],
                default='3',
                label="Número de Colunas"
            )),
        ]),
        label="Abas",
        default=[]
    )
    
    # Estilo personalizado
    primary_color = CharBlock(
        required=True, 
        label="Cor Primária", 
        help_text="Cor principal do componente (ex: #5E17EB)",
        default="#FF7E38"
    )
    
    secondary_color = CharBlock(
        required=True, 
        label="Cor Secundária", 
        help_text="Cor secundária do componente (ex: #FF7C3B)",
        default="#FF7C3B"
    )
    
    background_color = CharBlock(
        required=True, 
        label="Cor de Fundo", 
        help_text="Cor de fundo da seção (ex: #FFFFFF)",
        default="#FFFFFF"
    )

    class Meta:
        template = 'enap_designsystem/blocks/section_tabs_cards.html'
        icon = 'table'
        label = 'Seção de tabs com cards'




class CTAImagemBlock(blocks.StructBlock):
    # Content fields
    badge_text = blocks.CharBlock(default="Novidade", max_length=50)
    title = blocks.CharBlock(default="Conheça a", max_length=100)
    highlighted_title = blocks.CharBlock(default="Biblioteca do Futuro", required=False, max_length=100, help_text="Highlighted part of the title")
    description = blocks.RichTextBlock(default="Uma iniciativa da Diretoria de Inovação que nasce da necessidade e do desejo de transformar a biblioteca em um espaço de construção de conhecimento, colaboração e inovação.")
    button_text = blocks.CharBlock(default="Saiba mais", max_length=50)
    button_link = blocks.URLBlock(default="#")
    
    # Color settings
    gradient_start_color = blocks.CharBlock(default="#FF7E38", max_length=20, help_text="Cor inicial do gradiente (formato hexadecimal)")
    gradient_end_color = blocks.CharBlock(default="#FF3D82", max_length=20, help_text="Cor final do gradiente (formato hexadecimal)")
    button_color = blocks.CharBlock(default="#FFFFFF", max_length=20, help_text="Cor do botão (formato hexadecimal)")
    button_text_color = blocks.CharBlock(default="#FF7E38", max_length=20, help_text="Cor do texto do botão (formato hexadecimal)")
    
    # Images
    top_image = ImageChooserBlock(required=True, help_text="Imagem superior")
    bottom_image = ImageChooserBlock(required=True, help_text="Imagem inferior")

    class Meta:
        template = 'enap_designsystem/blocks/cta_imagem_block.html'
        icon = 'image'
        label = 'CTA com Imagem'
        group = 'Custom Blocks'




class ContainerInfo(blocks.StructBlock):
    # Header content
    title_prefix = blocks.CharBlock(default="Nossas", max_length=100)
    title_highlight = blocks.CharBlock(default="Bases de Dados", max_length=100)
    description = blocks.TextBlock(default="Acesse bases de dados com livros e periódicos eletrônicos, nacionais e internacionais, sobre administração pública e áreas correlatas")
    
    # Color settings - outside of StreamField
    highlight_color = blocks.CharBlock(default="#4CAF50", max_length=20, help_text="Cor principal do componente (formato hexadecimal)")
    
    # Main content as StreamField
    content_sections = blocks.StreamBlock([
        ('section', blocks.StructBlock([
            ('database_title', blocks.CharBlock(default="Portal de Periódicos da Capes", max_length=100)),
            ('database_description', blocks.TextBlock(default="A Biblioteca da Enap disponibiliza acesso a bases de dados com livros e periódicos eletrônicos, nacionais e internacionais. O acesso ao Portal é vinculado à rede da Enap, mas alunos, pesquisadores, professores e servidores têm acesso remoto.")),
            ('cards', blocks.ListBlock(
                blocks.StructBlock([
                    ('name', blocks.CharBlock(default="JSTOR", max_length=100)),
                    ('info', blocks.TextBlock(default="Base multidisciplinar com mais de 2.600 periódicos acadêmicos, livros e fontes primárias.")),
                    ('link', blocks.URLBlock(default="https://www.jstor.org/", required=False, help_text="Link para a base de dados")),
                ])
            )),
        ])),
    ])

    class Meta:
        template = 'enap_designsystem/blocks/container_info_block.html'
        icon = 'database'
        label = 'Informativo: Titulo, Descrição e Cards'
        group = 'Custom Blocks'





class ContatoBlock(blocks.StructBlock):
    # Header content
    title_prefix = blocks.CharBlock(default="Fale", max_length=100)
    title_highlight = blocks.CharBlock(default="Conosco", max_length=100)
    description = blocks.TextBlock(default="Entre em contato com a Biblioteca Graciliano Ramos")
    
    # Contact details
    phone_title = blocks.CharBlock(default="Telefone", max_length=100)
    phone = blocks.CharBlock(default="(61) 2020-3139", required=False)
    
    email_title = blocks.CharBlock(default="E-mail", max_length=100)
    email = blocks.CharBlock(default="biblioteca@enap.gov.br", required=False)
    
    address_title = blocks.CharBlock(default="Endereço", max_length=100)
    address = blocks.TextBlock(default="SPO Área Especial 2A - Térreo\nBrasília-DF - CEP: 70610-900", required=False)
    
    hours_title = blocks.CharBlock(default="Horário de Funcionamento", max_length=100)
    hours = blocks.TextBlock(default="Segunda a sexta-feira das 9h às 19h00", required=False)
    
    # Map
    map_embed_url = blocks.URLBlock(default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3839.7410214087293!2d-47.91252422392779!3d-15.783966284838556!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x935a3aec4bdd315d%3A0xe4b35324fd775722!2sEscola%20Nacional%20de%20Administra%C3%A7%C3%A3o%20P%C3%BAblica%20(Enap)!5e0!3m2!1spt-BR!2sbr!4v1650293487600!5m2!1spt-BR!2sbr", required=True)
    
    # Color settings
    highlight_color = blocks.CharBlock(default="#FF7E38", max_length=20, help_text="Cor principal do componente (formato hexadecimal)")

    class Meta:
        template = 'enap_designsystem/blocks/contato_block.html'
        icon = 'mail'
        label = 'Bloco de Contato'
        group = 'Custom Blocks'




class FormContato(blocks.StructBlock):
    """
    Componente de formulário de contato com personalização de cor.
    """
    cor_primaria = blocks.CharBlock(
        default="#FF7E38",
        help_text="Cor principal do componente (formato hexadecimal, ex: #5e17eb)"
    )
    
    titulo = blocks.CharBlock(
        default="Fale Conosco",
        help_text="Título principal do formulário",
        required=False
    )
    
    subtitulo = blocks.TextBlock(
        default="Entre em contato conosco para esclarecer dúvidas, enviar sugestões ou solicitar informações.",
        help_text="Texto de introdução",
        required=False
    )
    
    # Campos do lado esquerdo (formulário)
    titulo_formulario = blocks.CharBlock(
        default="Envie sua mensagem",
        help_text="Título da seção do formulário"
    )
    
    mostrar_texto_obrigatorio = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir texto informando sobre campos obrigatórios"
    )
    
    texto_obrigatorio = blocks.CharBlock(
        default="* Campo obrigatório",
        help_text="Texto exibido para informar sobre campos obrigatórios",
        required=False
    )
    
    texto_botao = blocks.CharBlock(
        default="Enviar mensagem",
        help_text="Texto do botão de envio"
    )
    
    mostrar_checkbox_copia = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir opção para enviar cópia para o remetente"
    )
    
    texto_checkbox_copia = blocks.CharBlock(
        default="Enviar cópia para mim (opcional)",
        help_text="Texto da opção para enviar cópia",
        required=False
    )
    
    # Campos do lado direito (informações de contato)
    titulo_informacoes = blocks.CharBlock(
        default="Informações de Contato",
        help_text="Título da seção de informações de contato"
    )
    
    endereco_titulo = blocks.CharBlock(
        default="Campus Asa Sul",
        help_text="Título do endereço",
        required=False
    )
    
    endereco = blocks.CharBlock(
        default="SAIS AE 2A Térreo - Enap Campus Asa Sul – Brasília-DF",
        help_text="Endereço completo",
        required=False
    )
    
    horario_titulo = blocks.CharBlock(
        default="Horário de Funcionamento",
        help_text="Título do horário de funcionamento",
        required=False
    )
    
    horario = blocks.CharBlock(
        default="Segunda a sexta-feira das 9h às 18h00",
        help_text="Horário de funcionamento",
        required=False
    )
    
    telefone_titulo = blocks.CharBlock(
        default="Telefone",
        help_text="Título do telefone",
        required=False
    )
    
    telefone = blocks.CharBlock(
        default="(61) 2020-3139",
        help_text="Número de telefone",
        required=False
    )
    
    email_titulo = blocks.CharBlock(
        default="E-mail",
        help_text="Título do e-mail",
        required=False
    )
    
    email = blocks.CharBlock(
        default="biblioteca@enap.gov.br",
        help_text="Endereço de e-mail",
        required=False
    )
    
    # Mapa e localização
    mostrar_mapa = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir mapa de localização"
    )
    
    imagem_mapa = ImageChooserBlock(
        required=False,
        help_text="Imagem do mapa (opcional, se preferir usar uma imagem estática)"
    )
    
    link_mapa = blocks.URLBlock(
        default="https://maps.google.com",
        help_text="Link para o mapa (ex: Google Maps)",
        required=False
    )
    
    texto_link_mapa = blocks.CharBlock(
        default="Visualizar Localização - Google Maps",
        help_text="Texto do link para o mapa",
        required=False
    )
    
    # Newsletter (opcional)
    mostrar_newsletter = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir seção de newsletter"
    )
    
    titulo_newsletter = blocks.CharBlock(
        default="Assine nossa Newsletter",
        help_text="Título da seção de newsletter",
        required=False
    )
    
    subtitulo_newsletter = blocks.TextBlock(
        default="Receba novidades, atualizações do acervo e eventos diretamente no seu e-mail",
        help_text="Subtítulo da seção de newsletter",
        required=False
    )
    
    placeholder_newsletter = blocks.CharBlock(
        default="Seu melhor e-mail",
        help_text="Texto de placeholder do campo de e-mail",
        required=False
    )
    
    texto_botao_newsletter = blocks.CharBlock(
        default="Inscrever-se",
        help_text="Texto do botão de inscrição",
        required=False
    )
    
    mostrar_categorias_newsletter = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir categorias de interesse na newsletter"
    )
    
    categorias_newsletter = blocks.ListBlock(
        blocks.StructBlock([
            ('nome', blocks.CharBlock(required=True)),
            ('marcado', blocks.BooleanBlock(default=False, required=False)),
        ]),
        default=[
            {'nome': 'Novas aquisições', 'marcado': True},
            {'nome': 'Eventos e workshops', 'marcado': True},
            {'nome': 'Biblioteca do Futuro', 'marcado': False},
            {'nome': 'Boletim informativo mensal', 'marcado': False},
        ],
        help_text="Categorias disponíveis para assinatura",
        required=False
    )
    
    texto_privacidade = blocks.CharBlock(
        default="Você pode cancelar sua inscrição a qualquer momento. Respeitamos sua privacidade.",
        help_text="Texto sobre privacidade",
        required=False
    )

    class Meta:
        template = "enap_designsystem/blocks/form_contato.html"
        icon = "mail"
        label = "Formulário de Contato"
        help_text = "Adiciona um formulário de contato com informações e newsletter"

    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}
        
        # Validação de cor hexadecimal
        cor_primaria = cleaned_data.get('cor_primaria', '')
        if not cor_primaria.startswith('#') or len(cor_primaria) != 7:
            errors['cor_primaria'] = ErrorList(['Formato de cor inválido. Use o formato hexadecimal (ex: #5e17eb)'])
        
        if errors:
            raise blocks.StructBlockValidationError(errors)
        
        return cleaned_data
    




class SobreLinhas(blocks.StructBlock):
    """
    Componente para exibir seções com títulos, ícones FontAwesome e conteúdo em formato de linhas.
    """
    cor_primaria = blocks.CharBlock(
        default="#FF7E38",
        help_text="Cor principal do componente (formato hexadecimal, ex: #5e17eb)"
    )
    
    cor_secundaria = blocks.CharBlock(
        default="#ff5a5f",
        help_text="Cor secundária para gradientes (formato hexadecimal, ex: #ff5a5f)",
        required=False
    )
    
    titulo = blocks.CharBlock(
        default="Sobre a Biblioteca",
        help_text="Título principal da página"
    )
    
    palavra_destaque = blocks.CharBlock(
        default="Biblioteca",
        help_text="Palavra do título que será destacada com gradiente"
    )
    
    subtitulo = blocks.TextBlock(
        default="Referência em Administração Pública e Gestão Governamental",
        help_text="Subtítulo ou descrição breve"
    )
    
    secoes = blocks.ListBlock(
        blocks.StructBlock([
            ('icone_fa', blocks.CharBlock(
                default="book",
                help_text="Código do ícone do FontAwesome (ex: book, home). Use apenas o nome sem 'fa-'."
            )),
            ('titulo_secao', blocks.CharBlock(
                default="Título da Seção",
                help_text="Título desta seção"
            )),
            ('conteudo', blocks.RichTextBlock(
                default="<p>Conteúdo da seção...</p>",
                help_text="Conteúdo detalhado desta seção"
            )),
        ]),
        min_num=1,
        help_text="Adicione seções com ícones, títulos e conteúdo"
    )
    
    mostrar_botao_acao = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text="Exibir botão de ação ao final"
    )
    
    texto_botao = blocks.CharBlock(
        default="Acesse o Regulamento",
        help_text="Texto do botão de ação",
        required=False
    )
    
    link_botao = blocks.URLBlock(
        default="#",
        help_text="Link para onde o botão direciona",
        required=False
    )
    
    class Meta:
        icon = "doc-full"
        label = "Sobre em Tópicos"
        help_text = "Cards com ícones e cor variavel"
        template = "enap_designsystem/blocks/sobre_linhas.html"
        
    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}
        
        # Validação de cor hexadecimal para cor primária
        cor_primaria = cleaned_data.get('cor_primaria', '')
        if not cor_primaria.startswith('#') or len(cor_primaria) != 7:
            errors['cor_primaria'] = ErrorList(['Formato de cor inválido. Use o formato hexadecimal (ex: #5e17eb)'])
            
        # Validação de cor hexadecimal para cor secundária (se fornecida)
        cor_secundaria = cleaned_data.get('cor_secundaria', '')
        if cor_secundaria and (not cor_secundaria.startswith('#') or len(cor_secundaria) != 7):
            errors['cor_secundaria'] = ErrorList(['Formato de cor inválido. Use o formato hexadecimal (ex: #ff5a5f)'])
        
        # Validação da palavra de destaque
        palavra_destaque = cleaned_data.get('palavra_destaque', '')
        titulo = cleaned_data.get('titulo', '')
        if palavra_destaque and palavra_destaque not in titulo:
            errors['palavra_destaque'] = ErrorList(['A palavra de destaque deve estar presente no título.'])
        
        if errors:
            raise blocks.StructBlockValidationError(errors)
        
        return cleaned_data
    




class EventoBlock(blocks.StructBlock):
    """Bloco para exibir eventos com filtros de categoria"""
    
    titulo_secao = blocks.CharBlock(
        default="Próximos Eventos",
        label="Título da Seção",
        help_text="Título que aparecerá no topo da seção de eventos"
    )
    
    descricao_secao = blocks.TextBlock(
        default="Participe de nossa programação diversificada de eventos presenciais e online",
        label="Descrição da Seção",
        help_text="Texto que aparecerá abaixo do título da seção"
    )
    
    cor_principal = blocks.CharBlock(
        default="#FF7E38",
        label="Cor Principal",
        help_text="Código de cor hexadecimal (ex: #3f51b5) que será aplicada nos destaques, botões e abas"
    )
    
    # Sem o campo de cor individual para cada categoria
    categorias = blocks.ListBlock(
        blocks.StructBlock([
            ('nome', blocks.CharBlock(label="Nome da Categoria")),
            ('slug', blocks.CharBlock(
                label="Slug da Categoria",
                help_text="Identificador único da categoria (opcional)",
                required=False
            )),
        ]),
        label="Categorias de Eventos",
        help_text="Defina as categorias que serão usadas para filtrar os eventos"
    )
    
    eventos = blocks.ListBlock(
        blocks.StructBlock([
            ('titulo', blocks.CharBlock(label="Título do Evento")),
            ('categoria', blocks.CharBlock(
                label="Categoria",
                help_text="Deve corresponder exatamente ao nome de uma categoria definida acima"
            )),
            ('imagem', ImageChooserBlock(label="Imagem do Evento")),
            ('data', blocks.DateBlock(label="Data do Evento")),
            ('hora_inicio', blocks.TimeBlock(label="Hora de Início")),
            ('hora_fim', blocks.TimeBlock(label="Hora de Término")),
            ('local', blocks.CharBlock(label="Local")),
            ('descricao', blocks.TextBlock(label="Descrição do Evento")),
            ('vagas_disponiveis', blocks.IntegerBlock(label="Vagas Disponíveis", min_value=0)),
        ]),
        label="Lista de Eventos",
        help_text="Adicione os eventos que serão exibidos"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/evento_block.html"
        icon = "date"
        label = "Bloco de Eventos com Filtro"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        
        # Gerar slugs automaticamente para as categorias que não possuem
        categorias = []
        for categoria in value['categorias']:
            cat = dict(categoria)
            if not cat.get('slug'):
                cat['slug'] = slugify(cat.get('nome', ''))
            categorias.append(cat)
        
        # Vamos ordenar os eventos por data
        eventos_ordenados = sorted(
            value['eventos'], 
            key=lambda e: datetime.combine(e['data'], e['hora_inicio'])
        )
        
        # Organizando eventos por categoria
        eventos_por_categoria = {}
        for evento in eventos_ordenados:
            categoria = evento['categoria']
            if categoria not in eventos_por_categoria:
                eventos_por_categoria[categoria] = []
            eventos_por_categoria[categoria].append(evento)
            
        context['categorias'] = categorias
        context['eventos_ordenados'] = eventos_ordenados
        context['eventos_por_categoria'] = eventos_por_categoria
        context['cor_principal'] = value.get('cor_principal', '#3f51b5')
        
        return context
    




class HeroAnimadaBlock(blocks.StructBlock):
    """Bloco para exibir um banner animado com imagem e conteúdo"""
    
    titulo = blocks.CharBlock(
        default="Biblioteca do Futuro",
        label="Título",
        help_text="Título principal do banner"
    )
    
    texto_destaque = blocks.CharBlock(
        default="Futuro",
        label="Texto com Destaque",
        help_text="Parte do título que receberá o efeito gradiente"
    )
    
    descricao = blocks.TextBlock(
        default="Reimaginando a experiência da biblioteca tradicional com tecnologia",
        label="Descrição",
        help_text="Texto descritivo que aparecerá abaixo do título"
    )
    
    badge_texto = blocks.CharBlock(
        default="Novo Projeto",
        label="Texto do Badge",
        help_text="Texto que aparece no badge acima do título",
        required=False
    )
    
    imagem = ImageChooserBlock(
        label="Imagem do Banner",
        help_text="Selecione uma imagem para o lado direito do banner"
    )
    
    botao_principal_texto = blocks.CharBlock(
        default="Ver Próximos Eventos",
        label="Texto do Botão Principal",
        help_text="Texto do botão principal"
    )
    
    botao_principal_link = blocks.CharBlock(
        default="#eventos",
        label="Link do Botão Principal",
        help_text="Link para onde o botão principal levará (URL ou #anchor)"
    )
    
    botao_secundario_texto = blocks.CharBlock(
        default="Saiba Mais",
        label="Texto do Botão Secundário",
        help_text="Texto do botão secundário",
        required=False
    )
    
    botao_secundario_link = blocks.CharBlock(
        default="#sobre",
        label="Link do Botão Secundário",
        help_text="Link para onde o botão secundário levará (URL ou #anchor)",
        required=False
    )
    
    cor_principal = blocks.CharBlock(
        default="#FF7E38",
        label="Cor Principal",
        help_text="Código de cor hexadecimal (ex: #4F46E5) para elementos de destaque"
    )
    
    cor_secundaria = blocks.CharBlock(
        default="#9333EA",
        label="Cor Secundária",
        help_text="Código de cor hexadecimal (ex: #9333EA) para complementar gradientes"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/hero_animada_block.html"
        icon = "view"
        label = "Banner Hero Animado"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['cor_principal'] = value.get('cor_principal', '#4F46E5')
        context['cor_secundaria'] = value.get('cor_secundaria', '#9333EA')
        return context
    



class BannerSearchBlock(blocks.StructBlock):
    """Banner com destaque e campo de busca para bibliotecas"""
    
    # Cores personalizáveis
    cor_primaria = blocks.CharBlock(
        default="#FF7E38",
        label="Cor Primária",
        help_text="Cor principal para textos e elementos (ex: #4a4a4a)"
    )
    
    cor_secundaria = blocks.CharBlock(
        default="#FF8502",
        label="Cor Secundária",
        help_text="Cor de destaque para títulos e botões (ex: #FF8502)"
    )
    
    cor_accent = blocks.CharBlock(
        default="#FFA135",
        label="Cor de Hover",
        help_text="Cor para efeitos de hover (ex: #FFA135)"
    )
    
    # Conteúdo textual
    titulo_principal = blocks.CharBlock(
        default="Descubra a",
        label="Título Principal",
        help_text="Primeira parte do título do banner"
    )
    
    titulo_destaque = blocks.CharBlock(
        default="Biblioteca Graciliano Ramos",
        label="Título em Destaque",
        help_text="Segunda parte do título que aparecerá com destaque"
    )
    
    subtitulo = blocks.TextBlock(
        default="Referência em Administração Pública e Gestão Governamental com mais de 29 mil obras em seu acervo",
        label="Subtítulo",
        help_text="Texto descritivo abaixo do título"
    )

    imagem_background = ImageChooserBlock(
    label="Imagem de Fundo",
    help_text="Imagem que será utilizada como fundo do banner",
    required=False
    )
    
    # Campo de busca
    texto_placeholder = blocks.CharBlock(
        default="O que você procura? Digite palavras-chave...",
        label="Texto do Placeholder",
        help_text="Texto que aparecerá como sugestão no campo de busca"
    )
    
    texto_botao = blocks.CharBlock(
        default="Buscar",
        label="Texto do Botão",
        help_text="Texto que aparecerá no botão de busca"
    )
    
    url_busca = blocks.CharBlock(
        default="/busca/",
        label="URL da Busca",
        help_text="URL para onde o formulário de busca será enviado"
    )
    
    # Badge de informação
    texto_badge = blocks.CharBlock(
        default="Segunda a sexta das 9h às 19h",
        label="Texto do Badge Informativo",
        help_text="Texto que aparecerá como informação adicional",
        required=False
    )
    
    # Imagem principal
    imagem_principal = ImageChooserBlock(
        label="Imagem Principal",
        help_text="Imagem que aparecerá no lado direito do banner"
    )
    
    # Badges flutuantes
    mostrar_badges = blocks.BooleanBlock(
        default=True,
        label="Mostrar Badges Flutuantes",
        help_text="Mostrar os badges de informação flutuantes ao redor da imagem",
        required=False
    )
    
    badge1_icone = blocks.CharBlock(
        default="📚",
        label="Ícone do Badge 1",
        help_text="Emoji ou ícone para o primeiro badge",
        required=False
    )
    
    badge1_texto = blocks.CharBlock(
        default="29 mil obras impressas",
        label="Texto do Badge 1",
        help_text="Texto que aparecerá no primeiro badge",
        required=False
    )
    
    badge2_icone = blocks.CharBlock(
        default="🌐",
        label="Ícone do Badge 2",
        help_text="Emoji ou ícone para o segundo badge",
        required=False
    )
    
    badge2_texto = blocks.CharBlock(
        default="Acervo digital completo",
        label="Texto do Badge 2",
        help_text="Texto que aparecerá no segundo badge",
        required=False
    )
    
    class Meta:
        template = "enap_designsystem/blocks/banner_search_block.html"
        icon = "search"
        label = "Banner com Busca"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['cor_primaria'] = value.get('cor_primaria')
        context['cor_secundaria'] = value.get('cor_secundaria')
        context['cor_accent'] = value.get('cor_accent')
        return context
    




class NavbarComponent(blocks.StructBlock):

    # Logo settings
    logo = ImageChooserBlock(required=False, help_text="Upload your logo image")
    
    # Border
    border_color = blocks.CharBlock(
        required=False, 
        default="#FF7E38",
        help_text="Color code for the 7px bottom border and hover effects (e.g. #3182ce)"
    )
    
    # Button
    portal_text = blocks.CharBlock(
        required=False, 
        default="Portal",
        help_text="Text for the portal button"
    )
    portal_url = blocks.CharBlock(
        required=False, 
        default="#",
        help_text="URL for the portal button"
    )
    
    # Menu items
    menu_items = blocks.ListBlock(
        blocks.StructBlock([
            ('text', blocks.CharBlock(required=False, help_text="Menu item text")),
            ('url', blocks.CharBlock(required=False, help_text="Menu item URL")),
            ('featured', blocks.BooleanBlock(required=False, help_text="Highlight this menu item"))
        ]),
        default=[
            {'text': 'Início', 'url': '#', 'featured': False},
            {'text': 'Acervo', 'url': '#acervo', 'featured': False},
            {'text': 'Áreas Temáticas', 'url': '#areas-tematicas', 'featured': False},
            {'text': 'Bases de Dados', 'url': '#bases-dados', 'featured': False},
            {'text': 'Sobre', 'url': '#sobre', 'featured': False},
            {'text': 'Contato', 'url': '#contato', 'featured': False}
        ]
    )
    
    class Meta:
        template = "enap_designsystem/blocks/navbar_component.html"
        icon = "site"
        label = "Navbar Component"






class SecaoAdesaoBlock(blocks.StructBlock):
    """
    Seção de grade com duas colunas (1fr 1fr) para apresentar informações sobre adesão 
    ao programa com um cartão de destaque verde.
    """
    # Coluna 1 - Conteúdo informativo
    titulo_informativo = blocks.CharBlock(
        required=True,
        max_length=100,
        default="Como aderir ao Enap Aqui?",
        help_text="Título da seção informativa (coluna esquerda)",
        verbose_name="Título"
    )
    
    texto_informativo = blocks.RichTextBlock(
        required=True,
        default=(
            "<p>A adesão ao Programa Enap Aqui é feita por meio da assinatura de "
            "um Acordo de Adesão, formalizado pela instituição interessada.</p>"
            "<p>O Acordo de Adesão ao Enap Aqui expressa o compromisso da instituição "
            "com a promoção de ações formativas voltadas a servidores públicos locais, "
            "por meio de uma abordagem híbrida que integra cursos a distância e oficinas "
            "presenciais, com foco em temas estratégicos para a gestão pública.</p>"
        ),
        help_text="Texto explicativo sobre o processo de adesão",
        verbose_name="Texto informativo"
    )
    
    # Coluna 2 - Cartão verde com call-to-action
    titulo_destaque = blocks.CharBlock(
        required=True,
        max_length=100,
        default="Torne-se um parceiro Enap Aqui",
        help_text="Título do cartão verde de destaque",
        verbose_name="Título do destaque"
    )
    
    texto_destaque = blocks.RichTextBlock(
        required=True,
        default="<p>Faça parte do Enap Aqui e acompanhe o processo:</p>",
        help_text="Texto curto para o cartão verde de destaque",
        verbose_name="Texto do destaque"
    )
    
    texto_botao = blocks.CharBlock(
        required=True,
        max_length=50,
        default="Aderir ao Enap Aqui",
        help_text="Texto que será exibido no botão",
        verbose_name="Texto do botão"
    )
    
    url_botao = blocks.URLBlock(
        required=True,
        default="#",
        help_text="URL para onde o botão vai redirecionar",
        verbose_name="URL do botão"
    )
    
    # Personalização (opcional)
    cor_fundo_destaque = blocks.CharBlock(
        required=False,
        max_length=7,
        default="#1F4D4D",
        help_text="Código hexadecimal da cor de fundo do cartão verde (ex: #1F4D4D)",
        verbose_name="Cor de fundo do destaque"
    )
    
    espaco_vertical = blocks.ChoiceBlock(
        choices=[
            ('pequeno', 'Pequeno'),
            ('medio', 'Médio'),
            ('grande', 'Grande'),
        ],
        default='medio',
        help_text="Espaçamento vertical da seção",
        verbose_name="Espaçamento"
    )
    

    class Meta:
        template = "enap_designsystem/blocks/cartao_destacado.html"
        icon = "placeholder"
        label = "Como Participar"
        verbose_name = "Como Participar"
        help_text = "Como Participar do Programa"
    



class TextoImagemBlock(blocks.StructBlock):
    """
    Componente simples de duas colunas com texto e imagem
    """
    # Coluna de texto
    titulo = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="Título da seção",
        verbose_name="Título"
    )
    
    texto = blocks.RichTextBlock(
        required=True,
        help_text="Conteúdo em texto",
        verbose_name="Texto"
    )
    
    # Coluna de imagem
    imagem = ImageChooserBlock(
        required=True,
        help_text="Imagem de destaque",
        verbose_name="Imagem"
    )
    
    # Opções de layout
    posicao_imagem = blocks.ChoiceBlock(
        choices=[
            ('direita', 'Imagem à direita'),
            ('esquerda', 'Imagem à esquerda'),
        ],
        default='direita',
        help_text="Posição da imagem em relação ao texto",
        verbose_name="Posição da imagem"
    )
    
    estilo_imagem = blocks.ChoiceBlock(
        choices=[
            ('normal', 'Normal'),
            ('arredondada', 'Cantos arredondados'),
            ('circular', 'Circular'),
            ('cobertura', 'Cobertura completa'),
        ],
        default='normal',
        help_text="Estilo de exibição da imagem",
        verbose_name="Estilo da imagem"
    )
    
    # Definições da classe
    class Meta:
        template = "enap_designsystem/blocks/texto_imagem.html"
        icon = "image"
        label = "Texto e Imagem"
        verbose_name = "Bloco de Texto com Imagem"
        help_text = "Bloco de duas colunas com título, texto e imagem"




class CardCursoBlock(BaseBlock):
    """
    A component for displaying course information.
    """
    type = blocks.ChoiceBlock(
        choices=[
            ('card-curso-em-breve', 'Curso em breve'),
            ('card-curso-aberto', 'Curso aberto'),
            ('card-curso-andamento', 'Curso em andamento'),
            ('card-curso-encerrado', 'Curso encerrado'),
        ],
        default='card-curso-em-breve',
        help_text="Escolha o status do curso",
        label="Status do curso"
    )

    title = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_("Título do curso"),
    )
    
    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Descrição"),
    )
    
    carga_horaria = blocks.CharBlock(
        required=True,
        max_length=50,
        label=_("Carga horária"),
    )
    
    modalidade = blocks.ChoiceBlock(
        choices=[
            ('presencial', 'Presencial'),
            ('online', 'Online'),
            ('hibrido', 'Híbrido'),
        ],
        default='presencial',
        label=_("Modalidade"),
    )
    
    highlight_color = blocks.CharBlock(
        required=False,
        max_length=7,
        help_text="Cor de destaque (formato #RRGGBB)",
        label=_("Cor de destaque"),
        default="#c3e92e",
    )
    
    link = blocks.StreamBlock(
        [
            ("button", ButtonBlock()),
        ],
        max_num=1,
        blank=True,
        required=False,
        label=_("Botão (link)"),
    )

    class Meta:
        template = "enap_designsystem/blocks/card_curso_block.html"
        icon = "cr-list-alt"
        label = _("Card Curso (Opção online ou presencial)")




class CarrosselCursosBlock(StructBlock):
    """
    Um wrapper de carrossel que permite adicionar múltiplos cards de curso.
    """
    cards = StreamBlock(
        [
            ("card", CardCursoBlock()),
        ],
        min_num=1,
        label=_("Cards de Curso"),
        help_text=_("Adicione os cards de curso que deseja exibir no carrossel")
    )
    
    slidesPerView_mobile = IntegerBlock(
        default=1,
        min_value=1,
        max_value=2,
        label=_("Cards por visualização (Mobile)"),
        help_text=_("Número de cards visíveis em dispositivos móveis")
    )
    
    slidesPerView_tablet = IntegerBlock(
        default=2,
        min_value=1,
        max_value=3,
        label=_("Cards por visualização (Tablet)"),
        help_text=_("Número de cards visíveis em tablets")
    )
    
    slidesPerView_desktop = IntegerBlock(
        default=3,
        min_value=1,
        max_value=4,
        label=_("Cards por visualização (Desktop)"),
        help_text=_("Número de cards visíveis em desktops")
    )
    
    auto_play = BooleanBlock(
        default=False,
        required=False,
        label=_("Auto-play"),
        help_text=_("Ativar rolagem automática do carrossel")
    )
    
    auto_play_delay = IntegerBlock(
        default=5000,
        min_value=1000,
        help_text=_("Tempo de espera entre slides em milissegundos (1000 = 1 segundo)"),
        label=_("Tempo de auto-play"),
        required=False
    )
    
    class Meta:
        template = "enap_designsystem/blocks/carrossel_cursos_block.html"
        icon = "view"
        label = _("Carrossel de Cursos")


class AccordionItemBlock(StructBlock):
    section_title = CharBlock(
        label="Título da Seção", 
        required=False, 
        help_text="Título principal da seção de accordions (opcional)"
    )
    highlight_color = CharBlock(
        label="Cor de Destaque", 
        required=False, 
        default="#5e17eb", 
        help_text="Cor de destaque no formato hexadecimal (ex: #5e17eb)"
    )
    
    # Lista de itens de acordeão
    accordion_items = ListBlock(
        StructBlock([
            ('accordion_title', CharBlock(
                label="Título do Accordion", 
                required=True, 
                help_text="Título que será mostrado no accordion (pergunta)"
            )),
            ('accordion_response', RichTextBlock(
                label="Resposta do Accordion", 
                required=True, 
                help_text="Conteúdo que será exibido quando o accordion for expandido"
            ))
        ]),
        label="Itens do Accordion",
        min_num=1,
        help_text="Adicione quantas perguntas e respostas desejar"
    )
    
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['highlight_color'] = value.get('highlight_color') or "#5e17eb"
        return context
    
    class Meta:
        template = "enap_designsystem/blocks/accordionsv2.html"
        icon = "list-ul"
        label = "Accordion v2"






class NavbarBlockv3(blocks.StructBlock):
    """Navigation bar component with customizable colors and links."""
    logo_image = ImageChooserBlock(required=True, help_text="Logo image for the navigation bar")
    primary_color = blocks.CharBlock(default="#024248", help_text="Primary color for navigation (hex code)")
    accent_color = blocks.CharBlock(default="#AD6BFC", help_text="Accent color for hover states (hex code)")
    button_color = blocks.CharBlock(default="#024248", help_text="Button color (hex code)")
    button_text_color = blocks.CharBlock(default="#FFFFFF", help_text="Button text color (hex code)")
    
    # Auth buttons configuration
    login_button_text = blocks.CharBlock(required=True, default="Entrar", help_text="Text for the login button")
    login_button_url = blocks.URLBlock(required=True, default="#", help_text="URL for the login button")
    
    cta_button_text = blocks.CharBlock(required=True, default="Acervo", help_text="Text for the call-to-action button")
    cta_button_url = blocks.URLBlock(required=True, default="#", help_text="URL for the call-to-action button")
    
    nav_items = blocks.ListBlock(
        blocks.StructBlock([
            ('link_text', blocks.CharBlock(required=True)),
            ('link_url', blocks.URLBlock(required=True)),
            ('is_active', blocks.BooleanBlock(required=False)),
        ])
    )
    
    class Meta:
        template = 'enap_designsystem/blocks/navbarv3.html'
        icon = 'site'
        label = 'Navbar Flutuante'





class HeroBlockv3(blocks.StructBlock):
    """Hero section with customizable colors, content, and background image."""
    title = blocks.CharBlock(required=True, help_text="Main headline text")
    subtitle = blocks.TextBlock(required=True, help_text="Supporting text below the headline")
    primary_color = blocks.CharBlock(default="#024248", help_text="Primary color (hex code)")
    accent_color = blocks.CharBlock(default="#AD6BFC", help_text="Accent color (hex code)")
    background_color = blocks.CharBlock(default="#E6FFFA", help_text="Background color (hex code)")
    
    primary_button_text = blocks.CharBlock(required=True, default="Escolha sua Área")
    primary_button_url = blocks.URLBlock(required=True, default="#")
    
    secondary_button_text = blocks.CharBlock(required=True, default="Como Funciona")
    secondary_button_url = blocks.URLBlock(required=True, default="#")
    show_play_icon = blocks.BooleanBlock(required=False, default=True)
    
    background_image = ImageChooserBlock(required=True, help_text="Hero section background image")
    show_play_button = blocks.BooleanBlock(required=False, default=True, help_text="Show play button overlay on image")
    
    class Meta:
        template = 'enap_designsystem/blocks/herov3.html'
        icon = 'image'
        label = 'Hero Section'



class AvisoBlock(blocks.StructBlock):
    """
    Bloco de aviso simples sem dependências adicionais
    """
    titulo = blocks.CharBlock(
        required=True,
        label="Título do Aviso",
        help_text="O título principal do aviso",
        max_length=100
    )
    
    data = blocks.DateBlock(
        required=True,
        label="Data do Aviso",
        help_text="Data associada ao aviso"
    )
    
    texto = blocks.RichTextBlock(
        required=True,
        label="Conteúdo do Aviso",
        help_text="O texto principal do aviso",
        features=['bold', 'italic', 'link']
    )
    
    imagem = ImageChooserBlock(
        required=False,
        label="Imagem",
        help_text="Imagem exibida ao lado do aviso"
    )
    
    cor_borda = blocks.CharBlock(
        required=True,
        label="Cor da Borda",
        help_text="Código hexadecimal da cor da borda (ex: #ffb74d)",
        default="#ffb74d",
        max_length=7
    )
    
    tag_texto = blocks.CharBlock(
        required=True,
        label="Texto da Tag",
        help_text="O texto exibido na tag destacada (ex: Importante, Urgente)",
        default="Importante",
        max_length=20
    )
    
    cor_tag = blocks.CharBlock(
        required=True,
        label="Cor da Tag",
        help_text="Código hexadecimal da cor da tag (ex: #ffb74d)",
        default="#ffb74d",
        max_length=7
    )
    
    botao_texto = blocks.CharBlock(
        required=True,
        label="Texto do Botão",
        help_text="O texto a ser exibido no botão",
        default="Saiba mais",
        max_length=30
    )
    
    botao_link = blocks.URLBlock(
        required=True,
        label="Link do Botão",
        help_text="URL para onde o botão direciona"
    )
    
    cor_botao = blocks.CharBlock(
        required=True,
        label="Cor do Botão",
        help_text="Código hexadecimal da cor do botão (ex: #F58A5F)",
        default="#F58A5F",
        max_length=7
    )
    
    class Meta:
        template = "enap_designsystem/blocks/aviso_block.html"
        icon = "warning"
        label = "Aviso"
        form_classname = "aviso-block struct-block"




class GalleryModernBlock(blocks.StructBlock):
    """Bloco para exibir uma galeria moderna com carrossel e filtros por categoria"""
    
    titulo_secao = blocks.CharBlock(
        default="Galeria de Eventos",
        label="Título da Seção",
        help_text="Título que aparecerá no topo da seção de galeria"
    )
    
    subtitulo_secao = blocks.CharBlock(
        default="Biblioteca do Futuro",
        label="Subtítulo da Seção",
        help_text="Texto que aparecerá abaixo do título da seção"
    )
    
    cor_principal = blocks.CharBlock(
        default="#0f172a",
        label="Cor Principal",
        help_text="Código de cor hexadecimal (ex: #0f172a) para os elementos principais"
    )
    
    cor_secundaria = blocks.CharBlock(
        default="#0284c7",
        label="Cor de Destaque",
        help_text="Código de cor hexadecimal (ex: #0284c7) para elementos de destaque"
    )
    
    categorias = blocks.ListBlock(
        blocks.StructBlock([
            ('nome', blocks.CharBlock(label="Nome da Categoria")),
        ]),
        label="Categorias da Galeria",
        help_text="Defina as categorias que serão usadas para filtrar os itens da galeria"
    )
    
    itens_galeria = blocks.ListBlock(
        blocks.StructBlock([
            ('titulo', blocks.CharBlock(label="Título do Item")),
            ('categoria', blocks.CharBlock(
                label="Categoria",
                help_text="Deve corresponder exatamente ao nome de uma categoria definida acima"
            )),
            ('imagem', ImageChooserBlock(label="Imagem")),
            ('descricao', blocks.TextBlock(
                label="Descrição", 
                required=False,
                help_text="Texto descritivo que aparecerá no lightbox"
            )),
        ]),
        label="Itens da Galeria",
        help_text="Adicione os itens que serão exibidos na galeria"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/gallery_modern.html"
        icon = "image"
        label = "Galeria Moderna com Filtro"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        
        # Gerar slugs automaticamente para as categorias que não possuem
        categorias = []
        for categoria in value['categorias']:
            cat = dict(categoria)
            if not cat.get('slug'):
                cat['slug'] = slugify(cat.get('nome', ''))
            categorias.append(cat)
        
        # Como não temos mais o campo data, vamos usar os itens na ordem em que foram adicionados
        itens_ordenados = value['itens_galeria']
        
        # Organizando itens por categoria
        itens_por_categoria = {}
        for item in itens_ordenados:
            categoria = item['categoria']
            if categoria not in itens_por_categoria:
                itens_por_categoria[categoria] = []
                
            # Adicionar o item à categoria correspondente
            itens_por_categoria[categoria].append(dict(item))
            
        context['categorias'] = categorias
        context['itens_ordenados'] = itens_ordenados
        context['itens_por_categoria'] = itens_por_categoria
        context['cor_principal'] = value.get('cor_principal', '#0f172a')
        context['cor_secundaria'] = value.get('cor_secundaria', '#0284c7')
        
        return context





class TeamModern(blocks.StructBlock):
    """Bloco para exibir um time de pessoas com carrossel."""
    title = blocks.CharBlock(label="Título", max_length=200, default="Temos uma rica experiência de diversos backgrounds")
    subtitle = blocks.TextBlock(
        label="Subtítulo", 
        default="Nossa filosofia é simples: reunir pessoas talentosas e oferecer a elas os recursos e suporte para fazer seu melhor trabalho."
    )
    
    # Definindo os membros da equipe diretamente na mesma classe, sem classe separada
    team_members = blocks.ListBlock(
        blocks.StructBlock([
            ('photo', ImageChooserBlock(label="Foto")),
            ('name', blocks.CharBlock(label="Nome", max_length=100)),
            ('role', blocks.CharBlock(label="Cargo", max_length=150)),
        ], icon="user", label="Membro da Equipe"),
        label="Membros da Equipe",
        min_num=1
    )

    class Meta:
        template = "enap_designsystem/blocks/team_modern.html"
        icon = "group"
        label = "Bloco de Time Moderno"





class CTA2Block(StructBlock):
    """Bloco StreamField para a seção Hero."""
    
    hero_badge = CharBlock(
        required=True,
        default="Gnova: Leitura ao ar livre",
        help_text="Texto do badge no topo da seção hero"
    )
    
    hero_title = CharBlock(
        required=True,
        default="Espaço para promover a rotatividade de livros e leitura ao ar livre.",
        help_text="Título principal da seção hero"
    )
    
    hero_description = RichTextBlock(
        required=True,
        features=['bold', 'italic', 'link'],
        default="<p>Um jardim interativo onde os livros podem ser trocados, lidos e apreciados em um ambiente natural.</p><p>Área para workshops, contação de histórias e eventos culturais.</p>",
        help_text="Descrição da seção hero (aceita formatação básica)"
    )
    
    hero_image = ImageChooserBlock(
        required=True,
        help_text="Imagem da seção hero (ideal: 1200x800px)"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/cta2.html"
        icon = "view"
        label = "CTA: text e 1 imagem"





class JobVacancyPage(Page):
    """Página individual para vaga de emprego."""
    
    STATUS_CHOICES = [
        ('aberta', _('Aberta')),
        ('em_andamento', _('Em Andamento')),
        ('encerrada', _('Encerrada')),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberta',
        verbose_name=_('Status da Vaga')
    )
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Imagem')
    )
    
    description = RichTextField(
        verbose_name=_('Descrição curta'),
        help_text=_('Texto breve que aparecerá no card')
    )

    link_text = models.CharField(
        max_length=100,
        verbose_name=_('Texto do botão'),
        default='Ver detalhes',
        blank=True
    )
    
    process_code = models.CharField(
        max_length=100,
        verbose_name=_('Código do Processo'),
        blank=True
    )
    
    registration_start = models.DateField(
        verbose_name=_('Início das Inscrições')
    )
    
    registration_end = models.DateField(
        verbose_name=_('Fim das Inscrições')
    )
    
    inscription_link = models.URLField(
        verbose_name=_('Link para Inscrição'),
        blank=True
    )
    
    full_description = RichTextField(
        verbose_name=_('Descrição completa da Vaga')
    )
    
    download_files = RichTextField(
        verbose_name=_('Arquivos para Download'),
        blank=True
    )

    navbar = models.ForeignKey(
		"EnapNavbarSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

    footer = models.ForeignKey(
		"EnapFooterSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

    card_type = models.CharField(
    choices=[
        ('card-primary', _('Card Primário')),
        ('card-secondary', _('Card Secundário')),
        ('card-terciary', _('Card Terciário')),
        ('card-horizontal', _('Card Horizontal')),
        ('card-bgimage', _('Card com Imagem de Fundo')),
    ],
    default='card-primary',
    max_length=50,
    verbose_name=_('Tipo de Card')
)
    
    
    content_panels = Page.content_panels + [
        FieldPanel('card_type'),
        FieldPanel("navbar"),
        FieldPanel('status'),
        FieldPanel('image'),
        FieldPanel('description'),
        FieldPanel('link_text'),
        MultiFieldPanel([
            FieldPanel('process_code'),
            FieldPanel('registration_start'),
            FieldPanel('registration_end'),
            FieldPanel('inscription_link'),
        ], heading=_('Informações de Inscrição')),
        FieldPanel('full_description'),
        FieldPanel('download_files'),
        FieldPanel("footer"),
    ]
    
    parent_page_types = ['JobVacancyIndexPage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['registration_period'] = f"{self.registration_start.strftime('%d/%m/%Y')} - {self.registration_end.strftime('%d/%m/%Y')}"
        
        # Adiciona informações para compartilhamento
        context['share_url'] = request.build_absolute_uri(self.url)
        
        return context
    
    def get_template(self, request, *args, **kwargs):
        return "enap_designsystem/blocks/job_vacancy_page.html"
    
    @property
    def get_status_label(self):
        """Retorna o label legível do status."""
        status_map = {
            'aberta': _('Vaga Aberta'),
            'em_andamento': _('Em Andamento'),
            'encerrada': _('Vaga Encerrada'),
        }
        return status_map.get(self.status)
    
    @property
    def get_status_color(self):
        """Retorna a classe CSS para cor do status."""
        status_colors = {
            'aberta': 'status-open',
            'em_andamento': 'status-in-progress',
            'encerrada': 'status-closed',
        }
        return status_colors.get(self.status, '')
    
    class Meta:
        verbose_name = _('Vaga de Emprego')
        verbose_name_plural = _('Vagas de Emprego')




class JobVacancyIndexPage(Page):
    """Página índice que lista todas as vagas."""
    
    intro = RichTextField(
        blank=True,
        verbose_name=_('Introdução')
    )

    card_type = models.CharField(
        choices=[
            ('card-primary', _('Card Primário')),
            ('card-secondary', _('Card Secundário')),
            ('card-terciary', _('Card Terciário')),
            ('card-horizontal', _('Card Horizontal')),
            ('card-bgimage', _('Card com Imagem de Fundo')),
        ],
        default='card-primary',
        max_length=50,
        verbose_name=_('Tipo de Card')
    )

    navbar = models.ForeignKey(
		"EnapNavbarSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

    footer = models.ForeignKey(
		"EnapFooterSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)
    
    content_panels = Page.content_panels + [
        FieldPanel("navbar"),
        FieldPanel('intro'),
        FieldPanel('card_type'),
        FieldPanel("footer"),
    ]
    
    subpage_types = ['JobVacancyPage']
    
    def get_index_children(self):
        """Retorna as páginas filhas ordenadas por data de início das inscrições."""
        return self.get_children().specific().live().order_by('-jobvacancypage__registration_start')
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Obter todas as vagas filhas desta página índice
        job_vacancies = JobVacancyPage.objects.live().descendant_of(self)
        
        # Separar por status
        context['open_jobs'] = job_vacancies.filter(status='aberta').order_by('-registration_start')
        context['in_progress_jobs'] = job_vacancies.filter(status='em_andamento').order_by('-registration_start')
        context['closed_jobs'] = job_vacancies.filter(status='encerrada').order_by('-registration_start')
        
        return context
    
    def get_template(self, request, *args, **kwargs):
        return "enap_designsystem/blocks/job_vacancy_index_page.html"
    
    class Meta:
        verbose_name = ('Página Índice de Vagas')





class JobVacanciesBlock(blocks.StructBlock):
    """
    Exibe cards de vagas de emprego separados por status.
    """
    
    indexed_by = blocks.PageChooserBlock(
        required=True,
        page_type='vagas.JobVacancyIndexPage',  # Ajuste conforme seu app
        label=_("Página índice"),
        help_text=_("Selecione a página índice que contém as vagas a serem exibidas.")
    )
    
    num_posts = blocks.IntegerBlock(
        default=6,
        label=_("Número de vagas a exibir por categoria"),
    )
    
    show_open = blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Mostrar vagas abertas"),
    )
    
    show_in_progress = blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Mostrar vagas em andamento"),
    )
    
    show_closed = blocks.BooleanBlock(
        default=False,
        required=False,
        label=_("Mostrar vagas encerradas"),
    )
    
    class Meta:
        template = "enap_designsystem/blocks/job_vacancies_block.html"
        icon = "clipboard-list"
        label = _("Vagas de Emprego")
    
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        
        indexer = value["indexed_by"].specific
        all_vacancies = indexer.get_children().live().specific()
        
        # Filtrar por status e limitar pelo número especificado
        open_jobs = []
        in_progress_jobs = []
        closed_jobs = []
        
        
        if value["show_open"]:
            open_jobs = [page for page in all_vacancies if hasattr(page, 'status') and page.status == 'aberta'][:value["num_posts"]]
            
        if value["show_in_progress"]:
            in_progress_jobs = [page for page in all_vacancies if hasattr(page, 'status') and page.status == 'em_andamento'][:value["num_posts"]]
            
        if value["show_closed"]:
            closed_jobs = [page for page in all_vacancies if hasattr(page, 'status') and page.status == 'encerrada'][:value["num_posts"]]
        
        context["open_jobs"] = open_jobs
        context["in_progress_jobs"] = in_progress_jobs
        context["closed_jobs"] = closed_jobs
        context["block"] = block_type
        
        return context
    



class CitizenServerBlock(blocks.StructBlock):
    """
    A custom block for 'Olhar cidadão, servidor atuante, Estado capaz' component
    with title, description, small text and alignment options.
    """
    title = blocks.CharBlock(required=True, help_text="Titulo (e.g. 'Olhar cidadão, servidor atuante, Estado capaz')")
    description = blocks.RichTextBlock(required=True, help_text="Descrição (e.g. 'A Enap é uma escola pública federal vinculada ao Ministério da Gestão e da Inovação em Serviços Públicos (MGI)')")
    small_text = blocks.CharBlock(required=False, help_text="Tag (e.g. 'Servir')")
    
    style_choice = blocks.ChoiceBlock(
        choices=[
            ('center', 'Texto Centralizado'),
            ('bottom', 'Texto Inferior'),
            ('overlay', 'Texto com Linha'),
        ],
        default='center',
        help_text="Choose the text display style"
    )
    
    background_media = blocks.StreamBlock([
        ('image', ImageChooserBlock(help_text="Imagem de fundo")),
        ('video', DocumentChooserBlock(help_text="Vídeo de fundo")),
    ], max_num=1, required=False, help_text="Escolha uma imagem ou vídeo de fundo")
    
    class Meta:
        template = "enap_designsystem/blocks/citizen_server_block.html"
        icon = "doc-full"
        label = "Banner Temático"






class ServiceCardsBlock(blocks.StructBlock):
    """
    A grid of service cards that can be added to a StreamField
    """
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True, help_text="Card image")),
            ('title', blocks.CharBlock(required=True, help_text="Card title")),
            ('description', blocks.RichTextBlock(required=True, help_text="Card description")),
            ('link', blocks.URLBlock(required=False, help_text="Optional link for the card")),
        ]),
        min_num=1,
        help_text="Add as many cards as you want"
    )

    class Meta:
        template = "enap_designsystem/blocks/service_cards.html"
        icon = "grip"
        label = "Cards Horizontais"






class FeatureListBlock(blocks.StructBlock):
    """
    A block with a featured item on the left and a list of related items on the right
    """
    # Featured item (left side)
    featured_image = ImageChooserBlock(required=True, help_text="Main featured image")
    featured_title = blocks.CharBlock(required=True, help_text="Featured item title")
    featured_description = blocks.RichTextBlock(required=True, help_text="Featured item description")
    featured_link_url = blocks.URLBlock(label="URL do link", required=True, help_text="Link for the featured item")
    
    
    # List items (right side)
    list_items = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True, help_text="Item image")),
            ('title', blocks.CharBlock(required=True, help_text="Item title")),
            ('description', blocks.RichTextBlock(required=True, help_text="Item description")),
            ('link_url', blocks.URLBlock(label="URL do link")),
        ]),
        min_num=1,
        help_text="Add items to be displayed on the right side"
    )

    class Meta:
        template = "enap_designsystem/blocks/feature_list_block.html"
        icon = "table"
        label = "Card Destaque com Cards Complementares"






class CarouselGreen(blocks.StructBlock):
    """Bloco de carrossel com título, tag e itens."""
    
    # Cabeçalho do carrossel
    tag = blocks.CharBlock(label="Tag", max_length=50, default="Ethos Público")
    title = blocks.CharBlock(label="Título", max_length=100, default="Acervo para Servidores")
    subtitle = blocks.CharBlock(label="Subtítulo", max_length=200, default="Comprometidos com a Transformação", required=False)
    
    # Estrutura para os itens do carrossel
    items = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(label="Imagem")),
            ('title', blocks.CharBlock(label="Título", max_length=100)),
            ('description', blocks.TextBlock(label="Descrição")),
            ('link_text', blocks.CharBlock(label="Texto do link", max_length=50, default="Acesse o curso")),
            ('link_url', blocks.URLBlock(label="URL do link")),
        ]),
        label="Itens do Carrossel",
        min_num=1
    )
    
    class Meta:
        template = "enap_designsystem/blocks/carousel_bggreen.html"
        icon = "view"
        label = "Carrossel de Cards com fundo verde"
        
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['title'] = value.get('title', '')
        context['subtitle'] = value.get('subtitle', '')
        context['items'] = value.get('items', [])
        
        # Para debug
        print(f"CarouselGreen - Contexto: {context}")
        print(f"CarouselGreen - Items: {len(value.get('items', []))}")
        
        return context
    



class TopicLinksBlock(blocks.StructBlock):
    """
    Bloco para exibir tópicos com links "Veja mais"
    """
    
    topic1_title = blocks.CharBlock(
        required=True,
        max_length=100,
        label=_("Título do tópico 1"),
        default="Ethos Público: Compromisso de servir"
    )
    topic1_link = blocks.URLBlock(
        required=True,
        label=_("Link do tópico 1"),
        help_text=_("URL para 'Veja mais' do tópico 1")
    )
    
    topic2_title = blocks.CharBlock(
        required=True,
        max_length=100,
        label=_("Título do tópico 2"),
        default="Cidadania ativa"
    )
    topic2_link = blocks.URLBlock(
        required=True,
        label=_("Link do tópico 2"),
        help_text=_("URL para 'Veja mais' do tópico 2")
    )
    
    topic3_title = blocks.CharBlock(
        required=True,
        max_length=100,
        label=_("Título do tópico 3"),
        default="Estado e Desenvolvimento"
    )
    topic3_link = blocks.URLBlock(
        required=True,
        label=_("Link do tópico 3"),
        help_text=_("URL para 'Veja mais' do tópico 3")
    )
    
    class Meta:
        template = "enap_designsystem/blocks/topic_links_block.html"
        icon = "list-ul"
        label = _("Tópicos para Links")




class Banner_Image_cta(blocks.StructBlock):
    """
    Bloco de banner hero com imagem, texto e botão de vídeo
    """
    tag = blocks.CharBlock(
        required=False,
        max_length=50,
        label=_("Tag"),
        default="Ethos Público"
    )
    
    title = blocks.CharBlock(
        required=True,
        max_length=200,
        label=_("Título"),
        default="Servir: a essência do serviço público"
    )
    
    description = blocks.TextBlock(
        required=True,
        label=_("Descrição"),
        default="A ideia do \"Propósito do Servir\" destaca que trabalhar no serviço público vai além de cumprir uma função; é um compromisso verdadeiro com a sociedade."
    )
    
    background_image = ImageChooserBlock(
        required=False,
        label=_("Imagem de fundo (opcional)"),
        help_text=_("Se não fornecida, será usado fundo verde padrão")
    )
    
    hero_image = ImageChooserBlock(
        required=True,
        label=_("Imagem principal")
    )

    video_text = blocks.CharBlock(
        required=False,
        max_length=50,
        label=_("Texto do botão de vídeo"),
        default="VEJA O VÍDEO"
    )
    
    video_url = blocks.URLBlock(
        required=False,
        label=_("URL do vídeo"),
        help_text=_("Link para o vídeo (YouTube, Vimeo, etc)")
    )
    
    class Meta:
        template = "enap_designsystem/blocks/banner_image_cta.html"
        icon = "image"
        label = _("Banner Hero com Imagem e Botão de Vídeo")





class FeatureWithLinksBlock(blocks.StructBlock):
    """
    A block with a featured image on the left and a grid of link cards on the right
    """
    # Featured item (left side)
    featured_image = ImageChooserBlock(required=True, help_text="Main featured image")
    featured_title = blocks.CharBlock(required=True, help_text="Featured title")
    featured_description = blocks.CharBlock(required=False, help_text="Featured description (optional)")
    
    # List items (right/bottom side) - Ajustado para garantir que funcione
    list_items = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True, help_text="Item thumbnail")),
            ('title', blocks.CharBlock(required=True, help_text="Item title")),
            ('description', blocks.RichTextBlock(required=True, help_text="Item description")),
            ('link', blocks.URLBlock(required=False, help_text="Link URL (entire card will be clickable)")),
        ]),
        min_num=1,
        max_num=10,  # Limite opcional
        default=[{'title': 'Exemplo de item', 'description': '<p>Descrição do item</p>'}],  # Valor padrão
        help_text="Add as many items as you want in the grid"
    )

    class Meta:
        template = "enap_designsystem/blocks/feature_with_links_block.html"
        icon = "link"
        label = "Card Destaque - cards com links ao lado"





class QuoteBlockModern(blocks.StructBlock):
    """
    Um bloco personalizado para citações com foto no Wagtail.
    """
    person_image = ImageChooserBlock(
        label="Foto da Pessoa",
        help_text="Adicione uma foto da pessoa sendo citada. Recomendação: imagem no formato retrato com pelo menos 500x700px."
    )
    
    quote_text = blocks.TextBlock(
        label="Texto da Citação",
        help_text="O texto da citação. Não é necessário adicionar aspas, elas serão adicionadas automaticamente."
    )
    
    author_name = blocks.CharBlock(
        label="Nome do Autor",
        max_length=100,
        help_text="Nome da pessoa sendo citada."
    )
    
    author_title = blocks.CharBlock(
        label="Título/Cargo do Autor",
        max_length=150,
        required=False,
        help_text="Cargo, profissão ou título da pessoa (opcional)."
    )
    
    color_theme = blocks.ChoiceBlock(
        choices=[
            ('default', 'Padrão (Branco)'),
            ('blue', 'Azul'),
            ('green', 'Verde'),
        ],
        default='default',
        label="Tema de Cor",
        help_text="Escolha um tema de cor para a citação."
    )

    class Meta:
        template = "enap_designsystem/blocks/quote_modern.html"
        icon = "openquote"
        label = "Citação com Foto"
        help_text = "Citação elegante com foto do autor."