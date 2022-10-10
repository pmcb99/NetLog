# NetLog
I built this as a side project to test my monitor internet speed. It emailed me whenever the speed was below a threshold, and logged all the data to CSV/Google Sheets. 


## INSTRUCTIONS
1. Add password to password file, and edit code to include your email, choose whether to use Gsheets logging, and you can modify your desired speed tolerances.
2. Run the command 'python3 Test.py'

## THINGS TO NOTE
This was designed to be run on a RPi, and I used crontab to run the script at whatever interval I desired. 
If you wanted, you could just use a while loop and the time module to continuously run tests.
