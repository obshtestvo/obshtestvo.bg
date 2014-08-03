from django.conf import settings
from django.views.generic.base import View
from restful.decorators import restful_view_templates


@restful_view_templates
class StyleView(View):
    def get(self, request):
        return {
            "page": "inner about faq",
            "projects": settings.FAKE_DB,
        }
