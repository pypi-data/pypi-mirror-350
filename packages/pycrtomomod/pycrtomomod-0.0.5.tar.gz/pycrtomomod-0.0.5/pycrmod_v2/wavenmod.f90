MODULE wavenmod
!
! 'waven.fin'
!
! Andreas Kemna                                            07-Oct-1993
!                                       Letzte Aenderung   07-Nov-1997
!
!.....................................................................

!Anzahl der Wellenzahlwerte
    INTEGER(KIND = 4),PUBLIC                        :: kwnanz

!Schalter steuert Art der Ruecktransformation
!( = 0 : keine Trafo (2D Fall),
!  = 1 : Gauss/Laguerre-Integration )
    INTEGER(KIND = 4),PUBLIC                        :: swrtr

!Wellenzahlwerte
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: kwn

!Wichtungsfaktoren fuer Ruecktransformation
    REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE :: kwnwi

!Fuer Ruecktransformation relevanter Abstandsbereich
    REAL(KIND(0D0)),PUBLIC                          :: amin,amax

END MODULE wavenmod
