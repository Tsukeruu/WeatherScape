# WeatherScape ☁️
  - **WeatherScape aims to enhance your experience as a wayland user, by providing you with a cozy setup that matches the weather**
    
  ![Demo](Preview/help.png)
  - **More arguements are yet to come as more functionality is included**
  <details>
  <summary>The purpose 🎯</summary>
    
  - **The primary purpose of weatherscape is to change your hyprland/wayland setup according to your local weather**
  
  - **This program is especially useful for people who love to customize their setup**
  
  - **People who find a need for this program are those who find coziness on their setup and love to match the weather**
  </details>
  
  <details>
  <summary>How it works 🛠️</summary>
    
  - **A GET request is made towards wttr.in which returns local forecast data. Inside of the json structured data includes weathercodes and other valuable information**
    
  - **WeatherScape stores multiple weather codes in a dictionary in a key-value pair relationship, where the value is a set of weather codes and the key is the classification**
    
  - **WeatherScape then filters through them according to the json file request, and finds which classification does the weather code belong to**
    
  - **WeatherScape comes with stored wallpapers, you can change them to fit your needs, and find wallpapers that you want to have during a specific weather condition**
  </details>

  <details>
  <summary>Disclaimer ⚠️</summary>
    
  - **WeatherScape runs solely on the internet connection, which works in a direct relationship**
    
  - **The faster internet you have, the faster the GET request will be**
    
  - **Returned data may not be accurate as this may be a problem with your location or in the wttr.in backend**
  </details>
  
