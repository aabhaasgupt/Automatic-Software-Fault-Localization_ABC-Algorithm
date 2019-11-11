
The tcas dataset has 41 wrong versions, 1 correct version with 1608 testcases, which is attached along with this file 

We have chosen some versions of programs as described in the paper and instrumented them and placed in folder instrumented for our experiment 

The current instrumented code is sixth version of the wrong 'c' program right now.

Generate the tcas program executables using following commands before running algorithm

	a) "Run gcc gcc tcas.c -o tcas_right.out" to get the executabe of correct version 

	b) "Run gcc gcc tcas_1.c(change filename as needed) -o tcas_wrong.out" to get the executabe of correct version 
	Important!! : the name of the wrong version 'c' file must be tcas_1.c

Run the main python file (tcas.py) which has algorithm to run 

Optional Changes, and customizations:
To change the parameters of execution give the following parameters(or give the --help with the python file to get more details):

parameters: 
-S, --InputVectorSize: Input Vector Size.
-I, --Iterations: Number Of Iterations.
-Ne, --NoEmployedBeesPI: Number of Employeed Bees per iteration.
-F, --FitnessChangeLimit: Abandon test case if change in fitness for many iterations is less than this.")
-D, --DependencyFitness: Dependency Fitness multiple value.
-A, --AbandonAfter: Abandon after trying for this many iterations.
-DE, --DivisionError: Add this to denominator for removing division by zero error.
-P, --Probes: Number of Probes.

