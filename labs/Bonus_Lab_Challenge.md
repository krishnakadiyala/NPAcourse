# Bonus Lab - Challenge

Using everything we have covered in the course so far, implement a script that covers the following tasks. Feel free to add additional features and refactoring as you work through it.

Note: There are many steps listed below but you don't need to complete each one, it is listing many of the different tasks and topics we have covered in this course so far. Go through and start by implementing the ones that sound more interesting to you and build up a more complete automation example. Alternativly, you could come up with a similar automation task more relevant to your current / past work and experience. The goal of this last section is to utilize what we've learned so far and see how we can use it moving forward.


* Create a python script called `automation_challenge.py` in the `scripts` directory
* Retrieve data using Netmiko, send a show command to at least 2 device types
* Retrieve data using Requests, send an API request to at least 2 APIs
  * For the above 2 steps, try creating a basic inventory
  * Think about how you want to represent your devices to make it easy for different parts of your script to draw from it
    * A nested dictionary or a list of dictionaries could work well here
* Add a command line input that allows you to select which command to run
* Store data for each device and each command in its own file (could use a folder for each device and a file for each command)
* Choose a few pieces of data from the command of your choice and parse it out into your own variable
  * Vlans and Neighbor data work great for this
* After you've parsed the output and retrieved a few pieces of data, print it to the screen in an easy to read format
* Create a report - store the data you parsed to a file, this time with additional comments making it easy to read
* Seperate out some of your variables and functions to a second file named `utils.py`
  * Import these features into your script
  * This process is making your overall automation more modular so you can reuse pieces
* Add concurrency to your script, specifically on your features that retrieve data
* Using the above inventory, modules, and concurrent features, retrieve and store configs from each device
  * Now that we have a file and module created allowing us to repeat our tasks, it should get easier to add additional functionalities
