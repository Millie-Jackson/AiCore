# AiCore

# Milestone 1
Created a model that detects whether the user is showing rock, paper, scissors or nothing to the camera using their hand.

The model was created using Teachable_Machine as it is a free online resource rather than writing from scratch. It uses 4 classes (Rock, Paper, Scissors and Nothing) trained using 200-300 webcam images each.

# Milestone 2
A virtual environment was created using MiniConda for a smooth creation and installation of dependencies. Dependencies used are opencv-pythong for webcam access, tensorflow for the mathamatical library and ipykernel for testing and documentation. 

VSCode, ipykernal and TensorFlow are the industry standard IDE and libraries for machine learning. 

The model was run on a local machine to ensure its accuracy using the following code:

    import cv2
    from keras.models import load_model
    import numpy as np
    model = load_model('YOUR_MODEL.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)
        # Press q to close the window
        print(prediction)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

# Milestone 3
Wrote a python script to simulate the game which asks for input and compares it to its own guess. The image is taken on the fly during game play and run through the model to get the prediction. The pc will then choose a position using a random number generator and compare the two. The basic win logic was writen as a win condition function and was tested separatly. Both predictions are stored in separate variable to avoid confusion. Finally the game logic was placed in it's own function so it only has to be called once. The program will close if the user presses the 'q' key on a keyboard and it will close the webcam and window.

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

# Milestone 4
A fuction was created to act as a countdown for the user to get their hand ready for input. The countdown is for 3 seconds and pints to the user (3, 2, 1, GO!). Time was imported to create this. It was also used elsewhere to slow down the play speed for an easyer user experience. The game holds and displays a score as part of the game function and will close automatically once someone has reached a score of 3. The scores are contained in a list rather than 2 separate variables in order to cut down on code and access then at the same time. The computer will aslo ask for the users name and use it 'in conversation'.

    def countdown(seconds):
    while seconds:
        print(seconds)
        time.sleep(1)
        seconds -= 1

# Conclusion
# Extra Features
1. Asks for users name then states 'name vs computer' and adds displays a score next to the users name
2. Run time has been slowed down using time.sleep() for an easyer user experience
3. Program closes after someone gets a score of 3 and congratulates the winner
4. Both scores are stored in a list for easyer access and reduce lines of code
# Desired
1. Text and instructions are written to the window for a more user friendly experience
2. Use different coloured text to differentiate between players
3. Allow the user to pick their colour
4. Capture a 'profile image' to display next to the users name and scoreboard
5. Creat a perminant scoreboard of all the players
6. Allow the user to press enter to take an image when they are ready
7. Allow functionality for friends to play together rather than against a computer
8. Create a more amusing 'personality' for the computer player in which it takes its guess after predicting the users guess and cheats its way to win everytime
9. Ask for additional input for the user to accuse the computer of cheating
10. Give the player a point for each corret accusation of cheating and use that as the main play condition
11. Tell the user how many times the computer successfully cheated and how many times it was cought