__author__ = 'jarvis'

from django import forms
from appbid import models as appModels


class AppForm(forms.ModelForm):
    app_store_link = forms.URLField(
        widget=forms.TextInput(attrs={'placeholder': 'Eg. https://itunes.apple.com/us/app/YOURAPP/id0000000?mt=8'}),
        required=False,
        help_text="Your app link in app store."

    )
    source_code = forms.BooleanField(
        required=False,
        help_text='Whether you provide the source code and document,when transferring the app.'
    )
    delivery_detail = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'cols': 86, 'rows': 25})
    )
    web_site = forms.URLField(
        required=False,
        help_text='The support web site link for your app.'
    )

    class Meta:
        model = appModels.App
        exclude = {'publisher'}

    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['apple_id'].widget.attrs['disabled'] = True
            self.fields['app_name'].widget.attrs['disabled'] = True
            self.fields['platform_version'].widget.attrs['disabled'] = True
            self.fields['rating'].widget.attrs['disabled'] = True
            self.fields['category'].widget.attrs['disabled'] = True
            self.fields['device'].widget.attrs['disabled'] = True
            if instance.status == 3:
                self.fields['store_type'].widget.attrs['disabled'] = True
                self.fields['title'].widget.attrs['disabled'] = True
                self.fields['app_store_link'].widget.attrs['disabled'] = True
                self.fields['dl_amount'].widget.attrs['disabled'] = True
                self.fields['revenue'].widget.attrs['disabled'] = True
                self.fields['monetize'].widget.attrs['disabled'] = True
                self.fields['description'].widget.attrs['disabled'] = True
                self.fields['begin_date'].widget.attrs['disabled'] = True
                self.fields['end_date'].widget.attrs['disabled'] = True
                self.fields['source_code'].widget.attrs['disabled'] = True
                self.fields['delivery_detail'].widget.attrs['disabled'] = True
                self.fields['unique_sell'].widget.attrs['disabled'] = True
                self.fields['web_site'].widget.attrs['disabled'] = True
                self.fields['app_type'].widget.attrs['disabled'] = True
            if instance.status == 2 or instance.status == 3:
                self.fields['begin_price'].widget.attrs['disabled'] = True
                self.fields['one_price'].widget.attrs['disabled'] = True
                self.fields['reserve_price'].widget.attrs['disabled'] = True
                self.fields['currency'].widget.attrs['disabled'] = True
                self.fields['minimum_bid'].widget.attrs['disabled'] = True


class AttachmentForm(forms.ModelForm):
    path = forms.FileField(
        label='Select a file'
    )

    class Meta:
        model = appModels.Attachment
        exclude = {'app'}


class AppInfoForm(forms.ModelForm):
    class Meta:
        model = appModels.AppInfo
        exclude = {'app'}

    def __init__(self, *args, **kwargs):
        super(AppInfoForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['price'].widget.attrs['disabled'] = True
