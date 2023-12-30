from django.db import models
from user.models import *

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=99, db_index=True)
    address = models.CharField(max_length=199, db_index=True)
    state = models.CharField(max_length=99, choices=STATE, db_index=True)
    sort_code = models.CharField(max_length=10, db_index=True)
                    
    def __str__(self):
        return f'{self.name}'

class SupportManager(models.Manager):
    def answer_support(self, customer_id):
        supports = super(SupportManager, self).filter(customer__id=customer_id)
        for support in supports:
            support.answer = True
            support.save()
        return support
    
    def read_support(self, customer_id):
        supports = super(SupportManager, self).filter(customer__id=customer_id)
        for support in supports:
            support.read = True
            support.save()
        return support

class Support(models.Model):
    read = models.BooleanField(default=False)
    answer = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    objects = SupportManager()

    def __str__(self):
        return f'Customer: {self.customer} - Answered: {self.answer}'

class FAQ(models.Model):
    question = models.CharField(max_length=99)
    answer = models.CharField(max_length=299)

    def __str__(self):
        return f'{self.question}'

class Conversation(models.Model):
    participants = models.ManyToManyField(User, db_index=True)

    def __str__(self):
        participants_names = ", ".join(participant.staffaccount_set.first().account_name for participant in self.participants.all() if participant.staffaccount_set.exists())
        return f'Conversation Between: {participants_names}'
        
class ChatManager(models.Manager):
    def read_chat(self, chat_id):
        chat = super(ChatManager, self).get(id=chat_id)
        chat.read = True
        chat.save()
        return chat

class Chat(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    objects = ChatManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Sender: {self.sender} - {self.conversation}'
