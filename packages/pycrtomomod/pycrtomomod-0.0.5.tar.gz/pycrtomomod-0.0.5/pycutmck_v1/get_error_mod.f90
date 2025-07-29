module get_error_modx
    contains
        subroutine get_error(ftext,errnr,errflag,intext)

          CHARACTER(256),INTENT (OUT) :: ftext
          INTEGER,INTENT (IN) :: errnr
          INTEGER,INTENT (IN) :: errflag
          CHARACTER(80),INTENT (IN) :: intext

          ! character(256) :: fetxt(101)
          INCLUDE 'crerror.h'
          ftext=TRIM(ADJUSTL(fetxt(errnr)))//' '//TRIM(intext)
          ! indicate that everything went well
          ! errflag  = 0


        end subroutine get_error
end module get_error_modx
