from models import User, Skill, SkillGroup, Task
from collections import OrderedDict

class UsersService:
    def all_ordered_by_skill_popularity_and_skill_count(self, order="ASC"):
        sql = """
          SELECT pu.*
          FROM projects_user as pu
          WHERE pu.is_active = 1 AND pu.is_browsable = 1
          ORDER BY (
            SELECT skill_popularity.popularity as rare_skill_rating
            FROM
              (SELECT COUNT(user_id) as popularity, skill_id FROM projects_user_skills GROUP BY skill_id) as skill_popularity,
              projects_user_skills AS u_skills
            WHERE skill_popularity.skill_id = u_skills.skill_id AND u_skills.user_id = pu.id
            ORDER BY skill_popularity.popularity """ + order + """
            LIMIT 1), (SELECT COUNT(skill_id) FROM projects_user_skills pus WHERE pus.user_id = pu.id) """ + order + """
        """
        return User.objects.raw(sql)

    """
    This exists entirely due to performance reasons. We are saving requests to the DB by building relations manually
    in the code instead of relying on the ORM.
    """
    def connect_data_as_dict(self, users, social_users=None, projects=None, skills=None, skill_groups=None):
        result = {
            "users": OrderedDict(),
            "skills": OrderedDict(),
            "skill_groups": OrderedDict(),
            "projects": None
        }

        # links
        # user's skills with skills ids as keys
        if skills is not None:
            user_skills_links_by_skill_id = {}
            for link in User.skills.through.objects.all():
                if link.skill_id not in user_skills_links_by_skill_id:
                    user_skills_links_by_skill_id[link.skill_id] = []
                user_skills_links_by_skill_id[link.skill_id].append(link.user_id)

        # user's projects with project ids as keys
        if projects is not None:
            user_projects_links_by_project_id = {}
            for link in User.projects_interests.through.objects.all():
                if link.project_id not in user_projects_links_by_project_id:
                    user_projects_links_by_project_id[link.project_id] = []
                user_projects_links_by_project_id[link.project_id].append(link.user_id)

        # skill's groups in dict with skill ids as keys
        if skills is not None and skill_groups is not None:
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

        if social_users is not None:
            for u in social_users:
                if u.user_id not in result["users"]:
                    continue
                result["users"][u.user_id].preloaded_uid = u.uid

        if projects is not None:
            for p in projects:
                if p.id not in user_projects_links_by_project_id:
                    continue
                for uid in user_projects_links_by_project_id[p.id]:
                    if not uid in result["users"]:
                        continue
                    if not hasattr(result["users"][uid], 'preloaded_projects_interests'):
                        result["users"][uid].preloaded_projects_interests = []
                    result["users"][uid].preloaded_projects_interests.append(p)

        if skill_groups is not None:
            for g in skill_groups:
                result["skill_groups"][g.id] = g
                result["skill_groups"][g.id].preloaded_per_user_skills = {}

        if skills is not None:
            for s in skills:
                result["skills"][s.id] = s
                if skill_groups is not None and s.id in skill_groups_links_by_skill_id:
                    for gid in skill_groups_links_by_skill_id[s.id]:
                        if not hasattr(result["skill_groups"][gid], 'preloaded_skills'):
                            result["skill_groups"][gid].preloaded_skills = []
                        result["skill_groups"][gid].preloaded_skills.append(s)
                if s.id not in user_skills_links_by_skill_id:
                    continue
                for uid in user_skills_links_by_skill_id[s.id]:
                    if not uid in result["users"]:
                        continue
                    if not hasattr(result["users"][uid], 'preloaded_skills'):
                        result["users"][uid].preloaded_skills = []
                    result["users"][uid].preloaded_skills.append(s)
                    if skill_groups is None:
                        continue
                    if s.id not in skill_groups_links_by_skill_id:
                        continue
                    for gid in skill_groups_links_by_skill_id[s.id]:
                        if uid not in result["skill_groups"][gid].preloaded_per_user_skills:
                            result["skill_groups"][gid].preloaded_per_user_skills[uid] = []
                        result["skill_groups"][gid].preloaded_per_user_skills[uid].append(s)
                        if result["skill_groups"][gid] not in result["users"][uid].skill_groups:
                            result["users"][uid].skill_groups.append(result["skill_groups"][gid])
        return result


class SkillService:

    def all_grouped_as_picker_options(self):
        skills_options = []
        for sgroup in SkillGroup.objects.prefetch_related('skills').all():
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
            'skills_options': skills_options
        }