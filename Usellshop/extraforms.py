from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory,NamedFormsetsMixin
from .models import *


class TagFm(InlineFormSetFactory):
        model=Tag
        fields='__all__'
        prefix = 'item-form'
        initial = [{'name': 'Tags'}]
        factory_kwargs = {
                        'can_delete': False}


    
class PrerequisiteFm(InlineFormSetFactory):
        model=Prerequisite
        fields='__all__'
        factory_kwargs = {'extra': 2, 'max_num': None,
                        'can_order': False, 'can_delete': False}

class LearningFm(InlineFormSetFactory):
        model=Learning
        fields='__all__'
        factory_kwargs = {'extra': 2, 'max_num': None,
                        'can_order': False, 'can_delete': False}
     
class VideoFm(InlineFormSetFactory):
        model=Video
        fields='__all__' 
        factory_kwargs = {'extra': 2, 'max_num': None,
                        'can_order': False, 'can_delete': False} 


class CourseInlineForm(NamedFormsetsMixin,CreateWithInlinesView):
    model = Course
    fields ='__all__'  # self.model fields
    inlines = [TagFm,PrerequisiteFm,LearningFm,VideoFm]
    inlines_names = ['Tag','Prerequisite','Learning','Video']
    template_name = "course/upload.html"
    success_url = "/"
    factory_kwargs = {'extra': 2, 'max_num': None,
                        'can_order': False, 'can_delete': False}