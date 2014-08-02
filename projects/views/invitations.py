from django.core.mail import send_mail
from django import forms
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from restful.decorators import restful_view_templates
from projects.services import TasksService
from projects.models import Invitation, InvitationAnswer, Project, Skill, Task, User


@restful_view_templates
class InvitationsView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            form = Form(data=request.params)
            if form.is_valid():
                data = form.cleaned_data
                task = data['task']
                if task.isdigit():
                    task_id = int(task)
                    task = Task.objects.get(pk=task_id)
                else:
                    task_service = TasksService()
                    task = task_service.add_task(task, data['project'], data['skill'])

                inv = Invitation()
                inv.task = task
                inv.inviter = current_user
                inv.save()

                invitation_answer = InvitationAnswer()
                invitation_answer.invitee = data['to_user']
                invitation_answer.save()

                try:
                    # send email
                    send_mail(
                        'Контакт от сайта на obshtestvo.bg',
                        u'Тип контакт: ' + form.cleaned_data['type'] + "\n" +
                        u'Организация: ' + form.cleaned_data['name'] + "\n" +
                        u'Проект: ' + form.cleaned_data['project'] + "\n" +
                        u'Email: ' + form.cleaned_data['email'] + "\n" +
                        u'Предложена помощ: ' + form.cleaned_data['help'] + "\n",
                        'noreply@obshtestvo.bg',
                        ['antitoxic@gmail.com'],
                        fail_silently=False
                    )
                    message = 'Благодарим Ви. Ще се свържем с Вас възможно най-скоро.'
                except:
                    status = 400
                    message = 'Изникна грешка при получаването на вашата информацията. Моля, опитайте по-късно'


            else:
                message = str(form.errors)
        except Exception as e:
            message = str(e)
        task = request.params.get('task')

        message = request.params.get('message')

        request.params.get('project')
        request.params.get('skill')



class Form(forms.Form):
    task = forms.CharField(required=True)
    project = forms.ModelChoiceField(required=True, queryset=Project.objects.all())
    skill = forms.CharField(required=True, queryset=Skill.objects.all())
    message = forms.CharField(required=True)
    to_user = forms.ModelChoiceField(required=True, queryset=User.objects.all())