from tortoise import models, fields

from apps.bot import app_name


class Button(models.Model):
    code = fields.CharField(max_length=50, unique=True)
    text_ru = fields.CharField(max_length=50, unique=True)
    text_uz = fields.CharField(max_length=50, unique=True)
    text_en = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = f'{app_name}_button'


class Keyboard(models.Model):
    code = fields.CharField(max_length=50, unique=True)
    buttons = fields.ManyToManyField('bot.Button', related_name='keyboards', through='bot_keyboardbuttonsordering',
                                     forward_key='button_id', backward_key='keyboard_id')

    class Meta:
        table = f'{app_name}_keyboard'


class KeyboardButtonsOrdering(models.Model):
    keyboard = fields.ForeignKeyField('bot.Keyboard', on_delete=fields.CASCADE, related_name='buttons_ordering')
    button = fields.ForeignKeyField('bot.Button', on_delete=fields.CASCADE, related_name='ordering')
    ordering = fields.SmallIntField()

    class Meta:
        table = f'{app_name}_keyboardbuttonsordering'


class Message(models.Model):
    code = fields.CharField(max_length=100, unique=True)
    text_ru = fields.TextField()
    text_uz = fields.TextField()
    text_en = fields.TextField()

    class Meta:
        table = f'{app_name}_message'
