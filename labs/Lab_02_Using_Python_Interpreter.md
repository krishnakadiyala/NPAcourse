
# Lab 2 - Using the Python Interpreter

This lab is an introductory lab that shows how simple accessing the Python Interpreter is.

##### Step 1

Connect to the course Jump Host Linux virtual machine using either RDP or SSH.

##### Step 2 (Only if you choose to use RDP)

While in the course virtual machine, click the **Terminal** icon on the desktop.

##### Step 3

Type in the word `python` and press `Enter`.

You will see the following prompt:

```
ntc@ntc-training:ntc$ python
Python 3.6.8 (default, Jun 11 2019, 01:16:11) 
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 

```

When you see the `$` at the command line prompt, this should tell you that you're at a "Linux shell" prompt.  When you see the `>>>`, you now know that you're at an interactive Python prompt using the native Python Interpreter.

##### Step 4

Once you're in the _shell_, type `print('Hello World!')`

```python
>>> print('Hello World!')
Hello World!

```

This means you are now in the Python Interpreter and can immediately start programming in Python. Since Python is an interpreted language, there is no requirement to create a complete program in a file before the code is executed. You can just start programming.

This was just a short mini-lab to understand how to access the Python Interpreter.

Note that modern network operating systems such as Cisco NX-OS and Arista EOS also have a Python execution engine, e.g. Python Interpreter on each switch.  If you SSH into a switch that supports Python, you'll be able to access a "shell" environment on the switch by also just typing "python".  

The next several labs will use the Python Interpreter (_shell_) to start conveying critical Python concepts to be aware of when starting a journey on network automation.
