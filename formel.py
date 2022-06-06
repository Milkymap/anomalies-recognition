"""
    Soit une video V = [I0, I1, ..., In-1]
    Nous voulons detecter des anomalies sur ces videos, une anomalie c'est
    juste une sous sequence S = [Im, Im+1, ..., im+k], de taille ((m+k) - m) + 1 : k + 1.
    Tel que m >= 0 and m + k<= n-1 donc S est inclus dans V.  

    Une solution serait de divisier la video V en plusieurs sous sequence de taille k + 1. 
    V = [I0, I1, ..., In-1]
        S0 = [I0, ..., Ik]
        S1 = [I0+p, ..., Ik+p]
        Sn = [I0+n*p, ..., Ik+n*p]
        S4 = [I0+4*p, ..., Ik+n*p]
    Donc pour une video V, on aura plusieurs sous sequence S = [s0, s1, .., sm]
    Maintenant, le problème revient à assigner pour chaque sous sequence, un label 0 | 1
    1 : violence
    0 : neutre 
    ...! 

    On a donc une classification binaire.     

    V = 0 1 2 3 4 5
    
    S00 = # # 0 => 1 | 0
    S01 = # 0 1 => 1 | 0
    S02 = 0 1 2 => 1 | 0
    S03 = 1 2 3 => 1 | 0
    S04 = 2 3 4 => 1 | 0
    S05 = 3 4 5 => 1 | 0
    S06 = 4 5 6 => 1 | 0
    S07 = 5 # # => 1 | 0

"""