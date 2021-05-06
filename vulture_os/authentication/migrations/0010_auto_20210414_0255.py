# Generated by Django 3.0.5 on 2021-04-14 02:55

import authentication.user_portal.models
import bson.objectid
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20210423_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_error',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Error</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>\n        <style>{{style}}</style>\n    </style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container">\n            <img id="vulture_img" src="{{image_1}}"/>\n            <p>{{message}}</p>\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML General content for error pages'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_learning',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Learning</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container" style="text-align:center;">\n            <p>Learning form</p>\n            {{form_begin}}\n                {{input_submit}}\n            {{form_end}}\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML Content for the learning page'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_logout',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Logout</title>\n     <link rel="stylesheet" href="//templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n     <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container" style="text-align:center;">\n            <p style="font-size:15px;font-weight:bold;">You have been successfully disconnected</p>\n            <a href="{{app_url}}">Return to the application</a>\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML Content for the logout page'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_message',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Info</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container">\n            <img id="vulture_img" src="{{image_1}}"/>\n            <p>{{message}}</p>\n            {% if link_redirect %}<a href="{{link_redirect}}">Go back</a>{% endif %}\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML Content for the message page'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_otp',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture OTP Authentication</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body> \n    <div class="container">\n        <div class="card card-container" style="text-align:center;">\n            {% if error_message != "" %}\n                  <div class="alert alert-danger" role="alert">{{error_message}}</div>\n            {% endif %}\n            <p>OTP Form</p>\n            {{form_begin}}\n                {{input_key}}\n                {{input_submit}}\n            {{form_end}}\n            {{form_begin}}\n                {% if resend_button %}\n                    {{resend_button}}\n                {% endif %}\n                {% if qrcode %}\n                    <p>Register the following QRcode on your phone :\n                    <img {{qrcode}} alt="Failed to display QRcode" height="270" width="270" />\n                    </p>\n                {% endif %}\n            {{form_end}}\n        </div>\n    </div>\n </body>\n</html>\n', help_text='HTML Content for the otp page'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_password',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Change Password</title>\n    <link rel="stylesheet" href="..//templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container" style="text-align:center;">\n            {{form_begin}}\n                <img id="vulture_img" src="{{image_1}}"/>\n                {% if error_message %}\n                    <div class="alert alert-danger">{{error_message}}</div>\n                {% endif %}\n                {% if dialog_change %}\n                    <p>Please fill the form to change your current password :</p>\n                    {{input_password_old}}\n                    {{input_password_1}}\n                    {{input_password_2}}\n                    {{input_submit}}\n\n                {% elif dialog_lost %}\n                    <p>Please enter an email address to reset your password:</p>\n\n                    {{input_email}}\n                    {{input_submit}}\n\n                {% endif %}\n            {{form_end}}\n        </div>\n    </div>\n </body>\n</html>\n', help_text='HTML Content for the password change page'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_registration',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Titre</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container" style="text-align:center;">\n            {{form_begin}}\n                <img id="vulture_img" src="{{image_1}}"/>\n                {% if error_message %}\n                    <div class="alert alert-danger">{{error_message}}</div>\n                {% endif %}\n                {{captcha}}\n                {{input_captcha}}\n                {% if step2 %}\n                    <p>Please fill the form to register your account :</p>\n                    {{input_username}}\n                    {% if ask_phone %}\n                    {{input_phone}}\n                    {% endif %}\n                    {{input_password_1}}\n                    {{input_password_2}}\n                    {{input_submit}}\n\n                {% elif step1 %}\n                    <p>Please enter your email address to receive the registration mail :</p>\n                    {{input_email}}\n                    {{input_submit}}\n                {% endif %}\n            {{form_end}}\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML Content for registration pages'),
        ),
        migrations.AlterField(
            model_name='portaltemplate',
            name='html_self',
            field=models.TextField(default='<!DOCTYPE html>\n<html>\n <head>\n    <meta charset="utf-8" />\n    <title>Vulture Self-Service</title>\n    <link rel="stylesheet" href="/templates/static/html/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">\n    <style>{{style}}</style>\n </head>\n <body>\n    <div class="container">\n        <div class="card card-container" style="text-align:center;" id="self_service">\n            <img id="vulture_img" src="{{image_1}}"/>\n            <br><br>\n            {% if error_message != "" %}\n                <div class="alert alert-danger">{{error_message}}</div>\n            {% endif %}\n            <p>Hello <b>{{username}}</b>!</p>\n            <p>You currently have access to the following apps:</p>\n            <ul class="list-group">\n                {% for app in application_list %}\n                  <li class="list-group-item"><b>{{app.name}}</b> - <a href="{{app.url}}">{{app.url}}</a>{% if app.status %}<span class="badge">Logged</span>{% endif %}</li>\n                {% endfor %}\n            </ul>\n            <a href="{{changePassword}}">Change password</a>\n            <br><a href="{{logout}}">Logout</a>\n        </div>\n    </div>\n </body>\n</html>', help_text='HTML Content for the self-service page'),
        )
    ]
