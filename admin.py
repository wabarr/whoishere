from django.contrib import admin
from whoishere.models import Course, Checkin, AttendancePoll

class CourseAdmin(admin.ModelAdmin):
    fields = ["nickname", "instructor", "semester", "year", "subject_code", "course_number"]


class CheckinAdmin(admin.ModelAdmin):
    fields = ["timestamp", "attendance_poll", "student_last_name", "student_first_name", "gw_email_handle", "GWID"]
    readonly_fields = ["timestamp"]
    list_display = fields
    list_filter = ["attendance_poll"]
    search_fields = ["student_last_name", "student_first_name", "gw_email_handle", "GWID"]

class AttendanceCheckAdmin(admin.ModelAdmin):
    fields = ["slug", "course", "starts", "expires"]
    readonly_fields = ["slug"]

admin.site.register(Course, CourseAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(AttendancePoll, AttendanceCheckAdmin)
