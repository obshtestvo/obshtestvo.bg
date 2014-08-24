# -*- coding: utf-8 -*-
from django.contrib.auth import settings
from django.core.mail import EmailMultiAlternatives
from django import forms
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags


# from restful.decorators import restful_view_templates 
from projects.services import JSONResponse
from projects.models import Invitation, Project, Skill, Task, User, InvitationAnswer


# @restful_view_templates
class InvitationsView(View):
    @method_decorator(login_required)
    def post(self, request):
        if request.is_ajax():
            try:
                form = Form(data=request.params)
                if form.is_valid():
                    data = form.cleaned_data
                    task_data = data['task']
                    project = data['project']
                    skill = data['skill']

                    if task_data.isdigit():
                        task_id = int(task_data)
                        task = Task.objects.get(pk=task_id)
                    else:
                        task = Task(name=task_data, project=project, skill=skill)
                        task.save()

                    inv = Invitation(task=task, project=project, skill=skill, message=data['message'], inviter=request.user, invitee=data['invitee'])
                    inv.save()
                    invitation_answer = InvitationAnswer(invitation=inv, invitee=data['invitee'])
                    invitation_answer.save()

                    try:
                        # send email
                        subject, from_email, to = 'Покана от obshtestvo.bg', settings.EMAIL_FROM, 'vladimirrussinov@gmail.com'
                        html_content = render_to_string('email_templates/invite.html', {'project': inv.project.name, 'skill': inv.skill.name,
                            'task': inv.task.name, 'inviter_mail': inv.inviter.email, 'inviter_name': inv.inviter.get_full_name(),
                            'invitee_name': inv.invitee.first_name, 'message': inv.message})
                        text_content = strip_tags(html_content)

                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()

                        message = 'Благодарим Ви. Ще се свържем с Вас възможно най-скоро.'
                    except Exception as e:
                        print e
                        message = 'Изникна грешка при получаването на вашата информацията. Моля, опитайте по-късно'

                    response = {
                        "message": message
                    }
                    return JSONResponse(response)

                else:
                    message = form.errors
                    response = {
                        "errors": message
                    }
                    return JSONResponse(response)
            except Exception as e:
                message = str(e)


class Form(forms.Form):
    task = forms.CharField(required=True)
    project = forms.ModelChoiceField(required=True, queryset=Project.objects.all())
    skill = forms.ModelChoiceField(required=True, queryset=Skill.objects.all())
    message = forms.CharField(required=True)
    invitee = forms.ModelChoiceField(required=True, queryset=User.objects.all())