from django.urls import path

from product.api.views import categoryCreations,itemCreations

urlpatterns = [
    path('category/',categoryCreations.as_view()),
    path('category/<int:id>/',categoryCreations.as_view()),
    path('item/',itemCreations.as_view()),
    path('item/<int:id>', itemCreations.as_view())
]