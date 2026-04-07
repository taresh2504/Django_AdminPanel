"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing,name='landing'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    # path('login_data/',views.login_data,name='login_data'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('admindashboard/add_dep/',views.add_dep,name='add_dep'),
    path('admindashboard/show_dep/',views.show_dep,name='show_dep'),
    path('admindashboard/save_dep/',views.save_dep,name='save_dep'),
    path('admindashboard/add_emp/',views.add_emp,name='add_emp'),
    path('admindashboard/save_emp/',views.save_emp,name='save_emp'),
    path('admindashboard/show_emp/',views.show_emp,name='show_emp'),
    path('admindashboard/emp_all_query/',views.emp_all_query,name='emp_all_query'),
    path('admindashboard/emp_all_query/reply/<int:pk>/',views.reply,name='reply'),
    path('admindashboard/emp_all_query/a_reply/<int:pk>/',views.a_reply,name='a_reply'),
    path('empdashboard/',views.empdashboard,name='empdashboard'),
    path('empdashboard/profile/',views.profile,name='profile'),
    path('empdashboard/settings/',views.settings,name='settings'),
    path('empdashboard/edit_profile/',views.edit_profile,name='edit_profile'),
    path('empdashboard/empquery/',views.empquery,name='empquery'),
    path('empdashboard/querydata/',views.querydata,name='querydata'),
    path('empdashboard/allquery/',views.allquery,name='allquery'),
    path('empdashboard/pendingquery/',views.pendingquery,name='pendingquery'),
    path('empdashboard/donequery/',views.donequery,name='donequery'),
    path('empdashboard/all_query/emp_q_edit/<int:pk>/',views.emp_q_edit,name='emp_q_edit'),
    path('empdashboard/all_query/emp_q_delete/<int:pk>/',views.emp_q_delete,name='emp_q_delete'),
    path('empdashboard/all_query/updated_querydata/<int:pk>/',views.updated_querydata,name='updated_querydata'),
    path('empdashboard/all_query/search/',views.search,name='search'),
    path('empdashboard/all_query/reset/',views.allquery,name='reset'),
    path('admindashboard/add_item/',views.add_item,name='add_item'),
    path('admindashboard/show_items/',views.show_items,name='show_items'),
    path('admindashboard/show_items/paynow/<int:pk>/',views.paynow,name='paynow'),
    path('pay_amount/<int:pk>/',views.pay_amount,name='pay_amount'),
    path('pay_status/<int:pk>/',views.pay_status,name='pay_status'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
