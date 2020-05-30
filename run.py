from web_scraping import *
from course import User
from gui import gui_interact

#TODO use method to track credits where applicable instead of augmenting
#TODO Add all courses
#TODO look for a more efficient way to store this data


applet = gui_interact.create_basic_app()
u = User()
gui_interact.set_courses_bottom(applet)
gui_interact.set_header(applet, u)

applet.get_main().mainloop()