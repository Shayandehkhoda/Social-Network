from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import UserSignupForm, UserLoginForm, UserInfoEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import User, FollowRelation
from django.core.exceptions import ValidationError

class SignupView(View):
    form_class = UserSignupForm
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'Already signed up', 'danger')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register successfully, please login', 'success')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form':form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                messages.error(request, 'Already logged in', 'danger')
                return redirect('/')
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
                messages.success(request, 'Loggedin Successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('/')
        messages.error(request, 'Wrong credentials please try again', 'danger')
        return render(request, self.template_name, {'form':form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully', 'success')
        return redirect('/')


class FollowView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == kwargs.get('user_id'):
            raise ValidationError('You cannot follow yourself')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        following = get_object_or_404(User, pk=user_id)
        existence = FollowRelation.objects.filter(follower=request.user, followed=following).exists()
        if not existence:
            FollowRelation.objects.create(follower=request.user, followed=following)
            messages.success(request, 'Followed successfully', 'success')
        else:
            messages.error(request, 'Already followed', 'error')
        return redirect('social:profile', username=following.username)


class UnFollowView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == kwargs.get('user_id'):
            raise ValidationError('You cannot unfollow yourself')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, user_id):
        following = get_object_or_404(User, pk=user_id)
        existence = FollowRelation.objects.filter(follower=request.user, followed=following).exists()
        if not existence:
            messages.error(request, 'Already unfollowed', 'error')
        else:
            FollowRelation.objects.get(follower=request.user, followed=following).delete()
            messages.success(request, 'Unfollowed successfully', 'success')
        return redirect('social:profile', username=following.username)


class UserInfoEditView(View):
    form_class = UserInfoEditForm
    template_name = 'accounts/user_info.html'

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.user:
            raise ValidationError('You cannot edit this profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.user)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update successfully', 'success')
            return redirect('social:profile', self.user.username)
        return render(request, self.template_name, {'form':form})



















