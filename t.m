img1 = imread('lena1.jpg');
BW1 = im2bw(img1,0.95);
BW2 = double(BW1);

w45 = [-2 -1 0; -1 0 -1; 0 1 2]     %正45度检测模板
g45 = imfilter(BW2, w45);   %对图像img进行滤波

BWsv = edge(BW2, 'sobel', 0.1, 'vertical');
BWsh = edge(BW2, 'sobel', 0.1, 'horizontal');
BWph = edge(BW2, 'prewitt', 0.1, 'horizontal');
BWpv = edge(BW2, 'prewitt', 0.1, 'vertical');
subplot(2,3,1),imshow(img1);title('origin');
subplot(2,3,2),imshow(BWsh);title('Sobel 水平');
subplot(2,3,3),imshow(BWsv);title('Sobel 垂直');
subplot(2,3,4),imshow(BWph);title('Prewitt 水平');
subplot(2,3,5),imshow(BWpv);title('Prewitt 垂直');
subplot(2,3,6),imshow(g45);title('自建45');

%用直方图阈值法
I=imread('cameraman.jpg');
subplot(2,2,1);
imshow(I);
title('原图像');
I1=rgb2gray(I);
subplot(2,2,2);
imhist(I1);
title('直方图');
subplot(2,2,3);
I2=im2bw(I1,165/415);
imshow(I2);
title('分割后的图像');

%用Otsu算法
I=imread('cameraman.jpg');
subplot(2,1,1);
imshow(I);
title('原图像');
subplot(2,1,2);
level=graythresh(I);
BW=im2bw(I,level);
imshow(BW);
title('分割后的图像');