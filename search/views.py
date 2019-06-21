from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import GroupInfo, ChurchInfo, SchoolInfo, GroupMeetingTime, GroupWithChurch, GroupWithSchool, ContactReport, IssueReport
from .notices import send_issue_report, send_contact_report
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, 'index.html')


def search(request):
    return render(request, 'search.html')


def result(request):
    # school = request.GET['school']
    church = request.GET['church']
    response = "You're looking at the results of church %s."
    return HttpResponse(response % church)


def church(request, church_id):
    response = "You're looking at the results of church %s."
    return HttpResponse(response % church_id)


def school(request, school_id):
    response = "You're looking at the results of school %s."
    return HttpResponse(response % school_id)


def group(request, group_id):
    response = ""
    group_json = {}
    try:
        group = GroupInfo.objects.get(pk=group_id)
        group_json = group.toDict()
    except GroupInfo.DoesNotExist:
        raise Http404("Group does not exist")

    school_jsons = {}
    try:
        groupWithSchools = GroupWithSchool.objects.filter(group=group)
        for groupWithSchool in groupWithSchools:
            school_info = groupWithSchool.school
            school_json = school_info.toDict()
            school_jsons.update(school_json)
    except GroupWithSchool.DoesNotExist:
        raise Http404("Group with school does not exist")

    church_jsons = {}
    try:
        groupWithChurchs = GroupWithChurch.objects.filter(group=group)
        for groupWithChurch in groupWithChurchs:
            church_info = groupWithChurch.church
            church_json = church_info.toDict()
            church_jsons.update(church_json)
    except GroupWithChurch.DoesNotExist:
        raise Http404("Group with church does not exist")

    meeting_time_jsons = {}
    try:
        groupMeetingTimes = GroupMeetingTime.objects.filter(group=group)
        for groupMeetingTime in groupMeetingTimes:
            meeting_time_json = groupMeetingTime.toDict()
            meeting_time_jsons.update(meeting_time_json)
    except GroupMeetingTime.DoesNotExist:
        raise Http404("Group meeting time does not exist")

    group_json[group.id]["school"] = school_jsons
    group_json[group.id]["church"] = church_jsons
    group_json[group.id]["metting"] = meeting_time_jsons
    response = group_json

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
    # context ={'group': group,'groupMeetingTimes':groupMeetingTimes,'groupWithSchools':groupWithSchools,'groupWithChurchs':groupWithChurchs}
    # response = "You're looking at the results of group %s."
    # return render(request, 'group.html', context)


def allGroup(request):
    group_jsons = {}
    try:
        groups = GroupInfo.objects.all()
        for group in groups:
            group_json = group.toDict()
            school_jsons = {}
            try:
                groupWithSchools = GroupWithSchool.objects.filter(group=group)
                for groupWithSchool in groupWithSchools:
                    school_info = groupWithSchool.school
                    school_json = school_info.toDict()
                    school_jsons.update(school_json)
            except GroupWithSchool.DoesNotExist:
                raise Http404("Group with school does not exist")

            church_jsons = {}
            try:
                groupWithChurchs = GroupWithChurch.objects.filter(group=group)
                for groupWithChurch in groupWithChurchs:
                    church_info = groupWithChurch.church
                    church_json = church_info.toDict()
                    church_jsons.update(church_json)
            except GroupWithChurch.DoesNotExist:
                raise Http404("Group with church does not exist")

            meeting_time_jsons = {}
            try:
                groupMeetingTimes = GroupMeetingTime.objects.filter(
                    group=group)
                for groupMeetingTime in groupMeetingTimes:
                    meeting_time_json = groupMeetingTime.toDict()
                    meeting_time_jsons.update(meeting_time_json)
            except GroupMeetingTime.DoesNotExist:
                raise Http404("Group meeting time does not exist")

            group_json[group.id]["school"] = school_jsons
            group_json[group.id]["church"] = church_jsons
            group_json[group.id]["metting"] = meeting_time_jsons
            group_jsons.update(group_json)
    except GroupInfo.DoesNotExist:
        raise Http404("Group does not exist")
    response = group_jsons

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def allChurch(request):
    church_jsons = {}
    try:
        churchs = ChurchInfo.objects.all()
        for church in churchs:
            church_json = church.toDict()

            group_jsons = {}
            try:
                groupWithChurchs = GroupWithChurch.objects.filter(
                    church=church)
                for groupWithChurch in groupWithChurchs:
                    group = groupWithChurch.group
                    group_json = group.toDict()
                    school_jsons = {}
                    try:
                        groupWithSchools = GroupWithSchool.objects.filter(
                            group=group)
                        for groupWithSchool in groupWithSchools:
                            school_info = groupWithSchool.school
                            school_json = school_info.toDict()
                            school_jsons.update(school_json)
                    except GroupWithSchool.DoesNotExist:
                        raise Http404("Group with school does not exist")
                    group_json[group.id]["school"] = school_jsons
                    group_jsons.update(group_json)
            except GroupWithChurch.DoesNotExist:
                raise Http404("Group with church does not exist")
            if len(group_jsons) > 0:
                church_json[church.id]["group"] = group_jsons
            church_jsons.update(church_json)
    except ChurchInfo.DoesNotExist:
        raise Http404("Church does not exist")

    response = church_jsons

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def allSchool(request):
    school_jsons = {}
    try:
        schools = SchoolInfo.objects.all()
        for school in schools:
            school_json = school.toDict()

            group_jsons = {}
            try:
                groupWithSchools = GroupWithSchool.objects.filter(
                    school=school)
                for groupWithSchool in groupWithSchools:
                    group = groupWithSchool.group
                    group_json = group.toDict()

                    church_jsons = {}
                    try:
                        groupWithChurchs = GroupWithChurch.objects.filter(
                            group=group)
                        for groupWithChurch in groupWithChurchs:
                            church_info = groupWithChurch.church
                            church_json = church_info.toDict()
                            church_jsons.update(church_json)
                    except GroupWithChurch.DoesNotExist:
                        raise Http404("Group with church does not exist")

                    meeting_time_jsons = {}
                    try:
                        groupMeetingTimes = GroupMeetingTime.objects.filter(
                            group=group)
                        for groupMeetingTime in groupMeetingTimes:
                            meeting_time_json = groupMeetingTime.toDict()
                            meeting_time_jsons.update(meeting_time_json)
                    except GroupMeetingTime.DoesNotExist:
                        raise Http404("Group meeting time does not exist")

                    group_json[group.id]["church"] = church_jsons
                    group_json[group.id]["metting"] = meeting_time_jsons
                    group_jsons.update(group_json)
                school_json[school.id]["group"] = group_jsons
            except GroupWithChurch.DoesNotExist:
                raise Http404("Group with church does not exist")

            school_jsons.update(school_json)
    except SchoolInfo.DoesNotExist:
        raise Http404("Group does not exist")
    response = school_jsons

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})



def send_contact(request):
    group = str(request.POST.get('group'))
    name = str(request.POST.get('name'))
    gender = str(request.POST.get('gender'))
    church = str(request.POST.get('church'))
    school = str(request.POST.get('school'))
    department = str(request.POST.get('department'))
    phone = str(request.POST.get('phone'))
    email = str(request.POST.get('email'))
    remark = str(request.POST.get('remark'))
    response = group + " "+name + " "+gender + " "+church + " "+school + \
        " "+department + " "+phone + " "+email + " "+remark

    # add to DB
    contactReport = ContactReport(group=group,name=name,gender=gender,church=church,school=school,department=department,phone=phone,email=email,remark=remark)
    contactReport.save()
    
    # send email
    send_contact_report(contactReport)
    
    return HttpResponse(response)



def send_report(request):
    issue_type = str(request.POST.get('type'))
    content = str(request.POST.get('content'))
    name = str(request.POST.get('name'))
    email = str(request.POST.get('email'))
    response = issue_type + " "+content + " "+name + " "+email + " " 
    if issue_type == None or content == None:
        return HttpResponse(response)

    # add to DB
    issueReport = IssueReport(issue_type=issue_type,content=content,name=name,email=email)
    issueReport.save()

    # send email
    send_issue_report(issueReport)

    return HttpResponse(response)
