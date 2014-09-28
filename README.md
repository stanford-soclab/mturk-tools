mturk-tools
===========

Some scripts to perform various tasks on Amazon Mechanical Turk, written for Stanford's Laboratory for Social Research (https://lsr.stanford.edu/). Calls the MTurk API through https://github.com/ctrlcctrlv/mturk-python.

### General info

You may need to install the python package xmltodict:

` $ pip install --user xmltodict `

(on Windows you may need to download https://github.com/martinblech/xmltodict and run, within that directory, 
        `python setup.py install`)

You will also need to put a file titled `mturkconfig.json` in the same directory as the scripts here, which looks like this:


```
{
  "use_sandbox" : false,
  "stdout_log" : true,
  "verify_mturk_ssl" : true,
  "aws_key" : "YOUR AWS KEY",
  "aws_secret_key" : "YOUR AWS SECRET KEY"
}
```

replacing the keys with your own, of course. 

### Usage

#### Recontacting workers

Use `recontact_workers.py`. This script will send emails to each worker in a list you provide, if these workers have a certain qualification (with, optionally, a specific value).

```
python recontact_workers.py worker_list email qualification_id qualification_value(optional)
```

where

  + `worker_list` is a text file consisting of one worker id per line;
  + `email` is a text file with the subject on the first line and the body in the rest of the file:
    ```
    Example Subject
    Example Message. Hello underlings!
    ```
  + `qualification_id` is a qualification id;
  + `qualification_value` is an optional argument specifying specific values of the qualification the worker must have. Multiple values are separated by '-'s. 

So if you wanted to only recontact workers with qualification XYZ with values 2 or 3, you would use the following command:

```
python recontact_workers.py worker_list email XYZ 2-3
```

#### Granting bonuses

Use `grant_bonuses.py`. This script will grant bonuses to workers in a list you provide:

```
python grant_bonuses.py worker_csv_file bonus_amount(optional) bonus_message(optional)
```

where
  
  + `worker_csv_file` is a csv file with each line consisting of assignment id, worker id, bonus amount and message. ie:
    ```
      ASSIGNID, WORKERID, 4, Good job!
    ```
    The last two entries are optional.
    
    If the last two entries are provided, then worker `WORKERID` will be granted the specified amount, with the specified message, for completing assignment `ASSIGNID`. Otherwise:
    + by default, `bonus_amount` is granted. (If this argument is not specified, workers are granted a default of 1.)
    + by default, `bonus_message` is sent. (If this is not specified, no accompanying message is sent to the worker.)
    
    
