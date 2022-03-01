import os
import time

from string import Template


SCRIPT_FILE_PATH = "temp/script-${UUID}.js"
TEMPLATE_FILE_PATH = "templates/report.html"
REPORT_FILE_PATH = "report/report.html"


def render_result_to_html(env, executed, failed, owner, comment):
    """
    Render result to HTML file.

    """
    project_working_directory = os.getcwd()
    template_file = os.path.join(project_working_directory, TEMPLATE_FILE_PATH)
    report_file = os.path.join(project_working_directory, REPORT_FILE_PATH)
    with open(template_file, 'r') as f:
        template = f.read()
    template = Template(template)
    pass_rate = round((int(executed) - int(failed)) / int(executed) * 100, 2)
    if float(pass_rate) == 100.0:
        bg_color = '#33cc33'
    elif float(pass_rate) < 60.0:
        bg_color = 'ff3300'
    else:
        bg_color = 'ffff00'
    report = template.substitute(env=env, date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), executed=executed,
                                 failed=failed, pass_rate=str(pass_rate) + '%', bg_color=bg_color,
                                 owner=owner, comment=comment)
    with open(report_file, mode='w') as f:
        f.write(report)