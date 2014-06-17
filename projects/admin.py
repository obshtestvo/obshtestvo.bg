from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.forms import ModelForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from suit.widgets import *
from pagedown.widgets import AdminPagedownWidget
from .models import *
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import reversion
from suit.admin import SortableTabularInline, SortableModelAdmin
from django.db import models
from django.templatetags.static import static
from django.utils.html import urlize, format_html
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters

from guardian.models import UserObjectPermission, GroupObjectPermission
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
@receiver(post_save, sender=User)
def user_perobject_permissions(sender, instance, created, **kwargs):
    if created:
        assign_perm('change_user', instance, instance)


@receiver(pre_delete, sender=User)
def remove_user_perobject_permissions(sender, instance, **kwargs):
    UserObjectPermission.objects.filter(user_id=instance.pk).delete()


def prepare_lookup_value(key, value):
    if key.endswith('__in') and type(value) == 'str':
        value = value.split(',')
    if key.endswith('__isnull'):
        value = not (value.lower() in ('', 'false', '0'))
    return value


class MultipleFilter(admin.RelatedFieldListFilter):
    # title = _('skills')
    # parameter_name = 'skills'
    template = 'admin/filter_multiple.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(MultipleFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.lookup_val = request.GET.getlist(self.lookup_kwarg, None)
        self.used_parameters = {}
        for p in self.expected_parameters():
            if p in request.GET:
                value = request.GET.getlist(p) if self.lookup_kwarg == p else request.GET.get(p)
                self.used_parameters[p] = prepare_lookup_value(p, value)

    def queryset(self, request, queryset):
        try:
            if self.lookup_kwarg in self.used_parameters:
                for lookup in self.used_parameters[self.lookup_kwarg]:
                    value = {self.lookup_kwarg: lookup}
                    queryset = queryset.filter(**value)
            else:
                queryset.filter(**self.used_parameters)
            return queryset
        except ValidationError as e:
            raise IncorrectLookupParameters(e)

    def choices(self, cl):
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        yield {
            'selected': self.lookup_val is None and not self.lookup_val_isnull,
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        for pk_val, val in self.lookup_choices:
            yield {
                'selected': smart_text(pk_val) in self.lookup_val,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: pk_val,
                }, [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if (isinstance(self.field, models.related.RelatedObject)
                and self.field.field.null or hasattr(self.field, 'rel')
                    and self.field.null):
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': EMPTY_CHANGELIST_VALUE,
            }



def close_link(instance):
    if not instance.id:
        return ''
    url = reverse('admin:%s_%s_change' % (
        instance._meta.app_label,  instance._meta.module_name),  args=[instance.id] ) + 'tools/' + 'toolfunc'
    return mark_safe(u'<a href="{u}">Close</a>'.format(u=url))


def avatar(obj):
    if (obj.facebook):
        url = u'http://graph.facebook.com/%s/picture?width=40&amp;height=40' % obj.facebook.split('=' if 'profile.php' in obj.facebook else '/')[-1]
    else:
        url = static('img/user-silhouette.png')
    return mark_safe(u'<img width="40" height="40" src="%s" />' % url)


# from guardian.admin import GuardedModelAdmin
class UserActivityInline(admin.TabularInline):
    model = UserActivity
    suit_classes = 'suit-tab suit-tab-activities'
    extra = 1

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    inlines = (UserActivityInline,)
    add_form = MyUserCreationForm
    list_filter = (('skills', MultipleFilter), ('projects_interests', MultipleFilter))
    list_display = ('full_name_display', 'email', 'available_after', 'skills_display', 'projects_interests_display')
    ordering = ('first_name',)
    suit_form_tabs = (
        ('system', 'System'),
        ('common', 'Common'),
        ('activities', 'Activities'),
    )
    def skills_display(self, user):
        result = ''
        for s in user.skills.all():
            result += '<span class="badge">'+s.name+'</span> '
        return mark_safe(result)
    skills_display.short_description = _('skills')

    def projects_interests_display(self, user):
        result = ''
        for p in user.projects_interests.all():
            result += '<span class="label label-info">'+p.name+'</span> '
        return mark_safe(result)
    skills_display.short_description = _('projects interested in')

    def full_name_display(self, user):
        return user.get_full_name()
    full_name_display.short_description = _('full name')

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-system',),
            'fields': ('username', 'password')}
        ),
        (_('Personal info'), {
            'classes': ('suit-tab suit-tab-system',),
            'fields': ('first_name', 'last_name', 'email')}
        ),
        (_('Permissions'), {
            'classes': ('suit-tab suit-tab-system',),
            'fields': ('is_active', 'is_browsable', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')

        }),
        (_('Important dates'), {
            'classes': ('suit-tab suit-tab-system',),
            'fields': ('last_login', 'date_joined')}
        ),
        (_('Custom'), {
            'classes': ('suit-tab suit-tab-common',),
            'fields': ('is_available', 'available_after', 'bio', 'avatar')}
        ),
    )


class ProjectActivityFrom(ModelForm):
    class Meta:
        widgets = {
            'can_accomodate': EnclosedInput(append='icon-user', attrs={'class': 'input-mini'}),
        }

class ProjectActivityInline(SortableTabularInline):
    model = ProjectActivity
    suit_classes = 'suit-tab suit-tab-activities'
    sortable = 'order'
    extra = 0
    form = ProjectActivityFrom

    def advanced(self, instance):
        if not instance.id:
            return ''
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.id] )
        return mark_safe(u'<a href="{u}">Edit</a>'.format(u=url) + ' ' + close_link(instance))

    readonly_fields = ('advanced',)

class TaskInline(SortableTabularInline):
    model = Task
    suit_classes = 'suit-tab suit-tab-tasks'
    sortable = 'order'
    extra = 0


class ProjectMotiveInline(SortableTabularInline):
    model = ProjectMotive
    suit_classes = 'suit-tab suit-tab-motives'
    sortable = 'order'
    extra = 0


class ProjectMilestoneFrom(ModelForm):
    class Meta:
        widgets = {
            # 'percent': RangeInput(append='%', attrs={"min":1, "max":100}),
            'percent': EnclosedInput(append='%', attrs={'class': 'input-mini'}),
            'target_date': forms.TextInput(attrs={'class': 'input-mini'}),
        }

class ProjectMilestoneInline(SortableTabularInline):
    form = ProjectMilestoneFrom
    model = ProjectMilestone
    suit_classes = 'suit-tab suit-tab-milestones'
    sortable = 'order'
    extra = 0



class ProjectUsageExampleStepForm(ModelForm):
    class Meta:
        widgets = {
            # 'percent': RangeInput(append='%', attrs={"min":1, "max":100}),
            'example_number': EnclosedInput(attrs={'class': 'input-mini'}),
            'icon':EnclosedInput(append='icon-heart', attrs={'class': 'input-mini'}),
        }


class ProjectUsageExampleStepInline(SortableTabularInline):
    model = ProjectUsageExampleStep
    suit_classes = 'suit-tab suit-tab-usage-examples'
    sortable = 'order'
    extra = 0
    form = ProjectUsageExampleStepForm

class RangeInput(EnclosedInput):
    """HTML5 Range Input."""
    input_type = 'range'

class ProjectAdminForm(ModelForm):
    class Meta:
        widgets = {
            'url': EnclosedInput(prepend='icon-globe'),
            'pm_url': EnclosedInput(prepend='icon-globe'),
            'facebook_group': EnclosedInput(prepend='icon-globe'),
            'github_repo': EnclosedInput(prepend='icon-globe'),
            'strategy': AdminPagedownWidget(),
            'description': AdminPagedownWidget()
        }

class ProjectAdmin(reversion.VersionAdmin, SortableModelAdmin):
    list_display = ('name',)
    sortable = 'order'
    form = ProjectAdminForm
    search_fields = ['name']
    list_filter = ['is_featured']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProjectActivityInline,
        ProjectMotiveInline,
        ProjectUsageExampleStepInline,
        ProjectMilestoneInline,
    ]
    suit_form_tabs = (
        ('general', 'General'),
        ('strategy', 'Strategy'),
        ('description', 'Description'),
        # ('advanced', 'Advanced Settings'),
        ('activities', 'Activities'),
        ('milestones', 'Milestones'),
        ('motives', 'Motives'),
        ('usage-examples', 'Usage examples steps'),
    )
    formfield_overrides = {
        models.TextField: {'widget': AutosizedTextarea(attrs={'rows':2, 'cols':50})},
    }
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'slug', 'url',  'short_description', 'is_forced_active','is_public','has_static_page',)
        }),
        ('Management', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('pm_url', 'facebook_group', 'github_repo',)
        }),
        ('Media', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': (
                'logo',
                'logo_styled',
                'logo_thumb',
                'cover_image',
                'complimenting_color',
            )
        }),
        ('Homepage', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('is_featured',)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-strategy',),
            'fields': ('strategy',)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-description',),
            'fields': (
                'description',
            )}
        ),
    )


class SkillGroupAdmin(SortableModelAdmin):
    list_display = ('name',)
    sortable = 'order'

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ProjectActivityAdminBase(admin.ModelAdmin):
    inlines = (UserActivityInline, TaskInline)

    def tools(self, instance):
        return close_link(instance)

    list_display = ('name', 'project', 'tools')

    def toolfunc(self, request, obj):
        pass
    toolfunc.label = "Close"  # optional
    toolfunc.short_description = "This will be the tooltip of the button"  # optional
    hobjectactions = ('toolfunc', )


class ProjectActivityAdmin(ProjectActivityAdminBase, reversion.VersionAdmin):
    suit_form_tabs = (
        ('general', 'General'),
        ('tasks', 'Tasks'),
        ('activities', 'User activities'),
    )

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'project',)
        }),
        ('Settings', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('is_organisational', 'is_template', 'can_accomodate', )
        }),
    )

# template, prepopulated forms:
# http://stackoverflow.com/questions/2223375/multiple-modeladmins-views-for-same-model-in-django-admin
# http://stackoverflow.com/questions/936376/prepopulate-django-non-model-form
class ProjectActivityTemplate(ProjectActivity):
    class Meta:
        proxy = True

class ProjectActivityTemplateForm(forms.ModelForm):
    class Meta:
        model = ProjectActivityTemplate
    is_template = forms.BooleanField(widget=forms.HiddenInput(), initial=1)
    order = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

class ProjectActivityTemplateAdmin(ProjectActivityAdminBase):
    form = ProjectActivityTemplateForm
    inlines = []
    fields = ('name', 'is_organisational', 'can_accomodate', 'order', 'is_template',)
    def queryset(self, request):
        return self.model.objects.filter(is_template=True)


class MemberAdminFrom(forms.ModelForm):
    class Meta:
        widgets = {
            'facebook':EnclosedInput(prepend='icon-share'),
            'email':EnclosedInput(prepend='icon-envelope'),
            # 'types': autocomplete_light.MultipleChoiceWidget(autocomplete='MemberTypeAutocomplete'),
            # 'skills': autocomplete_light.MultipleChoiceWidget(autocomplete='SkillAutocomplete'),
            # 'projects_interests': autocomplete_light.MultipleChoiceWidget(autocomplete='ProjectAutocomplete'),
        }

class MemberAdmin(admin.ModelAdmin):
    model = Member
    form = MemberAdminFrom
    ordering = ('name',)
    search_fields = ['name']
    list_filter = ('projects_interests', ('skills', MultipleFilter),'types', 'last_contacted_at')
    list_display = (avatar, 'name', 'facebook_as_link', 'email', 'skills_display')
    suit_form_tabs = (
        ('general', _('General')),
        ('specifics', _('Specifics')),
        # ('integration', _('System')),
    )
    formfield_overrides = {
        models.TextField: {'widget': AutosizedTextarea(attrs={'rows':2, 'cols':50})},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.DateField: {'widget': SuitDateWidget},
    }
    def skills_display(self, member):
        return ', '.join([obj.name for obj in member.skills.all()])
    skills_display.short_description = _('skills')

    def facebook_as_link(self, obj):
        return format_html(urlize(obj.facebook))
    facebook_as_link.short_description = 'Facebook'

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'facebook', 'email', 'date_joined',)
        }),
        (_('Expectations'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ( 'availability', 'available_after', )
        }),
        (_("Member's preferences"), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('skills', 'types', 'projects_interests','offered_help', )
        }),
        (_('Self-description & Comments'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('intro', 'comment')
        }),
        (_('Communication'), {
            'classes': ('suit-tab suit-tab-specifics',),
            'fields': ('last_contacted_at', 'latest_answer', 'contact_frequency', )
        }),
        # ('User', {
        #     'classes': ('suit-tab suit-tab-integration',),
        #     'fields': ('user', 'update_from_user')
        # }),
    )



# from guardian.admin import GuardedModelAdmin
class UpdateInline(GenericTabularInline):
    model = Update
    suit_classes = 'suit-tab suit-tab-updates'
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': AutosizedTextarea(attrs={'rows':1, 'cols':100})},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.DateField: {'widget': SuitDateWidget},
    }

class OrganisationAdmin(admin.ModelAdmin):
    model = Organisation
    inlines = (UpdateInline,)
    list_filter = ('middlemen',('types', MultipleFilter))
    list_display = ('name','representatives', 'types_display')
    search_fields = ['name']
    suit_form_tabs = (
        ('general', _('General')),
        ('updates', _('Updates')),
    )
    formfield_overrides = {
        models.TextField: {'widget': AutosizedTextarea(attrs={'rows':3, 'cols':70})},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.DateField: {'widget': SuitDateWidget},
    }
    def types_display(self, org):
        return ', '.join([obj.name for obj in org.types.all()])
    types_display.short_description = _('relation type')

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'types','strategy')
        }),
        (_('Contact'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('middlemen', 'representatives', 'contact', )
        }),
        (_('About'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('comment', 'found_via', 'working_with', )
        }),
        (_('Partner'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('partnered_project', 'provided_help',)
        }),
    )


class SponsorOrg(Organisation):
    class Meta:
        proxy = True
        verbose_name = Organisation._meta.verbose_name
        verbose_name_plural = Organisation._meta.verbose_name

class SponsorOrgAdmin(OrganisationAdmin):
    def has_add_permission(self, request):
        return False
    def queryset(self, request):
        return self.model.objects.filter(types__id=2)


class PartnerOrg(Organisation):
    class Meta:
        proxy = True
        verbose_name = Organisation._meta.verbose_name
        verbose_name_plural = Organisation._meta.verbose_name

class PartnerOrgAdmin(OrganisationAdmin):
    def has_add_permission(self, request):
        return False
    def queryset(self, request):
        return self.model.objects.exclude(partnered_project=None)


class AvailableMember(Member):
    class Meta:
        proxy = True
        verbose_name = Member._meta.verbose_name
        verbose_name_plural = Member._meta.verbose_name

class AvailableMemberAdmin(MemberAdmin):
    def has_add_permission(self, request):
        return False
    def queryset(self, request):
        return self.model.objects.filter(availability=Member.AVAILABLE)


class PaidMember(Member):
    class Meta:
        proxy = True
        verbose_name = Member._meta.verbose_name
        verbose_name_plural = Member._meta.verbose_name

class PaidMemberAdmin(MemberAdmin):
    def has_add_permission(self, request):
        return False
    def queryset(self, request):
        return self.model.objects.filter(availability=Member.ONLY_PAID)


class ReaderMember(Member):
    class Meta:
        proxy = True
        verbose_name = Member._meta.verbose_name
        verbose_name_plural = Member._meta.verbose_name

class ReaderMemberAdmin(MemberAdmin):
    def has_add_permission(self, request):
        return False
    def queryset(self, request):
        return self.model.objects.filter(availability=Member.ONLY_READER)



class EventAdmin(admin.ModelAdmin):
    model = Event
    ordering = ('name',)
    search_fields = ['name']
    list_filter = ('date', ('organizers', MultipleFilter))
    list_display = ('name', 'date')
    suit_form_tabs = (
        ('general', _('General')),
        # ('integration', _('System')),
    )
    formfield_overrides = {
        models.TextField: {'widget': AutosizedTextarea(attrs={'rows':2, 'cols':60})},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.DateField: {'widget': SuitDateWidget},
    }
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ('name', 'date', 'contact')
        }),
        (_('details'), {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ( 'strategy', 'organizers', 'comment')
        }),
    )

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(SponsorOrg, SponsorOrgAdmin)
admin.site.register(PartnerOrg, PartnerOrgAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ReaderMember, ReaderMemberAdmin)
admin.site.register(AvailableMember, AvailableMemberAdmin)
admin.site.register(PaidMember, PaidMemberAdmin)
admin.site.register(OrganisationType)
admin.site.register(MemberType)
admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillGroup, SkillGroupAdmin)
admin.site.register(UserProjectPause)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(ProjectActivityTemplate, ProjectActivityTemplateAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(UserActivity)
