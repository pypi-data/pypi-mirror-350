import numpy as np

class Time():
    def JD(self, year: int, month: int, day: int, hour: int, minutes: int, seconds: int):
        if month <= 2:
            month += 12
            year -= 1

        a = np.floor(year / 100)
        b = 2 - a + np.floor(a / 4)
        Jd = np.floor(365.25 * (year + 4716)) + np.floor(30.6001 * (month + 1)) + day + b - 1524.5 + hour / 24 + minutes / 1440 + seconds / 86400
    
        return Jd
    
    def day_number(self, month: int, mday: int, is_Leap: bool):
        if is_Leap:
            year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        l = []
        if month == 1:
            return mday
        if month != 1:  
            for i, el in enumerate(year):
                if i < month:
                    l.append(el)
                if i == month:
                    c = np.sum(l)
                    n = c + mday
                    break
            return n

    def GST_date_Earth(self, utc_year: int, utc_month: int, utc_mday: int, utc_hour: int, utc_min: int, utc_sec: int):
        date = [utc_year, utc_month, utc_mday, utc_hour, utc_min, utc_sec]
        d = self.JD(date[0], date[1], date[2], date[3], date[4], date[5]) - 2451545.0
        h = utc_hour + utc_min/60+utc_sec/3600
        GST_12am_J2000 = 6.69737
        dt = 0.06571
        sol_to_sid = 1.00274
        gst = GST_12am_J2000+dt*d+sol_to_sid*h
        gst_deg = gst%360
        # hours, minutes, seconds
        gst_hour = [int(gst_deg/15), ((gst_deg/15) - int(gst_deg/15))*60, 
                    (((gst_deg/15) - int(gst_deg/15))*60 - int(((gst_deg/15) - int(gst_deg/15))*60))*60]

        return gst_hour, gst_deg
    
    def LST_date_Earth(self, longitude: int | float, utc_year: int, utc_month: int, utc_mday: int, utc_hour: int, utc_min: int, utc_sec: int):
        dt = longitude/15
        gst_hour, gst_deg = self.GST_date_Earth(utc_year, utc_month, utc_mday, utc_hour, utc_min, utc_sec)
        lst = (gst_deg+dt)%24
        return lst
    
    # PTC - Planetary Time Coordinated
    # Start PJD - значение счётчика секунд которое вы хотите поставить на момент эпохи start_JD
    # По сути, это точка начала отсчёта секунд до или после эпохи J2000.0
    # И вы ставите сколько секунд до или после эпохи уже прошло в момент start_PJD
    # Например, я хочу чтобы start_JD было 2451540, и пишу что в этот момент start_PJD было равно 0 (или любому другому числу)
    def PTC_offset(self, Planet_is_Mars: bool, start_PJD: int | float, start_JD: int | float, planet_day_hours: int | float):
        if Planet_is_Mars:
            epoch = self.JD(2000, 1, 6, 12, 0, 0)
        else:
            epoch = self.JD(2000, 1, 1, 12, 0, 0)
        offset = start_PJD - (((start_JD - epoch)*86400) / (planet_day_hours*86400))
        return offset

    def PTC_date(self, planet_day_sec: int | float, offset: int | float, Planet_is_Mars: bool, utc_year: int, utc_month: int, utc_mday: int, utc_hour: int, utc_min: int, utc_sec: int):
        epoch_date = self.JD(utc_year, utc_month, utc_mday, utc_hour, utc_min, utc_sec)

        if Planet_is_Mars:
            epoch = self.JD(2000, 1, 6, 12, 0, 0)
        else:
            epoch = self.JD(2000, 1, 1, 12, 0, 0)

        epoch_sec = (epoch_date - epoch)*86400
        ptc = (epoch_sec/planet_day_sec) % 1 * 24 + offset
        hours = int(ptc)
        minutes = (ptc-hours)*60
        seconds = (minutes-int(minutes))*60
        ptc_time = [hours, minutes, seconds]
        ptc_lon = 360/(planet_day_sec / 24 / 60)*ptc
        return ptc_time
    
    def PTC_ST_date(self, planet_day_sec: int | float, offset: int | float, Planet_is_Mars: bool, PTC_ST_12am_J2000: int | float, utc_year: int, utc_month: int, utc_mday: int, utc_hour: int, utc_min: int, utc_sec: int):
        ptc_date = self.PTC_date(planet_day_sec, offset, Planet_is_Mars, utc_year, utc_month, utc_mday, utc_hour, utc_min, utc_sec)
        d = self.JD(0, 0, 0, ptc_date[0], ptc_date[1], ptc_date[2]) - 2451545.0
        h = ptc_date[0]+ptc_date[1]/60+ptc_date[2]/3600
        dt = 0.06571
        sol_to_sid = 1.00274
        ptc_st_now = PTC_ST_12am_J2000+dt*d+sol_to_sid*h
        ptc_st_deg = ptc_st_now%360
        coeff = 360/(planet_day_sec/24/60)
        # hours, minutes, seconds
        ptc_st_hour = [int(ptc_st_deg/coeff), ((ptc_st_deg/coeff) - int(ptc_st_deg/coeff))*60, 
                    (((ptc_st_deg/coeff) - int(ptc_st_deg/coeff))*60 - int(((ptc_st_deg/coeff) - int(ptc_st_deg/coeff))*60))*60]
        return ptc_st_hour, ptc_st_deg
