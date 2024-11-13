
# contextual_speech_correction

This is a ROS package which listens for raw text (produced from a speech recognizer) on the topic **speech_raw** and publishes the corrected text onto the topic **speech_corrected**. This performs a contextual, phoneme based correction, where the context is provided specifying a grammar (CFG) in the ***init_ros.py*** file.


## Prerequisites

- **Ubuntu 20.04 LTS**

To check OS version: Press Super key ⟶ Enter 'About' in the search ⟶ Scroll down and see OS Name.
- **ROS 1, noetic**

To check ROS version: Enter `ls /opt/ros` in a terminal window. You should see the directory `noetic`.

NOTE: If you get this error `ls: cannot access '/opt/ros': No such file or directory`, this means you do not have ROS 1 installed. You can follow the ROS installation steps [here](http://wiki.ros.org/noetic/Installation/Ubuntu).

- **Python 3.8**

To check your python version, enter `python --version`. You should see `Python 3.8.x` where x is any number.
In case this produces `Command 'python' not found` error, you should try `python3 --version`.

If this also produces an error it means you do not have Python 3 installed. You should run 
```
sudo apt update
sudo apt install python3.8
```

-  **Virtualenv**

You will need to create a python virtual environment. To do this you will need the `virtualenv` utility. Check if installed by running `virtualenv --version`. 

If not installed, do a simple pip install:
```pip install virtualenv```

## Installation

1. **Sourcing setup.bash:** `source /opt/ros/noetic/setup.bash`. Note you will need to do this everytime you open a new terminal window.   
For convinience you can add this line at the end of your ***~/.bashrc*** file so that it is automatically executed.
 
2. **Create a catkin workspace**
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
source devel/setup.bash
```
Note you will need to `source devel/setup.bash` everytime you open a terminal. So it is advisable to add it after the last line in ***~/.bashrc*** 

3. Clone the repository to fetch the ***contextual_speech_correction*** package. run
`git -C /src https://github.com/Aradhye2002/contextual-speech-correction.git`

Or if you are facing authentication problems, you can download a zip file from the github page. Make sure to extract the package in the directory `~/catkin_ws/src`

4. Create a python virtual environment:

```virtualenv -p /usr/bin/python3.8 <your-env-name>```

5. Change current environment to <you-env-name>:

```source <your-env-name>/bin/activate```

5. Install the dependencies:
```
cd /home/<user-name>/catkin_ws/src/contextual_speech_correction
pip install -r requirements.txt
```

## Documentation

- ***contextual_speech_correction*** implements a rosnode "speech_corrector" which serves to contextually correct raw text from a speech recognition system.
- The context is provided by specifying the CFG in the ***init_ros.py*** file. This is done by initializing the grammar-eng and grammar-hin variables.
- There are two modes: **hindi** and **english**. The mode is passed as a command line argument to ***init_ros.py***.
- You also need to specify the depth of derivations upto which you will search in the grammar. NOTE: The user specified CFG is internally represented in CNF and hence is in general much larger than the entered CFG. 
- A good rule of thumb for the depth is 30. Large values of depth also slow down the correction, so you have to balance between the two factors.
- The **speech_correcter** rosnode will listen for sentences of the type **std_msgs/String** on the channel **speech_raw** and output the corrected sentence onto the channel **speech_corrected**.

## Usage

- Make sure you have sourced all the mentioned files, and are in the required virtual environment.
- Initialize ros master: run 
    `roscore`

- Start listening on the **speech_corrected** channel for the corrected text: ```rostopic echo speech_corrected```
- Start the rosnode **speech_correcter**: ```rosrun contextual_speech_correction init_ros.py <lang>```
    Here the <lang> placeholder takes values "english" or "hindi" (without quotation marks).
- Write to **speech_raw** channel: ```rostopic pub std_msgs/String <raw_speech>```
    Where <raw_speech> is any string (with quotation marks) to be corrected.