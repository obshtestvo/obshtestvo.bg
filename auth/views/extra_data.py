from django.views.generic.base import View
from django.shortcuts import redirect
from django import forms

from restful.decorators import restful_view_templates

from projects.services import SkillService

from projects.models import Skill, Member, User

@restful_view_templates
class ExtraDataView(View):
    def get(self, request):
        details = request.session['partial_pipeline']['kwargs']['details']
        skills_options = SkillService.all_grouped_as_picker_options()
        member = None
        try:
            member = Member.objects.select_related('skills').get(name=details["first_name"]+' '+details["last_name"])
        except:
            pass

        uid = request.session['partial_pipeline']['kwargs']['uid']

        return {
            'details': details,
            'uid': uid,
            'avatar': User.get_facebook_avatar(uid),
            'skills_options': skills_options,
            'member': member,
            'usecase': request.params.get('usecase', 'now'),
        }

    def post(self, request):
        try:
            form = Form(data=request.params)
            if form.is_valid():
                data = form.cleaned_data
                request.session['saved_email'] = data['email']
                request.session['saved_name'] = data['name']
                request.session['saved_skills'] = data['skills']
                request.session['saved_available_after'] = data['available_after']
                backend = request.session['partial_pipeline']['backend']
                return redirect('social:complete', backend=backend)
            else:
                message = str(form.errors)
        except Exception as e:
            message = str(e)

        return {
            "status": message
        }, 400

class Form(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    skills = forms.CharField(required=True)
    available_after = forms.DateField(required=False)
