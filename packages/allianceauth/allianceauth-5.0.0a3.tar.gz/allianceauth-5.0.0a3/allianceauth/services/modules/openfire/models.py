from django.db import models


class OpenfireUser(models.Model):
    user = models.OneToOneField('auth.User',
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name='openfire')
    username = models.CharField(max_length=254)



    class Meta:
        permissions = (
            ("access_openfire", "Can access the Openfire service"),
        )
    def __str__(self):
        return self.username
