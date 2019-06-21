from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid


class ChurchInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    sec1 = models.CharField(max_length=20, verbose_name=_("sec1"))
    sec2 = models.CharField(max_length=20, verbose_name=_("sec2"))
    latitude = models.IntegerField(default=0, verbose_name=_("latitude"))
    longitude = models.IntegerField(default=0, verbose_name=_("longitude"))
    gps = models.IntegerField(default=0, verbose_name=_("gps"))
    address = models.CharField(max_length=200, verbose_name=_("address"))
    tel = models.CharField(max_length=20, blank=True,
                           null=True, verbose_name=_("tel"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("email"))
    remark = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("remark"))

    def __str__(self):
        return self.name
    def toDict(self):
        _dict = {self.id: {
            "sec1":self.sec1,
            "sec2":self.sec2,
            "name":self.name,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "gps":self.gps,
            "address":self.address,
            "tel":self.tel,
            "email":self.email,
            "remark":self.remark
            }
        }
        return _dict

    class Meta:
        verbose_name = _("Church info")
        verbose_name_plural = _("Church info")


class SchoolInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    nick_name = models.CharField(max_length=50, verbose_name=_("nick name"))
    local = models.CharField(max_length=20, verbose_name=_("local"))
    city = models.CharField(max_length=20, verbose_name=_("city"))

    def __str__(self):
        return self.name
    def toDict(self):
        _dict = {self.id: {
            "full_name":self.name,
            "nick_name":self.nick_name,
            "local":self.local,
            "city":self.city
            }
        }
        return _dict
    class Meta:
        verbose_name = _("School info")
        verbose_name_plural = _("School info")


class GroupInfo(models.Model):
    FELLOWSHIP = 'FELLOWSHIP'
    ADVANCED = 'ADVANCED'
    UNION = 'UNION'
    GROUP_TYPE_CHOICES = [
        (FELLOWSHIP, _("Fellowship")),
        (ADVANCED, _("Advanced")),
        (UNION, _("Union"))
    ]
    name = models.CharField(max_length=50, verbose_name=_("name"))
    group_type = models.CharField(
        max_length=10, verbose_name=_("type"), choices=GROUP_TYPE_CHOICES, default=FELLOWSHIP)
    tel = models.CharField(max_length=20, verbose_name=_(
        "tel"), blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name=_("email"))
    # schedule = models.FileField(upload_to='groups/'+uuid.value_from_object(uuid)+'/schedules', blank=True, null=True)
    # photo_1 = models.FileField(upload_to='groups/'+uuid.__str__()+'/photos', blank=True, null=True)
    # photo_2 = models.FileField(upload_to='groups/'+uuid.__str__()+'/photos', blank=True, null=True)
    # photo_3 = models.FileField(upload_to='groups/'+uuid.__str__()+'/photos', blank=True, null=True)
    remark = models.TextField(max_length=100, verbose_name=_(
        "remark"), blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    def toDict(self):
        _dict = {self.id: {
                "name":self.name,
                "tel":self.tel,
                "email":self.email,
                "type":self.group_type,
                "remark":self.remark
            }
        }
        return _dict
    class Meta:
        verbose_name = _("Group info")
        verbose_name_plural = _("Group info")


class GroupMeetingTime(models.Model):
    DATE_CHOICES = [
        ('SUN', _("SUN")),
        ('MON', _("MON")),
        ('TUE', _("TUE")),
        ('WED', _("WED")),
        ('THU', _("THU")),
        ('FRI', _("FRI")),
        ('SAT', _("SAT"))
    ]
    MEETING_TYPE_CHOICES = [
        ('REG', _("Regular")),
        ('BS', _("Bible Study")),
        ('OTHER', _("Other"))
    ]
    group = models.ForeignKey(
        GroupInfo, on_delete=models.CASCADE, verbose_name=_("group"))
    date = models.CharField(
        max_length=5, choices=DATE_CHOICES, verbose_name=_("date"))
    start_time = models.TimeField(
        blank=True, null=True, verbose_name=_("start time"))
    end_time = models.TimeField(
        blank=True, null=True, verbose_name=_("end time"))
    meeting_type = models.CharField(max_length=5, verbose_name=_(
        "meeting type"), choices=MEETING_TYPE_CHOICES, default='REG')
    remark = models.TextField(max_length=100, verbose_name=_(
        "remark"), blank=True, null=True)

    def __str__(self):
        return self.date
    def toDict(self):
        _dict = {self.id: {
            "date":self.date,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "meeting_type":self.meeting_type,
            "remark":self.remark
            }
        }
        return _dict
    class Meta:
        verbose_name = _("Group Meeting Time")
        verbose_name_plural = _("Group Meeting Time")


class GroupWithSchool(models.Model):
    group = models.ForeignKey(
        GroupInfo, on_delete=models.CASCADE, verbose_name=_("group"))
    school = models.ForeignKey(
        SchoolInfo, on_delete=models.CASCADE, verbose_name=_("school"))

    def __str__(self):
        return "%s with %s" % (self.group, self.school)

    class Meta:
        verbose_name = _("Group With School")
        verbose_name_plural = _("Group With School")


class GroupWithChurch(models.Model):
    group = models.ForeignKey(
        GroupInfo, on_delete=models.CASCADE, verbose_name=_("group"))
    church = models.ForeignKey(
        ChurchInfo, on_delete=models.CASCADE, verbose_name=_("church"))

    class Meta:
        verbose_name = _("Group With Church")
        verbose_name_plural = _("Group With Church")


    
class ContactReport(models.Model):
    GENDER_CHOICES = [
        ('MALE', _("MALE")),
        ('FEMALE', _("FEMALE"))
    ]
    STATUS_CHOICES = [
        ('UNP', _("Unprocessed")),
        ('PING', _("Processing")),
        ('PED', _("Processed")),
        ('O', _("Other"))
    ]
    group = models.CharField(max_length=50, verbose_name=_("suggestion group"))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, verbose_name=_("gender"))
    church = models.CharField(max_length=50,verbose_name=_("church"))
    school = models.CharField(max_length=50,verbose_name=_("school"))
    department = models.CharField(max_length=50, verbose_name=_("department"))
    phone = models.CharField(max_length=20, verbose_name=_("phone"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("email"))
    remark = models.TextField(verbose_name=_("remark"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNP', verbose_name=_("status"))
    reply_at = models.DateTimeField(auto_now_add=True, verbose_name=_("reply_at"))
    def __str__(self):
        return "%s. %s" % (self.id, self.name)
    class Meta:
        verbose_name = _("Contact Report")
        verbose_name_plural = _("Contact Report")

class IssueReport(models.Model):
    STATUS_CHOICES = [
        ('UNP', _("Unprocessed")),
        ('PING', _("Processing")),
        ('PED', _("Processed")),
        ('O', _("Other"))
    ]
    issue_type = models.CharField(max_length=20, verbose_name=_("issue type"))
    content = models.TextField(verbose_name=_("content"))
    name = models.CharField(max_length=20, verbose_name=_("name"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("email"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNP', verbose_name=_("status"))
    reply_at = models.DateTimeField(auto_now_add=True, verbose_name=_("reply_at"))
    def __str__(self):
        return "%s. %s" % (self.id, self.issue_type)
    class Meta:
        verbose_name = _("Issue Report")
        verbose_name_plural = _("Issue Report")