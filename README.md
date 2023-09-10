# Large Matrix Mutliplication using AWS

## Project Objective
### Large Matrix Multiplication developed using C++ that runs on automated AWS Cloud Instance, deployed using python and using boto3 AWS library.
### The purpose of this project is to schedule computation demanding tasks in AWS cloud without configuring 
### and creating instances manually and the instances will terminate after the job is done. 

## Project Description
### Python File will automatically create Amazon Ubuntu fee tier instance based on image id and instance type provided

### It will execute set of commands hardocoded in the code. In this case, the operation is to compute Large Matrix Multiplication. At the end of the execution, it will output the execution time.

### After execution of code, it will stop all running instances and terminate it thereafter

### Matrix of 5000 x 5000 being multiplied which is of complexity N^3

### Running matrix multiplication in two instances, one is t2.micro which has low specs - 1vCPUs, 2.5 GHz and 1 GB memory

### Other one is c4.4xlarge which has specs - 16 vCPUs, 2.9 GHz and 30 GB memory
