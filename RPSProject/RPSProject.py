import time
import cv2
import numpy as np
from random import *
from keras.models import load_model
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

score = [a for a in range(2)] #2 scores in one variable
score[0] = 0
score[1] = 0

playerGuess = "Blank"

def countdown(seconds):
    while seconds:
        print(seconds)
        time.sleep(1)
        seconds -= 1

def randomGuess():
    number = random()
    if number < 0.3:
        pcGuess = "Rock"
    elif number > 0.6:
        pcGuess = "Paper"
    else: pcGuess = "Scissors"    

def winCondition():
    if playerGuess== 'Rock' and pcGuess== 'Scissors' or playerGuess== 'Scissors' and pcGuess== 'Paper' or playerGuess== 'Paper' and pcGuess== 'Rock':
        print("You Win!")
        score[0] = score[0] + 1
    else: 
        print("You Lose!")
        score[1] = score[1] + 1 

def game():
    name = input("Whats your name? ")
    print(name, "vs computer")
    time.sleep(1)
    print("Ready? Ok")
    time.sleep(1)
    countdown(3)

    number = random()
    if number < 0.3:
        pcGuess = "Rock"
    elif number > 0.6:
        pcGuess = "Paper"
    else: pcGuess = "Scissors"

    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    cv2.imshow('frame', frame)

    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)

        if prediction[0][0] > 0.5:
            playerGuess = "Rock"
        elif prediction[0][1] > 0.5:
            playerGuess = "Paper"
        elif prediction[0][2] > 0.5:
            playerGuess = "Scissors"
        else: 
            prediction[0][3] > 0.5
            playerGuess = "Waiting..."

        print("I played ", pcGuess)
        time.sleep(1)
        print("You played " + playerGuess)
        time.sleep(1)
        winCondition()
        time.sleep(2)
        print(name, "Score: ", score[0])
        print("Computer Score: ", score[1])
        
        if score[0]== 3:
            print("You got to 3 before me!")
            # After the loop release the cap object
            cap.release()
            # Destroy all the windows
            cv2.destroyAllWindows()
        elif score[1]== 3:
            print("I got to 3 before you!")
            # After the loop release the cap object
            cap.release()
            # Destroy all the windows
            cv2.destroyAllWindows()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

game()

print("Bye!")
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()