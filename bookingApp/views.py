from django.shortcuts import render
import datetime

from .models import appointments

def homePage(request):

    # get today's date
    today = datetime.date.today()

    # calculate the date for Monday of this week
    monday = today - datetime.timedelta(days=today.weekday())

    # create a list to store the working days
    working_days = []

    # iterate over the range of days in the week, and append the weekdays to the list
    for i in range(5):
        working_days.append(monday + datetime.timedelta(days=i))

   
    start_time = datetime.time(hour=13, minute=0)
    end_time = datetime.time(hour=0, minute=0)

    time_delta = datetime.timedelta(minutes=30)
    shift_hours = ["00:00 AM"]

    while start_time != end_time:
        shift_hours.append(start_time.strftime('%I:%M %p'))
        start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + time_delta).time()

    #print(shift_hours)

    sessions=[]

    for i in range(1,len(shift_hours)):
        try:
            session = shift_hours[i] , shift_hours[i+1]
            sessions.append(session)
        except:
            pass
    sessions[-1]=('11:30 PM', '00:00 AM')

    gunler=["PAZARTESİ","SALI","ÇARŞAMBA","PERŞEMBE","CUMA"]

    present = datetime.datetime.now()

    if request.method == 'POST':
        selected_staff = request.POST.get('psikologSecimi')
        #print(selected_staff)

        selected_sessions=request.POST.getlist("session")
        dates=[]
        session=[]
        for a in selected_sessions:
            sub_item=a.split("*")
            dates.append(sub_item[1])
            session.append(sub_item[0])
            
        old_date_checker=[]
        for i in range(0,len(dates)):
            try:
                date1 = datetime.datetime.strptime(dates[i], "%b. %d, %Y")
            except:
                date1 = datetime.datetime.strptime(dates[i], '%B %d, %Y')

            old_date_checker.append(present < date1)

        

        if all(old_date_checker) and len(session) >= 8:
            obj = appointments()
            obj.psikolog=selected_staff
            obj.randevu_tarihi=dates
            obj.randevu_saati=session
            obj.save()
            print("Randevu sistemine kayıt yapıldı.")
            return render(request,"completed.html")
        else:
            print("Geçerli bir tarih giriniz veya haftalık 8 saat zorunlu seansı doldurunuz.")
            return render(request,"failed.html")
    return render(request, "home.html",{"days":working_days,"sessions":sessions,"gunler":gunler})



def calendar(request):
    staff = appointments.objects.all()


    return render(request,"calendar.html",{"staff":staff})