# Machine Energy

MachineEnergy class allows you to do energy tracking across distributed machines and devices over the cloud and helps analyse the machine with the least energy consumption and least amount of carbon footprint


## Inputs

 
Name | Input | Description 
 ----------- | ----------- |  -----------
`config` | str or dict | Configuration containing information about machines to distribute and run energy tracking.
`experiment_name` | str | Used for creating the experiment logging folder
`framework` | str | Used for specifying the framework which needs to be evaluated for running an example training script for energy tracking.
`train_func` | python function object | Contains a function which returns model after model.fit as input, used to evaluate energy tracking via custom script.


### Config

The config allows the user to configure the different machine details required for calculation of energy usage per machine. The energy usage tracking will be done parallely, across each machine.

A config will look like this:

```
{
  "machines": [
    {
      "machine_id": 1,
      "MACHINE_IP_ADDRESS": "machine_1_ip_address",
      "MACHINE_PORT": machine_1_port,
      "MACHINE_USER": "machine_1_username",
      "MACHINE_PASSWORD": "machine_1_password"
    },
    {
      "machine_id": 2,
      "MACHINE_IP_ADDRESS": "machine_2_ip_address",
      "MACHINE_PORT": machine_2_port,
      "MACHINE_USER": "machine_2_username",
      "MACHINE_KEY_FILENAME": "machine_2_key_file_path" # use keypath if key file is used instead of password
    }
  ],
  "run_local" : true
}
```

#### Config Arguments

Argument | Input | Description
--------- | ------- | -----------
`run_local` | bool | if set to true, the local machine where the script runs will also be included in energy tracking. The local machine is automatically added as machine id `0` 
`run_docker` | bool | if set to true, pulls docker images to respective remote machines and runs Energy Tracking in docker containers.      
`machines` | list of dict | list of machine configurations    
`machine_id` | int | id for each machine in ascending order.   
`MACHINE_IP_ADDRESS` | str | ip address for the remote machine   
`MACHINE_PORT` | int | port number for the remote machine   
`MACHINE_USER` | str | username for the remote machine   
`MACHINE_PASSWORD` | str | password for the remote machine   
`MACHINE_KEY_FILENAME` | str | if password not available, the path to RSA private key of the machine could be supplied to this argument.      

