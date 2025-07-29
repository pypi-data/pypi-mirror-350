MODULE electrmod
    !!$c 'electr.fin'
    !!$
    !!$c Andreas Kemna                                            22-Jan-1993
    !!$c                                       Letzte Aenderung   24-Oct-1996
    !!$
    !!$c.....................................................................
    !!$c Anzahl der
    INTEGER(KIND = 4),PUBLIC                          :: eanz

    !!$c Knotennummern der Elektroden
    INTEGER(KIND = 4),PUBLIC,ALLOCATABLE,DIMENSION(:) :: enr

END MODULE electrmod
