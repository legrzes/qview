import re

def normalizeStmt (stmt) :
    #
    stm = stmt.lower()

    stm = re.sub(r"[ \t\n\r]+", " ", stm)
    stm = re.sub(r"\+$", "", stm)
    stm = stm.replace('"', "")
    # multiple spaces
    stm = re.sub(r"\\\\", "", stm)
    stm = re.sub(r"\\'", "", stm)
    stm = re.sub(r'\\"', "", stm)
    stm = re.sub(r"'[^\']*'", "X", stm)
    stm = re.sub(r'"[^\"]*"', "X", stm)
    stm = re.sub(r"\s+", " ", stm)
    # All numbers => N
    # stm = re.sub(r"-?[0-9]+", "N", stm)
    stm = re.sub(r"([ =<>,\(]+)(-?[\.0-9]+)", "\\1" + "N", stm)
    # WHERE foo IN ('880987','882618','708228','522330')
    stm = re.sub(
        # r" (in|values)\s*\([^,]+,[^)]+\)", " \\1 (XYZ)", stm
        r" (in|values)\s*\([^)]+(\)|$)", " \\1 (XYZ)", stm

    )
    stm = re.sub(r"execute procedure\s+([^\( ]+).+", r"execute procedure \1()", stm)
    # tabs with names
    stm = cleanTable(stm)
    stm = re.sub(r"uidx_aqsc_([\w\d\_]+)", "uidx_aqsc_YYY12", stm)

    stm = re.sub(r"\|", "?", stm)
    stm = re.sub(r";", " ", stm)
    stm = re.sub(r"\s+", " ", stm)
    return stm.strip()

def cleanTable (tab) :
    tab1 = tab
    slen = len(tab)
    numbers = sum(c.isdigit() for c in tab)

    if numbers > 2:
        if "_" in tab:
            tab1 = ""

            for p in tab.split("_"):
                np = sum(c.isdigit() for c in p)
                if 'v2' == p:
                    tab1 += ""
                elif np > 0 and len(p) < 3:
                    tab1 += "Y_"
                elif np < 2:
                    tab1 += p + "_"
                else:
                    tab1 += "Y_"


    return tab
