/*
** EPITECH PROJECT, 2020
** main
** File description:
** Entry of the program
*/

#include <iostream>

#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

using Pixel = cv::Point3_<uint8_t>;

// static void modifyPixel(Pixel& pixel, const int* position [[ gnu::unused ]])
// {
    // pixel.x = 255;
// }

int main()
{
    // Create a VideoCapture object and use camera to capture the video
    cv::VideoCapture cap("test.mp4");
    if (!cap.isOpened()) {
        std::cerr << "Error opening video stream" << std::endl;
        return -1;
    }

    cv::namedWindow("mainWin", cv::WINDOW_NORMAL); // create new window
    cv::setWindowProperty("mainWin", cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN); // set fullscreen property

    while (1) {
        cv::Mat frame;

        // Capture frame-by-frame
        cap >> frame;

        // If the frame is empty, break immediately
        if (frame.empty()) {
            break;
        }

        // Display the resulting frame
        imshow("mainWin", frame);

        // cv::Mat modifiedFrame;
        // frame.forEach<Pixel>(&modifyPixel);
        // cv::resize(frame, modifiedFrame, cv::Size(1920, 1080), 0, 0, cv::INTER_AREA);
        // imshow("mainWin", modifiedFrame);

        // Press  ESC on keyboard to  exit
        char c = (char)cv::waitKey(1);
        if (c == 27) {
            break;
        }
    }
    cv::destroyAllWindows();
    return 0;
}
