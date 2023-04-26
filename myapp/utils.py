import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .forms import CreateUserForm, LoginForm
def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    '''form = LoginForm(request.POST)
    
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            email = request.POST.get('email')
            send_mail(
                'OTP',
                otp,
                'sagarkokadiya321@gmail.com',
                [email],
                fail_silently= False,
                )'''
    print(f"Your one time password is {otp}")
    
            