import numpy as np
import cv2
import os

DISPLAY = False
BASE_DIR = "Images"
OUTPUT_DIR = "Csv"
CONTOURS_OUTPUT_DIR = "Contours"
PX_MM = 10


def get_contours(original_image, image, save_path):
    img = original_image.copy()
    # j = 535
    # print("i:",i," j:", j, end=" ")
    v = np.median(image)
    sigma = 0.33
    # ---- Apply automatic Canny edge detection using the computed median----
    i = int(max(0, (1.0 - sigma) * v))
    j = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, i, j)
    # display("ori", original_image)

    # display("canny", edged)
    # display("gray", image)
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    # display("Canny Edges After Contouring", edged)
    text = f"i:{i} j:{j} Number of Contours found = {len(contours)}"
    # print(text)
    boxes = []
    w_h_list = []
    for idx, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        (x, y), (width, height), angle = rect

        if width < 8 and height < 8:
            continue
        boxes.append(box)

        # cv2.putText(img, str(idx), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX,2, (0,0,255),5,2)

        w_h_list.append((width, height))

    '''for idx, w_h in enumerate(w_h_list):
        print(f"{idx}, {w_h[0]:.2f},{w_h[1]:.2f}\n")
    print("-----------------------------------------")
    '''
    cv2.drawContours(img, boxes, -1, (255, 0, 0), 2)
    display(text, img)
    # cv2.waitKey(0)
    cv2.imwrite(save_path, img)

    return w_h_list


def display(name, image):
    if not DISPLAY:
        return
    cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(name, image)
    cv2.resizeWindow(name, len(image[0]) // 4, len(image) // 4)


def bg_substraction(image):
    return cv2.createBackgroundSubtractorKNN().apply(image), \
           cv2.createBackgroundSubtractorMOG2().apply(image),


def px_to_mm(x):
    return x / PX_MM


def export_to_csv(file_path, lst):
    data = "num,width,height,width_mm,height_mm\n"

    for idx, val in enumerate(lst):
        data += f"{idx},{val[0]},{val[1]},{px_to_mm(val[0])},{px_to_mm(val[1])}\n"

    with open(file_path, "w") as f:
        f.write(data)


def get_files_from_dir(dir):
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def main():
    files = get_files_from_dir(BASE_DIR)
    files = sorted(files)
    files = sorted(files, key=len)
    for idx, file in enumerate(files):
        file_path = os.path.join(BASE_DIR, file)
        os.rename(file_path, os.path.join(BASE_DIR, f"img{idx + 1}.jpeg"))
    files = get_files_from_dir(BASE_DIR)

    for idx, file in enumerate(files):
        file_path = os.path.join(BASE_DIR, file)
        file_name_no_ext = os.path.splitext(file)[0]
        csv_file_path = os.path.join(OUTPUT_DIR, file_name_no_ext + '.csv')
        contours_file_path = os.path.join(CONTOURS_OUTPUT_DIR, file)
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        width_height_lst = get_contours(image, gray, contours_file_path)
        export_to_csv(csv_file_path, width_height_lst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
