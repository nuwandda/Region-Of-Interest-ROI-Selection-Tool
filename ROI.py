import cv2
import math

points = []         #This list stores the actual coordinates of rectangle.
flag = False        #This flag checks whether the first rectangle is completed or not.
click_flag = False  #This flag starts select_edit_point in select_points.
click_flag2 = False #This flag checks whether select_edit_point is done or not.
click_flag3 = False #This flag controls main loop by checking all functions.
edit_flag = False   #This flag controls editing only for one point.
first_click = True  #This flag checks whether its first click or not.
finish_flag = False #This flag gives us the new image in the main loop.

#A function for calculating distance.
def distance(p0x, p0y, p1x, p1y):
    return math.sqrt((p0x - p1x)**2 + (p0y - p1y)**2)

#A function that checks a point is valid or not.
def check_position(p0x, p0y, p1x, p1y):
    if ((p1x + 10) < p0x) and ((p1y + 10) < p0y):
        return True
    else:
        return False


#This function lets user to select two points on the screen
#and then draws a rectangle with those points.
def select_points(event, x, y, flags, param):
    global points,flag,click_flag,first_click, click_flag3, input_flag

    if event == cv2.EVENT_LBUTTONDBLCLK and first_click == True:
        points.append(x)
        points.append(y)
        first_click = False

    elif event == cv2.EVENT_LBUTTONDBLCLK and check_position(x, y, points[0], points[1]):
        points.append(x)
        points.append(y)

        if distance(points[0], points[1], points[2], points[3]) > 10:
            flag = True
            click_flag = True
            click_flag3 = True
            cv2.rectangle(image, (points[0], points[1]), (points[2], points[3]), (0, 0, 255), 2)
            cv2.circle(image, (points[0], points[1]), 2, (0, 255, 0), -1)
            cv2.circle(image, (points[2], points[3]), 2, (0, 255, 0), -1)
            cv2.circle(image, (points[0], points[1]), 10, (0, 255, 255))
            cv2.circle(image, (points[2], points[3]), 10, (0, 255, 255))


        cv2.imshow("image", image)
        if click_flag == True:
            cv2.setMouseCallback("image", select_edit_point)

#With this function, after selecting the first points on the screen,
#you can select a point that is still on the screen to determine which point you are going
#edit.
def select_edit_point(event, x, y, flags, param):
    global editing_points,flag,edit_flag,click_flag2, click_flag3, input_flag

    if flag == True and event == cv2.EVENT_LBUTTONDBLCLK:

        #Next two lines calculate distance between the points
        dist_to_top = distance(x, y, points[0], points[1])
        dist_to_bot = distance(x, y, points[2], points[3])
        if dist_to_top < 10 and edit_flag == False:
            cv2.circle(image, (points[0], points[1]), 2, (255, 0, 255), -1)
            edit_flag = True
            click_flag2 = False
            click_flag3 = True
            #Starts another mouse activity for selecting new location for last selected point.
            cv2.setMouseCallback("image", new_top_point)
        elif dist_to_bot < 10 and edit_flag == False:
            cv2.circle(image, (points[2], points[3]), 2, (255, 0, 255), -1)
            edit_flag = True
            click_flag2 = False
            click_flag3 = True
            #Starts another mouse activity for selecting new location for last selected point.
            cv2.setMouseCallback("image", new_bot_point)

#After selection of editing points, this function draws new rectangle with new point.
def new_bot_point(event, x, y, flags, param):
    global editing_points, click_flag2, edit_flag,image, finish_flag, click_flag3, input_flag

    if event == cv2.EVENT_LBUTTONDBLCLK and check_position(x, y, points[0], points[1]) == True:
        if click_flag2 == False:
            cv2.rectangle(clone, (points[0], points[1]), (x, y), (0, 0, 255), 2)
            cv2.circle(clone, (points[0], points[1]), 2, (0, 255, 0), -1)
            cv2.circle(clone, (x, y), 2, (0, 255, 0), -1)
            cv2.circle(clone, (points[0], points[1]), 10, (0, 255, 255))
            cv2.circle(clone, (x, y), 10, (0, 255, 255))
            points[2] = x
            points[3] = y
            click_flag2 = True
            edit_flag = False
            finish_flag = True
            click_flag3 = False
            cv2.setMouseCallback("image", select_edit_point)

#After selection of editing points, this function draws new rectangle with new point.
def new_top_point(event, x, y, flag, param):
    global editing_points, click_flag2, edit_flag, finish_flag, click_flag3, input_flag

    if event == cv2.EVENT_LBUTTONDBLCLK and check_position(points[2], points[3], x, y) == True:
        if click_flag2 == False:
            cv2.rectangle(clone, (x, y), (points[2], points[3]), (0, 0, 255), 2)
            cv2.circle(clone, (x, y), 2, (0, 255, 0), -1)
            cv2.circle(clone, (points[2], points[3]), 2, (0, 255, 0), -1)
            cv2.circle(clone, (x, y), 10, (0, 255, 255))
            cv2.circle(clone, (points[2], points[3]), 10, (0, 255, 255))
            points[0] = x
            points[1] = y
            click_flag2 = True
            edit_flag = False
            finish_flag = True
            click_flag3 = False
            cv2.setMouseCallback("image", select_edit_point)

#Just a function for saving data to a txt file. Giving points as arguement.
def write_points(p0x, p0y, p1x, p1y):
    name = input('Enter the name of the object you are going to select : ')
    text_file = open("roi_file.txt", "w")
    text_file.write(str(name) + str((p0x, p0y)) + str((p1x, p1y)))
    text_file.close()

image = cv2.imread("img2.jpg")
clone = cv2.imread("img2.jpg")
cv2.namedWindow("image")
cv2.setMouseCallback("image", select_points)
click_flag3 = True

while True:
    #This condition shows the edited image on the screen.
    if finish_flag == True:
        cv2.imshow("image", clone)
        image = clone
        clone = cv2.imread("img2.jpg")
        finish_flag = False
    #If the top condition fails, then this condition gives us all images except the last
    #one, the edited rectangle.
    elif click_flag3 == True:
        cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
write_points(points[0], points[1],points[2], points[3])


