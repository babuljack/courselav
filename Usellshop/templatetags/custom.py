
from django import template
import math

from Usellshop.models import UserCourse , Course 
register = template.Library()

@register.simple_tag
def is_enrolled(request , course):
   
    user = None
    if not request.user.is_authenticated:
        return False
        # i you are enrooled in this course you can watch every video
    user = request.user
    try:
        user_course = UserCourse.objects.get(user = user  , course = course)
        return True
    except:
        return False

