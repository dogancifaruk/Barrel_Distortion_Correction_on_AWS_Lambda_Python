import cv2
import boto3
import numpy as np

s3 = boto3.resource('s3')

def lambda_handler(event, context):
	# Obtained from camera calibration
	K = np.array([[  3.6467990983524174e+02, 0., 3.2932846845849457e+02],
              [0.,      3.6467990983524174e+02, 2.5598789691130796e+02],
              [    0.  ,     0.  ,     1.  ]])

	# Obtained from camera calibration
	D = np.array([  -3.8053738493716022e-01, 1.1784853392985892e-01,
       -7.8189429931945203e-03, -3.9611137326712887e-03,
       -1.5221291812014469e-02   ])

	# Used to scale the output
	Knew = K.copy()
	Knew[(0,1), (0,1)] = 0.79 * Knew[(0,1), (0,1)]	
	
	print("Downloading image")

	s3.meta.client.download_file( <source-bucket-name>, <source-file-name>, '/tmp/CAM1.jpg')
	
	print("Reading image")

	img=cv2.imread("/tmp/CAM1.jpg")

	print("Correcting image")

	img_undistorted = cv2.undistort(src=img, cameraMatrix=K, distCoeffs=D, newCameraMatrix=Knew)

	print("Writing corrected image")

	cv2.imwrite('/tmp/CAM2.jpg', img_undistorted)

	print("Saving image to bucket")

	s3.Bucket( <destination-bucket-name> ).upload_file('/tmp/CAM2.jpg', <destination-file-name> )

	print("Done")

if __name__ == "__main__":
	print("entered if statement")
	lambda_handler(42, 42)
