from django.db import models
from django.contrib.sessions.models import Session

class Device(models.Model):
    brand = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    family = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    model = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return "{} {} {}".format(
            self.brand,
            self.family,
            self.model
        )
    
    class Meta:
        unique_together = [('brand','family','model'),]

class Browser(models.Model):
    family = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    version = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return "{} {}".format(
            self.family,
            self.version
        )
    
    class Meta:
        unique_together = [('family','version'),]

class OS(models.Model):
    family = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    version = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return "{} {}".format(
            self.family,
            self.version
        )
    
    class Meta:
        unique_together = [('family','version'),]

class Client(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True
    )
    deactivating_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    browser = models.ForeignKey(
        Browser,
        on_delete=models.CASCADE,
    )
    os = models.ForeignKey(
        OS,
        on_delete=models.CASCADE,
    )
    ua_string = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    ip = models.GenericIPAddressField()
    
    """ 
        That Model could also be used as statistical Evaluation
        Thats why blank=True, null=True // 
    """
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='users_session'
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    @property
    def is_active():
        return not self.deactivating_date or self.deactivating_date == ''
