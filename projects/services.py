from projects.models import SkillGroup, Skill

class SkillPickerService:
    def all(self):
        skills_options = []
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

        return skills_options