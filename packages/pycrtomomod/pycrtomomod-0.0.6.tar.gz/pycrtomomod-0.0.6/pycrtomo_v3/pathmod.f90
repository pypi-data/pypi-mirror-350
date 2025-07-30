MODULE pathmod
!!$c 'path.fin'
!!$
!!$c Andreas Kemna                                            25-Jun-1996
!!$c                                       Letzte Aenderung   24-Oct-1996
!!$
!!$c.....................................................................

!!$c (Back-) Slash
  CHARACTER(1),PUBLIC :: slash

!!$c RAM-Disk-Pfad
  CHARACTER (60),PUBLIC ::    ramd

!!$c Laenge des RAM-Disk-Pfades
  INTEGER(KIND = 4),PUBLIC ::     lnramd

!!$c UNIX COMMANDS
  CHARACTER(6),PUBLIC,PARAMETER :: mkdir_cmd='mkdir '
  CHARACTER(6),PUBLIC,PARAMETER :: rmdir='rm -R '

  PUBLIC :: clear_string

CONTAINS

  SUBROUTINE clear_string (string)
!!!$ PURPOSE
!!!$ extract the first "part" of a string until the first blank and
!!!!$ remove the rest

    CHARACTER (*) :: string

    INTEGER ( KIND = 4 ) :: iblank

    string = ADJUSTL(string)

    iblank = INDEX(string,' ')

    IF (iblank ==  1) RETURN

    IF (iblank /= 0) string = string(:iblank - 1)

   END SUBROUTINE clear_string

END MODULE pathmod
