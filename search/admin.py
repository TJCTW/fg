from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import SchoolInfo, ChurchInfo, GroupInfo, GroupMeetingTime, GroupWithSchool, GroupWithChurch
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


class GroupWithChurchAdmin(ImportExportModelAdmin):
    list_display = ('id', 'group', 'church')
    list_filter = ('group', 'church')
    search_fields = ['group__name', 'church__name']


class GroupWithSchoolAdmin(ImportExportModelAdmin):
    # resource_class = GroupWithSchoolResource
    list_display = ('id', 'group', 'school')
    search_fields = ['group__name', 'school__name']


admin.site.register(SchoolInfo, SchoolInfoAdmin)
admin.site.register(ChurchInfo, ChurchInfoAdmin)
admin.site.register(GroupInfo, GroupInfoAdmin)
admin.site.register(GroupWithSchool, GroupWithSchoolAdmin)
admin.site.register(GroupMeetingTime, GroupMeetingTimeAdmin)
admin.site.register(GroupWithChurch, GroupWithChurchAdmin)
