#!/bin/bash
 
set -e
 
ENVIRONMENT=JupyterSystemEnv
 
# Change the notebook name below in notebook_name.ipynb
NOTEBOOK_FILE=/home/ec2-user/SageMaker/notebook_name.ipynb
 
source /home/ec2-user/anaconda3/bin/activate "$ENVIRONMENT"
 
nohup jupyter nbconvert --ExecutePreprocessor.timeout=-1 --ExecutePreprocessor.kernel_name=python3 --to notebook --execute "$NOTEBOOK_FILE" &
 
source /home/ec2-user/anaconda3/bin/deactivate
 
# Configure the idle time to be wait for by seconds (e.g. 60 = 1min, 120 = 2min)
IDLE_TIME=60
 
echo "Fetching the autostop script"
wget https://raw.githubusercontent.com/aws-samples/amazon-sagemaker-notebook-instance-lifecycle-config-samples/master/scripts/auto-stop-idle/autostop.py
 
echo "Starting the SageMaker autostop script in cron"
 
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/python $PWD/autostop.py --time $IDLE_TIME --ignore-connections") | crontab -