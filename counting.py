import cv2
import requests
from bs4 import BeautifulSoup
from ultralytics import YOLO
model = YOLO(r"C:\Users\gdhar\OneDrive\Desktop\peoplecounting\runs\detect\train9pt\weights\best.pt") 
cap = cv2.VideoCapture(r"C:\Users\gdhar\OneDrive\Desktop\peoplecounting\data1.mp4")


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Perform detection
    results = model(frame) 
    person_count = 0

    # Loop over detected items
    for result in results:
        boxes = result.boxes  

        for box in boxes:
            # Unpack bounding box coordinates and confidence 
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = box.conf[0] 
            label = int(box.cls[0])  

            if label == 0 or label ==1 and conf > 0.5:
                person_count +=1
                

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), )
                cv2.putText(frame, 'Person Detected', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # Display the number of people detected on the frame
    cv2.putText(frame, f'People Count: {person_count}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the result
    cv2.imshow('People Counting', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
def outdoor_temperature():
    city = "chennai"

    url = "https://www.google.com/search?q=" + "weather+" + city
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

# Extracting the temperature
    temp_element = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
    if temp_element:
        temp = temp_element.text
        return (int(temp[:-2]))


def calculate_required_temperature(people_count,outdoor_temp,base_temp,room_size,comfort):
    max_ppl=60
    base_size=500
    effective_ppl=min(max_ppl,people_count)
    size_factor=base_size/room_size
    
    indoor = effective_ppl*0.5*size_factor
    if outdoor_temp > 25:
        outdoor_sensitivity= outdoor_temp*0.1
    else:
        outdoor_sensitivity =0
    required= base_temp - indoor - outdoor_sensitivity

    return max(int(required),comfort)

    

def control_hvac(temperature):
    print(f"Setting temperature to {temperature}°C.")
outdoor=outdoor_temperature()
basetemp=24
comfort = 20
temperature = calculate_required_temperature(person_count,outdoor,basetemp,4200,comfort)

# Control the HVAC system
control_hvac(temperature)

cap.release()
cv2.destroyAllWindows()

