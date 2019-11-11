
/*  -*- Last-Edit:  Fri Jan 29 11:13:27 1993 by Tarak S. Goradia; -*- */
/* $Log: tcas.c,v $
 * Revision 1.2  1993/03/12  19:29:50  foster
 * Correct logic bug which didn't allow output of 2 - hf
 * */

#include <stdio.h>

int addNum(int one, int two)
{
	int num = one + two;
	return num;
}
int subNum(int one, int two)
{
	int num = one - two;
	return num;
}
main(argc, argv)
int argc;
int *argv[];
{
	
	//printf("%d",argc);
	if(argc < 5)
	{
		fprintf(stdout, "Erroasdasdr: Command line arguments are\n");
		fprintf(stdout, "Cur_Vertical_Sep, High_Confidence, Two_of_Three_Reports_Valid\n");
		fprintf(stdout, "Own_Tracked_Alt, Own_Tracked_Alt_Rate, Other_Tracked_Alt\n");
		fprintf(stdout, "Alt_Layer_Value, Up_Separation, Down_Separation\n");
		fprintf(stdout, "Other_RAC, Other_Capability, Climb_Inhibit\n");
		exit(1);
	}
	
	int a = atoi(argv[1]);
	int b = atoi(argv[2]);
	int c = atoi(argv[3]);
	char *fileName = argv[4];

	int d=0;
	d=addNum(d,a);
	d=addNum(d,b);
	d=addNum(d,c);
	FILE *fp;
	fp = fopen(fileName, "w+");
	fprintf(fp,"result %d\n",d);
	//fprintf(stdout, "\n%d\n", d);
	exit(0);
}