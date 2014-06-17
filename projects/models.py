from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from guardian.shortcuts import assign_perm
from django.utils import timezone
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation, ContentType
# from django.contrib.contenttypes.models import ContentType
# from django.db.models import Q


# def remove_perobject_permissions(sender, instance, **kwargs):
#     filters = Q(content_type=ContentType.objects.get_for_model(instance),
#                 object_pk=instance.pk)
#     UserObjectPermission.objects.filter(filters).delete()
#     GroupObjectPermission.objects.filter(filters).delete()


class Event(models.Model):
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
    name = models.CharField(_('name'), max_length=200,)
    date = models.DateField(_('date'), blank=True, null=True)
    organizers = models.ManyToManyField('Organisation', related_name="events", blank=True, verbose_name=_("organizers"))
    contact = models.TextField(_('contact info'), blank=True)
    comment = models.TextField(_('comment'), blank=True)
    strategy = models.TextField(_('strategy'), blank=True)



class Update(models.Model):
    class Meta:
        verbose_name = _('update')
        verbose_name_plural = _('updates')
    change = models.TextField(_('change'), blank=True)
    date = models.DateTimeField(_('date'), default=timezone.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name


class Organisation(models.Model):
    class Meta:
        verbose_name = _('organisation')
        verbose_name_plural = _('organisations')
    name = models.CharField(_('name'), max_length=200,)
    strategy = models.TextField(_('strategy'), blank=True)
    middlemen = models.ManyToManyField('Member', related_name="middleman_organisations", blank=True,null=True,
                                      verbose_name=_("middle men"))
    representatives = models.CharField(_('Representative'), max_length=30, blank=True)

    found_via = models.CharField(_('Found via'), max_length=30, blank=True)
    contact = models.TextField(_('contact info'), blank=True)
    comment = models.TextField(_('comment'), blank=True)
    working_with = models.TextField(_('Also working with'), blank=True)
    types = models.ManyToManyField('OrganisationType', related_name="organisations", blank=True, verbose_name=_("Type of organisation"))
    updates = GenericRelation(Update, verbose_name=_("Updates"), blank=True)

    partnered_project = models.ForeignKey('Project', related_name="partners", blank=True, null=True, verbose_name=_("partnered project"))
    provided_help = models.TextField(_('Provided help'), blank=True)

    def __unicode__(self):
        return self.name


class OrganisationType(models.Model):
    class Meta:
        verbose_name = _('organisation type')
        verbose_name_plural = _('organisation types')
    name = models.CharField(_('name'), max_length=200,)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    class Meta:
        verbose_name = _('skill')
        verbose_name_plural = _('skills')
        ordering = ['id']
    name = models.CharField(_('name'), max_length=200,)
    groups = models.ManyToManyField('SkillGroup', related_name="skills", blank=True, verbose_name=_("groups"))


    def __unicode__(self):
        return self.name

class SkillGroup(models.Model):
    class Meta:
        verbose_name = _('skill group')
        verbose_name_plural = _('skill groups')
        ordering = ['order']
    name = models.CharField(_('name'), max_length=200,)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

class MemberType(models.Model):
    class Meta:
        verbose_name = _('member type')
        verbose_name_plural = _('member types')
    name = models.CharField(_('name'), max_length=200,)

    def __unicode__(self):
        return self.name

class Member(models.Model):
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
    DAILY = 'd'
    WEEKLY = 'w'
    EVERY_TWO_WEEKS = '2w'
    EVERY_MONTH = '1m'
    EVERY_QUARTER = '2w'
    CONTACT_FREQUENCY_CHOICE = (
        (DAILY, _('Almost every day')),
        (WEEKLY, _('Once a week')),
        (EVERY_TWO_WEEKS, _('Every two weeks')),
        (EVERY_MONTH, _('Once a month')),
        (EVERY_QUARTER, _('Once a couple of months')),
    )
    ONLY_READER = 'reader'
    ONLY_PAID = 'paid_only'
    AVAILABLE = 'available'
    AVAILABILITY_CHOICE = (
        (AVAILABLE, _('Available')),
        (ONLY_PAID, _('Member will work but not volunteer')),
        (ONLY_READER, _('Member only looking')),
    )
    projects_active = models.ManyToManyField('Project', blank=True, related_name="active_members", verbose_name=_("Working on projects"))
    availability = models.CharField(max_length=20,
                                      choices=AVAILABILITY_CHOICE,
                                      default=ONLY_READER,
                                      verbose_name=_("Availability"))

    user = models.ForeignKey('User', related_name="member", blank=True, null=True)
    update_from_user = models.BooleanField(_('Daily sync from associated user?'), default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    name = models.CharField(_('name'), max_length=30, blank=False)
    email = models.EmailField(_('email address'), blank=True)
    facebook = models.CharField(_('facebook profile'), max_length=255, blank=True)
    working_on = models.ForeignKey('Project', related_name="working_members", blank=True, null=True, verbose_name=_("working on"))
    skills = models.ManyToManyField('Skill', related_name="members", blank=True,
                                      verbose_name=_("skills"))

    intro = models.TextField(_('intro'), blank=True)
    comment = models.TextField(_('comment'), blank=True)
    offered_help = models.TextField(_('Type of helped offered'),
                                    blank=True,
                                    help_text=_("If it's a consultant or other non-member, you can add some description here"))

    is_available = models.BooleanField(_('Available for work?'), default=False)
    available_after = models.DateField(_('available after'), blank=True, null=True)

    last_contacted_at = models.DateField(_('last contact'), blank=True, null=True)
    latest_answer = models.TextField(_('latest answer'), blank=True)
    contact_frequency = models.CharField(max_length=2,
                                      choices=CONTACT_FREQUENCY_CHOICE,
                                      default=DAILY,
                                      verbose_name=_("Contact frequency"))

    is_paid_only = models.BooleanField(_('Paid only'), default=False)
    types = models.ManyToManyField('MemberType', related_name="members", blank=True, verbose_name=_("Relation to Obshtestvo"))
    projects_interests = models.ManyToManyField('Project', blank=True, related_name="interested_members", verbose_name=_("Projects interested in"))

    def __unicode__(self):
        return self.name

    def sync_with(self, user):
        pass

    def override(self, user):
        pass

    def fill_gaps_to(self, user):
        pass

    def fill_gaps_from(self, user):
        pass

def user_file_name(instance, filename):
    return '/'.join(['user', filename])

class User(AbstractUser):
    is_browsable = models.BooleanField(_('Is this a user you can browse amongst others'), default=True)
    is_available = models.BooleanField(_('Is the user available for work'), default=True)
    available_after = models.DateField(_('available after'), blank=True, null=True)
    has_confirmed_data = models.BooleanField(_('has confirmed custom data'), default=True)
    bio = models.TextField(_('biography'), blank=True, null=True)
    avatar = models.FileField(_('avatar'), upload_to=user_file_name, blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name="users", blank=True,
                                      verbose_name=_("skills"))
    projects_interests = models.ManyToManyField('Project', blank=True, related_name="interested_users", verbose_name=_("Projects that user's interested in"))

    def get_avatar(self):
        src = None
        if self.avatar:
            src = settings.MEDIA_URL + self.avatar.url()
        else:
            uid = settings.SOCIAL_AUTH_FACEBOOK_KEY
            if self.social_auth.all().count() > 0:
                uid = self.social_auth.all()[0].uid
            src = 'http://graph.facebook.com/' + uid + '/picture'
        return src

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        abstract = False

class UserPointSpending(models.Model):
    person = models.ForeignKey('User', related_name="spendings")
    points = models.PositiveIntegerField(_('points'), max_length=10)
    product = models.CharField(_('product'), max_length=30, blank=False)

class UserActivity(models.Model):
    person = models.ForeignKey('User', related_name="activities")
    project_activity = models.ForeignKey('ProjectActivity',
                                         related_name="user_activities")
    progress = models.IntegerField(_('progress made'), max_length=3)
    is_active = models.BooleanField(_('active'), default=True)
    last_stopped_at = models.DateTimeField(_('last time user stopped working on this'),
                                           blank=True, null=True)
    needs_replacement = models.BooleanField(_('user needs replacement'), default=False)

    class Meta:
        unique_together = ('person', 'project_activity',)
        verbose_name_plural = "User Activities"

    def __unicode__(self):
        return unicode(self.person.get_full_name() + ' on ' + self.project_activity.name)


# @receiver(post_save, sender=UserActivity)
# def user_activity_perobject_permissions(sender, instance, **kwargs):
#     assign_perm('change_useractivity', instance.person, instance)
#     assign_perm('add_useractivity', instance.person, instance)


# pre_delete.connect(remove_perobject_permissions, UserActivity)

def project_file_name(instance, filename):
    return '/'.join(['project', filename])


class Project(models.Model):
    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['order']
    name = models.CharField(_('name'), max_length=140, blank=False)
    strategy = models.TextField(_('strategy'), blank=True)
    description = models.TextField(_('description'), blank=True)
    short_description = models.TextField(_('short description'), blank=True)

    facebook_group = models.CharField(_('facebook group'), max_length=255, blank=True)
    github_repo = models.CharField(_('github repository'), max_length=255, blank=True)
    pm_url = models.CharField(_('project management URL'), max_length=255, blank=True)
    url = models.CharField(_('url'), max_length=255, blank=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    is_featured = models.BooleanField(_('Is featured'), default=False)
    is_forced_active = models.BooleanField(_('Is active (forced)'), default=False)
    has_static_page = models.BooleanField(_('Does it have a static page'), default=False)
    is_public = models.BooleanField(_('Is public'), default=True)

    logo = models.FileField(_('logo'), upload_to=project_file_name, blank=True)
    logo_styled = models.FileField(_('logo styled to fit obshtestvo.bg'), upload_to=project_file_name, blank=True)
    logo_thumb = models.FileField(_('logo fit for usage in square-image gallery'), upload_to=project_file_name, blank=True, null=True)
    cover_image = models.FileField(_('cover image'), upload_to=project_file_name, blank=True)
    complimenting_color = models.CharField(_('color that matches the style of the logo'), max_length=7, blank=True)
    order = models.PositiveIntegerField()

    def users(self):
        return User.objects.exclude(pauses__project=self).filter(
            project_activities__project=self,
            project_activities__user_activities__is_active=True).distinct()

    def get_logo_thumb(self):
        if self.logo_thumb:
            return self.logo_thumb.url

    def __unicode__(self):
        return unicode(self.name)

    # when fully implemented this function should consider how many people joined the project
    # and whether the project has an "owner"
    def is_active(self):
        return self.is_forced_active

class ProjectMilestone(models.Model):
    class Meta:
        verbose_name = _('project milestone')
        verbose_name_plural = _('project milestones')
    project = models.ForeignKey('Project', related_name="milestones")
    description = models.TextField(_('description'))
    target_date = models.CharField(_('target date'), max_length=255, blank=True)
    date = models.DateField(_('actual date happened'), blank=True, null=True)
    is_done = models.BooleanField(_('done'), default=False)
    is_technical = models.BooleanField(_('technical'), default=False)
    percent = models.PositiveIntegerField(_('Show at'), max_length=3)
    order = models.PositiveIntegerField()




class UserProjectPause(models.Model):
    project = models.ForeignKey('Project', related_name="pauses")
    person = models.ForeignKey('User', related_name="pauses")

    class Meta:
        unique_together = ('project', 'person',)


# @receiver(post_save, sender=UserProjectPause)
# def user_pause_perobject_permissions(sender, instance, **kwargs):
#     assign_perm('add_userprojectpause', instance.person, instance)
#     assign_perm('delete_userprojectpause', instance.person, instance)
#     assign_perm('change_userprojectpause', instance.person, instance)


# pre_delete.connect(remove_perobject_permissions, UserProjectPause)


class ProjectActivity(models.Model):
    project = models.ForeignKey('Project', related_name="activities", blank=True, null=True)
    users = models.ManyToManyField('User', through='UserActivity',
                                   related_name="project_activities")
    name = models.CharField(_('name'), max_length=140, blank=False)
    is_organisational = models.BooleanField(_('organisation related'),
                                            default=False)
    is_template = models.BooleanField(_('template activity'),
                                            default=False)
    can_accomodate = models.IntegerField(_('Max people'),
                                         max_length=3, default=1)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('project activity')
        verbose_name_plural = _('project activities')

    def __unicode__(self):
        return unicode(self.name)


class ProjectMotive(models.Model):
    class Meta:
        verbose_name = _('project motive')
        verbose_name_plural = _('project motives')
    project = models.ForeignKey('Project', related_name="motives")
    title = models.CharField(_('name'), max_length=30, blank=False)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.title)


class ProjectUsageExampleStep(models.Model):
    class Meta:
        verbose_name = _('project usage example step')
        verbose_name_plural = _('project usage example steps')
    project = models.ForeignKey('Project', related_name="example_steps")
    title = models.CharField(_('name'), max_length=140, blank=False)
    order = models.PositiveIntegerField()
    icon = models.CharField(_('icon'), max_length=30, blank=False)
    example_number = models.PositiveIntegerField(_('Example number'))

    def __unicode__(self):
        return unicode(self.title)


class Task(models.Model):
    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
    activity = models.ForeignKey('ProjectActivity', related_name="tasks")
    name = models.CharField(_('name'), max_length=30, blank=False)
    points = models.PositiveIntegerField(_('points'), max_length=4, default=5)
    is_complete = models.BooleanField(_('is this complete'), default=False)
    order = models.PositiveIntegerField()


    # return RecycleSpot.objects.select_related("type").filter(materials__name__in=types).only(*cls.FIELDS).distinct()
    # return RecycleSpot.objects.select_related("type").filter(materials__name__in=types).only(*cls.FIELDS).distinct()

    # ref: https://docs.djangoproject.com/en/dev/ref/models/queries/
    # ref: https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.select_related
    # .select_related('blog')