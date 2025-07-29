module errmod
! 'err.fin'

! Andreas Kemna                                            06-Feb-1993
!                                       Letzte Aenderung   24-Oct-1996

!.....................................................................

! COMMON

! Fehlernummer
        integer :: errnr

! Fehlerart
! 0 : GKS - nicht aktiv, Programm nicht verlassen
! 1 : GKS - nicht aktiv, Programm verlassen
! 2 : GKS - aktiv      , Programm nicht verlassen
! 3 : GKS - aktiv      , Programm verlassen und GKS schlieáen
         integer :: errflag

! Fehlertext
        character(80), public :: fetxt

!.....................................................................

        ! common/cerr/    errnr,
     ! 1                  errflag,
     ! 1                  fetxt
end module errmod
