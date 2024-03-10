from django.db import models


class PersonDetail(models.Model):
    """
    This model is used for keeping information about person.
    """
    GENDER_CHOICES = (("male","MALE"),
                      ("femail","FEMAIL"))
    name = models.CharField(max_length = 100, unique=True)
    gender = models.CharField(max_length = 6, choices=GENDER_CHOICES)

    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

class RelationShip(models.Model):
    """
    This model is used or keeping relationship information data related to each person.
    """
    RELATIVE_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('wife', 'Wife'),
        )
    first_person = models.ForeignKey(PersonDetail,  related_name='person_set', on_delete=models.CASCADE)
    second_relation = models.ForeignKey(PersonDetail, related_name='relation_set', on_delete=models.CASCADE)
    r_type=models.CharField(max_length=6, choices=RELATIVE_CHOICES)
    
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)