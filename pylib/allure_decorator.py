import allure


def allure_decorator(epic=None, feature=None, story=None, title=None):
    def decorator(func):
        if epic:
            func = allure.epic(epic)(func)
        if feature:
            func = allure.feature(feature)(func)
        if story:
            func = allure.story(story)(func)
        if title:
            func = allure.title(title)(func)
        return func
    return decorator
