from django.urls import path

from .views import(DataSetView, train_view ,
                   split_view, predict_view)

routes = [
    (r'dataset', DataSetView)
]

urlpatterns = [
    path('api/split_data/<int:id>', split_view, name="split_data"),
    path('api/train_model/<int:id>', train_view, name="train_model"),
    path('api/predict/<int:id>', predict_view, name="predict")
]