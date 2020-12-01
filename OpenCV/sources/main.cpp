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
        // imshow("mainWin", frame);
        // frame.forEach<Pixel>(&modifyPixel);

        cv::Mat downscaled;
        cv::resize(frame, downscaled, cv::Size(), 0.25, 0.25, cv::INTER_AREA);
        cv::Mat upscaled;
        cv::resize(downscaled, upscaled, cv::Size(), 4, 4, cv::INTER_AREA);

        cv::Mat concatenated;
        cv::hconcat(frame, upscaled, concatenated);
        imshow("mainWin", concatenated);

        // Press  ESC on keyboard to  exit
        char c = (char)cv::waitKey(1);
        if (c == 27) {
            break;
        }
    }
    cv::destroyAllWindows();
    return 0;
}
