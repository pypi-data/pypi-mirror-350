from django.db import models
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail import blocks
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from coderedcms.models import CoderedWebPage
from modelcluster.models import ClusterableModel
from wagtail.blocks import URLBlock
from wagtail.search import index
import requests

from .blocks.layout_blocks import EnapAccordionBlock

from wagtail.blocks import StreamBlock, StructBlock, CharBlock, ChoiceBlock, RichTextBlock, ChooserBlock, ListBlock

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, InlinePanel
from wagtail.documents.models import Document
from wagtail.fields import StreamField
from .blocks import ButtonBlock
from .blocks import ImageBlock
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable

from wagtail.images.models import Image
from django.dispatch import receiver
from wagtail.images import get_image_model_string
from enap_designsystem.blocks import EnapFooterGridBlock
from enap_designsystem.blocks import EnapFooterSocialGridBlock 
from enap_designsystem.blocks import EnapAccordionPanelBlock
from enap_designsystem.blocks import EnapNavbarLinkBlock
from enap_designsystem.blocks import EnapCardBlock
from enap_designsystem.blocks import EnapCardGridBlock
from enap_designsystem.blocks import EnapSectionBlock



from enap_designsystem.blocks import PageListBlock
from enap_designsystem.blocks import NewsCarouselBlock
from enap_designsystem.blocks import DropdownBlock
from enap_designsystem.blocks import CoursesCarouselBlock
from enap_designsystem.blocks import SuapCourseBlock
from enap_designsystem.blocks import PreviewCoursesBlock
from enap_designsystem.blocks import EventsCarouselBlock
from enap_designsystem.blocks import EnapBannerBlock
from enap_designsystem.blocks import FeatureImageTextBlock
from enap_designsystem.blocks import EnapAccordionBlock
from enap_designsystem.blocks.base_blocks import ButtonGroupBlock
from enap_designsystem.blocks.base_blocks import CarouselBlock
from enap_designsystem.blocks import CourseIntroTopicsBlock
from .blocks import WhyChooseEnaptBlock
from .blocks import CourseFeatureBlock
from .blocks import CourseModulesBlock
from .blocks import ProcessoSeletivoBlock
from .blocks import TeamCarouselBlock  
from .blocks import TestimonialsCarouselBlock
from .blocks import CarouselGreen
from .blocks import TeamModern
from .blocks import HeroBlockv3
from .blocks import TopicLinksBlock
from .blocks import AvisoBlock
from .blocks import FeatureListBlock
from .blocks import ServiceCardsBlock
from .blocks import CitizenServerBlock
from .blocks import CarrosselCursosBlock
from .blocks import Banner_Image_cta
from .blocks import FeatureWithLinksBlock
from .blocks import QuoteBlockModern
from .blocks import CardCursoBlock


from wagtail.snippets.blocks import SnippetChooserBlock

from enap_designsystem.blocks import LAYOUT_STREAMBLOCKS
from enap_designsystem.blocks import DYNAMIC_CARD_STREAMBLOCKS
from enap_designsystem.blocks import CARD_CARDS_STREAMBLOCKS

# class ComponentLayout(models.Model):
#     name = models.CharField(max_length=255)
#     content = models.TextField()

#     panels = [
#         FieldPanel("name"),
#         FieldPanel("content"),
#     ]

#     class Meta:
#         abstract = True



class ENAPComponentes(Page):
	"""Página personalizada independente do CoderedWebPage."""
	
	admin_notes = models.TextField(
		verbose_name="Anotações Internas",
		blank=True,
		help_text="Escreva observações importantes. Este campo é visível apenas para administradores."
	)

	template = "enap_designsystem/pages/enap_layout.html"

	body = StreamField(
		LAYOUT_STREAMBLOCKS,
		null=True,
		blank=True,
		use_json_field=True,
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
		FieldPanel("body"),
		FieldPanel("footer"),
		FieldPanel("admin_notes"),
	]

	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""
	
	search_fields = Page.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("body"),
		index.FilterField("url", name="url_filter"),
	]
	
	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []
			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):
				result.append(block_value.source)
			return result

		if self.body:
			for block in self.body:
				content.extend(extract_text_from_block(block.value))

		return content

	class Meta:
		verbose_name = "ENAP Componentes"
		verbose_name_plural = "ENAP Componentes"


class ENAPFormacao(CoderedWebPage):
	"""Página personalizada herdando todas as características de CoderedWebPage."""
	
	admin_notes = models.TextField(
		verbose_name="Anotações Internas",
		blank=True,
		help_text="Escreva observações importantes."
	)

	template = "enap_designsystem/pages/template_cursos.html"
	miniview_template = "coderedcms/pages/article_page.mini.html"
	search_template = "coderedcms/pages/article_page.search.html"

	content = StreamField(
		[
			("banner", EnapBannerBlock()), 
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	feature = StreamField(
		[
			("enap_herofeature", FeatureImageTextBlock()),
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	accordion_cursos = StreamField(
		[
			("enap_accordion", EnapAccordionBlock()),
			('button_group', ButtonGroupBlock()),
			('carousel', CarouselBlock()),
			('dropdown', DropdownBlock()),
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	body = StreamField(
		CARD_CARDS_STREAMBLOCKS,
		null=True,
		blank=True,
		use_json_field=True,
	)

	modal = models.ForeignKey(
		"enap_designsystem.Modal",  # Use o caminho completo para o modelo Modal
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
		verbose_name="Modal"
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

	modalenap = models.ForeignKey(
		"enap_designsystem.ModalBlock",  # Use o caminho completo incluindo o app
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	alert = models.ForeignKey(
		"Alert",  
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	wizard = models.ForeignKey(
		"Wizard",  
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	FormularioContato = models.ForeignKey(
		"FormularioContato",  
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	tab = models.ForeignKey(
		"Tab",  
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = CoderedWebPage.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("content"),
		index.SearchField("feature"),
		index.SearchField("accordion_cursos"),
		index.SearchField("body"),
		index.FilterField("url", name="url_filter")
	]

	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []
			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):
				result.append(block_value.source)
			return result

		streamfields = [
			self.content,
			self.feature,
			self.accordion_cursos,
			self.body,
		]

		for sf in streamfields:
			if sf:
				for block in sf:
					content.extend(extract_text_from_block(block.value))

		return content

	# Painéis no admin do Wagtail
	content_panels = CoderedWebPage.content_panels + [
		FieldPanel('navbar'),
		FieldPanel('modal'), 
		FieldPanel('modalenap'), 
		FieldPanel('wizard'),
		FieldPanel('alert'),
		FieldPanel('FormularioContato'),
		FieldPanel('tab'),
		FieldPanel('footer'),
		FieldPanel('content'),
		FieldPanel('feature'),
		FieldPanel('accordion_cursos'),
	]

	class Meta:
		verbose_name = "Template ENAP Curso"
		verbose_name_plural = "Template ENAP Cursos"

class ENAPTemplatev1(CoderedWebPage):
	"""Página personalizada herdando todas as características de CoderedWebPage."""
	
	admin_notes = models.TextField(
		verbose_name="Anotações Internas",
		blank=True,
		help_text="Escreva observações importantes."
	)

	template = "enap_designsystem/pages/template_homeI.html"
	miniview_template = "coderedcms/pages/article_page.mini.html"
	search_template = "coderedcms/pages/article_page.search.html"

	page_title = models.CharField(
		max_length=255, 
		default="Título Padrão", 
		verbose_name="Título da Página"
	)


	body = StreamField(
		DYNAMIC_CARD_STREAMBLOCKS,
		null=True,
		blank=True,
		use_json_field=True,
	)


	teste_courses = StreamField(
		[("courses_carousel", CoursesCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	suap_courses = StreamField(
		[("suap_courses", SuapCourseBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)

	noticias = StreamField(
		[("eventos_carousel", EventsCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	teste_noticia = StreamField(
		[("noticias_carousel", NewsCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	teste_preview = StreamField(
		[("page_preview_teste", PageListBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)

	dropdown_content = StreamField(
		[("dropdown", DropdownBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)
	
	paragrafo = RichTextField(
		blank=True, 
		help_text="Adicione o texto do parágrafo aqui.", 
		verbose_name="Parágrafo sessao dinamica"
	)
	
	video_background = models.FileField(
		upload_to='media/videos', 
		null=True, 
		blank=True, 
		verbose_name="Vídeo de Fundo"
	)

	background_image = StreamField(
		[
			("image", ImageBlock()),
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	linkcta = RichTextField(blank=True)
	button_link = models.URLField(
		"Link do Botão",
		blank=True,
		help_text="URL do link do botão"
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

	# Painéis no admin do Wagtail
	content_panels = CoderedWebPage.content_panels + [
		FieldPanel('navbar'),
		FieldPanel('video_background'),
		MultiFieldPanel(
			[
				FieldPanel('page_title'),
				FieldPanel('paragrafo'),
				FieldPanel('background_image'),
				FieldPanel('button_link'),
			],
			heading="Título e Parágrafo CTA Dinamico"
		),
		FieldPanel('teste_courses'),
		FieldPanel('suap_courses'),
		
		FieldPanel('noticias'),
		FieldPanel('dropdown_content'),
		FieldPanel('teste_preview'),
		FieldPanel('teste_noticia'),  
		FieldPanel('footer'),
	]

	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = CoderedWebPage.search_fields + [
		index.SearchField("page_title", boost=3),
		index.SearchField("paragrafo", boost=2),
		index.FilterField("url", name="url_filter"),
	]

	def get_searchable_content(self):
		content = super().get_searchable_content()

		if self.page_title:
			content.append(self.page_title)
		if self.paragrafo:
			content.append(self.paragrafo)
		if self.linkcta:
			content.append(self.linkcta)

		def extract_text_from_block(block_value):
			result = []

			if isinstance(block_value, list):  # lista de blocos (ex: StreamBlock)
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):  # tipo StructValue
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):  # RichText
				result.append(block_value.source)

			return result

		# StreamFields a indexar
		streamfields = [
			self.body,
			self.teste_courses,
			self.suap_courses,
			self.noticias,
			self.teste_noticia,
			self.teste_preview,
			self.dropdown_content,
		]

		for sf in streamfields:
			if sf:
				for block in sf:
					content.extend(extract_text_from_block(block.value))

		return content

	
	
	class Meta:
		verbose_name = "Enap home v1"
		verbose_name_plural = "Enap Home v1"


class ENAPTeste(CoderedWebPage):
	"""Página personalizada herdando todas as características de CoderedWebPage."""
	
	admin_notes = models.TextField(
		verbose_name="Anotações Internas",
		blank=True,
		help_text="Escreva observações importantes."
	)

	template = "enap_designsystem/pages/template_homeII.html"
	miniview_template = "coderedcms/pages/article_page.mini.html"
	search_template = "coderedcms/pages/article_page.search.html"

	page_title = models.CharField(
		max_length=255, 
		default="Título Padrão", 
		verbose_name="Título da Página"
	)


	body = StreamField(
		DYNAMIC_CARD_STREAMBLOCKS,
		null=True,
		blank=True,
		use_json_field=True,
	)


	teste_courses = StreamField(
		[("courses_carousel", CoursesCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	suap_courses = StreamField(
		[("suap_courses", SuapCourseBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)

	noticias = StreamField(
		[("eventos_carousel", EventsCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	teste_noticia = StreamField(
		[("noticias_carousel", NewsCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	teste_preview = StreamField(
		[("page_preview_teste", PageListBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)

	dropdown_content = StreamField(
		[("dropdown", DropdownBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)
	
	paragrafo = RichTextField(
		blank=True, 
		help_text="Adicione o texto do parágrafo aqui.", 
		verbose_name="Parágrafo sessao dinamica"
	)
	
	video_background = models.FileField(
		upload_to='media/videos', 
		null=True, 
		blank=True, 
		verbose_name="Vídeo de Fundo"
	)

	background_image = StreamField(
		[
			("image", ImageBlock()),
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	linkcta = RichTextField(blank=True)
	button_link = models.URLField(
		"Link do Botão",
		blank=True,
		help_text="URL do link do botão"
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

	# Painéis no admin do Wagtail
	content_panels = CoderedWebPage.content_panels + [
		FieldPanel('navbar'),
		FieldPanel('video_background'),
		MultiFieldPanel(
			[
				FieldPanel('page_title'),
				FieldPanel('paragrafo'),
				FieldPanel('background_image'),
				FieldPanel('button_link'),
			],
			heading="Título e Parágrafo CTA Dinamico"
		),
		FieldPanel('teste_courses'),
		FieldPanel('suap_courses'),
		FieldPanel('noticias'),
		FieldPanel('dropdown_content'),
		FieldPanel('teste_preview'),
		FieldPanel('teste_noticia'),  
		FieldPanel('footer'),
	]

	class Meta:
		verbose_name = "Enap Home v2"
		verbose_name_plural = "Home V2"





@register_snippet
class EnapFooterSnippet(ClusterableModel):
	"""
	Custom footer for bottom of pages on the site.
	"""

	class Meta:
		verbose_name = "ENAP Footer"
		verbose_name_plural = "ENAP Footers"

	image = StreamField([
		("logo", ImageChooserBlock()),
	], blank=True, use_json_field=True)

	name = models.CharField(
		max_length=255,
		blank=False,
		null=False,
		help_text="Título do snippet"
	)

	links = StreamField([
		("enap_footergrid", EnapFooterGridBlock()),
	], blank=True, use_json_field=True)

	social = StreamField([
		("enap_footersocialgrid", EnapFooterSocialGridBlock()),
	], blank=True, use_json_field=True)

	panels = [
		FieldPanel("name"),
		FieldPanel("image"),
		FieldPanel("social"),
		FieldPanel("links"),
	]

	def __str__(self) -> str:
		return self.name
	

@register_snippet
class EnapAccordionSnippet(ClusterableModel):
	"""
	Snippet de Accordion estilo FAQ.
	"""
	class Meta:
		verbose_name = "ENAP Accordion"
		verbose_name_plural = "ENAP Accordions"

	name = models.CharField(
		max_length=255,
		blank=False,
		null=False,
		help_text="Nome do snippet para facilitar a identificação no admin."
	)

	panels_content = StreamField([
		("accordion_item", EnapAccordionPanelBlock()),
	], blank=True, use_json_field=True)

	panels = [
		FieldPanel("name"),
		FieldPanel("panels_content"),
	]

	def __str__(self):
		return self.name


@register_snippet
class EnapNavbarSnippet(ClusterableModel):
	"""
	Snippet para a Navbar do ENAP, permitindo logo, busca, idioma e botão de contraste.
	"""

	name = models.CharField(
		max_length=255,
		blank=False,
		null=False,
		help_text="Nome do snippet para facilitar a identificação no admin."
	)

	logo = StreamField([
		("image", ImageChooserBlock())
	], blank=True, use_json_field=True, verbose_name="Logo da Navbar")

	links = StreamField([
		("navbar_link", EnapNavbarLinkBlock()),
	], blank=True, use_json_field=True)

	panels = [
		FieldPanel("name"),
		FieldPanel("logo"),
		FieldPanel("links"),
	]

	class Meta:
		verbose_name = " ENAP Navbar"
		verbose_name_plural = "ENAP Navbars"

	def __str__(self):
		return self.name


ALERT_TYPES = [
	('success', 'Sucesso'),
	('error', 'Erro'),
	('warning', 'Aviso'),
	('info', 'Informação'),
]
@register_snippet
class Alert(models.Model):
	
	title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título")
	message = RichTextField(verbose_name="Mensagem") 
	alert_type = models.CharField(
		max_length=20, 
		choices=ALERT_TYPES, 
		default='success', 
		verbose_name="Tipo de Alerta"
	)
	button_text = models.CharField(
		max_length=50, 
		blank=True, 
		default="Fechar", 
		verbose_name="Texto do Botão"
	)
	show_automatically = models.BooleanField(
		default=True, 
		verbose_name="Mostrar automaticamente"
	)
	
	panels = [
		FieldPanel('title'),
		FieldPanel('message'),
		FieldPanel('alert_type'),
		FieldPanel('button_text'),
		FieldPanel('show_automatically'),
	]
	
	def __str__(self):
		return self.title or f"Alerta ({self.get_alert_type_display()})"
	
	class Meta:
		verbose_name = "ENAP Alerta"
		verbose_name_plural = "ENAP Alertas"




# Os ícones, cores de fundo e cores dos ícones serão aplicados automaticamente
# com base no tipo de alerta selecionado

class AlertBlock(StructBlock):
	title = CharBlock(required=False, help_text="Título do alerta (opcional)")
	message = RichTextBlock(required=True, help_text="Mensagem do alerta")
	alert_type = ChoiceBlock(choices=ALERT_TYPES, default='success', help_text="Tipo do alerta")
	button_text = CharBlock(required=False, default="Fechar", help_text="Texto do botão (deixe em branco para não mostrar botão)")
	
	class Meta:
		template = "enap_designsystem/blocks/alerts.html"
		icon = 'warning'
		label = 'ENAP Alerta'




class WizardChooserBlock(ChooserBlock):
	@property
	def target_model(self):
		from enap_designsystem.models import Wizard  # Importação local para evitar referência circular
		return Wizard

	def get_form_state(self, value):
		return {
			'id': value.id if value else None,
			'title': str(value) if value else '',
		}

@register_snippet
class Wizard(ClusterableModel):
	"""
	Snippet para criar wizards reutilizáveis
	"""
	title = models.CharField(max_length=255, verbose_name="Título")
	
	panels = [
		FieldPanel('title'),
		InlinePanel('steps', label="Etapas do Wizard"),
	]
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "ENAP Wizard"
		verbose_name_plural = "ENAP Wizard"


class WizardStep(Orderable):
	"""
	Uma etapa dentro de um wizard
	"""
	wizard = ParentalKey(Wizard, on_delete=models.CASCADE, related_name='steps')
	title = models.CharField(max_length=255, verbose_name="Título da Etapa")
	content = models.TextField(blank=True, verbose_name="Conteúdo")
	
	panels = [
		FieldPanel('title'),
		FieldPanel('content'),
	]
	
	def __str__(self):
		return f"{self.title} - Etapa {self.sort_order + 1}"


class WizardBlock(StructBlock):
	"""
	Bloco para adicionar um wizard a uma página
	"""
	wizard = WizardChooserBlock(required=True)
	current_step = ChoiceBlock(
		choices=[(1, 'Etapa 1'), (2, 'Etapa 2'), (3, 'Etapa 3'), (4, 'Etapa 4'), (5, 'Etapa 5')],
		default=1,
		required=True,
		help_text="Qual etapa deve ser exibida como ativa",
	)
	
	def get_context(self, value, parent_context=None):
		context = super().get_context(value, parent_context)
		wizard = value['wizard']
		
		# Adiciona as etapas do wizard ao contexto
		steps = wizard.steps.all().order_by('sort_order')
		
		# Adapta o seletor de etapa atual para corresponder ao número real de etapas
		current_step = min(int(value['current_step']), steps.count())
		
		context.update({
			'wizard': wizard,
			'steps': steps,
			'current_step': current_step,
		})
		return context
	
	class Meta:
		template = 'enap_designsystem/blocks/wizard.html'
		icon = 'list-ol'
		label = 'ENAP Wizard'




@register_snippet
class Modal(models.Model):
	"""
	Snippet para criar modais reutilizáveis
	"""
	title = models.CharField(max_length=255, verbose_name="Título do Modal")
	content = RichTextField(verbose_name="Conteúdo do Modal")
	button_text = models.CharField(max_length=100, verbose_name="Texto do Botão", default="Abrir Modal")
	button_action_text = models.CharField(max_length=100, verbose_name="Texto do Botão de Ação", blank=True, help_text="Deixe em branco para não exibir um botão de ação")
	
	panels = [
		FieldPanel('title'),
		FieldPanel('content'),
		FieldPanel('button_text'),
		FieldPanel('button_action_text'),
	]
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "ENAP Modal"
		verbose_name_plural = "ENAP Modais"




@register_snippet
class ModalBlock(models.Model):
	"""
	Modal configurável que pode ser reutilizado em várias páginas.
	"""
	title = models.CharField(verbose_name="Título", max_length=255)
	content = RichTextField(verbose_name="Conteúdo", blank=True)
	button_text = models.CharField(verbose_name="Texto do botão", max_length=100, default="Abrir Modal")
	button_action_text = models.CharField(verbose_name="Texto do botão de ação", max_length=100, blank=True)
	
	# Novas opções
	SIZE_CHOICES = [
		('small', 'Pequeno'),
		('medium', 'Médio'),
		('large', 'Grande'),
	]
	size = models.CharField(verbose_name="Tamanho do Modal", max_length=10, choices=SIZE_CHOICES, default='medium')
	
	TYPE_CHOICES = [
		('message', 'Mensagem'),
		('form', 'Formulário'),
	]
	modal_type = models.CharField(verbose_name="Tipo de Modal", max_length=10, choices=TYPE_CHOICES, default='message')
	
	# Campos para formulário
	form_placeholder = models.CharField(verbose_name="Placeholder do formulário", max_length=255, blank=True)
	form_message = models.TextField(verbose_name="Mensagem do formulário", blank=True)
	
	panels = [
		FieldPanel('title'),
		FieldPanel('content'),
		FieldPanel('button_text'),
		FieldPanel('button_action_text'),
		FieldPanel('size'),
		FieldPanel('modal_type'),
		FieldPanel('form_placeholder'),
		FieldPanel('form_message'),
	]
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "Modal"
		verbose_name_plural = "Modais"


class ModalBlockStruct(blocks.StructBlock):
	modalenap = blocks.PageChooserBlock(
		required=True,
		label="Escolha um Modal",
	)

	class Meta:
		template = "enap_designsysten/blocks/modal_block.html"


@register_snippet
class Tab(ClusterableModel):
	"""
	Snippet para criar componentes de abas reutilizáveis com diferentes estilos
	"""
	title = models.CharField(max_length=255, verbose_name="Título do Componente")
	
	style = models.CharField(
		max_length=20,
		choices=[
			('style1', 'Estilo 1 (Com borda e linha inferior)'),
			('style2', 'Estilo 2 (Fundo verde quando ativo)'),
			('style3', 'Estilo 3 (Fundo verde quando ativo, sem bordas)'),
		],
		default='style1',
		verbose_name="Estilo Visual"
	)
	
	panels = [
		FieldPanel('title'),
		FieldPanel('style'),
		InlinePanel('tab_items', label="Abas"),
	]
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = "Enap Tab"
		verbose_name_plural = "Enap Tabs"


class TabItem(Orderable):
	"""
	Um item de aba dentro do componente Tab
	"""
	tab = ParentalKey(Tab, on_delete=models.CASCADE, related_name='tab_items')
	title = models.CharField(max_length=255, verbose_name="Título da Aba")
	content = RichTextField(verbose_name="Conteúdo da Aba")
	
	panels = [
		FieldPanel('title'),
		FieldPanel('content'),
	]
	
	def __str__(self):
		return f"{self.tab.title} - {self.title}"
	

class TabBlock(StructBlock):
	tab = SnippetChooserBlock(
		'enap_designsystem.Tab', 
		required=True, 
		help_text="Selecione um componente de abas"
	)
	
	class Meta:
		template = "enap_designsystem/blocks/draft_tab.html"
		icon = 'table'
		label = 'ENAP Abas'

@register_snippet
class FormularioContato(models.Model):
	titulo = models.CharField(max_length=100, default="Formulário de Contato")
	estilo_campo = models.CharField(
		max_length=20,
		choices=[
			('rounded', 'Arredondado (40px)'),
			('square', 'Quadrado (8px)'),
		],
		default='rounded',
		help_text="Escolha o estilo de borda dos campos do formulário"
	)
	
	panels = [
		FieldPanel('titulo'),
		FieldPanel('estilo_campo'),
	]
	
	def __str__(self):
		return self.titulo
	
	class Meta:
		verbose_name = "ENAP Formulário de Contato"
		verbose_name_plural = "ENAP Formulários de Contato"




class DropdownLinkBlock(StructBlock):
	link_text = CharBlock(label="Texto do link", required=True)
	link_url = URLBlock(label="URL do link", required=True)
	
	class Meta:
		template = "enap_designsystem/blocks/dropdown.html"
		icon = "link"
		label = "Link do Dropdown"

# Bloco principal do dropdown
class DropdownBlock(StructBlock):
	label = CharBlock(label="Label", required=True, default="Label")
	button_text = CharBlock(label="Texto do botão", required=True, default="Select")
	dropdown_links = ListBlock(DropdownLinkBlock())
	
	class Meta:
		template = "enap_designsystem/blocks/dropdown.html"
		icon = "arrow-down"
		label = "Dropdown"




class MbaEspecializacao(Page):
	"""Página de MBA e Especialização com componente CourseIntroTopics."""

	template = 'enap_designsystem/pages/mba_especializacao.html'

	navbar = models.ForeignKey(
		"EnapNavbarSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	course_intro_topics = StreamField([
		('course_intro_topics', CourseIntroTopicsBlock()),
		# Outros blocos podem ser adicionados aqui se necessário
	], use_json_field=True, blank=True)

	why_choose = StreamField([
		# Outros blocos existentes
		('why_choose', WhyChooseEnaptBlock()),
	], blank=True, null=True)

	testimonials_carousel = StreamField([
		# Outros blocos existentes
		('testimonials_carousel', TestimonialsCarouselBlock()),
	], blank=True, null=True)

	preview_courses = StreamField(
		[("preview_courses", PreviewCoursesBlock())],
		null=True,
		blank=True,
		use_json_field=True,
	)

	content = StreamField(
		[
			("banner", EnapBannerBlock()), 
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	teste_noticia = StreamField(
		[("noticias_carousel", NewsCarouselBlock())], 
		null=True,
		blank=True,
		use_json_field=True,
	)

	footer = models.ForeignKey(
		"EnapFooterSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	
	content_panels = Page.content_panels + [
		FieldPanel('navbar'),
		FieldPanel('content'),
		FieldPanel('course_intro_topics'),
		FieldPanel('why_choose'),
		FieldPanel('testimonials_carousel'),
		FieldPanel('preview_courses'),
		FieldPanel('teste_noticia'),
		FieldPanel("footer"),
	]
	
	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""
	
	search_fields = Page.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("course_intro_topics"),
		index.SearchField("why_choose"),
		index.SearchField("testimonials_carousel"),
		index.SearchField("preview_courses"),
		index.SearchField("content"),
		index.SearchField("teste_noticia"),
		index.FilterField("url", name="url_filter"),
	]

	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []

			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):  # StructValue
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):  # RichText
				result.append(block_value.source)

			return result

		streamfields = [
			self.content,
			self.course_intro_topics,
			self.why_choose,
			self.testimonials_carousel,
			self.preview_courses,
			self.teste_noticia,
		]

		for sf in streamfields:
			if sf:
				for block in sf:
					content.extend(extract_text_from_block(block.value))

		return content
	
	class Meta:
		verbose_name = "MBA e Especialização"
		verbose_name_plural = "MBAs e Especializações"



class TemplateEspecializacao(Page):
	"""Página de MBA e Especialização com componente CourseIntroTopics."""

	template = 'enap_designsystem/pages/template_mba.html'

	navbar = models.ForeignKey(
		"EnapNavbarSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	feature_course = StreamField([
		('feature_course', CourseFeatureBlock()),
	], use_json_field=True, blank=True)

	content = StreamField(
		[
			("banner", EnapBannerBlock()), 
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	feature_estrutura = StreamField([
		('feature_estrutura', CourseModulesBlock()),
	], use_json_field=True, blank=True)

	feature_processo_seletivo = StreamField([
		('feature_processo_seletivo', ProcessoSeletivoBlock()),
	], use_json_field=True, blank=True)

	team_carousel = StreamField([
		('team_carousel', TeamCarouselBlock()),
	], use_json_field=True, blank=True)

	footer = models.ForeignKey(
		"EnapFooterSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)
	
	content_panels = Page.content_panels + [
		FieldPanel('navbar'),
		FieldPanel('content'),
		FieldPanel('feature_course'),
		FieldPanel('feature_estrutura'),
		FieldPanel('feature_processo_seletivo'),
		FieldPanel('team_carousel'),
		FieldPanel("footer"),
	]
	
	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = Page.search_fields + [
		index.SearchField("content"),
		index.SearchField("feature_course"),
		index.SearchField("feature_estrutura"),
		index.SearchField("feature_processo_seletivo"),
		index.SearchField("team_carousel"),
		index.FilterField("url", name="url_filter"),
	]

	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []

			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):  # StructValue
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):  # RichText
				result.append(block_value.source)

			return result

		streamfields = [
			self.content,
			self.feature_course,
			self.feature_estrutura,
			self.feature_processo_seletivo,
			self.team_carousel,
		]

		for sf in streamfields:
			if sf:
				for block in sf:
					content.extend(extract_text_from_block(block.value))

		return content
	
	class Meta:
		verbose_name = "MBA e Especialização Especifico"
		verbose_name_plural = "MBAs e Especializações"





class OnlyCards(Page):
	template = 'enap_designsystem/pages/template_only-cards.html'

	featured_card = StreamField([
		("enap_section", EnapSectionBlock([
			("enap_cardgrid", EnapCardGridBlock([
				("enap_card", EnapCardBlock()),
			])),
		])),
	], blank=True, use_json_field=True)

	banner = StreamField(
		[
			("banner", EnapBannerBlock()), 
		],
		null=True,
		blank=True,
		use_json_field=True,
	)

	course_intro_topics = StreamField([
		('course_intro_topics', CourseIntroTopicsBlock()),
		# Outros blocos podem ser adicionados aqui se necessário
	], use_json_field=True, blank=True)

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
		FieldPanel('navbar'),
		FieldPanel('banner'),
		FieldPanel('course_intro_topics'),
		FieldPanel('featured_card'),
		FieldPanel("footer"),
	]

	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = Page.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("banner"),
		index.SearchField("course_intro_topics"),
		index.SearchField("featured_card"),
		index.FilterField("url", name="url_filter"),
	]
	
	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []
			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):
				result.append(block_value.source)
			return result

		streamfields = [
			self.banner,
			self.course_intro_topics,
			self.featured_card,
		]

		for sf in streamfields:
			if sf:
				for block in sf:
					content.extend(extract_text_from_block(block.value))

		return content


	class Meta:
		verbose_name = "ENAP apenas com cards(usar paar informativos)"
		verbose_name_plural = "ENAP Pagina so com cards"






class AreaAluno(Page):
	"""Página personalizada herdando todas as características de CoderedWebPage."""

	template = "enap_designsystem/pages/area_aluno.html"

	body = StreamField(
		LAYOUT_STREAMBLOCKS,
		null=True,
		blank=True,
		use_json_field=True,
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
		FieldPanel("footer"),
		FieldPanel("body"),
	]

	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = Page.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("body"),
		index.FilterField("url", name="url_filter"),
	]
	
	def get_searchable_content(self):
		content = super().get_searchable_content()

		def extract_text_from_block(block_value):
			result = []
			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):
				result.append(block_value.source)
			return result

		if self.body:
			for block in self.body:
				content.extend(extract_text_from_block(block.value))

		return content


	class Meta:
		verbose_name = "Area do aluno"
		verbose_name_plural = "Area do aluno"


class EnapSearchElastic(Page):
	"""Página de busca, implementada com ElasticSearch da ENAP."""

	template = 'enap_designsystem/pages/page_search.html'

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
		FieldPanel('navbar'),
		FieldPanel("footer"),
	]

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)

		query = request.GET.get("q", "").strip()
		if query:
			# Busca usando o backend ativo (Elasticsearch, confirmado!)
			results = Page.objects.live().search(query)
		else:
			results = Page.objects.none()

		context["query"] = query
		context["results"] = results
		context["results_count"] = results.count()
		return context

	class Meta:
		verbose_name = "ENAP Busca (ElasticSearch)"
		verbose_name_plural = "ENAP Buscas (ElasticSearch)"


class Template001(Page):
	"""Página de MBA e Especialização com vários componentes."""

	template = 'enap_designsystem/pages/template_001.html'

	# Navbar (snippet)
	navbar = models.ForeignKey(
		"EnapNavbarSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)

	# Banner fields
	
	banner_background_image = models.ForeignKey(
		get_image_model_string(),
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+',
		verbose_name=_("Banner Background Image")
	)  

	banner_title = models.CharField(
		max_length=255,
		default="Título do Banner",
		verbose_name=_("Banner Title")
	)
	banner_description = RichTextField(
		features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
		default="<p>Descrição do banner. Edite este texto para personalizar o conteúdo.</p>",
		verbose_name=_("Banner Description")
	)
	
	# Feature Course fields
	title_1 = models.CharField(
		max_length=255,
		default="Título da feature 1",
		verbose_name=_("Primeiro título")
	)
	description_1 = models.TextField(
		default="It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English.",
		verbose_name=_("Primeira descrição")
	)
	title_2 = models.CharField(
		max_length=255,
		default="Título da feature 2",
		verbose_name=_("Segundo título")
	)
	description_2 = models.TextField(
		default="It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English.",
		verbose_name=_("Segunda descrição")
	)
	image = models.ForeignKey(
		get_image_model_string(),
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+',
		verbose_name=_("Imagem da feature")
	)
	
	# Estrutura como StreamField
	# Estrutura como StreamField
	feature_estrutura = StreamField([
		('feature_estrutura', CourseModulesBlock()),
	], use_json_field=True, blank=True, null=True, default=[
		('feature_estrutura', {
			'title': 'Estrutura do curso',
			'modules': [
				{
					'module_title': '1º Módulo',
					'module_description': 'Descrição do primeiro módulo',
					'module_items': [
						'Conceitos básicos',
						'Fundamentos teóricos',
						'Práticas iniciais'
					]
				},
				{
					'module_title': '2º Módulo',
					'module_description': 'Descrição do segundo módulo',
					'module_items': [
						'Desenvolvimento avançado',
						'Estudos de caso',
						'Projetos práticos'
					]
				},
				{
					'module_title': '3º Módulo',
					'module_description': 'Descrição do terceiro módulo',
					'module_items': [
						'Especialização',
						'Projeto final',
						'Apresentação'
					]
				}
			]
		})
	]) # Removi a vírgula extra aqui

	# Team Carousel como StreamField
	team_carousel = StreamField([
		('team_carousel', TeamCarouselBlock()),
	], use_json_field=True, blank=True, null=True, default=[
		('team_carousel', {
			'title': 'Nossa Equipe',
			'description': 'Equipe de desenvolvedores e etc',
			'view_all_text': 'Ver todos',
			'members': [
				{'name': 'Membro 1', 'role': 'Cargo 1', 'image': None},
				{'name': 'Membro 2', 'role': 'Cargo 2', 'image': None},
				{'name': 'Membro 3', 'role': 'Cargo 3', 'image': None},
				{'name': 'Membro 4', 'role': 'Cargo 4', 'image': None},
		]
	})])
	
	# Processo Seletivo fields
	processo_title = models.CharField(
		max_length=255, 
		default="Processo seletivo",
		verbose_name=_("Título do Processo Seletivo")
	)
	processo_description = models.TextField(
		default="Sobre o processo seletivo",
		verbose_name=_("Descrição do Processo Seletivo")
	)
	
	# Módulo 1
	processo_module1_title = models.CharField(
		max_length=255,
		default="Inscrição",
		verbose_name=_("Título do 1º Módulo")
	)
	processo_module1_description = models.TextField(
		default="Lorem ipsum dolor sit amet",
		verbose_name=_("Descrição do 1º Módulo")
	)
	
	# Módulo 2
	processo_module2_title = models.CharField(
		max_length=255,
		default="Seleção",
		verbose_name=_("Título do 2º Módulo")
	)
	processo_module2_description = models.TextField(
		default="Lorem ipsum dolor sit amet",
		verbose_name=_("Descrição do 2º Módulo")
	)
	
	# Módulo 3
	processo_module3_title = models.CharField(
		max_length=255,
		default="Resultado",
		verbose_name=_("Título do 3º Módulo")
	)
	processo_module3_description = models.TextField(
		default="Lorem ipsum dolor sit amet",
		verbose_name=_("Descrição do 3º Módulo")
	)

	# Footer (snippet)
	footer = models.ForeignKey(
		"EnapFooterSnippet",
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="+",
	)
	
	# Painéis de conteúdo organizados em seções
	content_panels = Page.content_panels + [
		FieldPanel('navbar'),
		
		MultiFieldPanel([
			FieldPanel('banner_background_image', classname="default-image-14"),
			FieldPanel('banner_title'),
			FieldPanel('banner_description'),
		], heading="Banner"),
		
		MultiFieldPanel([
			FieldPanel('title_1'),
			FieldPanel('description_1'),
			FieldPanel('title_2'),
			FieldPanel('description_2'),
			FieldPanel('image', classname="default-image-14"),
		], heading="Feature Course"),
		
		FieldPanel('feature_estrutura'),
		
		MultiFieldPanel([
			FieldPanel('processo_title'),
			FieldPanel('processo_description'),
			FieldPanel('processo_module1_title'),
			FieldPanel('processo_module1_description'),
			FieldPanel('processo_module2_title'),
			FieldPanel('processo_module2_description'),
			FieldPanel('processo_module3_title'),
			FieldPanel('processo_module3_description'),
		], heading="Processo Seletivo"),
		
		FieldPanel('team_carousel'),
		
		FieldPanel("footer"),
	]
	
	@property
	def url_filter(self):
		if hasattr(self, 'full_url') and self.full_url:
			return self.full_url
		return self.get_url_parts()[2] if self.get_url_parts() else ""

	search_fields = Page.search_fields + [
		index.SearchField("title", boost=3),
		index.SearchField("banner_title", boost=2),
		index.SearchField("banner_description"),
		index.SearchField("title_1"),
		index.SearchField("description_1"),
		index.SearchField("title_2"),
		index.SearchField("description_2"),
		index.SearchField("processo_title"),
		index.SearchField("processo_description"),
		index.SearchField("processo_module1_title"),
		index.SearchField("processo_module1_description"),
		index.SearchField("processo_module2_title"),
		index.SearchField("processo_module2_description"),
		index.SearchField("processo_module3_title"),
		index.SearchField("processo_module3_description"),
		index.SearchField("feature_estrutura"),
		index.SearchField("team_carousel"),
		index.FilterField("url", name="url_filter"),
	]
	
	def get_searchable_content(self):
		content = super().get_searchable_content()

		fields = [
			self.banner_title,
			self.banner_description,
			self.title_1,
			self.description_1,
			self.title_2,
			self.description_2,
			self.processo_title,
			self.processo_description,
			self.processo_module1_title,
			self.processo_module1_description,
			self.processo_module2_title,
			self.processo_module2_description,
			self.processo_module3_title,
			self.processo_module3_description,
		]

		for f in fields:
			if f:
				content.append(str(f))

		def extract_text_from_block(block_value):
			result = []
			if isinstance(block_value, list):
				for subblock in block_value:
					result.extend(extract_text_from_block(subblock))
			elif hasattr(block_value, "get"):
				for key, val in block_value.items():
					result.extend(extract_text_from_block(val))
			elif isinstance(block_value, str):
				result.append(block_value)
			elif hasattr(block_value, "source"):
				result.append(block_value.source)
			return result

		if self.feature_estrutura:
			for block in self.feature_estrutura:
				content.extend(extract_text_from_block(block.value))
		if self.team_carousel:
			for block in self.team_carousel:
				content.extend(extract_text_from_block(block.value))

		return content


	class Meta:
		verbose_name = "Template 001"
		verbose_name_plural = "Templates 001"






class HolofotePage(Page):
    """Template Holofote"""

    template = "enap_designsystem/pages/template_holofote.html"

    footer = models.ForeignKey(
        "EnapFooterSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    navbar = models.ForeignKey(
        "EnapNavbarSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    
    body = StreamField([
        ('citizen_server', CitizenServerBlock()),
        ('topic_links', TopicLinksBlock()),
		('feature_list_text', FeatureWithLinksBlock()), 
		('QuoteModern', QuoteBlockModern()),
        ('service_cards', ServiceCardsBlock()),
        ('carousel_green', CarouselGreen()),
        ('section_block', EnapSectionBlock()),
        ('feature_list', FeatureListBlock()),
        ('service_cards', ServiceCardsBlock()),
        ('banner_image_cta', Banner_Image_cta()),
        ('citizen_server', CitizenServerBlock()),
        ("carrossel_cursos", CarrosselCursosBlock()),
		("enap_section", EnapSectionBlock([
			("enap_cardgrid", EnapCardGridBlock([
				("enap_card", EnapCardBlock()),
				('card_curso', CardCursoBlock()),
			])),
		])),
        # Outros blocos padrão do Wagtail
        ('heading', blocks.CharBlock(form_classname="title", label=_("Título"))),
        ('paragraph', blocks.RichTextBlock(label=_("Parágrafo"))),
        ('image', ImageChooserBlock(label=_("Imagem"))),
        ('html', blocks.RawHTMLBlock(label=_("HTML")))
    ], null=True, blank=True, verbose_name=_("Conteúdo da Página"))
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel("footer"),
        FieldPanel("navbar"),
    ]
    
    class Meta:
        verbose_name = _("Template Holofote")