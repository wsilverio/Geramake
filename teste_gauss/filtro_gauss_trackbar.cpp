#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui_c.h>
#include <string>

using namespace cv;
using namespace std;

Mat img, filtro;
int m = 5; // largura e altura do filtro
int sigma = 3;

void filtragem(int, void *){

    // impar e positivo
    m |= 1;

    GaussianBlur(img, filtro, Size(m, m), sigma);
    // GaussianBlur(img, filtro, Size(m, m), -sigma);

    // Mat sub = img - filtro;

    imshow("filtro gaussiano", filtro);

    // imshow("img - filtro", sub);
    // moveWindow("img - filtro", sub.cols + 30, 30);
}

int main(void){

    // img = imread("../images/Lenna.png");
    img = imread("Fig0340(a)(dipxe_text).tif");

    namedWindow("filtro gaussiano", WINDOW_AUTOSIZE);

    createTrackbar("m x m: ", "filtro gaussiano", &m, 35, filtragem);
    createTrackbar("sigma: ", "filtro gaussiano", &sigma, 10, filtragem);
    filtragem(m, 0);

    waitKey();

    return 0;
}
