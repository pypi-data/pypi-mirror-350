!> \file invhpmod.f90
!> \brief variable delarations
!> \details Replacement of former 'invhp.fin' 
!> @author Andreas Kemna
!> @date 04/16/1996, last change 07/16/2007
MODULE invhpmod
!!$c 'invhp.fin'
!!$
!!$c Andreas Kemna                                            16-Apr-1996
!!$c                                       Letzte Aenderung   16-Jul-2007
!!$
!!$c.....................................................................
!!$
!!$c Kanalnummer
  INTEGER (KIND=4) ::     kanal

!!!$c Dateinamen
  CHARACTER (128) ::   delem,delectr,dstrom,&
       dsigma,dvolt,dsens,dstart,&
!!$cdiff+<
       dd0,dm0,dfm0,&
!!$cdiff+>
       drandb

!!$c Schalter ob allererste Iteration (Initialisierung)
  LOGICAL ::      lsetup

!!$c Schalter ob "final phase improvement" initialisiert werden soll
  LOGICAL ::      lsetip

!!$c Schalter ob weiterer Datensatz invertiert werden soll
  LOGICAL ::      lagain

!!$c Indexvariablen
  INTEGER (KIND=4) ::  j,k,l

!!$c Zeitvariablen
  REAL             ::     izeit,tazeit(2)

!!$c Zusaetzliche Fehlervariable
  INTEGER (KIND=4) ::     errnr2

END MODULE invhpmod
