import StringIO
from PIL import Image

from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import ModelForm, Form
from django.shortcuts import redirect

from restful.shortcuts import get_updated_data

from restful.decorators import restful_view_templates
from guardian.decorators import permission_required_or_403

from projects.services import SkillService
from projects.models import Project, User, Skill

@restful_view_templates
class UserView(View):

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('projects.change_user', (User, 'id', 'id')))
    def put(self, request, id):
        user = User.objects.get(pk=id)
        current_ids = list(User.objects.filter(pk=id).values_list('projects_interests__id', flat=True))
        project_ids = list(Project.objects.values_list('id', flat=True))
        ProjectLinkModel = User.projects_interests.through
        links = []
        for id in request.params.get('projects', []):
            id = int(id)
            if id in current_ids:
                current_ids.remove(id)
            else:
                if id in project_ids:
                    links.append(ProjectLinkModel(user_id=user.id, project_id=id))

        if filter(None, current_ids):
            ProjectLinkModel.objects.filter(project_id__in=current_ids).delete()
        if links:
            ProjectLinkModel.objects.bulk_create(links)

@restful_view_templates
class UserProfileView(View):

    default_thumbnail_size = 128, 128

    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('projects.change_user', (User, 'id', 'id')))
    def get(self, request, id):
        user = User.objects.select_related('skills').get(pk=id)
        skills = SkillService().all_grouped_as_picker_options()
        form = UserModelForm()
        user.get_avatar()
        #raise Exception("Error with select2grouped bad string searching leads to fake skills")

        return {"form": form,
                "profile": user,
                "all_skills": skills}


    @method_decorator(login_required)
    @method_decorator(permission_required_or_403('projects.change_user', (User, 'id', 'id')))
    def post(self, request, id):
        user = User.objects.get(pk=id)
        full_name = request.params['full_name'].split(' ')
        submitted_skills_ids = request.params['skills'].split('|')

        processed_skills_ids = []
        for s_id in submitted_skills_ids:
            if not s_id.isdigit():
                s = Skill()
                s.name = s_id
                s.save()
                s_id = s.id
            processed_skills_ids.append(s_id)

        new_data = request.params.copy()
        new_data['first_name'] = full_name[0]
        new_data['last_name'] = full_name[1]
        new_data.setlist('skills', processed_skills_ids)

        if request.params['user_active'] == "now":
            new_data['available_after'] = None

        form = UserModelForm(data=get_updated_data(user, new_data), files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            avatar = request.FILES.get('avatar', False)
            if avatar:
                img = Image.open(u'upload/user/avatar_' + str(user.id) + '.jpg')
                img.thumbnail(self.default_thumbnail_size, Image.ANTIALIAS)
                img.save(u'upload/user/avatar_' + str(user.id) + '.jpg')
        else:
            raise Exception(form.errors)

        return redirect("user-profile", id)


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'skills', "avatar", "profession", "motivation", "location", "available_after"]