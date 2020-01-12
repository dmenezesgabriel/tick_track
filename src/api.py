from src.controllers.activity import DefaultActivity as activity_controller


async def load_activities():
    return activity_controller.load_activities()
