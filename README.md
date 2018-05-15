
     Employee Management System in Python Flask
    ----------------------------------------------------------------- 
Instruction to running this program.

Create a directory called **instance** in the root direcotry of the project. In the **instance directory** create a file called **config.py**. In the **config.py** file set your **SQLALCHEMY_DATABASE_URI='mysql://yourusername:yourpassword@localhost/youratabasename'**. Also, don't forget to set your **SECRET_KEY** value.

To run the program, follow the below instructions:
```
pip install virtualenv
git clone https://github.com/momojohnson/employee-management-app
virutalenv venv
**windows specific command to activate virtualenv:**
cd venv/Scripts/activate 
**Linux specific command to activate virtualenv: **
source/bin/activate
pip install -r requirements.txt 

**Set environment variable in windows to either production, development, or testing.**
FLASK_CONFIG=development
FLASL_APP=run.py
flash run

**Set environment variable in Linux to either production, development, or testing.**
export FLASK_CONFIG=development
export FLASK_APP=run.py 
flask run 
```





