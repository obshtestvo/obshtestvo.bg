from django.views.generic.base import View
from collections import OrderedDict


from restful.decorators import restful_view_templates

from projects.models import SkillGroup, User, Project, Skill

@restful_view_templates
class UsersView(View):

    def get(self, request):
        # get users and order them by
        users_sql = """
          SELECT pu.*
          FROM projects_user as pu
          WHERE pu.is_active = 1 AND pu.is_browsable = 1
          ORDER BY (
            SELECT skill_popularity.popularity as rare_skill_rating
            FROM
              (SELECT COUNT(user_id) as popularity, skill_id FROM projects_user_skills GROUP BY skill_id) as skill_popularity,
              projects_user_skills AS u_skills
            WHERE skill_popularity.skill_id = u_skills.skill_id AND u_skills.user_id = pu.id
            ORDER BY skill_popularity.popularity
            LIMIT 1), (SELECT COUNT(skill_id) FROM projects_user_skills pus WHERE pus.user_id = pu.id)
        """
        result = {
            "users": OrderedDict(),
            "skills": OrderedDict(),
            "skill_groups": OrderedDict(),
            "projects": None
        }

        # no-join queries
        users = User.objects.raw(users_sql)
        projects = Project.objects.all()
        skills = Skill.objects.all()
        sgroups = SkillGroup.objects.all()


        # links
        user_skills_links_by_skill_id = {}
        for link in User.skills.through.objects.all():
            if link.skill_id not in user_skills_links_by_skill_id:
                user_skills_links_by_skill_id[link.skill_id] = []
            user_skills_links_by_skill_id[link.skill_id].append(link.user_id)

        user_projects_links_by_project_id = {}
        for link in User.projects_interests.through.objects.all():
            if link.project_id not in user_projects_links_by_project_id:
                user_projects_links_by_project_id[link.project_id] = []
            user_projects_links_by_project_id[link.project_id].append(link.user_id)

        skill_groups_links_by_skill_id = {}
        for link in Skill.groups.through.objects.all():
            if link.skill_id not in skill_groups_links_by_skill_id:
                skill_groups_links_by_skill_id[link.skill_id] = []
            skill_groups_links_by_skill_id[link.skill_id].append(link.skillgroup_id)

        # building results and linking objects
        result["projects"] = projects
        for u in users:
            result["users"][u.id] = u
            result["users"][u.id].skill_groups = []
        for p in projects:
            if p.id not in user_projects_links_by_project_id:
                continue
            for uid in user_projects_links_by_project_id[p.id]:
                if not hasattr(result["users"][uid], 'preloaded_projects_interests'):
                    result["users"][uid].preloaded_projects_interests = []
                result["users"][uid].preloaded_projects_interests.append(p)
        for g in sgroups:
            result["skill_groups"][g.id] = g
            result["skill_groups"][g.id].preloaded_per_user_skills = {}
        for s in skills:
            result["skills"][s.id] = s
            if s.id in skill_groups_links_by_skill_id:
                for gid in skill_groups_links_by_skill_id[s.id]:
                    if not hasattr(result["skill_groups"][gid], 'preloaded_skills'):
                        result["skill_groups"][gid].preloaded_skills = []
                    result["skill_groups"][gid].preloaded_skills.append(s)
            if s.id not in user_skills_links_by_skill_id:
                continue
            for uid in user_skills_links_by_skill_id[s.id]:
                if not hasattr(result["users"][uid], 'preloaded_skills'):
                    result["users"][uid].preloaded_skills = []
                result["users"][uid].preloaded_skills.append(s)
                if s.id not in skill_groups_links_by_skill_id:
                    continue
                for gid in skill_groups_links_by_skill_id[s.id]:
                    if uid not in result["skill_groups"][gid].preloaded_per_user_skills:
                        result["skill_groups"][gid].preloaded_per_user_skills[uid] = []
                    result["skill_groups"][gid].preloaded_per_user_skills[uid].append(s)
                    if result["skill_groups"][gid] not in result["users"][uid].skill_groups:
                        result["users"][uid].skill_groups.append(result["skill_groups"][gid])


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
        return result