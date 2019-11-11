import sys
import subprocess
import random
import numpy as np
import copy
import time
#subprocess.check_output(['ls','-l']) #all that is technically needed...
#print subprocess.check_output(['ls', '-l'])
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Test:

    def get_initial_test_cases(self):

        ct = 0
        self.right_results_execution_employed_bees = []
        self.wrong_results_execution_employed_bees = []
        for ind,bee in enumerate(self.testCases):
            #if ct not in [556,869,905,1322,1323,1324,1326,1327,1328,1329,1330]:
            #    continue
            if len(bee) != self.testCaseVectorSize:
                continue
            self.wrong_results_execution_employed_bees.append(self.execute_current_bee(bee,ind,False))
            #print(ind)
            #time.sleep(0.02)
        print(bcolors.WARNING + "init: testCases executed on the wrong tcas" + bcolors.ENDC)
        #time.sleep(3)
        ct = 0
        for ind,bee in enumerate(self.testCases):
            #if ct not in [556,869,905,1322,1323,1324,1326,1327,1328,1329,1330]:
            #    continue
            if len(bee) != self.testCaseVectorSize:
                continue
            self.right_results_execution_employed_bees.append(self.execute_current_bee(bee,ind,True))
            #print(ind)
        print(bcolors.WARNING + "init: testCases executed on the right tcas" + bcolors.ENDC)
        self.load_probe_values(True,len(self.testCases))
        self.compare_and_fill_pass_or_fail()
        flag=True
        cc = 0
        for b in self.compare_exec_result_employeed_bees:
            if not b:
                flag=False
                #print(cc,b)
            cc += 1
        if flag == True:
            print(bcolors.FAIL + "All the test cases passed for the wrong version of the program!\n\n" + bcolors.ENDC)
        fitnessValues_employeed_bees = self.fitnessFunction(self.compare_exec_result_employeed_bees,self.employeed_bees_probes_detected)

        testCases_that_failed = []
        testCases_that_failed_fitness =[]
        testCases_that_passed = []
        testCases_that_passed_fitness = []

        for i in range(len(self.testCases)):
            if not self.compare_exec_result_employeed_bees[i]:
                testCases_that_failed.append(self.testCases[i])
                testCases_that_failed_fitness.append(fitnessValues_employeed_bees[i])
            else:
                testCases_that_passed.append(self.testCases[i])
                testCases_that_passed_fitness.append(fitnessValues_employeed_bees[i])
        sortedFailedTestCases = [x for _, x in sorted(zip(testCases_that_failed_fitness, testCases_that_failed))]
        sortedPassedTestCases = [x for _, x in sorted(zip(testCases_that_passed_fitness, testCases_that_passed))]
        sortedTestCases = []

        if len(sortedFailedTestCases) <= self.numberOfEmployeedBees:
            for i in range(len(sortedFailedTestCases)):
                sortedTestCases.append(sortedFailedTestCases[i])
            for i in range(self.numberOfEmployeedBees - len(sortedFailedTestCases)):
                sortedTestCases.append(sortedPassedTestCases[i])
        else:
            for i in range(self.numberOfEmployeedBees):
                sortedTestCases.append(sortedFailedTestCases[i])

        #sortedTestCases = [x for _,x in sorted(zip(fitnessValues_employeed_bees,self.testCases))]

        #for f in fitnessValues_employeed_bees:
        #    if f != 0.0:
        #        print("fitness != 0,",f)

        #time.sleep(3)
        #for fitness in fitnessValues_employeed_bees:
        #    if fitness != 0:
        #        print(fitness)

        #reset parameters:
        self.right_results_execution_employed_bees = []
        self.wrong_results_execution_employed_bees = []
        self.probe_values_for_all_testcases_employeed_bees = {}
        self.employeed_bees_probes_detected = []
        self.compare_exec_result_employeed_bees = []
        self.compare_exec_result_unemployeed_bees = []
        #print(sortedTestCases[:self.numberOfEmployeedBees])
        return sortedTestCases

    def init_children_parents(self):
        
        """
        self.parents.append([])
        self.parents.append([])
        self.parents.append([])
        self.parents.append([0,2])
        self.parents.append([1])
        

        self.children.append([3])
        self.children.append([4])
        self.children.append([3])
        self.children.append([])
        self.children.append([])

        """
        self.parents.append([8, 9, 4, 5])
        self.parents.append([2, 6])
        self.parents.append([17])
        self.parents.append([2])
        self.parents.append([3])
        self.parents.append([3])
        self.parents.append([18])
        self.parents.append([6])
        self.parents.append([7])
        self.parents.append([7])
        self.parents.append([4, 8, 17])
        self.parents.append([5, 9, 18])
        self.parents.append([])
        self.parents.append([12])
        self.parents.append([13])
        self.parents.append([14])
        self.parents.append([15])
        self.parents.append([16])
        self.parents.append([17])
        self.parents.append([18])
        self.parents.append([19])
        self.parents.append([19])
        self.parents.append([19])
        self.parents.append([19])

        self.children.append([])
        self.children.append([])
        self.children.append([1, 3])
        self.children.append([4, 5])
        self.children.append([0, 10])
        self.children.append([0, 11])
        self.children.append([1, 7, ])
        self.children.append([8, 9])
        self.children.append([0, 10, ])
        self.children.append([0, 11, ])
        self.children.append([])
        self.children.append([])
        self.children.append([13, ])
        self.children.append([14, ])
        self.children.append([15, ])
        self.children.append([16, ])
        self.children.append([17, ])
        self.children.append([2, 10, 18])
        self.children.append([6, 11, 19, ])
        self.children.append([20, 21, 22, 23])
        self.children.append([])
        self.children.append([])
        self.children.append([])
        self.children.append([])
        

    def selectLeader(self,bees,fitnessValues):
        prob_softmax = []
        roulette_wheel = []
        denominator = 0.0
        for value in fitnessValues:
            denominator+=value
        for value in fitnessValues:
            if denominator!=0:
                prob_softmax.append(value/denominator)
            else:
                prob_softmax.append(0)

        prob_till_now = 0.0
        #for i in range(len(prob_softmax)):
        for prob in prob_softmax:
            prob_till_now += prob
            roulette_wheel.append(prob_till_now)
        random_value = random.uniform(0,1)
        ind = 0
        for value in roulette_wheel:
            if random_value<value:
                return bees[ind]
            else:
                ind+=1
        return bees[ind-1]

    def testCaseBelongsToS(self, bee):
        # change this when required
        return True

    def load_test_cases(self):
        testCaseList=[]
        ct=0
        with open('./testcases.txt') as file:
            for line in file.readlines():
                ct += 1
                if len(line.split()) == 0:
                    continue
                if line[len(line)-1]=="\n":
                    line = line[:len(line)-1]
                tokens = []
                tokens = line.split()
                #tokens[len(tokens)-1] = tokens[len(tokens)-1][:-2]
                #958 1 1 2597 574 4253 0 399 400 0 0 1\n
                for i in range(self.testCaseVectorSize - len(tokens)):
                    tokens.append('0')
                testCaseList.append(" ".join(tokens))
                if len(tokens) != self.testCaseVectorSize:
                    print(bcolors.FAIL + "Invalid number of arguments on line: " + str(ct) + bcolors.ENDC,len(tokens), tokens)
                    #time.sleep(1)
            for i in range(len(testCaseList)):
                testCaseList[i]=testCaseList[i].split()
                for j in range(len(testCaseList[i])):
                    testCaseList[i][j]= int(testCaseList[i][j])
        return testCaseList

    def copyBee(self, bee):
        newBee=[]
        for item in bee:
            newBee.append((item))

        return newBee

    def mutate(self, bee):
        j = random.choice(range(self.testCaseVectorSize)) # j belongs to {1, 2,...,D}
        #X k = random.choice(range(len(self.employeed_bees))) # k belongs to {1, 2,...Ne}
        while(self.leaderBee == bee): # because k!= i
            self.leaderBee = random.choice(self.employeed_bees) ########## choose a leader according to roulette selection
        #print(self.employeed_bees[j], bee[j], self.leaderBee[j])

        mutatedBee = self.copyBee(bee)
        oldjVal = mutatedBee[j]
        #while mutatedBee[j] == oldjVal:
        mutatedBee[j] = bee[j] + (random.choice([-1,0,1]) * (bee[j] - self.leaderBee[j]))
        while(not self.testCaseBelongsToS(mutatedBee)): # change this when required and when we understand what V belongs to S
            mutatedBee[j] = bee[j] + (random.choice([-1,0,1]) * (bee[j] - self.leaderBee[j]))
        return mutatedBee

    def execute_current_bee(self,bee,index,is_right_version):
        if is_right_version:
            command = './tcas_right.out'
            fileName = 'ProbeValuesRight' + str(index) + '.txt'
        else:
            command = './tcas_wrong.out'
            fileName = 'ProbeValuesWrong' + str(index) + '.txt'
        arguments = []
        arguments.append(command)
        tokens = [str(bee[i]) for i in range(len(bee))]
        arguments.extend(tokens)

        arguments.append(fileName)
        # print str(arguments)
        subprocess.check_call(arguments)
        result = -1
        fileName = './'+fileName
        with open(fileName) as file:
            for line in file.readlines():
                tokens = line.split(' ')
                if tokens[0]=='result':
                    result = int(tokens[1])
        return result

    def load_probe_values(self,is_employeed_bees, number_of_bees):
        if is_employeed_bees:
            self.probe_values_for_all_testcases_employeed_bees = {}
            self.employeed_bees_probes_detected = []
            for ind in range(number_of_bees):# change 30 if u r changing number of bees
                fileName = 'ProbeValuesWrong' + str(ind) + '.txt'
                probeDictValues = {}
                probevalue = []
                with open(fileName) as file:
                    for line in file.readlines():
                        tokens = line.split(' ')
                        if tokens[0] != 'result':
                            probe_id = int(tokens[0])
                            if probe_id not in probeDictValues:
                                line_num = tokens[1]
                                value = tokens[2]
                                visited = tokens[3]
                                probeDictValues[probe_id] = (int(line_num),float(value),int(visited))
                                self.line_num[probe_id] = int(line_num)
                for probe_id in probeDictValues.keys():
                    probevalue.append(probe_id)
                
                self.probe_values_for_all_testcases_employeed_bees[ind] = probeDictValues
                self.employeed_bees_probes_detected.append(probevalue)
        else:
            self.probe_values_for_all_testcases_unemployeed_bees = {}
            self.unemployeed_bees_probes_detected = []
            for ind in range(number_of_bees):  # change 30 if u r changing number of bees
                fileName = 'ProbeValuesWrong' + str(ind) + '.txt'
                probeDictValues = {}
                probevalue = []
                with open(fileName) as file:
                    for line in file.readlines():
                        tokens = line.split(' ')
                        if tokens[0] != 'result':
                            probe_id = int(tokens[0])
                            probevalue.append(probe_id)
                            if probe_id not in probeDictValues:
                                line_num = tokens[1]
                                value = tokens[2]
                                visited = tokens[3]
                                probeDictValues[probe_id] = (int(line_num), float(value), int(visited))

                self.probe_values_for_all_testcases_unemployeed_bees[ind] = probeDictValues
                self.unemployeed_bees_probes_detected.append(probevalue)

    def compare_and_fill_pass_or_fail(self):
        self.compare_exec_result_employeed_bees = []
        self.compare_exec_result_unemployeed_bees = []
        for x, y in zip(self.right_results_execution_employed_bees, self.wrong_results_execution_employed_bees):
            if x==y:
                self.compare_exec_result_employeed_bees.append(True)
            else:
                self.compare_exec_result_employeed_bees.append(False)
        for x, y in zip(self.right_results_execution_unemployed_bees, self.wrong_results_execution_unemployed_bees):
            if x==y:
                self.compare_exec_result_unemployeed_bees.append(True)
            else:
                self.compare_exec_result_unemployeed_bees.append(False)

    def fitnessFunction(self, testCasePassedOrNot, testCaseProbesList):
        # testCaseProbesList  => [[2,1,0,3,4,6,5],[2,1,4,6,3,5], ....] list of probeIds that got executed for each testCase
        # testCasePassedOrNot => [True, False, True, ....]
        # self.parentsList [[parents],[parents],[1,4,3,5], ....]
        # self.childrenList [[children], [children], [1,4,2,3], ....]
        # self.totalNumberOfProbes
        multipleVal = self.dependency # must be less than 1
        st_k_list = []
        score_k_list = []

        # make stk values
        for j in range(self.totalNumberOfProbes):
            a_10 = 0.0
            a_11 = 0.0
            a_01 = 0.0
            a_00 = 0.0
            topVal = 0.0
            botVal = 0.0
            for i in range(len(testCaseProbesList)):
                if j in testCaseProbesList[i]:
                    if testCasePassedOrNot[i] == True:  # execute and passed
                        a_10 += 1
                    else:  # execute and failedz
                        a_11 += 1
                else:
                    if testCasePassedOrNot[i] == True:  # did not execute and passed
                        a_01 += 1
                    else:  # did not execute and failed
                        a_00 += 1

            topVal = a_11 / (a_11 + a_01 + self.addToRemoveDivisionByZero)
            botVal = a_10 / (a_10 + a_00 + self.addToRemoveDivisionByZero)
            stkVal = topVal / (topVal + botVal + self.addToRemoveDivisionByZero)
            st_k_list.append(stkVal)
        # make score values
        for i in range(len(st_k_list)):
            score_i = st_k_list[i]
            for j in range(len(self.parents[i])):
                score_i *= multipleVal
            for j in range(len(self.children[i])):
                score_i *= (1 - multipleVal)
            score_k_list.append(score_i)
        fbest = max(score_k_list)
        fBestInd = np.argmax(score_k_list)

        if(fbest > self.f_best[1]):
            
            self.f_best[0] = fBestInd
            self.f_best[1] = fbest
        #print("================probe number:" + str(fBestInd) + ". has max fitness of: "+ str(fbest) +"." )
        fitnessMatrix = []
        for i in range(len(testCaseProbesList)):
            scoreForThisFitness = []
            for j in testCaseProbesList[i]:
                scoreForThisFitness.append(score_k_list[j])
            fitnessMatrix.append(scoreForThisFitness)

        fitnessValues = []
        for i in range(len(fitnessMatrix)):
            fitnessValues.append(max(fitnessMatrix[i]))
        return fitnessValues

    def execute_employeed_and_unemployed_bees(self):
        self.right_results_execution_employed_bees = []
        self.right_results_execution_unemployed_bees = []
        self.wrong_results_execution_employed_bees = []
        self.wrong_results_execution_unemployed_bees = []
        for ind,bee in enumerate(self.employeed_bees):
            self.wrong_results_execution_employed_bees.append(self.execute_current_bee(bee,ind,False))
        for ind,bee in enumerate(self.unemployeedBees):
            self.wrong_results_execution_unemployed_bees.append(self.execute_current_bee(bee,ind,False))

        for ind,bee in enumerate(self.employeed_bees):
            self.right_results_execution_employed_bees.append(self.execute_current_bee(bee,ind,True))
        for ind,bee in enumerate(self.employeed_bees):
            self.right_results_execution_unemployed_bees.append(self.execute_current_bee(bee,ind,True))
        self.load_probe_values(True,self.numberOfEmployeedBees)
        self.load_probe_values(False,self.numberOfEmployeedBees)

    def abandonTestCase(self, beeHistory):
        xmin = []
        xmax = []
        for i in range(len(beeHistory[0])):
            xmin.append(1000000000000)
            xmax.append(-1000000000000)
        for bee in beeHistory:
            if bee[i] < xmin[i]:
                xmin[i] = bee[i]
            if bee[i] > xmax[i]:
                xmax[i] = bee[i]
        newBee = []
        for i in range(len(bee)):
            randNum = random.random()
            vecI = xmin[i] + (randNum * (xmax[i] - xmin[i]))
            newBee.append(vecI)
        return newBee

    def __init__(self):
        self.testCaseVectorSize = 12
        self.numberOfIterations = 19
        self.numberOfEmployeedBees = 30
        self.addToRemoveDivisionByZero = 0.1
        self.totalNumberOfProbes = 24
        self.fitnessChangeLimit = 0.01
        self.dependency = 0.9
        self.searchLimit = 10

        for i in range(len(sys.argv)):
            if sys.argv[i] == "-S" or sys.argv[i] == "--InputVectorSize":
                self.testCaseVectorSize = int(sys.argv[i+1])
            if sys.argv[i] == "-I" or sys.argv[i] == "--Iterations":
                self.numberOfIterations = int(sys.argv[i+1])
            if sys.argv[i] == "-Ne" or sys.argv[i] == "--NoEmployedBeesPI":
                self.numberOfEmployeedBees = int(sys.argv[i+1])
            if sys.argv[i] == "-F" or sys.argv[i] == "--FitnessChangeLimit":
                self.fitnessChangeLimit = float(sys.argv[i+1])
            if sys.argv[i] == "-D" or sys.argv[i] == "--DependencyFitness":
                self.dependency = float(sys.argv[i+1])
            if sys.argv[i] == "-A" or sys.argv[i] == "--AbandonAfter":
                self.searchLimit = int(sys.argv[i+1])
            if sys.argv[i] == "-DE" or sys.argv[i] == "--DivisionError":
                self.addToRemoveDivisionByZero = float(sys.argv[i+1])
            if sys.argv[i] == "-P" or sys.argv[i] == "--Probes":
                self.totalNumberOfProbes = int(sys.argv[i+1])
            if sys.argv[i] == "-h" or sys.argv[i] == "--help":
                print( "-S, --InputVectorSize: Input Vector Size.")
                print( "-I, --Iterations: Number Of Iterations.")
                print( "-Ne, --NoEmployedBeesPI: Number of Employeed Bees per iteration.")
                print( "-F, --FitnessChangeLimit: Abandon test case if change in fitness for many iterations is less than this.")
                print( "-D, --DependencyFitness: Dependency Fitness multiple value.")
                print( "-A, --AbandonAfter: Abandon after trying for this many iterations.")
                print( "-DE, --DivisionError: Add this to denominator for removing division by zero error.")
                print( "-P, --Probes: Number of Probes.")
                exit(0)


        print(bcolors.OKBLUE + "Input Vector Size: " + str(self.testCaseVectorSize) + bcolors.ENDC)                                                            
        print(bcolors.OKBLUE + "Number Of Iterations: " + str(self.numberOfIterations) + bcolors.ENDC)                                                         
        print(bcolors.OKBLUE + "Number of Employeed Bees per iteration: " + str(self.numberOfEmployeedBees) + bcolors.ENDC)                                     
        print(bcolors.OKBLUE + "Abandon test case if change in fitness for many iterations is less than: " + str(self.fitnessChangeLimit) + bcolors.ENDC)      
        print(bcolors.OKBLUE + "Dependency Fitness multiple val: " + str(self.dependency) + bcolors.ENDC)                                                      
        print(bcolors.OKBLUE + "Abandon after trying for: " + str(self.searchLimit) + " Iterations" + bcolors.ENDC)                                              
        print(bcolors.OKBLUE + "Add this to denominator for removing division by zero error: " + str(self.addToRemoveDivisionByZero) + bcolors.ENDC)             
        print(bcolors.OKBLUE + "Number of Probes: " + str(self.totalNumberOfProbes) + bcolors.ENDC)          
        #make the dependency graph
        self.parents = []
        self.children = []
        self.line_num = {}
        self.init_children_parents()
        self.right_results_execution_employed_bees = []
        self.right_results_execution_unemployed_bees = []
        self.wrong_results_execution_employed_bees = []
        self.wrong_results_execution_unemployed_bees = []
        employeedBee_history = [[] for i in range(self.numberOfEmployeedBees)]
        self.unemployeedBees = []
        self.testCases = self.load_test_cases()
        fitnessChange_tracker = [[] for i in range(self.numberOfEmployeedBees)]
        self.f_best = [-1,-1]
        self.testCaseVectorSize = len(self.testCases[0])
        # Get Initial Employeed Bees
        self.employeed_bees = self.get_initial_test_cases()   ########### get best 30
        unemployeed_bees_of_last_iteration = []
        
        
        
        for bee in self.employeed_bees:
            unemployeed_bees_of_last_iteration.append(self.copyBee(bee))

        """
            for i in range(len(self.employeed_bees)):
                #print(self.employeed_bees[i])
                self.employeed_bees[i] = self.employeed_bees[i].split()
                for j in range(len(self.employeed_bees[i])):
                    self.employeed_bees[i][j] = int(self.employeed_bees[i][j])
        """
        #print(i,self.employeed_bees[i])
        #randomize leader bee for the first iteration
        self.leaderBee = random.choice(self.employeed_bees)
        print("\n--------------------------------------------------------------------------------------------------\n")
        for iteration in range(self.numberOfIterations):
            print("Iteration num: " + str(iteration + 1))
            #print("Length of employeed Bees: " + str(len(self.employeed_bees)) + ". Length of unemployeed Bees: " + str(len(self.unemployeedBees)))

            for i in range(len( self.employeed_bees)):
                employeedBee_history[i].append( self.employeed_bees[i])

            #mutate the bees
            self.unemployeedBees = []
            for bee in  self.employeed_bees:
                self.unemployeedBees.append(self.mutate(bee))

            for i in range(len(self.employeed_bees)):
                while self.employeed_bees[i] == self.unemployeedBees[i]:
                    self.unemployeedBees[i] = self.mutate(self.employeed_bees[i])
                #print(self.employeed_bees[i],self.unemployeedBees[i])

            #for thisIterUnBee,lastIterUnBee in zip(self.unemployeedBees,unemployeed_bees_of_last_iteration):
            #    if lastIterUnBee == thisIterUnBee:
            #        print("Common unemployedBee from last iteration:",lastIterUnBee)
            
            unemployeed_bees_of_last_iteration = []
            for bee in self.unemployeedBees:
                unemployeed_bees_of_last_iteration.append(self.copyBee(bee))

            #execute the bees
            self.execute_employeed_and_unemployed_bees()
            self.compare_and_fill_pass_or_fail()
            #print("Executed the employed and unemployed bees")
            fitnessValues_employeed_bees = self.fitnessFunction(self.compare_exec_result_employeed_bees,self.employeed_bees_probes_detected)
            fitnessValues_unemployeed_bees = self.fitnessFunction(self.compare_exec_result_unemployeed_bees,self.unemployeed_bees_probes_detected)

            fitDif = []
            for i in range(len(fitnessValues_employeed_bees)):
                fitDif.append(fitnessValues_employeed_bees[i] - fitnessValues_unemployeed_bees[i])
            #6. Make Yi or the employeed bees for next iteration
            employeedBees_for_next_iteration = []
            fitnessValues_for_next_iteration_bees = []
            for i in range(len(fitnessValues_employeed_bees)):
                if fitnessValues_employeed_bees[i] > fitnessValues_unemployeed_bees[i]:
                    employeedBees_for_next_iteration.append(self.employeed_bees[i])
                    fitnessValues_for_next_iteration_bees.append(fitnessValues_employeed_bees[i])
                else:
                    employeedBees_for_next_iteration.append(self.unemployeedBees[i])
                    fitnessValues_for_next_iteration_bees.append(fitnessValues_unemployeed_bees[i])

            #7. Select Leder Bee
            self.leaderBee = self.selectLeader(employeedBees_for_next_iteration,fitnessValues_for_next_iteration_bees)

            #8. track fitness change
            for i in range(len(fitnessChange_tracker)):
                change_in_fitness = fitnessValues_employeed_bees[i] - max(fitnessValues_employeed_bees[i],fitnessValues_for_next_iteration_bees[i])
                fitnessChange_tracker[i].append(change_in_fitness)

            #9. Whether or not to abandon a test case
            for i in range(len(fitnessChange_tracker)):
                if len(fitnessChange_tracker[i]) == self.searchLimit:

                    #print("Variance" + str(np.var(fitnessChange_tracker[i])))
                    #there is no change in fitness so abandon this food source
                    if np.var(fitnessChange_tracker[i]) <= self.fitnessChangeLimit:

                        #print("Abandon food source: ", employeedBees_for_next_iteration[i])
                        employeedBees_for_next_iteration[i] = self.abandonTestCase(employeedBee_history[i])
                        fitnessChange_tracker[i] = []

                    #there is a substantial change in fitness so keep looking around this food source
                    else:
                        fitnessChange_tracker.remove(fitnessChange_tracker[0])
                        continue
                else:
                    continue
            """
            #10. Save the best fitnessValue
            maxFit = max(fitnessValues_employeed_bees)
            if maxFit > self.f_best[1]:
                self.f_best[0] = self.employeed_bees[np.argmax(fitnessValues_employeed_bees)]
                self.f_best[1] = max(fitnessValues_employeed_bees)
            """
            
            print(bcolors.HEADER + "currently, Faulty Line Num:" + str(self.line_num[self.f_best[0]]) + " and fBest:" + str(self.f_best[1]) + bcolors.ENDC)
            print("\n--------------------------------------------------------------------------------------------------\n")

        #print("Done!!")


if __name__ == "__main__":
    abc = Test()
