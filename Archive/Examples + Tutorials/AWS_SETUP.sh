#USEFUL COMMANDS
#rm -rf <folder> 
#sudo su -

#BASH SCRIPT TUTORIAL:
#.sh file
#add #!/bin/bash
#chmod 755 myscript.sh
#./myscript.sh

#######################################
# INSTALL NUMPY/OPENCV
# SOURCE: https://github.com/opencv/opencv/issues/6066
#######################################
# Setting up build env
sudo yum update -y
sudo yum install -y git cmake gcc-c++ gcc python-devel chrpath
mkdir -p robotfilmmaker/cv2 build/numpy

# Build numpy
pip install --install-option="--prefix=$PWD/build/numpy" numpy
cp -rf build/numpy/lib64/python2.7/site-packages/numpy robotfilmmaker

# Build OpenCV 3.3
NUMPY=$PWD/robotfilmmaker/numpy/core/include
cd build
git clone https://github.com/Itseez/opencv.git
git clone https://github.com/Itseez/opencv_contrib.git

cd opencv_contrib
git checkout 3.3.0
cd ..

cd opencv
git checkout 3.3.0

mkdir mybuild
cd mybuild

cmake \
-D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/home/ec2-user/build/opencv \
-D WITH_TBB=ON \
-D WITH_IPP=ON \
-D WITH_V4L=ON \
-D ENABLE_AVX=ON \
-D ENABLE_SSSE3=ON \
-D ENABLE_SSE41=ON \
-D ENABLE_SSE42=ON \
-D ENABLE_POPCNT=ON \
-D ENABLE_FAST_MATH=ON \
-D BUILD_EXAMPLES=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \
-D OPENCV_EXTRA_MODULES_PATH=/home/ec2-user/build/opencv_contrib/modules \
-D BUILD_opencv_aruco=OFF \
-D BUILD_opencv_bgsegm=OFF \
-D BUILD_opencv_bioinspired=OFF \
-D BUILD_opencv_ccalib=OFF \
-D BUILD_opencv_cnn_3dobj=OFF \
-D BUILD_opencv_cvv=OFF \
-D BUILD_opencv_datasets=OFF \
-D BUILD_opencv_dnn_modern=OFF \
-D BUILD_opencv_dnns_easily_fooled=OFF \
-D BUILD_opencv_dpm=OFF \
-D BUILD_opencv_freetype=OFF \
-D BUILD_opencv_fuzzy=OFF \
-D BUILD_opencv_hdf=OFF \
-D BUILD_opencv_img_hash=OFF \
-D BUILD_opencv_lline_descriptor=OFF \
-D BUILD_opencv_matlab=OFF \
-D BUILD_opencv_optflow=OFF \
-D BUILD_opencv_phase_unwrapping=OFF \
-D BUILD_opencv_plot=OFF \
-D BUILD_opencv_reg=OFF \
-D BUILD_opencv_rgbd=OFF \
-D BUILD_opencv_saliency=OFF \
-D BUILD_opencv_sfm=OFF \
-D BUILD_opencv_stereo=OFF \
-D BUILD_opencv_surface_matching=OFF \
-D BUILD_opencv_text=OFF \
-D BUILD_opencv_xfeatures2d=OFF \
-D BUILD_opencv_ximgproc=OFF \
-D BUILD_opencv_xobjdetect=OFF \
-D BUILD_opencv_xphoto=OFF \
-D PYTHON2_NUMPY_INCLUDE_DIRS="$NUMPY" ..

make -j`cat /proc/cpuinfo | grep MHz | wc -l`

cd

cp build/opencv/mybuild/lib/cv2.so robotfilmmaker/cv2/__init__.so
cp -L build/opencv/mybuild/lib/*.so.3.3 robotfilmmaker/cv2

# OPTIONAL STRIP?
strip --strip-all robotfilmmaker/cv2/*

# CONTINUE
chrpath -r '$ORIGIN' robotfilmmaker/cv2/__init__.so
touch robotfilmmaker/cv2/__init__.py

# OPTIONAL (FOR LAMBDA PACKAGING)
cp template.py robotfilmmaker/lambda_function.py
cd robotfilmmaker
zip -r ../robotfilmmaker.zip *

#######################################
# INSTALL BOTO3
#######################################
sudo su -
pip install boto3
exit

#######################################
# INSTALL S3FS
# SOURCE: https://cloudkul.com/blog/mounting-s3-bucket-linux-ec2-instance/
#######################################
sudo su -

# Install dependencies
yum update all
sudo yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel

# Install s3fs
git clone https://github.com/s3fs-fuse/s3fs-fuse.git

cd s3fs-fuse
./autogen.sh
./configure --prefix=/usr --with-openssl
make
sudo make install

# Check s3fs
which s3fs

# Create password file for AWS access
touch /etc/passwd-s3fs
vim /etc/passwd-s3fs

# Paste in your passwords in the text	
Your_accesskey:Your_secretkey

# Change permission of file
sudo chmod 640 /etc/passwd-s3fs

# To create directory and mount: Create mys3bucket folder, and use it to mount bucket your_bucketname
mkdir mys3bucket
s3fs your_bucketname -o use_cache=/tmp -o allow_other -o multireq_max=5 mys3bucket

# To unmount
umount /mys3bucket


