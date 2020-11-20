# popfindr_notify

Tool which can help find Xbox Series X in your nearby Targets stores that have it in stock. It will send a notification to your phone once a 
stock update has been made by popfindr. 

# Setup
- Clone repo into virtual env
- Install requirements:
```pip install -r requirements.txt ```

## Setup: Get popfindr request url
You want to navigate to the popfindr [site](https://popfindr.com/inventory/target/207-41-0001?title=Xbox%20Series%20X%20Console&img=https://i.imgur.com/y5w5njS.jpg). 
You want to open up Chrome dev tools -> Network tab.
Type in your zipcode and click the 'Get Stock' button.
In the network tab click the new entry and copy the request url.
Be sure to save this somewhere

## Setup: Generate notify push endpoint
In the terminal, run ```python notify.py```.
Copy the **Endpoint** url and save this somewhere.
On a phone and/or laptop go to the second url or scan the QR code. 
![Subcribe](/images/notify_subscribe.jpg?raw=true)

Click the subscribe button to start recieving notifications.

## Setup: Run the listener
Run this command and replace the url with the ones saved from earlier:
```bash
  python3 main.py -u <POPFINDR_URL> -n <NOTIFY_URL>
```

You should recieve a notification if there are any in stock. You can have the listener running. It will check every 0.5s.
