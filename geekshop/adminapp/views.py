from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_read'))
    else:
        user_form = ShopUserRegisterForm()
    content = {
        'form': user_form
    }
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_read'))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_item.is_active = not user_item.is_active
        user_item.save()
        return HttpResponseRedirect(reverse('adminapp:user_read'))

    content = {
        'user_to_delete': user_item
    }
    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all().order_by('-is_active')
    content = {
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рудактирование категории'
        return context

    # def get_success_url(self):
    #     self.object = self.get_object()
    #     if self.object.is_active:
    #         return self.success_url
    #     return reverse_lazy('adminapp:categories')
    #
    # def form_valid(self, form):
    #     pass


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.success_url)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category=category_item).order_by('-is_active')
#     content = {
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Product.objects.filter(category__pk=category_pk).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context


class ProdyctCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs['pk']])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProdyctUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        category = get_object_or_404(ProductCategory, pk=self.object.category.pk)
        context['category'] = category
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])
