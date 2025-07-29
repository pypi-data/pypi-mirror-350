use crate::{small_linalg::Vector3, PhysicsQuantity};
use std::ops::{Add, Div, Index, IndexMut, Mul, Neg, Sub};
use crate::small_linalg::{Matrix2, Matrix3x2, Vector2};

#[derive(Clone, Copy, PartialEq, Debug)]
pub struct Matrix2x3<T: PhysicsQuantity> {
    pub data: [[T; 3]; 2],
}

impl<T: PhysicsQuantity> Matrix2x3<T> {
    pub fn new(data: [[T; 3]; 2]) -> Self {
        Self { data }
    }

    pub fn from_f64(data: [[f64; 3]; 2]) -> Self {
        let mut converted = [[<T as PhysicsQuantity>::zero(); 3]; 2];
        for i in 0..2 {
            for j in 0..3 {
                converted[i][j] = T::from_raw(data[i][j]);
            }
        }
        Self::new(converted)
    }

    pub fn as_f64(&self) -> Matrix2x3<f64> {
        Matrix2x3::new([
            [self.data[0][0].as_f64(), self.data[0][1].as_f64(), self.data[0][2].as_f64()],
            [self.data[1][0].as_f64(), self.data[1][1].as_f64(), self.data[1][2].as_f64()],
        ])
    }

    pub fn transpose(&self) -> super::matrix3x2::Matrix3x2<T> {
        super::matrix3x2::Matrix3x2::new([
            [self.data[0][0], self.data[1][0]],
            [self.data[0][1], self.data[1][1]],
            [self.data[0][2], self.data[1][2]],
        ])
    }

    pub fn row(&self, i: usize) -> Vector3<T> {
        assert!(i < 2);
        Vector3::new(self.data[i])
    }
}

impl<T: PhysicsQuantity + Neg<Output = T>> Neg for Matrix2x3<T> {
    type Output = Self;
    fn neg(self) -> Self {
        Self::new([
            [ -self.data[0][0], -self.data[0][1], -self.data[0][2] ],
            [ -self.data[1][0], -self.data[1][1], -self.data[1][2] ],
        ])
    }
}

impl<T: PhysicsQuantity + Add<Output = T>> Add for Matrix2x3<T> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        let mut out = [[<T as PhysicsQuantity>::zero(); 3]; 2];
        for i in 0..2 {
            for j in 0..3 {
                out[i][j] = self.data[i][j] + rhs.data[i][j];
            }
        }
        Self::new(out)
    }
}

impl<T: PhysicsQuantity + Sub<Output = T>> Sub for Matrix2x3<T> {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        let mut out = [[<T as PhysicsQuantity>::zero(); 3]; 2];
        for i in 0..2 {
            for j in 0..3 {
                out[i][j] = self.data[i][j] - rhs.data[i][j];
            }
        }
        Self::new(out)
    }
}

impl<T: PhysicsQuantity> Index<(usize, usize)> for Matrix2x3<T> {
    type Output = T;
    fn index(&self, idx: (usize, usize)) -> &Self::Output {
        &self.data[idx.0][idx.1]
    }
}

impl<T: PhysicsQuantity> IndexMut<(usize, usize)> for Matrix2x3<T> {
    fn index_mut(&mut self, idx: (usize, usize)) -> &mut Self::Output {
        &mut self.data[idx.0][idx.1]
    }
}

impl<T: PhysicsQuantity> Matrix2x3<T> {
    pub fn dot_vector3<U, V>(&self, vec: &Vector3<U>) -> Vector2<V>
    where
        U: PhysicsQuantity,
        V: PhysicsQuantity + Add<Output = V>,
        T: Mul<U, Output = V>,
    {
        let r0 = self.data[0][0] * vec[0] + self.data[0][1] * vec[1] + self.data[0][2] * vec[2];
        let r1 = self.data[1][0] * vec[0] + self.data[1][1] * vec[1] + self.data[1][2] * vec[2];
        Vector2::new([r0, r1])
    }
}


impl<T, U, V> Mul<Vector3<U>> for Matrix2x3<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Vector2<V>;

    fn mul(self, rhs: Vector3<U>) -> Vector2<V> {
        self.dot_vector3(&rhs)
    }
}

impl<T, U, V> Mul<Matrix2x3<U>> for Matrix2<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Matrix2x3<V>;

    fn mul(self, rhs: Matrix2x3<U>) -> Self::Output {
        let mut result = [[<V as PhysicsQuantity>::zero(); 3]; 2];
        for i in 0..2 {
            for j in 0..3 {
                result[i][j] = self[(i, 0)] * rhs[(0, j)] + self[(i, 1)] * rhs[(1, j)];
            }
        }
        Matrix2x3::new(result)
    }
}


impl<T, U, V> Mul<Matrix3x2<U>> for Matrix2x3<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Matrix2<V>;

    fn mul(self, rhs: Matrix3x2<U>) -> Self::Output {
        let mut result = [[<V as PhysicsQuantity>::zero(); 2]; 2];
        for i in 0..2 {
            for j in 0..2 {
                result[i][j] =
                    self[(i, 0)] * rhs[(0, j)] + self[(i, 1)] * rhs[(1, j)] + self[(i, 2)] * rhs[(2, j)];
            }
        }
        Matrix2::new(result)
    }
}

impl<T> Matrix2x3<T>
where
    T: PhysicsQuantity
    + Mul<T, Output = T>
    + Add<T, Output = T>
    + Sub<T, Output = T>
    + Div<T, Output = T>
    + Copy,
{
    pub fn pseudoinverse(&self) -> Option<Matrix3x2<T>> {
        let a_t = self.transpose();
        let a_at = *self * a_t;
        let a_at_inv = a_at.inverse()?;
        Some(a_t * a_at_inv)
    }
}