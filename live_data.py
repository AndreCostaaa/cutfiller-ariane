import numpy as np
import cv2
import os
import pylab as plt
import matplotlib.image as mpimg

DISPLAY = True
BASE_DIR = "Images"
OUTPUT_DIR = "Csv"
CONTOURS_OUTPUT_DIR = "Contours"
def get_contours(original_image, image, save_path):

    contours = None
    img = original_image.copy()
    #j = 535
    #print("i:",i," j:", j, end=" ")

    high_thresh, thresh_im = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    v = np.median(image)
    sigma = 0.33
    # ---- Apply automatic Canny edge detection using the computed median----
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    #display("ori", original_image)
    edged = cv2.Canny(image,lower ,upper)
    #display("canny", edged)
    cv2.imshow("Edged", edged)
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    #display("Canny Edges After Contouring", edged)
    text = f"i:{lower} j:{upper} Number of Contours found = {len(contours)}"
    boxes = []
    w_h_list = []


    for idx, contour in enumerate(contours):

        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        (x, y), (width, height), angle = rect

        if width < 10 and height < 10:
            continue
        boxes.append(box)

        #cv2.putText(img, str(idx), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX,2, (0,0,255),5,2)

        w_h_list.append((width, height))
    '''
    for idx, w_h in enumerate(w_h_list):
        print(f"{idx}, {w_h[0]:.2f},{w_h[1]:.2f}\n")
    print("-----------------------------------------")
    '''
    return text, boxes

    cv2.imshow(text, img)
    #display(text,img)
    #cv2.destroyAllWindows()

    '''
    fig = plt.figure(figsize=(15,8))
    fig.add_subplot(121)
    plt.title(f"i: {i} j: {j} contours: {len(contours)}")
    plt.imshow(edged)

    fig.add_subplot(122)
    plt.title("image")
    plt.imshow(img)
    plt.show()
    '''

    # Draw all contours
    # -1 signifies drawing all contours
    #cv2.drawContours(original_image, contours, -1, (0, 255, 0), 3)
    #display(save_path, original_image)
    #cv2.imwrite(save_path, img)
    #cv2.destroyAllWindows()
    return w_h_list


def display(name, image):
    if not DISPLAY:
        return
    cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(name, image)
    cv2.resizeWindow(name, len(image[0]) // 4, len(image) // 4)
    cv2.waitKey(0)


def bg_substraction(image):

    return cv2.createBackgroundSubtractorKNN().apply(image),\
           cv2.createBackgroundSubtractorMOG2().apply(image),

def export_to_csv(file_path, lst):

    data = "num,width,height\n"

    for idx, val in enumerate(lst):
        data += f"{idx},{val[0]:.2f},{val[1]:.2f}\n"

    with open(file_path, "w") as f:
        f.write(data)

def get_files_from_dir(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def main():
    # Create an object to hold reference to camera video capturing
    vidcap = cv2.VideoCapture(0)

    while True:
        if not vidcap.isOpened():
            break
        ret, frame = vidcap.read()
        # continue to display window until 'q' is pressed
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text, boxes = get_contours(frame,gray, "")
        cv2.drawContours(frame, boxes, -1, (255, 0, 0), 2)
        cv2.imshow("Frame", frame)  # show captured frame
        print(text)
        cv2.imshow("Gray", gray)
        # press 'q' to break out of the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()