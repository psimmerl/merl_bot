## imports and variable definitions ##

from keras.models import load_model
from pure_pursuit import PurePursuitPlusPID
from helper_functions import *
import numpy as np 

FPS = 30 #will need to decide on this depending on how quickly the computer can run the model
model_file = "pilotnet_model.h5"
model = load_model(model_file)
controller = PurePursuitPlusPID()

## I assume you would also initialize the reader/writer nodes here and start a loop to continuously read from the topic from the car

# img = (read from topic idk how you do that)
img = process_img(img)
img = img.reshape(1,200,400,3).reshape(1,1,200,400,3) #get into correct shape for network
prediction = model.predict(img)[0]
trajectory_prediction = np.array([[float(x),prediction[x]] for x in range(len(prediction))]) # construct line from predicted points, each being one meter apart

#velocity = read from topic
#speed = np.linalg.norm(velocity)

throttle, steer = controller.get_control(trajectory_prediction, speed, desired_speed = 25, dt=1./FPS)

#send_control(throttle, steer) # I assume you would use the write node to do this
#continue looping