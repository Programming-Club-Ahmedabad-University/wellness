from django.db import models

from account.models import Account

answer_types = (
    ("1", "values"),
    ("2", "yes_or_no")
)


class Questions(models.Model):
    question_number = models.IntegerField()
    question_text = models.TextField(null=True, blank=True)
    answer_type = models.CharField(max_length=10, choices=answer_types)

    def __str__(self):
        return str(self.question_number)


class Answers(models.Model):
    answer_number = models.IntegerField()
    answer_type = models.CharField(max_length=10, choices=answer_types)
    answer_value = models.IntegerField(null=True, blank=True)
    yes_or_no = models.CharField(null=True, blank=True, max_length=5)
    answer_text = models.TextField(null=True, blank=True)
    answer_date = models.DateTimeField(auto_now=True)
    answer_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='answers')
    answer_test = models.IntegerField()

    class Meta:
        ordering = ['-answer_date']

    def get_latest_date(self):
        return self.objects.last()

    def __str__(self):
        return (f"{ self.answer_user }_{ self.answer_user.last_screening_number }_{ self.answer_number }")
