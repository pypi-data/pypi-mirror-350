__version__ = "0.5"


def info():
    return {
        "name": "Hamidreza",
        "age": 22,
        "major": "Computer Engineering",
        "job": "Full Stack Developer",
        "focus": "AI Development",
        "site": "https://hamidrezamoghaddam.ir",
        "email": "h4midrezam@gmail.com"
    }


def time():
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def say_hello(name=None):
    """Returns a greeting message"""
    if name:
        return f"Hello {name}! I'm Hamidreza, nice to meet you."
    return "Hello! I'm Hamidreza Moghaddam, a Full Stack Developer focused on AI."


def get_skills():
    """Returns a list of skills"""
    return [
        "Full Stack Development",
        "AI Development",
        "Python Programming",
        "Web Development",
        "Data Science",
        "Machine Learning"
    ]


def about_me():
    """Returns more detailed information about Hamidreza"""
    return """
    I'm Hamidreza Moghaddam, a 22-year-old Full Stack Developer with a focus on AI development.
    I have a background in Computer Engineering and I'm passionate about creating innovative solutions.
    Currently working on AI projects and exploring new technologies.
    Feel free to reach out to me at h4midrezam@gmail.com or visit my website at hamidrezamoghaddam.ir
    """
