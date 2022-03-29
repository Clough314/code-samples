from datetime import date, timedelta
from calendar import monthrange
from math import *
from skyfield import api, almanac
from fpdf import FPDF

YEAR = 2021
LOCATION = api.wgs84.latlon(+40.808889, -96.678889)

ts = api.load.timescale()
eph = api.load('de421.bsp')

t0 = ts.utc(YEAR, 1, 1)
t1 = ts.utc(YEAR, 12, 31)

t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, LOCATION))
sunrise = {e[0].utc_datetime().date(): e[0].utc_datetime().time() for e in zip(t, y) if e[1]}

t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))

# This logic reconciles a lunar-solar calendar with Gregorian.
uposathas = dict()
for uposatha, phase in zip(t, y):
    t_sun = sunrise[uposatha.utc_datetime().date()]
    t_moon = uposatha.utc_datetime().time()
    if t_moon < t_sun:
        uposathas[uposatha.utc_datetime().date() - timedelta(days = 1)] = phase
    else:
        uposathas[uposatha.utc_datetime().date()] = phase

# I redacted some hardcoded lists here for privacy.
# WEEKLY, MONTHLY, etc. should ideally be populated from CSV or similar.

pdf = FPDF('L', 'cm', 'Letter')

def print_tasks(heading, tasks, top): # handles column wrapping
    left = pdf.get_x()
    if pdf.get_y() + 0.65 * 2 > 20:
        pdf.set_y(top)
        pdf.set_x(left+5.2)
        left = pdf.get_x()
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(3.7, 0.65, txt=heading, ln=2)
    pdf.set_font('Arial', '', 11)
    for task in tasks:
        pdf.cell(0.5, 0.5, border=1)
        pdf.cell(0.075, 0.5)
        pdf.cell(3.5, 0.5, txt=task, ln=2)
        pdf.set_xy(pdf.get_x() - 0.5 - 0.075, pdf.get_y() + 0.15)
        print(pdf.get_y())
        if pdf.get_y() + 0.65 > 20:
            pdf.set_y(top)
            pdf.set_x(left+5.2)
            left = pdf.get_x()

# This mess is just printing task lists with headings and rows of checkboxes.
# If I wrote this now, I'd do it in LuaTeX to avoid all the manual formatting.
for month in range(12):

    month += 1
    month_curr = date(YEAR, month, 1)
    month_next = date(YEAR + (month == 12), month * (month != 12) + 1, 1)
    num_days = (month_next - month_curr).days
    dates = [date(YEAR, month, n + 1) for n in range(num_days)]

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, txt=month_curr.strftime('%B'), align='C')
    pdf.ln(1)

    pdf.set_font('Arial', '', 11)
    pdf.cell(3.7)
    for n in range(num_days):
        pdf.cell(0.65, txt=str(n+1), align='C')
    pdf.ln(0.5)

    for task in DAILY:
        pdf.cell(3.5, 0.5, txt=task, align='R')
        pdf.cell(0.2)
        for n in range(num_days):
            pdf.cell(0.075, 0.5)
            pdf.cell(0.5, 0.5, border=1)
            pdf.cell(0.075, 0.5)
        pdf.ln(0.65)

    pdf.ln(0.3)

    top = pdf.get_y()
    for d in dates:
        weekday = d.strftime('%a')
        tasks = list()
        heading = str()
        if d.day == 1:
            heading = d.strftime('%a') + f'. 1--7'
            if d.month == 1:
                tasks = MONTHLY + ANNUALLY + SEMIANNUALLY
            elif d.month == 7:
                tasks = MONTHLY + SEMIANNUALLY
            else:
                tasks = MONTHLY
            print_tasks(heading, tasks, top)
        if d.weekday() == 5: # Saturday
            heading = f'Sat. {d.day}--{(d + timedelta(days=1)).day}'
            if d.timetuple().tm_yday % 2 == 0:
                tasks = WEEKLY
            else:
                tasks = WEEKLY + BIWEEKLY
            print_tasks(heading, tasks, top)
        if d in uposathas:
            heading = d.strftime('%a') + f'. {d.day} (Q{uposathas[d]})'
            tasks = UPOSATHA
            print_tasks(heading, tasks, top)

    pdf.ln(1)

pdf.output('chort.pdf')
