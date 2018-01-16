from django.db import models


class ScentGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Scent(models.Model):
    name = models.CharField(max_length=30)
    # group = models.ForeignKey(ScentGroup)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return '#{} {}'.format(self.id, self.name)


class TestResult(models.Model):
    scent = models.ForeignKey(Scent, related_name='tests')
    guess = models.ForeignKey(Scent, related_name='guesses')
    created_at = models.DateTimeField(auto_now_add=True)
