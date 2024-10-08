"""
URL configuration for hr_salary_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from payroll.views import UploadFileView, GeneratePDFView, DownloadPayslipsView, SendPayslipsView, landing_page_view
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),




    path('', landing_page_view, name='landing-page'),
    path('', include('payroll.urls')),
    
    path('upload/', UploadFileView.as_view(), name='upload_file'), 
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate_pdf'),
    path('download-payslips/', DownloadPayslipsView.as_view(), name='download_payslips'),  
    path('send-payslips/', SendPayslipsView.as_view(), name='send_payslips'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
