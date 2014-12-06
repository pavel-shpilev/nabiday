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

    def get_score(self):
        if self.state == 'plus':
            return 1
        elif self.state == 'minus':
            return -1
        else:
            return 0

    def to_json_object(self):
        return {
            'description': self.description,
            'state': self.state,
        }

