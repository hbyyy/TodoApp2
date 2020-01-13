from django.db import models


# Create your models here.
from members.models import User


class Todo(models.Model):
    PRIORITY_CHOICE = (
        ('HI', 'high'),
        ('MD', 'medium'),
        ('LO', 'low')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICE, default=PRIORITY_CHOICE[2][0])
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content},{self.created_date},{self.get_priority_display()},{self.is_done}'


class TodoDetail(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.todo.content}, {self.content}'
