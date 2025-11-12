import os,sys,re
import imputils.stmtutils as su
import logging

logging.basicConfig( level=logging.DEBUG)
FLIN=sys.argv[1]
SRVNM="unknow"
if len(sys.argv) >2:
    SRVNM=sys.argv[2]

print ("filein",FLIN)
SDB={}
def main () :
    print ("main")


    infl=open(FLIN,'r')
    outfl = open(FLIN+".in", 'w')
    outsdbfl = open(FLIN + ".sdb", 'w')
    logging.info('ImportPG|' + 'Importing from file|' + FLIN)
    dt=""
    tm=""
    lc = 0
    lc_ok=0
    lc_wrn=0

    for line in infl :

        line=line.strip()
        lc+=1
        print ("LINE",line)
        if "INFO pg_stat_activity" in line:
            (dt,tm)=line.split(" ")[2:4]
        if '|' in line and "wait_event_type" not in line:
            v=[l.strip() for l in line.split("|")]


            if len(v)<19 :
                logging.warning('ImportPG|'+'Too short line|'+str(lc)+"|"+line)
                lc_wrn+=1
                continue
            if len(tm)<4 :
                logging.warning('ImportPG|'+'Problem with time|'+str(lc)+"|"+line)
                lc_wrn+=1
                continue
            #print (v[19])
            if v[19].endswith("+") :
                #multiline
                v[19]= re.sub(r"\+$", " ", v[19]).strip()
                v[19] = re.sub(r"\\[rnt]", " ", v[19]).strip()
                print ('multiline')
                for mln in infl:
                    lc += 1
                    print(mln)
                    v1 = [l.strip() for l in mln.split("|")]

                    if len(v1)<19  :
                        logging.warning('ImportPG|' + 'Too short multi line|' + str(lc) + "|" + mln)
                        lc_wrn += 1
                        break
                    if  len(v1[0])>1 :
                        logging.warning('ImportPG|' + 'Wrong multi line|' + str(lc) + "|" + mln)
                        lc_wrn += 1
                        break
                    origv1_19=v1[19]
                    v1[19] = re.sub(r"\+$", " ", v1[19]).strip()
                    v1[19] = re.sub(r"\\[rnt]+", " ", v1[19]).strip()
                    print ("before1",v)
                    print("before2", v1)
                    v = [x +" "+ y for x, y in zip(v, v1)]
                    print ("after",v)
                    if  not origv1_19.endswith("+"):
                        break

            #[l.strip() for l in my_list])
            """
            0:datid|datname|pid|leader_pid|usesysid|5:usename|6:application_name|client_addr|8:client_hostname|client_port|10:backend_start|
            11:xact_start|query_start|state_change|wait_event_type|15:wait_event|state|backend_xid|backend_xmin|19:query|20:backend_type
            (id, nstmt, dt, tm, unm, dnm, hnm, pnm, "session", status)
            """
            lc_ok += 1
            hnm=v[8]
            if hnm=="" :
                hnm=v[7]
            if hnm == "":
                hnm = 'local'
            nsql=su.normalizeStmt(v[19])
            print ("writing",v[19],nsql)
            rec="{}|{}|{}|{}|{}|{}|{}|{}|0|{}".format(nsql[:250],dt,tm[0:4],v[5].strip(),v[1].strip(),hnm.strip(),v[6].strip(),v[2].strip(),SRVNM)
            outfl.write(rec+"\n")
            if dt not in SDB :
                SDB[dt]={}
            if nsql not in SDB[dt] :
                    SDB[dt][nsql]=v[19]
                    if len(nsql)>1 :
                        outsdbfl.write("{}\t{}\t{}\n".format(dt,nsql[:250],v[19].replace(" +"," ").strip()))

    logging.info('ImportPG|' + 'lines in file|' + str(lc) + "|exported lines|" +  str(lc_ok)+ "|warnings|" +  str(lc_wrn))
if __name__ == '__main__':
    main()
