# -*- coding: utf-8 -*-

# django imports
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

# grappelli imports
from django.db.models import Q
from grappelli.models import NavigationItem

def get_navigation(request):
    """
    Get navigation for the currently logged-in User (AJAX request).
    """
    
    if request.method == 'GET':            
            if request.user.is_superuser:
                object_list = NavigationItem.objects.all()
            else:
                object_list = NavigationItem.objects.filter(Q(groups__in=request.user.groups.all()) | Q(users=request.user)).distinct()
    else:
        object_list = ""
    
    return render_to_response('admin/includes_grappelli/navigation.html', {
        'object_list': object_list,
    })
get_navigation = staff_member_required(get_navigation)

