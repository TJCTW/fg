from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from .models import SchoolInfo, ChurchInfo, GroupInfo, GroupMeetingTime, GroupWithSchool, GroupWithChurch, ContactReport, IssueReport
# Register your models here.



class GroupResource(resources.ModelResource):
    # school = fields.Field(
    #     column_name='school',
    #     attribute='school',
    #     widget=ForeignKeyWidget(SchoolInfo, 'name'))

    class Meta:
        model = GroupInfo
        # fields = ('name', 'group_type')
        # export_order = ('group_type', 'name')


class GroupWithSchoolResource(resources.ModelResource):
    group = fields.Field(
        column_name='group',
        attribute='group',
        widget=ForeignKeyWidget(GroupInfo, 'name'))
    group_type = fields.Field(
        column_name='group_type',
        attribute='group',
        widget=ForeignKeyWidget(GroupInfo, 'group_type'))
    school = fields.Field(
        column_name='school',
        attribute='school',
        widget=ForeignKeyWidget(SchoolInfo, 'name'))

    class Meta:
        model = GroupWithSchool


class GroupMeetingTimeInline(admin.TabularInline):
    model = GroupMeetingTime
    extra = 1


class GroupWithSchoolInline(admin.StackedInline):
    model = GroupWithSchool
    extra = 1


class GroupWithChurchInline(admin.StackedInline):
    model = GroupWithChurch
    extra = 1


class GroupInfoInline(admin.StackedInline):
    model = GroupInfo
    extra = 1

# Admin


class SchoolInfoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'local', 'city')
    list_filter = ('local', 'city')
    search_fields = ['name', 'local', 'city']


class GroupInfoAdmin(ImportExportModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    # resource_class = GroupWithSchoolResource
    list_display = ('id', 'name', 'group_type')
    search_fields = ['name']
    inlines = [GroupWithChurchInline,
               GroupWithSchoolInline, GroupMeetingTimeInline]


class ChurchInfoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'sec1', 'sec2')
    list_filter = ('sec1', 'sec2')
    search_fields = ['name', 'sec1', 'sec2']


class GroupMeetingTimeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'group', 'date', 'start_time',
                    'end_time', 'meeting_type', 'remark')
    list_filter = ('date', 'meeting_type')
    search_fields = ['group__name']


class GroupWithChurchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'group', 'church', 'church_sec1', 'church_sec2')
    list_filter = ('group', 'church', 'church__sec2', 'church__sec1')
    search_fields = ['group__name', 'church__name', 'church__sec2', 'church__sec1']

    def church_sec1(self, obj):
        return obj.church.sec1
    church_sec1.short_description = _('sec1')
    church_sec1.admin_order_field = 'church__sec1'

    def church_sec2(self, obj):
        return obj.church.sec2
    church_sec2.short_description = _('sec2')
    church_sec2.admin_order_field = 'church__sec2'


class GroupWithSchoolAdmin(ImportExportModelAdmin):
    # resource_class = GroupWithSchoolResource
    list_display = ('id', 'group', 'school', 'school_local', 'school_city')
    list_filter = ('group', 'school', 'school__city', 'school__local')
    search_fields = ['group__name', 'school__name', 'school__city', 'school__local']

    def school_local(self, obj):
        return obj.school.local
    school_local.short_description = _('local')
    school_local.admin_order_field = 'school__local'
    def school_city(self, obj):
        return obj.school.city
    school_city.short_description = _('city')
    school_city.admin_order_field = 'school__city'

class ContactReportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','school','name','reply_at','status','action_button')
    # list_filter = ('status')
    list_editable = ('status',)
    search_fields = ['name']
    actions = ['send_mail']
    @staticmethod
    def action_button(self):
        button_url="#"
        # assuming the url is saved as 'button_url'
        # enter the url to be parsed when the button will be clicked and name the button
        return format_html('<a class="button" href="%s">再次寄信</a>' % button_url)

    def send_mail(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully to send mail." % message_bit)
    send_mail.short_description = _("Send Mail")

class IssueReportAdmin(ImportExportModelAdmin):
    list_display = ('id','issue_type','content','reply_at','status')
    list_filter = ('issue_type', 'status')
    search_fields = ['issue_type','content','status']
    list_editable = ('status',)


admin.site.register(SchoolInfo, SchoolInfoAdmin)
admin.site.register(ChurchInfo, ChurchInfoAdmin)
admin.site.register(GroupInfo, GroupInfoAdmin)
admin.site.register(GroupWithSchool, GroupWithSchoolAdmin)
admin.site.register(GroupMeetingTime, GroupMeetingTimeAdmin)
admin.site.register(GroupWithChurch, GroupWithChurchAdmin)
admin.site.register(ContactReport,ContactReportAdmin)
admin.site.register(IssueReport,IssueReportAdmin)
