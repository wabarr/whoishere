from django.contrib import admin
from whoishere.models import Course, Checkin, AttendancePoll
import csv
from django.http import HttpResponse

class CourseAdmin(admin.ModelAdmin):
    fields = ["nickname", "instructor", "semester", "year", "subject_code", "course_number"]


class CheckinAdmin(admin.ModelAdmin):
    fields = ["timestamp", "attendance_poll", "student_last_name", "student_first_name", "gw_email_handle", "GWID"]
    readonly_fields = ["timestamp"]
    list_display = fields
    list_filter = ["attendance_poll", "attendance_poll__course__year", "attendance_poll__course__semester","attendance_poll__course__nickname"]
    search_fields = ["student_last_name", "student_first_name", "gw_email_handle", "GWID"]
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class AttendanceCheckAdmin(admin.ModelAdmin):
    fields = ["slug", "course", "starts", "expires"]
    readonly_fields = ["slug"]

admin.site.register(Course, CourseAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(AttendancePoll, AttendanceCheckAdmin)
