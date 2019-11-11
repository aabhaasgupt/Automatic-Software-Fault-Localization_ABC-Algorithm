
/*  -*- Last-Edit:  Fri Jan 29 11:13:27 1993 by Tarak S. Goradia; -*- */
/* $Log: tcas.c,v $
 * Revision 1.2  1993/03/12  19:29:50  foster
 * Correct logic bug which didn't allow output of 2 - hf
 * */

#include <stdio.h>

#define OLEV 600       /* in feets/minute */
#define MAXALTDIFF 600 /* max altitude difference in feet */
#define MINSEP 300     /* min separation in feet */
#define NOZCROSS 100   /* in feet */
/* variables */
FILE *fp;
struct probe
{
    int id;
    int num;
    double value;
    int pass;
} probes[24];
typedef int bool;

int Cur_Vertical_Sep;
bool High_Confidence;
bool Two_of_Three_Reports_Valid;

int Own_Tracked_Alt;
int Own_Tracked_Alt_Rate;
int Other_Tracked_Alt;

int Alt_Layer_Value; /* 0, 1, 2, 3 */
int Positive_RA_Alt_Thresh[4];

int Up_Separation;
int Down_Separation;

/* state variables */
int Other_RAC; /* NO_INTENT, DO_NOT_CLIMB, DO_NOT_DESCEND */
#define NO_INTENT 0
#define DO_NOT_CLIMB 1
#define DO_NOT_DESCEND 2

int Other_Capability; /* TCAS_TA, OTHER */
#define TCAS_TA 1
#define OTHER 2

int Climb_Inhibit; /* true/false */

#define UNRESOLVED 0
#define UPWARD_RA 1
#define DOWNWARD_RA 2

void initialize()
{
    Positive_RA_Alt_Thresh[0] = 400;
    Positive_RA_Alt_Thresh[1] = 500;
    Positive_RA_Alt_Thresh[2] = 640;
    Positive_RA_Alt_Thresh[3] = 740;
}

int ALIM()
{
    probes[0].id = 0;
    probes[0].num = 58;
    probes[0].value = 0;
    probes[0].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[0].id, probes[0].num, probes[0].value, probes[0].pass);
    return Positive_RA_Alt_Thresh[Alt_Layer_Value];
}

int Inhibit_Biased_Climb()
{
    probes[1].id = 1;
    probes[1].num = 63;
    probes[1].value = 0;
    probes[1].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[1].id, probes[1].num, probes[1].value, probes[1].pass);
    return (Climb_Inhibit ? Up_Separation + NOZCROSS : Up_Separation);
}

bool Non_Crossing_Biased_Climb()
{
    int upward_preferred;
    int upward_crossing_situation;
    bool result;
    probes[2].id = 2;
    probes[2].num = 72;
    probes[2].value = 0;
    probes[2].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[2].id, probes[2].num, probes[2].value, probes[2].pass);
    upward_preferred = Inhibit_Biased_Climb() > Down_Separation;
    probes[3].id = 3;
    probes[3].num = 73;
    probes[3].value = 0;
    probes[3].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[3].id, probes[3].num, probes[3].value, probes[3].pass);
    if (upward_preferred)
    {
        probes[4].id = 4;
        probes[4].num = 75;
        probes[4].value = 0;
        probes[4].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[4].id, probes[4].num, probes[4].value, probes[4].pass);
        result = !(Own_Below_Threat()) || ((Own_Below_Threat()) && (!(Down_Separation >= ALIM())));
    }
    else
    {
        probes[5].id = 5;
        probes[5].num = 79;
        probes[5].value = 0;
        probes[5].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[5].id, probes[5].num, probes[5].value, probes[5].pass);
        result = Own_Above_Threat() && (Cur_Vertical_Sep >= MINSEP) && (Up_Separation >= ALIM());
    }
    return result;
}

bool Non_Crossing_Biased_Descend()
{
    int upward_preferred;
    int upward_crossing_situation;
    bool result;
    probes[6].id = 6;
    probes[6].num = 90;
    probes[6].value = 0;
    probes[6].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[6].id, probes[6].num, probes[6].value, probes[6].pass);
    upward_preferred = Inhibit_Biased_Climb() > Down_Separation;
    probes[7].id = 7;
    probes[7].num = 91;
    probes[7].value = 0;
    probes[7].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[7].id, probes[7].num, probes[7].value, probes[7].pass);
    if (upward_preferred)
    {
        probes[8].id = 8;
        probes[8].num = 93;
        probes[8].value = 0;
        probes[8].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[8].id, probes[8].num, probes[8].value, probes[8].pass);
        result = Own_Below_Threat() && (Cur_Vertical_Sep >= MINSEP) && (Down_Separation >= ALIM());
    }
    else
    {
        probes[9].id = 9;
        probes[9].num = 97;
        probes[9].value = 0;
        probes[9].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[9].id, probes[9].num, probes[9].value, probes[9].pass);
        result = !(Own_Above_Threat()) || ((Own_Above_Threat()) && (Up_Separation >= ALIM()));
    }
    return result;
}

bool Own_Below_Threat()
{
    probes[10].id = 10;
    probes[10].num = 133;
    probes[10].value = 0;
    probes[10].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[10].id, probes[10].num, probes[10].value, probes[10].pass);
    return (Own_Tracked_Alt <= Other_Tracked_Alt); /* operator mutation */
}

bool Own_Above_Threat()
{
    probes[11].id = 11;
    probes[11].num = 109;
    probes[11].value = 0;
    probes[11].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[11].id, probes[11].num, probes[11].value, probes[11].pass);
    return (Other_Tracked_Alt < Own_Tracked_Alt);
}

int alt_sep_test()
{
    bool enabled, tcas_equipped, intent_not_known;
    bool need_upward_RA, need_downward_RA;
    int alt_sep;
    probes[12].id = 12;
    probes[12].num = 118;
    probes[12].value = 0;
    probes[12].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[12].id, probes[12].num, probes[12].value, probes[12].pass);
    enabled = High_Confidence && (Own_Tracked_Alt_Rate <= OLEV) && (Cur_Vertical_Sep > MAXALTDIFF);
    probes[13].id = 13;
    probes[13].num = 119;
    probes[13].value = 0;
    probes[13].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[13].id, probes[13].num, probes[13].value, probes[13].pass);
    tcas_equipped = Other_Capability == TCAS_TA;
    probes[14].id = 14;
    probes[14].num = 120;
    probes[14].value = 0;
    probes[14].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[14].id, probes[14].num, probes[14].value, probes[14].pass);
    intent_not_known = Two_of_Three_Reports_Valid && Other_RAC == NO_INTENT;
    probes[15].id = 15;
    probes[15].num = 122;
    probes[15].value = 0;
    probes[15].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[15].id, probes[15].num, probes[15].value, probes[15].pass);
    alt_sep = UNRESOLVED;
    probes[16].id = 16;
    probes[16].num = 124;
    probes[16].value = 0;
    probes[16].pass = 1;
    fprintf(fp, "%d %d %f %d \n", probes[16].id, probes[16].num, probes[16].value, probes[16].pass);
    if (enabled && ((tcas_equipped && intent_not_known) || !tcas_equipped))
    {
        probes[17].id = 17;
        probes[17].num = 126;
        probes[17].value = 0;
        probes[17].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[17].id, probes[17].num, probes[17].value, probes[17].pass);
        need_upward_RA = Non_Crossing_Biased_Climb() && Own_Below_Threat();
        probes[18].id = 18;
        probes[18].num = 127;
        probes[18].value = 0;
        probes[18].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[18].id, probes[18].num, probes[18].value, probes[18].pass);
        need_downward_RA = Non_Crossing_Biased_Descend() && Own_Above_Threat();
        probes[19].id = 19;
        probes[19].num = 128;
        probes[19].value = 0;
        probes[19].pass = 1;
        fprintf(fp, "%d %d %f %d \n", probes[19].id, probes[19].num, probes[19].value, probes[19].pass);
        if (need_upward_RA && need_downward_RA)
        /* unreachable: requires Own_Below_Threat and Own_Above_Threat
           to both be true - that requires Own_Tracked_Alt < Other_Tracked_Alt
           and Other_Tracked_Alt < Own_Tracked_Alt, which isn't possible */
        {
            probes[20].id = 20;
            probes[20].num = 132;
            probes[20].value = 0;
            probes[20].pass = 1;
            fprintf(fp, "%d %d %f %d \n", probes[20].id, probes[20].num, probes[20].value, probes[20].pass);
            alt_sep = UNRESOLVED;
        }
        else if (need_upward_RA)
        {
            probes[21].id = 21;
            probes[21].num = 104;
            probes[21].value = 0;
            probes[21].pass = 1;
            fprintf(fp, "%d %d %f %d \n", probes[21].id, probes[21].num, probes[21].value, probes[21].pass);
            alt_sep = UPWARD_RA;
        }
        else if (need_downward_RA)
        {
            probes[22].id = 22;
            probes[22].num = 136;
            probes[22].value = 0;
            probes[22].pass = 1;
            fprintf(fp, "%d %d %f %d \n", probes[22].id, probes[22].num, probes[22].value, probes[22].pass);
            alt_sep = DOWNWARD_RA;
        }
        else
        {
            probes[23].id = 23;
            probes[23].num = 138;
            probes[23].value = 0;
            probes[23].pass = 1;
            fprintf(fp, "%d %d %f %d \n", probes[23].id, probes[23].num, probes[23].value, probes[23].pass);
            alt_sep = UNRESOLVED;
        }
    }
    return alt_sep;
}
char *concat(const char *s1, const char *s2)
{
    char *result = malloc(strlen(s1) + strlen(s2) + 1); // +1 for the null-terminator
    // in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}
main(argc, argv) 
int argc;
char *argv[];
{
    int ind;
    if (argc < 13)
    {
        fprintf(stdout, "Error: Command line arguments are\n");
        fprintf(stdout, "Cur_Vertical_Sep, High_Confidence, Two_of_Three_Reports_Valid\n");
        fprintf(stdout, "Own_Tracked_Alt, Own_Tracked_Alt_Rate, Other_Tracked_Alt\n");
        fprintf(stdout, "Alt_Layer_Value, Up_Separation, Down_Separation\n");
        fprintf(stdout, "Other_RAC, Other_Capability, Climb_Inhibit\n");
        exit(1);
    }
    initialize();
    Cur_Vertical_Sep = atoi(argv[1]);
    High_Confidence = atoi(argv[2]);
    Two_of_Three_Reports_Valid = atoi(argv[3]);
    Own_Tracked_Alt = atoi(argv[4]);
    Own_Tracked_Alt_Rate = atoi(argv[5]);
    Other_Tracked_Alt = atoi(argv[6]);
    Alt_Layer_Value = atoi(argv[7]);
    Up_Separation = atoi(argv[8]);
    Down_Separation = atoi(argv[9]);
    Other_RAC = atoi(argv[10]);
    Other_Capability = atoi(argv[11]);
    Climb_Inhibit = atoi(argv[12]);
    char *fileName = argv[13];
    fp = fopen(fileName, "w+");
    //fprintf(stdout, "%d\n", alt_sep_test());
    fprintf(fp, "result %d\n", alt_sep_test());
    //for(ind=0;ind<27;ind++)
    //{
    //fprintf(fp,"%d %d %f %d \n",ind,probes[ind].num,probes[ind].value,probes[ind].pass );
    //}
    fclose(fp);
    exit(0);
}
