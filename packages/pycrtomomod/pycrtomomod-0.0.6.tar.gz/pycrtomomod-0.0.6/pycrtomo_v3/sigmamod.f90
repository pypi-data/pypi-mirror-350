MODULE sigmamod
!!$
!!$c 'sigma.fin'
!!$
!!$c Andreas Kemna                                            10-Jul-1993
!!$c                                       Letzte Aenderung   20-Oct-1997
!!$
!!$c.....................................................................
!!$c Referenzleitfaehigkeit
    COMPLEX(KIND(0D0)),PUBLIC                          :: sigma0

    ! conductivities of the individual elements
    COMPLEX(KIND(0D0)),PUBLIC,ALLOCATABLE,DIMENSION(:) :: sigma
    !!$c save variable
    COMPLEX(KIND(0D0)),PUBLIC,ALLOCATABLE,DIMENSION(:) :: sigma2

    !!$c Background-Werte
    REAL(KIND(0D0)),PUBLIC                             :: bet0,pha0

    !!$ c Schalter ob "background" Werte eingelesen werden sollen
   LOGICAL,PUBLIC                                     :: lrho0

    !!$c Schalter ob "starting model" eingelesen werden soll
    LOGICAL,PUBLIC                                     :: lstart
    !!$c initial seed fuers verrauschen vom startmodell
   INTEGER(KIND = 4),PUBLIC                           :: iseedpri
    !!$c noise for starting model
   REAL(KIND(0D0)),PUBLIC                             :: modl_stdn


END MODULE sigmamod
