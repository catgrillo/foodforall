from recipes.models import Recipe, Comment, Fav, Ingredient
from recipes.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse_lazy
from recipes.forms import CreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from recipes.forms import CommentForm, IngredientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from recipes.utils import dump_queries
# from django.db.models import Q
# from django.contrib.humanize.templatetags.humanize import naturaltime

class RecipeListView(OwnerListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    # By convention:
    # template_name = "myarts/article_list.html"

    def get(self, request) :
        # recipe_list = Recipe.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_recipes.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        # ctx = {'recipe_list' : recipe_list, 'favorites': favorites}
        # return render(request, self.template_name, ctx)

        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            recipe_list = Recipe.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # query = Q(title__contains=strval)
            # query.add(Q(text__contains=strval), Q.OR)
            # ad_list = Recipe.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :

            recipe_list = Recipe.objects.all().order_by('-updated_at')[:10]


        ctx = {'recipe_list' : recipe_list, 'search': strval, 'favorites': favorites}
        retval = render(request, self.template_name, ctx)

        dump_queries()
        return retval;


class RecipeDetailView(OwnerDetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"

    def get(self, request, pk) :
        x = Recipe.objects.get(id=pk)
        comments = Comment.objects.filter(recipe=x).order_by('-updated_at')
        ingredients = Ingredient.objects.filter(recipe=x).order_by('-created_at')
        # instructions_list=list()
        # for line in x.instructions:

        comment_form = CommentForm()
        context = { 'recipe' : x, 'ingredients':ingredients, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)



class RecipeCreateView(OwnerCreateView):
    model = Recipe
    fields = ['title', 'description', 'instructions']

    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

    # def get(self, request, pk=None):
    #     # x = Recipe.objects.get(id=pk)
    #     form = CreateForm()
    #     # ingredients = Ingredient.objects.filter(recipe=x).order_by('-created_at')
    #     ingredient_form = IngredientForm()
    #     context = {'ingredient_form':ingredient_form, 'form': form}
    #     # context = {'recipe':x, 'ingredients':ingredients, 'ingredient_form':ingredient_form, 'form': form}
    #     return render(request, self.template_name, context)

class RecipeUpdateView(OwnerUpdateView):
    model = Recipe
    fields = ['title', 'description', 'instructions']

    template_name = 'recipes/recipe_update.html'
    success_url = reverse_lazy('recipes:all')

    # def get(self, request, pk):
    #     pic = get_object_or_404(Recipe, id=pk, owner=self.request.user)
    #     form = CreateForm(instance=pic)
    #     ctx = {'form': form}
    #     return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Recipe, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

    def get(self, request, pk=None):
        x = get_object_or_404(Recipe, id=pk, owner=self.request.user)
        form = CreateForm(instance=x)
        # x = Recipe.objects.get(id=pk)
        ingredients = Ingredient.objects.filter(recipe=x).order_by('-created_at')
        ingredient_form = IngredientForm()
        context = {'recipe':x, 'ingredients':ingredients, 'ingredient_form':ingredient_form, 'form': form}
        return render(request, self.template_name, context)


class RecipeDeleteView(OwnerDeleteView):
    model = Recipe

class UserRecipeListView(OwnerListView):
    model = Recipe
    template_name = "recipes/user_recipe_list.html"

    def get(self, request, pk=None):
        my_recipes = Recipe.objects.all()
        # Recipe.objects.filter(owner=self.request.user)
        # my_recipes = Recipe.objects.filter(favs=)
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_recipes.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        context = {'my_recipes':my_recipes, 'favorites':favorites}
        return render(request, self.template_name, context)

class HomePage(OwnerListView):
    model = Recipe
    template_name = "recipes/home_page.html"

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Recipe, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, recipe=f)
        comment.save()
        return redirect(reverse('recipes:recipe_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "recipes/recipe_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        forum = self.object.recipe
        return reverse('recipes:recipe_detail', args=[forum.id])

class IngredientCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        f = get_object_or_404(Recipe, id=pk)
        ingredient = Ingredient(name = request.POST['ingredient'], measurement=request.POST['measurement'], owner=request.user, recipe=f)
        ingredient.save()
        return redirect(reverse('recipes:recipe_update', args=[pk]))

class IngredientDeleteView(OwnerDeleteView):
    model = Ingredient
    template_name = 'recipes/recipe_ingredient_delete.html'

    def get_success_url(self):
        forum = self.object.recipe
        return reverse('recipes:recipe_update', args=[forum.id])


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Recipe, id=pk)
        fav = Fav(user=request.user, recipe=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Recipe, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, recipe=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


def stream_file(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    response = HttpResponse()
    response['Content-Type'] = recipe.content_type
    response['Content-Length'] = len(recipe.picture)
    response.write(recipe.picture)
    return response


