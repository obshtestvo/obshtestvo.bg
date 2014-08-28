from django.conf.urls import patterns, include, url
from django.contrib import admin
from web.views import home, about, project, support, members, contact, faq, report, style
from login.views import login
from auth.views import extra_data, entry
from projects.views import dashboard, user, users, temp, invitations, answer
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about\.html$', about.AboutView.as_view(), name='about'),
    url(r'^elements$', style.StyleView.as_view(), name='styleguide'),
    url(r'^report\.html$', report.ReportView.as_view(), name='report'),
    url(r'^faq\.html$', faq.FaqView.as_view(), name='faq'),
    url(r'^support\.html$', support.SupportView.as_view(),
        name='support'),
    url(r'^members$', members.MembersView.as_view(), name='members'),
    url(r'^contact$', contact.ContactView.as_view(), name='contact'),
    url(r'^project/(?P<name>[^/]+)\.html$',
       project.ProjectView.as_view(),
       name='project'),
    url(r'', include('auth.urls', namespace='social')),
    url(r'^email/$', extra_data.ExtraDataView.as_view(), name='require_extra_data'),
    url(r'^logout/$', entry.LogoutView.as_view(), name='logout'),
    url(r'^join/$', login.LoginView.as_view(), name='join'),
    url(r'^user/(?P<id>\d+)$', user.UserView.as_view(), name='user'),
    url(r'^supplies/$', users.UsersView.as_view(), name='users'),
    url(r'^supplies/invitations/answer/$', invitations.AnswersView.as_view(), name='invitations'),
    url(r'^supplies/invitations/$', invitations.InvitationsView.as_view(), name='invitation_answer'),
    url(r'^temp/$', temp.TempView.as_view(), name='temp'),
    url(r'^dashboard/$', dashboard.DashboardView.as_view(), name='dash'),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )