#include <Keyboard.h>


const int button_pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10}; // pin numbers for each button connected to
const int num_buttons = 9; // total number of buttons

char key_chars[] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}; // characters/keys to send for each button

bool button_state[num_buttons]; // to keep track of button state
bool last_button_state[num_buttons]; // to keep track of last button state

void setup() {
  for(int i=0;i<num_buttons;i++){ // for each button
    pinMode(button_pins[i], INPUT_PULLUP); //
    button_state[i] = HIGH; // initialize assuming buttons are not pressed
    last_button_state[i] = HIGH; // set last state as HIGH
  }
  Keyboard.begin(); // start listening
}

void loop() {
  for(int i=0;i<num_buttons;i++){ // for each button 
    button_state[i] = digitalRead(button_pins[i]); // read current state of the button (LOW when pressed)

    if(button_state[i] != last_button_state[i] && button_state[i] == LOW){ // check if button state has changed (HIGH -> LOW)
      Keyboard.press(key_chars[i]); // press the corresponding key
    }else if(button_state[i] != last_button_state[i] && button_state[i] == HIGH){ // check if button state has changed (LOW -> HIGH)
      Keyboard.release(key_chars[i]); // release the corresponding key
    }

    last_button_state[i] = button_state[i]; // update last button state
  }
  delay(50); // delay for debouncing
}
