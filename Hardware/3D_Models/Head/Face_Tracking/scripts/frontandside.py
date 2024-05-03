import cv2
import time

def main() -> None:
    # initialize video object
    cap = cv2.VideoCapture(0)
    success = True
    fps = 30
    interval_ms = 1000 / fps

    # load cascade files for frontal and profile face detection
    face_cascade_frontal = cv2.CascadeClassifier('../trained_data/haarcascade_frontalface_default.xml')
    face_cascade_profile = cv2.CascadeClassifier('../trained_data/haarcascade_profileface.xml')

    # initialize variables for face tracking
    prev_face = None
    frame_count = 0
    face_detection_interval = 5 # Adjust this value to change the frequency of face detection
    prev_quadrant = None

    while success:
        # start fps timer
        start_ms = get_cur_ms()

        # read image and keep count
        success, image = cap.read()
        frame_count += 1

        # get image dimensions
        height, width = image.shape[:2]

        # draw 9 equal quadrants
        third_width = width // 3
        third_height = height // 3
        for i in range(3):
            for j in range(3):
                x1 = j * third_width
                y1 = i * third_height
                x2 = x1 + third_width
                y2 = y1 + third_height
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

        # detect face every face_detection_interval frames
        if frame_count % face_detection_interval == 0:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces_frontal = face_cascade_frontal.detectMultiScale(gray, 1.3, 5)
            faces_profile = face_cascade_profile.detectMultiScale(gray, 1.3, 5)
            faces = list(faces_frontal) + list(faces_profile)  # combine frontal and profile faces

            # choose the closest face
            closest_face = None
            closest_distance = 0
            for (x, y, w, h) in faces:
                distance = w * h
                if distance > closest_distance:
                    closest_face = (x, y, w, h)
                    closest_distance = distance

            if closest_face is not None:
                x, y, w, h = closest_face

                # update the previous face coordinates with the closest face
                prev_face = (x, y, w, h)

                # draw rectangle around the closest face
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # determine the quadrant based on the point half distance from the center to the top
                face_center_x = x + w // 2
                face_center_y = y + h // 4  # Point half distance from center to top
                quadrant = get_quadrant(face_center_x, face_center_y, width, height)

                # print the quadrant only if it's different from the previous one
                if quadrant != prev_quadrant:
                    print(f"Closest face is in quadrant {quadrant}")
                    prev_quadrant = quadrant
        else:
            # use the previous face coordinates for tracking
            if prev_face is not None:
                x, y, w, h = prev_face
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                prev_face = None

        # display image
        cv2.imshow('Webcam', image)

        # wait to maintain fps but keep checking for 'q'
        done = False
        cur_ms = get_cur_ms()
        while not (done or start_ms + interval_ms < cur_ms):
            cur_ms = get_cur_ms()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                done = True

        # if 'q' is pressed break out of loop
        if done:
            break

    cap.release()
    cv2.destroyAllWindows()

def get_cur_ms() -> float:
    return time.time() * 1000

def get_quadrant(x, y, width, height):
    third_width = width // 3
    third_height = height // 3

    col = x // third_width
    row = y // third_height

    return row * 3 + col + 1

if __name__ == '__main__':
    main()