
from django.core.mail import send_mail
from django.conf import settings

def send_issue_report(issueReport):
    from_email = settings.DEFAULT_FROM_EMAIL
    content = '錯誤類型: ' + issueReport.issue_type + '\n' \
        + '內容: ' + issueReport.content + '\n' \
        + '姓名: ' + issueReport.name + '\n' \
        + 'Email: ' + issueReport.email + '\n'

    send_mail('我要去團契 錯誤回報', content, from_email, ['example@gmail.com'], fail_silently=False)

def send_contact_report(contactReport):
    from_email = settings.DEFAULT_FROM_EMAIL
    content = '團契查詢結果(僅供參考): ' + contactReport.group + '\n' \
        + '姓名: ' + contactReport.name + '\n' \
        + '性別: ' + contactReport.gender + '\n' \
        + '原屬教會: ' + contactReport.church + '\n' \
        + '學校: ' + contactReport.school + '\n' \
        + '科系: ' + contactReport.department + '\n' \
        + '電話: ' + contactReport.phone + '\n' \
        + 'Email: ' + contactReport.email + '\n' \
        + '備註: ' + contactReport.remark + '\n'
    send_mail('我要去團契 網頁回覆資料', content, from_email, ['example@gmail.com'], fail_silently=False)

    pass