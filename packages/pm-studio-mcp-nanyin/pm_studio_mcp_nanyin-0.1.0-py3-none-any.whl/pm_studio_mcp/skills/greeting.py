from pm_studio_mcp.constant import GREETING_TEMPLATE

class GreetingUtils:
    @staticmethod
    def greeting_with_pm_studio(name: str):
        """
        Respond to a greeting message with a formatted template.
        """
        return f"use command tool to print '{GREETING_TEMPLATE.format(name=name)}', and end the task."