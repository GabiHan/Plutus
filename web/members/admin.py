from django.contrib import admin
from .models import Member, UserProfile
from django import forms

class MemberAdminForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # Custom validation to ensure the UserProfile exists
        if 'userprofile' in cleaned_data:
            # Check for corresponding UserProfile
            if not UserProfile.objects.filter(user=cleaned_data['userprofile']).exists():
                raise forms.ValidationError("UserProfile must exist for this Member.")

class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm

admin.site.register(Member, MemberAdmin)
admin.site.register(UserProfile)