from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apiApp.urls')),  
    path('api/auth/' , include('dj_rest_auth.urls')),
    path('api/auth/registration/' , include('dj_rest_auth.registration.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# این خط فقط نام متغیر urlpatterns را نوشته است و هیچ مقداری به آن اختصاص نداده
# در جنگو، urlpatterns باید یک لیست از مسیرهای URL باشد که به viewها اشاره می‌کند
# اگر فقط 'urlpatterns' نوشته شود، برنامه با خطا مواجه می‌شود چون مقداردهی نشده است