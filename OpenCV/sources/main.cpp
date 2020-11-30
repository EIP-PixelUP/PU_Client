/*
** EPITECH PROJECT, 2020
** main
** File description:
** Entry of the program
*/

#include <iostream>

#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>

int main()
{
    // Create a VideoCapture object and use camera to capture the video
    cv::VideoCapture cap("test.mp4");
    if (!cap.isOpened()) {
        std::cerr << "Error opening video stream" << std::endl;
        return -1;
    }

    while (1) {
        cv::Mat frame;

        // Capture frame-by-frame
        cap >> frame;

        // If the frame is empty, break immediately
        if (frame.empty()) {
            break;
        }

        // Display the resulting frame
        imshow("Frame", frame);

        // Press  ESC on keyboard to  exit
        char c = (char)cv::waitKey(1);
        if (c == 27) {
            break;
        }
    }
    return 0;
}
