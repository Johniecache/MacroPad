# Documentation
### Overview
This is where the majority of the external (non-coded) documentaiton for this project is held. This will range from written documentation to photo.

## Setup Instructions
Items needed: Solder, Soldering Iron, Insulated Tinned Wire, Copper Wire (optional), (9) 2-pin keyboard switches, Keyboard Frame (3D printed or otherwise), ATmega32U4 pro micro, Pliers/Drill

1. Setup your workstation. Ensure all parts needed are at your disposal.
2. Put Keyboard Switches into the Keyboard Frame.
3. Measure Copper Wire to a little over the length of the strech of one set of pins on the back of the Keyboard Switches. For this project it was roughly 3 inches.
4. Cut the Copper Wire to size, do this 4 times total.
5. Straighten the Copper Wire by either:
   * Taking Pliers to the both ends of the copper wire and pulling them apart.
   * Taking a Drill and putting the Copper Wire in a vice then wrapping the wire around the Drill and starting the Drill.
   * Any other method not mentioned.
6. Line the Copper Wire up with one of the two prins on the back of the Keyboard Switches (one per switch per row). This should like up with 3 switches and 3 unique pins.
7. Solder the Copper Wire to all of the 2-pins on the back of the Keyboard Switches that has just been lined up.
8. Do this for the other 2 rows. In the end there should be 3 Copper Wire across 3 rows of Keyboard Switches.
   * If available use a multimeter to test the resistance across the copper at each Solder joint. The resistance should be zero across the Copper Wire.
9. Solder the 4th piece of Copper Wire across all 3 of the other pieces of Copper Wire. This should look like an E when done where each line across is soldered to pins and the line going up is connecting them all.
   * If available test the resistance with a multimeter again to ensure all is connected properly.
10. Cut 10 pieces of Insulated Tinned Wire to about 2 1/2 to 3 inches (9 red and 1 black if available).
11. Strip about 1/8 inch on both ends of all the Insulated Tinned Wire that have just been cut to length.
12. Pre Solder the ends of all the Insulated Tinned Wire that has just been stripped.
13. Pre Solder each "open" (each pin that isn't soldered to the Copper Wire) pin on all 9 of the Keyboard Switches.
14. Solder one of the (black) Insulated Tinned Wire to any (prio conncecting) Copper Wire.
15. Connect the just connected Insulated Tinned Wire to the GND of the ATmega32U4 microcontroller device.
16. Solder the remaining 9 (red) Insulated Tinned Wire to each of the exposed (open) pins on the Keyboard Switches.
17. Solder the other ends of these (red) wires to the ATmega32U4 with this configuration (check docs/images.md for clarification):
  * Keyboard Switch -> Pin #
  * Bottom Left -> 10
  * Bottom Middle -> 9
  * Bottom Right -> 8
  * Middle Left -> 7
  * Middle Middle -> 6
  * Middle Right -> 5
  * Top Left -> 4
  * Top Middle -> 3
  * Top Right -> 2
18. Plug the ATmega32U4 into PC via USB-c
19. Flash the firmware to the Microcontroller
20. Test
