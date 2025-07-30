MODULE modelmod
!!$c 'model.fin'
!!$       
!!$c Andreas Kemna                                            10-Jul-1993
!!$c                                       Letzte Aenderung   24-Oct-1996
!!$
!!$c.....................................................................
!!$c Anzahl der Modellparameter
  INTEGER(KIND = 4),PUBLIC                          :: manz
        
!!$c Zeiger auf Modellparameter
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE :: mnr

!!!$ >> RM ref model regu
!!!$ variance of magnitude (re) and phase (im) of the reference model
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: w_ref_re
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: w_ref_im
  INTEGER,PUBLIC,DIMENSION(:),ALLOCATABLE :: ind_ref_grad
!!!$ << RM ref model regu
  
END MODULE modelmod
