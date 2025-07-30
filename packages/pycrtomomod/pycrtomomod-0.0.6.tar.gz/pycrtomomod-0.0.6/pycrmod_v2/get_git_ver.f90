!> \file get_git_ver.f90
!> \brief get the <I>git </I> version info from the file <I>my_git_version.h</I> 
!> \details the file is automatically created at the first compile time.
!> @author Roland Martin
!> @date <I> unknown </I>

MODULE get_ver

  IMPLICIT none

  CHARACTER (256),PUBLIC  ::   version(5)

  PUBLIC :: get_git_ver
  
CONTAINS

  SUBROUTINE get_git_ver

  INCLUDE 'my_git_version.h'
  
  version(1)=TRIM(ADJUSTL(my_git_version(1)))
  version(2)=TRIM(ADJUSTL(my_git_version(2)))
  version(3)=TRIM(ADJUSTL(my_git_version(3)))
  version(4)=TRIM(ADJUSTL(my_git_version(4)))
  version(5)=TRIM(ADJUSTL(my_git_version(5)))
  
  PRINT*,'Git-Branch  ',TRIM(version(1))
  PRINT*,'Commit-ID   ',TRIM(version(2))
  PRINT*,'Created     ',TRIM(version(3))
  PRINT*,'Compiler    ',TRIM(version(4))
  PRINT*,'OS          ',TRIM(version(5))
  
END SUBROUTINE get_git_ver
END MODULE get_ver
