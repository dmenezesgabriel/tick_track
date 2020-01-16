from src.controllers.activity import DefaultActivity as activity_controller


async def load_all():
    return activity_controller.load_all()


async def load_today():
    return activity_controller.load_today()


async def load_range(start_date, end_date):
    return activity_controller.load_range(start_date, end_date)
