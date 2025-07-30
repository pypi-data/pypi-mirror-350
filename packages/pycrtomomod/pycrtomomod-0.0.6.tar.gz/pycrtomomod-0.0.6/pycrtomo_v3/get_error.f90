SUBROUTINE get_error(ftext,errnr,errflag,intext)

  INTEGER,INTENT (IN) :: errnr,errflag
  CHARACTER(80),INTENT (IN) :: intext
  CHARACTER(256),INTENT (OUT) :: ftext

  INCLUDE 'crerror.h'
  
  ftext=TRIM(ADJUSTL(fetxt(errnr)))//' '//TRIM(intext)
  
  
END SUBROUTINE get_error
