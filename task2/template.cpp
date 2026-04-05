#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;

int main()
{
    // Load the three fragment images as grayscale — do not change these lines
    cv::Mat frag_a = cv::imread("./assets/fragment_a.png", cv::IMREAD_GRAYSCALE);
    cv::Mat frag_b = cv::imread("./assets/fragment_b.png", cv::IMREAD_GRAYSCALE);
    cv::Mat frag_c = cv::imread("./assets/fragment_c.png", cv::IMREAD_GRAYSCALE);

    if (frag_a.empty() || frag_b.empty() || frag_c.empty()) {
        cerr << "Could not load one or more fragment images from ./assets/\n";
        return -1;
    }

    // TODO: reverse the charm on each fragment, merge the recovered channels
    // into a single BGR image, save it as ./assets/memory_restored.png,
    // and print the number of non-zero pixels in the result.

    cv::Mat s1, s2, s3;
    mat1.convertTo(s1, CV_32S);
    mat2.convertTo(s2, CV_32S);
    mat3.convertTo(s3, CV_32S);
    return 0;
}
