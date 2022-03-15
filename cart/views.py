from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from cart.forms import PaymentForm
from course.models import Course, Enroll
from .cart import Cart
from .models import Payment



@login_required
def payment(request):
    cart = Cart(request)

    context = {'cart': cart}
    return render(request, 'payment.html', context)


@login_required
@require_POST
def cart_add(request, slug):
    cart = Cart(request)  
    course = get_object_or_404(Course, slug=slug)
    cart.add(course=course, quantity=1, update_quantity=False)
    return redirect('cart_detail')


@login_required
def cart_remove(request, slug):
    cart = Cart(request)
    course = get_object_or_404(Course, slug=slug)
    cart.remove(course)
    if len(cart) == 0:
        return redirect('all_courses')
    else:
        return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart})


@login_required(login_url='/login')
def cart_checkout(request):

    carts = Cart(request)
    for cart in carts:
        course = cart['course']
        Enroll.objects.create(course=course, student_id=request.user.id, is_paid=True)
    messages.success(request, 'Successfully checked out!')
    carts.clear()
    return redirect(reverse_lazy('cart_detail'))







