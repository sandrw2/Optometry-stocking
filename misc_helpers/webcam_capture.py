def capture():
    import cv2

    # Start webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam", frame)
        
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite("captured_image.jpg", frame)
            print("Image saved as captured_image.jpg")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

capture()