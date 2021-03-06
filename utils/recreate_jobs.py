import asyncio

from loader import cities, tracking
from utils import (
    get_prayer_data,
    schedule_all,
    schedule_calendar_gen,
    setup_city,
)


async def recreate_jobs():
    """Recreate jobs for the apscheduler.

    This function will be called on startup. Updates prayer times and schedules
    reminders for everyone. Also schedules calendar generation for all users
    who have tracking on.
    """

    user_cities = await cities.find().to_list(None)
    user_cities = [city["city"] for city in user_cities]

    for city in user_cities:
        await setup_city(city)
        prayer_times, hijri_date = await get_prayer_data(city)
        await schedule_all(city, prayer_times, hijri_date)
        # to try and avoid sending too many requests
        await asyncio.sleep(5)

    tracking_on_users = await tracking.find().to_list(None)

    for user in tracking_on_users:
        tg_user_id = user["tg_user_id"]
        await schedule_calendar_gen(tg_user_id)
