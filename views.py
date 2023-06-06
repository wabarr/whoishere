from whoishere.models import Checkin, AttendancePoll
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django import forms
import qrcode
import qrcode.image.svg
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import modelform_factory



#class URLForm(forms.Form):
#    URL = forms.URLField(label="URL", max_length=500)


class QRView(LoginRequiredMixin, TemplateView):
    template_name = "whoishere/qr.html"

    def get_context_data(self, *args, **kwargs):
        context = super(QRView, self).get_context_data(*args, **kwargs)
        ## create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=50,
            border=4,
        )
        #use reverse to get the URL, then build the full url with domain
        URL = self.request.build_absolute_uri(reverse("checkin-view", args=(self.kwargs["slug"],)))
        context["URL"] = URL

        qr.add_data(URL)
        qr.make(fit=True)
        img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        context["svg"] = img.to_string(encoding='unicode')

        #get the AttendancePoll object so you can dislay it on the QR template
        try:
            ob=AttendancePoll.objects.get(slug=self.kwargs["slug"])
            context["object"] = ob
        except ObjectDoesNotExist:
            pass

        return context


class CheckinModelForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = "__all__"
        widgets = {
            'attendance_poll': forms.HiddenInput(),
            'student_last_name': forms.TextInput(attrs={'placeholder': 'your last name'}),
            'student_first_name': forms.TextInput(attrs={'placeholder': 'your first name'}),
            'gw_email_handle': forms.TextInput(attrs={'placeholder': 'GW email handle (part before @gwu.edu)'}),
            'GWID': forms.TextInput(attrs={'placeholder': 'GWID (e.g. G12345678)'})
        }

    def clean(self):
        cleaned_data = super(CheckinModelForm, self).clean()
        try:
            ob = AttendancePoll.objects.get(pk=cleaned_data["attendance_poll"].pk)
            if ob.expires > now() and ob.starts < now():
                return cleaned_data
            else:
                raise ValidationError("I can't check you in because this attendance poll is not currently open.")
        except ObjectDoesNotExist:
            raise ValidationError("Sorry, I can't check you in for an attendance poll that doesn't exist.")


class CheckinView(CreateView):
    model = Checkin
    success_url = "/success/"
    form_class = CheckinModelForm

    def get_initial(self):
        initial = super(CheckinView, self).get_initial()
        pollObject = AttendancePoll.objects.get(slug=self.kwargs["slug"])

        try:
            initial["student_last_name"] = self.request.session.get("student_last_name")
        except:
            pass

        try:
            initial["student_first_name"] = self.request.session.get("student_first_name")
        except:
            pass

        try:
            initial["GWID"] = self.request.session.get("GWID")
        except:
            pass

        try:
            initial["gw_email_handle"] = self.request.session.get("gw_email_handle")
        except:
            pass

        initial["attendance_poll"] = pollObject.pk
        return initial

    def get_context_data(self, **kwargs):
        context = super(CheckinView, self).get_context_data()
        context["pollObject"] = AttendancePoll.objects.get(slug=self.kwargs["slug"])
        return context

    def get_success_url(self):
        self.request.session["student_last_name"] = self.object.student_last_name
        self.request.session["student_first_name"] = self.object.student_first_name
        self.request.session["GWID"] = self.object.GWID
        self.request.session["gw_email_handle"] = self.object.gw_email_handle
        self.request.session["last_poll_participated"] = self.object.attendance_poll.id
        return super(CheckinView, self).get_success_url()


class SuccessView(TemplateView):
    template_name = 'whoishere/success.html'

class SplashView(TemplateView):
    template_name = "whoishere/splash.html"

class AttendancePollList(LoginRequiredMixin, ListView):
    template_name = "whoishere/attendancepoll_list.html"
    queryset = AttendancePoll.objects.all()#to be filtered in template

    def get_context_data(self, **kwargs):
        context = super(AttendancePollList, self).get_context_data()
        count = 0
        polls = AttendancePoll.objects.all()
        for poll in polls:
            if poll.is_active():
                count += 1
        context["active_poll_count"] = count
        return context

class AttendancePollCreate(LoginRequiredMixin, CreateView):
    model = AttendancePoll
    success_url = "/attendance-polls"
    form_class = modelform_factory(model=AttendancePoll, fields=["course", "starts", "expires"])

class CheckinList(ListView):
    template_name = "whoishere/checkin_list.html"
    #the queryset gets attendance poll objects, rather than checkins, to simplify grouping by attendance poll in template logic
    queryset = AttendancePoll.objects.all()