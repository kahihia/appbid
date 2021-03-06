__author__ = 'rulongwang'

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class UserPrivateItem(models.Model):
    """UserPrivateItem table info - such as is_bid_approved."""
    key = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class UserPrivateItemAdmin(admin.ModelAdmin):
    """The set of UserPrivateItem table displaying in admin page."""
    list_display = ('key', 'description')


class UserPrivateSetting(models.Model):
    """UserPrivateSetting table info."""
    user = models.ForeignKey(User)
    user_private_item = models.ForeignKey(UserPrivateItem)
    value = models.TextField()


class UserDetail(models.Model):
    """UserDetail table info."""
    DEVELOPER_STATUS = (
        (1, "Normal User"),
        (2, "Pending"),
        (3, "Certified Developer"),
        (4, "Failed"),
    )
    user = models.OneToOneField(User, blank=True)
    developer_status = models.IntegerField(choices=DEVELOPER_STATUS, null=True, blank=True, default=1)
    birthday = models.DateField(blank=True, null=True)
    real_name = models.CharField(blank=True, max_length=255, null=True)
    street_address = models.CharField(blank=True, max_length=300, null=True)
    city = models.CharField(blank=True, max_length=255, null=True)
    state_provience = models.CharField(blank=True, max_length=255, null=True)
    post_code = models.CharField(blank=True, max_length=255, null=True)
    country = models.CharField(blank=True, max_length=255, null=True)


class UserDetailAdmin(admin.ModelAdmin):
    """The set of UserDetail table displaying in admin page."""
    list_display = ('user', 'real_name', 'city', 'country')


def content_file_name(instance, filename):
    """The path of saving attachment file. The pattern is user_id/filename"""
    return '/'.join([str(instance.user.id), 'avatar.jpg'])


class UserPublicProfile(models.Model):
    """UserPublicProfile table info."""
    GENDER_TYPES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Secret'),
    )
    user = models.OneToOneField(User, blank=True)
    thumbnail = models.FileField(max_length=255, upload_to=content_file_name, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_TYPES, blank=True, default=3, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    twitter_account = models.CharField(max_length=255, blank=True, null=True)
    facebook_account = models.CharField(max_length=255, blank=True, null=True)
    weibo_account = models.CharField(max_length=255, blank=True, null=True)
    weixin_account = models.CharField(max_length=255, blank=True, null=True)


class UserPublicProfileAdmin(admin.ModelAdmin):
    """The set of UserPublicProfile table displaying in admin page."""
    list_display = ('user', 'gender', 'homepage', 'weibo_account')


class SubscriptionItem(models.Model):
    """SubscriptionItem table info - email notification."""
    user = models.ManyToManyField(User)
    key = models.CharField(max_length=255)
    item = models.CharField(max_length=255)


class SubscriptionItemAdmin(admin.ModelAdmin):
    """The set of SubscriptionItem table displaying in admin page."""
    list_display = ('key', 'item')


class SecurityVerification(models.Model):
    """SecurityVerification table info."""
    VERIFICATION_TYPE = (
        (1, 'email'),
        (2, 'phone'),
    )
    user = models.ForeignKey(User)
    vtype = models.IntegerField(choices=VERIFICATION_TYPE)
    value = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(auto_now=True)


class UserLoginInfo(models.Model):
    """User login info."""
    user = models.ForeignKey(User)
    ip = models.CharField(max_length=255, null=True)
    #The address that IP belong.
    address = models.CharField(max_length=255, null=True)
    login_date = models.DateTimeField(auto_now_add=True)


class BlackList(models.Model):
    """Black list."""
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class BlackListAdmin(admin.ModelAdmin):
    """The set of SubscriptionItem table displaying in admin page."""
    list_display = ('user', 'comment', 'create_time')


admin.site.register(UserPrivateItem, UserPrivateItemAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(SubscriptionItem, SubscriptionItemAdmin)
admin.site.register(UserPublicProfile, UserPublicProfileAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(UserPrivateSetting)
admin.site.register(SecurityVerification)
admin.site.register(UserLoginInfo)




