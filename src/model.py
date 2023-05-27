import cv2
import numpy as np
import matplotlib.pyplot as plt


class MyModel:
    def _process_rice_image(self, imgs):
        res_cnts = []
        for img in imgs:
            rice_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # print(plt.imshow(rice_gray, cmap='gray'))
            rice_blur = cv2.GaussianBlur(rice_gray, (11, 11), 0)
            # plt.imshow(rice_blur, cmap='gray')
            rice_canny = cv2.Canny(rice_blur, 30, 150, 5)
            # print(plt.imshow(rice_canny, cmap='gray'))
            rice_dilated = cv2.dilate(rice_canny, (1, 1), iterations=2)
            # print(plt.imshow(rice_dilated, cmap="gray"))
            (cnts, heirarchy) = cv2.findContours(rice_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.drawContours(rice_canny, cnts, -1, (0, 255, 0), 2)
            # print(plt.imshow(rice_gray))
            res_cnts.append(cnts)
        return res_cnts

    def _process_black_rice_image(self, imgs):
        lower_bound = np.array([0, 0, 0])
        upper_bound = [
            np.array([55, 55, 55]),
            np.array([62, 62, 62]),
            np.array([68, 68, 68]),
            # for avg
            np.array([72, 72, 72]),

            np.array([72, 72, 72])
        ]

        res_cnts = []
        for i, img in enumerate(imgs):
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # define kernel size
            kernel = np.ones((7, 7), np.uint8)
            # find the colors within the boundaries
            mask = cv2.inRange(rgb, lower_bound, upper_bound[2])

            # Remove unnecessary noise from mask
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Segment only the detected region
            segmented_img = cv2.bitwise_and(img, img, mask=mask)

            cnts, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            res_cnts.append(cnts)
            output = cv2.drawContours(segmented_img, cnts, -1, (0, 0, 255), 3)
        return res_cnts

    def _print_items(self, rice_counts, black_rice_counts):
        print('Results: ')
        for i in range(0, len(rice_counts)):
            print('file', i + 1, ': ')
            print('\tBlack Rice:', len(black_rice_counts[i]))
            print('\tRice:', len(rice_counts[i]))

    def process_image(self, imgs):
        # imgs = [cv2.imread (img_path) for img_path in img_paths]
        cnt_rice = self._process_rice_image(imgs)
        cnt_black_rice = self._process_black_rice_image(imgs)
        self._print_items(cnt_rice, cnt_black_rice)

        #  output

        res = []
        for i in range(len(imgs)):
            res.append(
                {
                    'black_rice': len(cnt_black_rice[i]),
                    'rice': len(cnt_rice[i])
                }
            )
        # return cnt_rice, cnt_black_rice
        return res;

# if __name__ == "__main__":
#     model = MyModel()
#     res = []
#     img_names = [
#         "../img/count_1.jpg",
#         "../img/count_2.jpg",
#         "../img/count_3.jpg",
#         "../img/count_4.jpg",
#         "../img/count_5.jpg"
#     ]
#     imgs = []
#     # load data
#     for img_sing in img_names:
#         temp_img = cv2.imread(img_sing)
#         print(cv2.imshow("image", temp_img))
#         # waits for user to press any key
#         # (this is necessary to avoid Python kernel form crashing)
#         cv2.waitKey(0)
#
#         # closing all open windows
#         cv2.destroyAllWindows()
#         imgs.append(temp_img)
#
#     # load data
#     res_cnt, black_rice_cnt = model.process_image(imgs)
