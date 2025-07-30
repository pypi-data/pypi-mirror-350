
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtail.admin.panels import FieldPanel
from django.db import models


from .base_blocks import BaseBlock
from .html_blocks import ButtonBlock



class EnapNavbarBlock(blocks.StructBlock):
	"""
	Bloco para permitir a seleção de um snippet de Navbar.
	"""

	navbar = SnippetChooserBlock("enap_designsystem.EnapNavbarSnippet")

	class Meta:
		template = "enap_designsystem/blocks/navbar/navbar_block.html"
		icon = "menu"
		label = "Navbar ENAP"


class EnapAccordionBlock(BaseBlock):
    """
    Allows selecting an accordion snippet
    """

    accordion = SnippetChooserBlock("enap_designsystem.EnapAccordionSnippet")
    
    def get_searchable_content(self, value):
        content = []

        snippet = value.get("accordion")
        if snippet:
            for block in snippet.panels_content:
                if block.block_type == "accordion_item":
                    item = block.value
                    content.append(item.get("title", ""))
                    content.append(item.get("content", "").source if hasattr(item.get("content", ""), "source") else "")
        return content
    
    class Meta:
        template = "enap_designsystem/blocks/accordions.html"
        icon = "bars"
        label = _("Accordion ENAP")


class EnapFooterLinkBlock(BaseBlock):
    """
    Um componente com texto e link para footer
    """

    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Nome amigável"),
    )
    link = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Link"),
    )
    class Meta:
        template = "enap_designsystem/blocks/footer_link_block.html"
        icon = "cr-list-alt"
        label = _("Footer link")


class EnapFooterSocialBlock(BaseBlock):
	"""
	Um componente individual de rede social no footer.
	"""

	social_network = blocks.ChoiceBlock(
		choices=[
			("facebook", "Facebook"),
			("instagram", "Instagram"),
			("whatsapp", "WhatsApp"),
			("twitter", "Twitter"),
			("linkedin", "LinkedIn"),
			("youtube", "YouTube"),
		],
		label=_("Rede Social"),
		required=True,
		help_text="Escolha a rede social."
	)

	url = blocks.URLBlock(
		required=True,
		label=_("Link da Rede Social"),
		help_text="Insira o link para o perfil ou página."
	)
	class Meta:
		template = "enap_designsystem/blocks/footer/footer_social_block.html"
		icon = "site"
		label = _("Rede Social")


class CardBlock(BaseBlock):
    """
    A component of information with image, text, and buttons.
    """

    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_("Image"),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )
    subtitle = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Subtitle"),
    )
    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Body"),
    )
    links = blocks.StreamBlock(
        [("Links", ButtonBlock())],
        blank=True,
        required=False,
        label=_("Links"),
    )

    class Meta:
        template = "coderedcms/blocks/card_foot.html"
        icon = "cr-list-alt"
        label = _("Card")


class EnapCardBlock(BaseBlock):
    """
    A component of information with image, text, and buttons.
    
    """

    type = blocks.ChoiceBlock(
		choices=[
			('card-primary', 'Tipo primário'),
			('card-secondary', 'Tipo secundário'),
			('card-terciary', 'Tipo terciário'),
			('card-bgimage', 'Tipo BG Image'),
            ('card-horizontal', 'Tipo Horizontal'),
            
		],
		default='card-primary',
		help_text="Escolha o tipo/cor do card",
		label="Tipo de card"
	)

    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_("Image"),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )
    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Body"),
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
        template = "enap_designsystem/blocks/card_block.html"
        icon = "cr-list-alt"
        label = _("Enap Card")


class EnapBannerBlock(blocks.StructBlock):
    """
    Bloco para o Hero Banner com imagem de fundo, título e descrição.
    """
    background_image = ImageChooserBlock(
        required=False, 
        label=_("Background Image"),
    )
    title = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_("Title"),
        default="Título do Banner",
    )
    description = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Description"),
        default="Descrição do banner. Edite este texto para personalizar o conteúdo.",

    )

    def get_searchable_content(self, value):
        return [
            value.get("title", ""),
            value.get("description", "").source if hasattr(value.get("description", ""), "source") else ""
        ]
    
    class Meta:
        template = "enap_designsystem/blocks/banner.html"
        icon = "image"
        label = _("Hero Banner")
        initialized = True



class EnapBannerVideoBlock(blocks.StructBlock):
    """
    Bloco para o Hero Banner com imagem de fundo, título e descrição.
    """
    video_background = models.FileField(
        upload_to='media/imagens', 
        null=True, 
        blank=True, 
        verbose_name="Vídeo de Fundo"
    )
    title = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_("Title"),
    )
    description = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Description"),
    )

    class Meta:
        template = "enap_designsystem/blocks/banner-video.html"
        icon = "image"
        label = _("Video Banner")



class FeatureImageTextBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.RichTextBlock(required=True)

    def get_searchable_content(self, value):
        return [
            value.get("title", ""),
            value.get("description", "").source if hasattr(value.get("description", ""), "source") else ""
        ]
    
    class Meta:
        template = "enap_designsystem/blocks/feature-img-texts.html"
        label = _("Feature Imagem e Texto")


class EnapAccordionPanelBlock(blocks.StructBlock):
	"""
	Bloco individual de uma seção de accordion dentro do snippet.
	"""

	title = blocks.CharBlock(
		required=True,
		max_length=255,
		label="Pergunta / Titulo"
	)

	content = blocks.RichTextBlock(
		required=True,
		label="Resposta",
		features=["bold", "italic", "link"]
	)

	class Meta:
		icon = "list-ul"
		label = "Item do Accordion"


class EnapNavbarLinkBlock(blocks.StructBlock):
	"""
	Bloco para representar um link na Navbar.
	"""

	label = blocks.CharBlock(required=True, max_length=255, label="Texto do Link")
	url = blocks.URLBlock(required=True, label="URL do Link")
	style = blocks.ChoiceBlock(
		choices=[
			("default", "Padrão"),
			("button", "Botão"),
			("icon", "Ícone"),
		],
		default="default",
		label="Estilo do Link"
	)

	class Meta:
		icon = "link"
		label = "Link da Navbar"
