from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .forms import MessageForm
from .models import Message
from django.db.models import Count
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

User = get_user_model()

@never_cache
def home_view(request):
    form = MessageForm()  # always define a default
    print("home_view called:", request.method, request.POST)
    if request.method == 'POST':
        if 'preview' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                return render(request, 'notif-message-preview.html', {
                    'form': form,
                    'data': form.cleaned_data
                })
        
        elif 'post' in request.POST:
            print("Posting message...")
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save()
                messages.success(request, " Merci pour votre confiance. Votre message a ete envoye au BDE pour etre pris en compte. et gardez toujours a l'esprit que votre voix compte! 🎉")
                # Collect recipients
                exe_users = User.objects.filter(user_type='EXE')
                rep_users = User.objects.filter(user_type='REP', departement=message.departement)
                recipients = list(exe_users.values_list('email', flat=True)) + \
                             list(rep_users.values_list('email', flat=True))

                # Send email notification
                if recipients:
                    send_mail(
                        subject="New Message Posted",
                        message=f"A new message has been posted in {message.departement}:\n\n{message.content}",
                        from_email='darwill367@gmail.com',  # or settings.DEFAULT_FROM_EMAIL
                        recipient_list=recipients,
                        fail_silently=False,
                    )

                # Success feedback
                
                return redirect('home')  # PRG pattern

            else:
                messages.error(request, "Please correct the highlighted fields before posting.")
                return render(request, 'home.html', {'form': form})

        elif 'modify' in request.POST:
            form = MessageForm(request.POST)
            return render(request, 'home.html', {'form': form})

        elif 'cancel' in request.POST:
            return redirect('home')

    # GET request or fallthrough
    return render(request, 'home.html', {'form': form})


def notif_view(request):
    user = request.user
    if user.user_type == 'EXEC':
       g_info_messages = Message.objects.filter(departement='G.I').order_by('-created_at')
       d_info = Message.objects.filter(departement='D').order_by('-created_at')
       glt_info = Message.objects.filter(departement='GLT').order_by('-created_at')
       seg_info = Message.objects.filter(departement='SEG').order_by('-created_at')
       bts_info = Message.objects.filter(departement='BTS').order_by('-created_at')   
       gc_info = Message.objects.filter(departement='G.CIVIL').order_by('-created_at')    
       ba_info = Message.objects.filter(departement='BA').order_by('-created_at')
       jc_info = Message.objects.filter(departement='JC').order_by('-created_at')

       departements = {
            'G.INFO': g_info_messages,
            'D': d_info,
            'GLT': glt_info,
            'SEG': seg_info,
            'BTS': bts_info,
            'G.CIVIL': gc_info,
            'BA': ba_info,
            'JC': jc_info,
        }

       context = {
            'departements': departements,
        }


    elif user.user_type == 'REP':
        messages_qs = Message.objects.filter(departement=user.departement).order_by('-created_at')
        message_count = messages_qs.count()

        # Paginate REP messages (10 per page)
        paginator = Paginator(messages_qs, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "messages": page_obj,
            "message_count": message_count,
        }

    else:
        context = {}

    return render(request, "notifs-main-page.html", context)


def department_messages(request, departement):
    messages_qs = Message.objects.filter(departement=departement).order_by('-created_at')

    # Paginate EXEC department messages (10 per page)
    paginator = Paginator(messages_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "notifs-main-page.html", {
        "messages": page_obj,
        "departement": departement,
    })




def message_detail(request, slug):
    message = get_object_or_404(Message, slug=slug)
    return render(request, "notif-message-content.html", {"message": message})

def exe_departement_list(request):
    user = request.user
    if user.user_type == 'EXEC':
       g_info_messages = Message.objects.filter(departement='G.I').order_by('-created_at')
       d_info = Message.objects.filter(departement='D').order_by('-created_at')
       glt_info = Message.objects.filter(departement='GLT').order_by('-created_at')
       seg_info = Message.objects.filter(departement='SEG').order_by('-created_at')
       bts_info = Message.objects.filter(departement='BTS').order_by('-created_at')   
       gc_info = Message.objects.filter(departement='G.CIVIL').order_by('-created_at')    
       ba_info = Message.objects.filter(departement='BA').order_by('-created_at')
       jc_info = Message.objects.filter(departement='JC').order_by('-created_at')

       departements = {
            'G.INFO': g_info_messages,
            'D': d_info,
            'GLT': glt_info,
            'SEG': seg_info,
            'BTS': bts_info,
            'G.CIVIL': gc_info,
            'BA': ba_info,
            'JC': jc_info,
        }

       context = {
            'departements': departements,
        }
    return render(request, "exe-departements-list.html", context)

def about_us_view(request):
    return render(request, "a-propos.html")
# views.py
