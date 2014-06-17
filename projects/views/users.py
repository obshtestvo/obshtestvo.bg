from django.views.generic.base import View

from restful.decorators import restful_view_templates

from projects.models import SkillGroup, User, Project

@restful_view_templates
class UsersView(View):

    def get(self, request):
        skills_options = []
        users = User.objects.select_related('skills', 'projects_interests').filter(is_active=True, is_browsable=True).order_by('first_name')
        projects = Project.objects.all()

        for sgroup in SkillGroup.objects.select_related('skills').all():
            skills_options.append({
                "text": sgroup.name,
                "id": -1,
                "group": sgroup.name,
            })
            for skill in sgroup.skills.all():
                skills_options.append({
                    "text": skill.name,
                    "id": skill.id,
                    "group": sgroup.name,
                })

        return {
            'page': "users-page",
            'projects': projects,
            'users': users,
            'skills_options': skills_options
        }