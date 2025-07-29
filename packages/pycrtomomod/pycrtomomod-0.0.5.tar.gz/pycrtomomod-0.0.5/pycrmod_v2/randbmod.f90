MODULE randbmod
!!$c 'randb.fin'
!!$
!!$c Andreas Kemna                                            03-May-1993
!!$c                                       Letzte Aenderung   15-Jul-2007
!!$
!!$c.....................................................................

!!!$Anzahl der vorgegebenen Potentialwerte (Dirichletsche Randbedingung)
  INTEGER(KIND = 4),PUBLIC                             :: rwdanz

!!!$Knotennummern der vorgegebenen Potentialwerte
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE    :: rwdnr

!!!$Randwerte (Dirichletsche Randbedingung)
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE    :: rwddc
    COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: rwd

!!!$Zeiger ab wann Potentialwerte automatisch belegt werden sollen
    INTEGER(KIND = 4),PUBLIC                           :: rwdbnr

!!!$Anzahl der Randwerte (Neumannsche Randbedingung)
    INTEGER(KIND = 4),PUBLIC                           :: rwnanz
    
!!!$Randwerte (Neumannsche Randbedingung)
!!!$(fuer 'beta' belegt mit den Widerstandswerten der Randelemente)
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE    :: rwndc
    COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: rwn
  

END MODULE randbmod
