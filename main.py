import requests
from datetime import datetime
import smtplib

MY_LAT = 12.968570  # Your latitude
MY_LONG = 79.140320  # Your longitude
my_email = [YOUR-EMAIL]
password = [YOUR-PASSWORD]


while True:
    time_now = datetime.now()
    hour_current = time_now.hour
    min_current = time_now.minute
    sec_current = time_now.second
    if sec_current == 0:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        # Your position is within +5 or -5 degrees of the ISS position.


        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5
        sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5
        sunrise_min = int(data["results"]["sunrise"].split("T")[1].split(":")[1])
        sunset_min = int(data["results"]["sunset"].split("T")[1].split(":")[1])

        if sunrise_min < 30:
            sunrise_min_req = sunrise_min + 30
        else:
            sunrise_min_req = 30 - (60 - sunrise_min)

        if sunset_min < 30:
            sunset_min_req = sunrise_min + 30
        else:
            sunset_min_req = 30 - (60 - sunset_min)


        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and sunrise_hour <= hour_current <= sunset_hour and sunrise_min <= min_current <= sunset_min:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=[RECEIPIENT EMAIL],
                                    msg=f"Subject:SPOT THE STATION\n\nThe International Space Station is currently "
                                        f"just above you and when"
                                        f" you gaze up at the sky NOW, you'll spot the station zooming above your "
                                        f"head.\nCHECK "
                                        f" IT OUT QUICK !!!\nThe current time is {hour_current}:{min_current}"
                                    )

    


