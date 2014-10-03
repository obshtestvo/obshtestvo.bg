# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import settings
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMultiAlternatives
from django import forms
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from restful.decorators import restful_view_templates

from projects.models import Invitation, Project, Skill, Task, User, InvitationAnswer

@restful_view_templates
class InvitationFInish(View):

    @method_decorator(login_required)
    def post(self, request, pk=None):
        user = request.user
        choice = request.params.get('answer')

        if pk is not None and choice is not None:

            # request.params
            # {answer: Yes}
            answer_instance_pk = pk
            try:
                answer_instance = InvitationAnswer.objects.get(pk=answer_instance_pk)
            except InvitationAnswer.DoesNotExist:
                return redirect('home')

            if answer_instance.invitee == user:
                if answer_instance.is_answered is False:
                    answer_instance.answer = choice
                    answer_instance.answered_at = datetime.now()

                    answer_instance.is_answered = True
                    answer_instance.save()

                    subject, from_email, to = 'Отговор на покана от obshtestvo.bg', settings.EMAIL_FROM, 'vladimirrussinov@gmail.com'
                    html_content = render_to_string('email_templates/answer.html', {'answer': answer_instance, 'site': get_current_site(request).domain})
                    text_content = strip_tags(html_content)

                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    # message = 'Благодарим Ви. Ще се свържем с Вас възможно най-скоро.
            return redirect('users')
        else:
            return redirect('home')
