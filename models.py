from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import random
import string
from django.utils.timezone import now
import datetime
import re




class Course(models.Model):
    instructor = models.CharField(max_length=100, null=False, blank=False, default = "W. Andrew Barr")
    semester = models.CharField(max_length=100, null=False, blank=False, choices=[("Spring", "Spring"), ("Fall", "Fall")])
    year = models.PositiveIntegerField( validators=[MinValueValidator(2023), MaxValueValidator(2050)])
    subject_code = models.CharField(default='ANTH', max_length=4, null=False, blank=False, choices=[("ANTH", "ANTH"), ("HOMP", "HOMP")])
    course_number = models.PositiveIntegerField(validators=[MinValueValidator(1001), MaxValueValidator(7000)])
    nickname = models.CharField(null=True, blank=True, max_length=50, help_text="a shorthand way to refer to the course")
    def __str__(self):
        return "{} - {} {} ({}{})".format(self.nickname, self.subject_code, self.course_number, self.semester[0:1], str(self.year)[2:4])


class AttendancePoll(models.Model):
    slug=models.SlugField(max_length=6, null=True, blank=True, help_text="to be auto populated", unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    starts = models.DateTimeField(default=now)
    expires = models.DateTimeField(null=True, blank=True, help_text="Leave blank to default to 30 minutes from now")

    def save(self, *args, **kwargs):
        while not self.slug:
            try:
                self.slug=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            except:
                pass
        if not self.expires:
            self.expires = self.starts + datetime.timedelta(minutes=30)
        super(AttendancePoll, self).save(*args, **kwargs)

    def is_active(self):
        if self.starts < now() < self.expires:
            return True
        else:
            return False

    def __str__(self):
        return "{} - {}".format((self.expires.strftime("%x")), self.course)


GWID_validator = RegexValidator(r"^G[0-9]{8}$", "Your GWID must be a capital G followed by 8 numbers")
def email_handle_validator(value):
    if re.search("@", value):
        raise ValidationError("Include only the part of your email before the @ symbol")


class Checkin(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    attendance_poll = models.ForeignKey(AttendancePoll, on_delete=models.CASCADE)
    student_last_name = models.CharField(max_length=100, null=False, blank=False)
    student_first_name = models.CharField(max_length=100, null=False, blank=False)
    gw_email_handle = models.CharField(max_length=100, validators=[email_handle_validator], null=False, blank=False, help_text="The part of your GW email address before @gwu.edu")
    GWID = models.CharField(max_length=9, validators=[GWID_validator], null=False, blank=False)

    def __str__(self):
        return "{} -> {} @ {}".format(self.student_last_name, self.attendance_poll.course.__str__(), self.timestamp)

