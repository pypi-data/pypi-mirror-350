# enap_designsystem/context_processors.py

from django.conf import settings

def global_template_context(request):
	return {
		'debug': settings.DEBUG
	}
