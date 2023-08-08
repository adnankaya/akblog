from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import transaction

import uuid
# internals
from .models import Developer, Skill

# globals
User = get_user_model()


class DeveloperService(object):

    
    @classmethod
    def create_developer(cls, request, form):
        with transaction.atomic():
            try:
                user = User.objects.get(email=request.POST["email"])
                raise ValueError(_("Email is already exist!"))
            except User.DoesNotExist:
                user = User.objects.create(
                    email=request.POST["email"],
                    username=request.POST["email"],
                    first_name=request.POST["firstname"],
                    last_name=request.POST["lastname"],
                )
                user.set_password(uuid.uuid4().hex)
                user.save()
            try:
                developer = Developer.objects.get(user=user)
            except Developer.DoesNotExist:
                developer = form.save(commit=False)
                developer.user = user
                developer.save()

            skill_ids = request.POST.getlist('skills')
            skills = Skill.objects.filter(id__in=skill_ids)
            if len(skill_ids) > settings.MAX_DEVELOPERS_SKILLS_NUMBER:
                raise ValueError(_("Maximum skill number is {}".format(
                    settings.MAX_DEVELOPERS_SKILLS_NUMBER)))
            for skill in skills:
                developer.skills.add(skill)
            
            return developer

    