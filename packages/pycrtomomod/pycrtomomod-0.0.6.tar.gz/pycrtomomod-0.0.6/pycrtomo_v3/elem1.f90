!> \file elem1.f90
!> \brief form functions of linear boundary elements
!> \details Kemna (1995): The potential function \f$ \tilde \phi (s)\f$ is approximated with a linear function of the boundary \f$ C \f$:
!> \f[ \tilde \phi (s) \approx c_1^{(j)}+c_2^{(j)}s \f]
!> with \f$ s \in C^{(j)} \ \ (j=1,...,n_r) \f$. The constants \f$ c_1^{(j)}, c_2^{(j)}\f$ can be determined by the corresponding node values \f$ \tilde \phi_{i_1 (j)}, \tilde \phi_{i_1 (j)} \ \ i_1 (j),i_2(j) \in \{1,...,n_k\}) \f$ (see figure below).
!> \image html elem1_sketch.png "Boundary element with linear approach"
!> The approach yields (Schwarz 1991)
!> \f[ \int_{C^{(j)}}{\tilde \phi ^2} ds = \tilde \phi ^{(j)^T} S_3^{'(j)} \tilde \phi ^{(j)} \ \ with S_3^{'(j)} = \frac{L^{(j)}}{6} \left( \begin{array}{cc} 2 & 1 \\ 1 & 2 \end{array} \right), \f]
!> requiring \f$ \tilde \phi^{(j)} = \left( \tilde \phi_{i_1(j)}, \tilde \phi_{i_1(j)} \right)^T \f$ and the length \f$ L^{(j)} \f$ of the \f$ j\f$-th boundary element.
!> The \f$ 2\times 2\f$ matrix \f$ S_3^{'(j)} \f$ can be regarded as \f$n_k \times n_k \f$ matrix \f$ S_3^{(j)}\f$, if it is filled with zeros according to the contributing indices \f$ i_1(j), i_2(j) \f$. The resulting matrix element \f$ (s_3^{(j)})_{mn} \ \ (m,n \in \{ 1,..., n_k \})\f$ is
!> \f[ (s_3^{(j)})_{mn} = \left\{ \begin{array}{cc} (s_3^{'(j)})_{\kappa\lambda}, & if \kappa,\lambda \in \{ 1,2 \}\  with \  m=i_\kappa (j) \ and \ n= i_\lambda(j) \\ 0, & else. \end{array} \right. \f]
!> where \f$ (s_3^{'(j)})_{\kappa\lambda} \f$ is an element of \f$ S_3^{'(j)}\f$. It follows that
!> \f[ \tilde\phi^{(j)^T} S_3^{'(j)}\tilde\phi^{(j)} = \tilde\phi^{T} S_3^{(j)}\tilde\phi  \f]
!> @author Andreas Kemna
!> @date 10/11/1993, last change 11/05/1997

subroutine elem1()

!     Unterprogramm liefert die Elementmatrix 'elmam(2,2)' und den Element-
!     vektor 'elve(2)' fuer ein Randelement mit linearem Ansatz ( Element-
!     typ Nr.1 ).

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   22-Sep-1998

!.....................................................................

  USE elemmod,only:xk,yk,elmam,elve

  IMPLICIT none

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Grundelementmatrix
  INTEGER (KIND = 4)  ::     s4(2,2)

!     Grundelementvektor
  INTEGER (KIND = 4)  ::     sb(2)

!     Hilfsvariablen
  REAL (KIND(0D0))    ::     x21,y21,l

!     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j

!.....................................................................

  data sb/1,1/
  data s4/2,1,1,2/

  x21 = xk(2) - xk(1)
  y21 = yk(2) - yk(1)

  l = dsqrt(x21*x21 + y21*y21)

  do i=1,2
     elve(i) = l * dble(sb(i)) / 2d0

     do j=1,2
        elmam(i,j) = l * dble(s4(i,j)) / 6d0
     end do
  end do

  return
end subroutine elem1
