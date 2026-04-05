#include <iostream>
#include <opencv2/opencv.hpp>
#include <convolution.hpp>
#include <bits/stdc++.h>

using namespace std;

int main()
{
    // The two kernels — do not change these
    cv::Mat K1 = (cv::Mat_<double>(3, 3) <<
         1,  2,  1,
         0,  0,  0,
        -1, -2, -1
    );

    cv::Mat K2 = (cv::Mat_<double>(3, 3) <<
         1,  0, -1,
         2,  0, -2,
         1,  0, -1
    );

    cv::Mat img = cv::imread("./assets/hogwarts.png", cv::IMREAD_COLOR);
    cv::Mat img_f;
    img.convertTo(img_f, CV_64FC1);

    if (img.empty()) {
        cerr << "Could not load image at ./assets/hogwarts.png\n";
        return -1;
    }

    cv::Mat K1_v = (cv::Mat_<double>(3, 1) << 1, 0, -1);
    cv::Mat K1_h = (cv::Mat_<double>(1, 3) << 1, 2, 1);

    cv::Mat K2_v = (cv::Mat_<double>(3, 1) << 1, 2, 1);
    cv::Mat K2_h = (cv::Mat_<double>(1, 3) << 1, 0, -1);

    cv::Mat intermediate1;
    cv::Mat intermediate2;
    cv::Mat intermediate3;

    intermediate1 = convolve(img, K1_v);         // Convolve Vertically
    intermediate2 = convolve(intermediate1, K1_h);        // Convolve Horizontally
    intermediate3 = convolve(intermediate2, K2_v);
    img_f = convolve(intermediate3, K2_h);

    cv::namedWindow("Output", cv::WINDOW_NORMAL);
    cv::imshow("Output", img_f);
    cv::waitKey(0); // Wait for key press before moving to the next image

    // TODO: apply K1 and K2 to img_f with as few multiplications per pixel as possible.
    // Print the number of multiplications your approach uses per pixel.

    return 0;
}
