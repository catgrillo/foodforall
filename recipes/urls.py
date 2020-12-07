from django.urls import path, reverse_lazy
from . import views

app_name='recipes'
urlpatterns = [
    path('', views. HomePage.as_view(), name='home_page'),
    path('recipes', views.RecipeListView.as_view(), name='all'),
    path('recipes/<int:pk>', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/create',
        views.RecipeCreateView.as_view(success_url=reverse_lazy('recipes:all')), name='recipe_create'),
    path('recipes/<int:pk>/update',
        views.RecipeUpdateView.as_view(success_url=reverse_lazy('recipes:all')), name='recipe_update'),
    path('recipes/<int:pk>/delete',
        views.RecipeDeleteView.as_view(success_url=reverse_lazy('recipes:all')), name='recipe_delete'),
    path('your_recipes', views.UserRecipeListView.as_view(), name='user_recipe_list'),

    path('recipe_picture/<int:pk>', views.stream_file, name='recipe_picture'),
    path('recipe/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='recipe_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('recipes')), name='recipe_comment_delete'),
    path('recipe/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='recipe_favorite'),
    path('recipe/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='recipe_unfavorite'),

    path('recipe/<int:pk>/ingredient', views.IngredientCreateView.as_view(), name='recipe_ingredient_create'),
    path('ingredient/<int:pk>/delete', views.IngredientDeleteView.as_view(), name='recipe_ingredient_delete'),

]
