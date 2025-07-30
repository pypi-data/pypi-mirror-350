!> \file get_unit.f90
!> \brief returns a free <I>FORTRAN</I> unit number
!> @author John Burkhardt, Roland Martin
SUBROUTINE get_unit ( iunit )

  !     !$*****************************************************************************
  !
  ! GET_UNIT returns a free FORTRAN unit number.
  !
  !  Discussion:
  !
  !    A "free" FORTRAN unit number is an integer between 0 and 119 
  !    (on INTEL processors, 0 - 119 is a valid I/O number and 
  !    0 - 2**31-1 on ALPHA processors)
  !    which is not currently associated with an I/O device.  A free FORTRAN unit
  !    number is needed in order to open a file with the OPEN command.
  !
  !    If IUNIT = 0, then no free FORTRAN unit could be found, although
  !    all 99 units were checked (except for units 5, 6 and 9, which
  !    are commonly reserved for console I/O).
  !
  !    Otherwise, IUNIT is an integer between 0 and 119, representing a
  !    free FORTRAN unit.  Note that GET_UNIT assumes that units 5 and 6
  !    are special, and will never return those values.
  !
  !  Licensing:
  !
  !    This code is distributed under the GNU LGPL license. 
  !
  !  Modified:
  !
  !    06 December 2010
  !
  !  Author:
  !
  !    John Burkardt
  !
  !  Modifications (set I/O range to 0 - 119):
  !    Roland Martin
  !
  !  Parameters:
  !
  !    Output, integer ( kind = 4 ) IUNIT, the free unit number.
  !
  IMPLICIT NONE

  INTEGER ( kind = 4 ) :: i
  INTEGER ( kind = 4 ) :: ios
  INTEGER ( kind = 4 ) :: iunit
  LOGICAL              :: lopen

  iunit = 0

  DO i = 0, 119

     IF ( i /= 5 .AND. i /= 6 .AND. i /= 9 ) THEN

        INQUIRE ( unit = i, opened = lopen, iostat = ios )

        IF ( ios == 0 ) THEN
           IF ( .NOT. lopen ) THEN
              iunit = i
              RETURN
           END IF
        END IF

     END IF

  END DO

END SUBROUTINE get_unit

SUBROUTINE read_comments (unit)
  INTEGER,INTENT (IN)   :: unit
  INTEGER               :: ios
  CHARACTER (256)       :: buff

  READ ( unit , '(a)' , ERR = 11 , END = 10 , IOSTAT = ios ) buff
  
!  PRINT * , TRIM( buff), ios
  buff = ADJUSTL(buff) ! remove leading spaces

  IF ( buff (1:1) /= '#' .OR. buff == '' .OR. ios /= 0 ) THEN
! The case ios /= 0 was the solution to buffer underrun errors
! This lead to curious line readings..
     BACKSPACE ( unit )

  ELSE

     DO WHILE ( buff (1:1) == '#' .AND..NOT. ios /= 0 ) ! lines with comment 
        
        READ ( unit , '(a)' , ERR = 11 , END = 10 , IOSTAT = ios ) buff

!        PRINT * , TRIM ( buff )

     END DO

     BACKSPACE ( unit )

  END IF

10 RETURN

11 PRINT * , 'read_comment error::' , buff

END SUBROUTINE read_comments
