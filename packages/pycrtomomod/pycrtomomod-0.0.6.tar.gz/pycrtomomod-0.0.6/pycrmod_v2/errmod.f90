!> \file errmod.f90
!> \brief variable declarations for error handling
!> \details Replacement of former 'err.fin'
!> @author Andreas Kemna, Roland Martin
!> @date 02/06/1993, last change 10/24/1996

MODULE errmod
!'err.fin'
!
!Andreas Kemna                                            06-Feb-1993
!                                      Letzte Aenderung   24-Oct-1996
!.....................................................................
!Fehlernummer
  INTEGER(KIND = 4)  ::     errnr
!Kanaele
  INTEGER(KIND = 4)  ::     fperr
  INTEGER(KIND = 4)  ::     fprun
  INTEGER(KIND = 4)  ::     fpinv
  INTEGER(KIND = 4)  ::     fpcjg
  INTEGER(KIND = 4)  ::     fpeps
  INTEGER(KIND = 4)  ::     fpcfg

! die io nummern werden nun ueber get_unit belegt..
!    9 - error.dat   -> fperr
!    10 - run.ctr    -> fprun
!    12 - crtomo.cfg -> fpcrf
!    13 - inv.ctr    -> fpinv
!    14 - cjg.ctr    -> fpcjg
!    15 - eps.ctr    -> fpeps
!Fehlerart
!0 : GKS - nicht aktiv, Programm nicht verlassen
!1 : GKS - nicht aktiv, Programm verlassen
!2 : GKS - aktiv      , Programm nicht verlassen
!3 : GKS - aktiv      , Programm verlassen und GKS schlieáen
  INTEGER(KIND = 4)  ::     errflag

!Fehlertext
  CHARACTER (256),PUBLIC   ::   fetxt

END MODULE errmod
