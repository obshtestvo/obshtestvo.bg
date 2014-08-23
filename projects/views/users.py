# coding=utf-8
from django.views.generic.base import View

from restful.decorators import restful_view_templates

from projects.models import SkillGroup, User, Project, Skill, Task
from projects.services import UsersService, JSONResponse

@restful_view_templates
class UsersView(View):

    def get(self, request):

        if request.is_ajax():
            if request.GET.get('userId'):
                user_id = int(request.GET.get('userId'))
                user = User.objects.get(pk=user_id)

                data = [{'skill': s.name,
                        'skill_id':  s.pk,
                        'user': user.first_name,
                        'email': user.email,
                } for s in user.skills.iterator()]

                return JSONResponse(data)

            if request.GET.get('skillId'):
                project_id = int(request.GET.get('projectId'))
                skill_id = int(request.GET.get('skillId'))
                tasks = Task.objects.filter(skill_id=skill_id, project_id=project_id)

                data = [{'name': t.name,
                        'task_id':  t.pk,
                        'task_description':  t.description,
                        'task_project':  t.project.name,
                        'task_skill':  t.skill.name,
                } for t in tasks]

                return JSONResponse(data)

        user_service = UsersService()

        # no-join queries
        users = user_service.all_ordered_by_skill_popularity_and_skill_count()
        social_users = User.social_auth.related.model.objects.all()
        projects = Project.objects.all()
        skills = Skill.objects.all()
        sgroups = SkillGroup.objects.all()

        result = user_service.connect_data_as_dict(users=users, social_users=social_users, projects=projects, skills=skills, skill_groups=sgroups)

        skills_options = []
        for id in result["skill_groups"]:
            group = result["skill_groups"][id]
            skills_options.append({
                "text": group.name,
                "id": -1,
                "group": group.name,
            })
            for skill in group.preloaded_skills:
                skills_options.append({
                    "text": skill.name,
                    "id": skill.id,
                    "group": group.name,
                })

        result["page"] = "users-page"
        result["skills_options"] = skills_options
        result["anonymous"] = [
            {'name': 'Анонимко Анонимков', "type": "male" },
            {'name': "Анонимка Анонимкова", "type": "female" },
            {'name': "Минзухар Лешников", "type": "male" },
            {'name': "Портокалка Табуреткова", "type": "female" },
            {'name': "Пъпешка Оризова", "type": "female" },
            {'name': "Авокадо Де Парло", "type": "male" },
            {'name': "Нар Народен", "type": "male" },
            {'name': "Фъстъчка Пъдпъдъкова", "type": "female" },
            {'name': "Tиква царевичкова","type": "female" },
        ]
        return result