from django.db import models


class Place(models.Model):
    def __str__(self):
        return "{}:{}".format(self.description, self.state)

    description = models.CharField(max_length=255, unique=True)
    state = models.CharField(
        max_length=10, 
        choices=(
            ('neutral', 'neutral'),
            ('plus', 'plus'),
            ('minus', 'minus')
        ),
        default='neutral'
    )

    def to_json_object(self):
        return {
            'description': self.description,
            'state': self.state,
        }

