# coding=utf-8
from django.views.generic.base import View

from restful.decorators import restful_view_templates

from projects.models import SkillGroup, User, Project, Skill
from projects.services import UsersService

@restful_view_templates
class UsersView(View):

    def get(self, request):
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
            {'name': "Портокалка Табореткова", "type": "female" },
            {'name': "Пъпешка Оризова", "type": "female" },
            {'name': "Авокадо Де Парло", "type": "male" },
            {'name': "Нар Народен", "type": "male" },
            {'name': "Фъстъчка Пъдпъдъкова", "type": "female" },
            {'name': "Tиква царевичкова","type": "female" },
        ]
        return result