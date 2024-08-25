import cv2
import mediapipe as mp
import pyautogui

# Initialize OpenCV and MediaPipe
cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()

# Function to recognize gestures
def recognize_gesture(landmarks):
    # Example: Simple gesture recognition based on landmark positions
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    
    if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y:
        return 'click'
    elif index_tip.y < thumb_tip.y and index_tip.y < middle_tip.y:
        return 'move'
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (MediaPipe requires RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform hand tracking
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        # Iterate over detected hands
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Recognize gesture
            gesture = recognize_gesture(hand_landmarks.landmark)
            
            # Map gesture to actions
            if gesture == 'click':
                pyautogui.click()
            elif gesture == 'move':
                index_tip = hand_landmarks.landmark[8]
                screen_x = int(index_tip.x * pyautogui.size().width)
                screen_y = int(index_tip.y * pyautogui.size().height)
                pyautogui.moveTo(screen_x, screen_y)

    # Display the modified frame with hand landmarks
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
